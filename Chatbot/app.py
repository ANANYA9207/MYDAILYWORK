from flask import Flask, render_template, request
from chatbot import get_response   # your chatbot file

app = Flask(__name__)
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/get", methods=["POST"])
def chatbot_reply():
    user_input = request.form["msg"]
    response, _ = get_response(user_input)
    return response
if __name__ == "__main__":
    app.run(debug=True)
