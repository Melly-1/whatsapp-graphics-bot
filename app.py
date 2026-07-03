from flask import Flask, request
import requests
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_ID = os.getenv("PHONE_ID")

def send_message(recipient, message):
    url = f"https://graph.facebook.com/v20.0/{PHONE_ID}/messages"
    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    data = {
        "messaging_product": "whatsapp",
        "to": recipient,
        "text": {"body": message}
    }
    requests.post(url, headers=headers, json=data)

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        verify_token = "graphics_bot_2026"
        if request.args.get("hub.verify_token") == verify_token:
            return request.args.get("hub.challenge")
        return "Verification failed", 403

    if request.method == "POST":
        data = request.get_json()
        try:
            msg = data["entry"][0]["changes"][0]["value"]["messages"][0]
            from_number = msg["from"]
            text = msg["text"]["body"].lower()

            # --- BOT LOGIC FOR KINGSLEY SARFO BOATENG GRAPHICS ---
            if "hi" in text or "hello" in text or text == "menu":
                reply = """Hi 👋 Welcome to *Kingsley Sarfo Boateng Graphics*!
We design Posters, Flyers, Logos & Social Media Designs.

Reply with:
1. Price List
2. Place New Order
3. Turnaround Time
4. Portfolio / Samples
5. Talk to Designer"""

            elif text == "1":
                reply = """💰 *PRICE LIST - Kingsley Sarfo Boateng Graphics*
Poster A3: GHS 80
Flyer A5 [1 side]: GHS 50
Flyer A5 [2 sides]: GHS 80
Social Media Post: GHS 30
Logo Design: GHS 200
*Includes 2 revisions*"""

            elif text == "2":
                reply = """📝 *PLACE ORDER*
Send me this info:
1. What do you need? [Poster/Flyer/Logo]
2. Text to put on it
3. Colors/ideas or reference image
I’ll send you a quote + mockup within 2 hours."""

            elif text == "3":
                reply = """⏰ *TURNAROUND TIME*
Flyers/Posters: 24 hours
Social Media Posts: 6 hours
Logo: 3-5 days
Rush orders available +50%.
Working hours: Mon-Sat, 9am-8pm"""

            elif text == "4":
                reply = f"""🎨 *OUR PORTFOLIO & CONTACT*
Check our work and chat with us directly:
{https://wa.me/233505200301}

Send "samples" + Poster, Flyer, Logo to see examples"""

            elif text == "5":
                reply = """👨‍💻 Kingsley will reply you shortly.
Meanwhile, what’s your project about?"""

            else:
                reply = "Sorry, I didn’t get that. Type 'menu' to see options again."

            send_message(from_number, reply)
        except Exception as e:
            print(e)

        return "ok", 200


