import sqlite3
import random
from datetime import datetime
from nlp_utils import preprocess
from database import setup_database

setup_database()

def fetch_intents():
    conn = sqlite3.connect("chatbot.db")
    cur = conn.cursor()
    cur.execute("SELECT intent, pattern, response FROM intents")
    rows = cur.fetchall()
    conn.close()

    intents = {}
    for intent, pattern, response in rows:
        if intent not in intents:
            intents[intent] = {"patterns": [], "responses": []}
        intents[intent]["patterns"].append(pattern)
        intents[intent]["responses"].append(response)

    return intents

intents = fetch_intents()

def score_intent(user_words, patterns):
    score = 0
    for pattern in patterns:
        pattern_words = preprocess(pattern)
        score += len(user_words.intersection(pattern_words))
    return score

def get_response(user_input):
    user_words = preprocess(user_input)

    best_intent = None
    best_score = 0

    for intent, data in intents.items():
        score = score_intent(user_words, data["patterns"])
        if score > best_score:
            best_score = score
            best_intent = intent

    if best_intent is None:
        return "Sorry, I didn't understand.", None

    if "time" in intents[best_intent]["responses"]:
        return f"Current time is {datetime.now().strftime('%H:%M:%S')}", best_intent

    if "date" in intents[best_intent]["responses"]:
        return f"Today's date is {datetime.now().strftime('%d-%m-%Y')}", best_intent

    return random.choice(intents[best_intent]["responses"]), best_intent


if __name__ == "__main__":
    print("Rule-Based NLP Chatbot (type 'exit' to stop)\n")

    while True:
        user = input("You: ")
        response, intent = get_response(user)
        print("Bot:", response)

        with open("chatlog.txt", "a") as log:
            log.write(f"You: {user}\nBot: {response}\n")

        if intent == "bye":
            break

