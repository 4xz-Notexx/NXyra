from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
CORS(app)

# ================= EMAIL CONFIG =================
EMAIL_ADDRESS = "custompros420@gmail.com"
EMAIL_PASSWORD = "fascuqohxfrmhqjk"
# ================================================

@app.route("/")
def home():
    return "NXyra backend running"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data.get("message", "").strip().lower()

    # ✅ SIMPLE MATH HANDLER (ANY NUMBERS)
    if re.fullmatch(r"[0-9+\-*/(). ]+", msg):
        try:
            reply = f"Answer: {eval(msg)}"
        except:
            reply = "Invalid mathematical expression."
    else:
        reply = (
            "⚠️ I currently answer only simple mathematical expressions.\n"
            "Examples: 5+7, (10+2)*3"
        )

    return jsonify({"reply": reply})

@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.get_json()
    message = data.get("message", "")

    try:
        email = EmailMessage()
        email["From"] = EMAIL_ADDRESS
        email["To"] = EMAIL_ADDRESS
        email["Subject"] = "NXyra Feedback"
        email.set_content(message)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(email)

        return jsonify({"status": "Feedback sent successfully"})
    except Exception as e:
        return jsonify({"status": "Failed to send feedback", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

