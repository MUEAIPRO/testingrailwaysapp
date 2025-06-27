from flask import Flask, request
import telegram
from crewai import Agent, Task, Crew
import os



# --- Telegram Bot Setup ---
# TELEGRAM_TOKEN = os.environ.get("8018732559:AAHqBfV_xNehm11upX_QS9npz2z43vbpyBY")

TELEGRAM_TOKEN = "8018732559:AAHqBfV_xNehm11upX_QS9npz2z43vbpyBY"
bot = telegram.Bot(token=TELEGRAM_TOKEN)

# --- Flask App Setup ---
app = Flask(__name__)

# --- Agent Tool ---
def course_info_tool(_):
    return """📍 Location: Hitech City, Hyderabad

1️⃣ Data Science Course (6 months)
- Mon to Fri
- Topics: Python, ML, DL
- Projects & placements

2️⃣ Generative AI Course (3 months)
- Mon to Fri
- Tools: OpenAI, LangChain, CrewAI
- Real-world agent labs

3️⃣ Prompt Engineering (45 days)
- Mon to Fri
- Tools: ChatGPT, Gemini, 25+ APIs
- Ideal for marketers, devs & creators

✅ All courses offer: live sessions, expert instructors, certificates, and placement help."""

# --- Agent Setup ---
def build_virtual_assistant():
    assistant = Agent(
        role="VirtualAssistantBot",
        goal="Assist users with Mue AI course and training details",
        backstory="You are a friendly, informative assistant for Mue AI answering questions from new students.",
        tools=[course_info_tool]
    )
    return Crew(agents=[assistant])

# --- Webhook to Handle Telegram Messages ---
@app.route("/webhook", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    message = update.message
    chat_id = message.chat.id
    text = message.text.lower()

    # CrewAI Handling
    if any(keyword in text for keyword in ["training", "course", "ai", "mue"]):
        crew = build_virtual_assistant()
        task = Task(description="Tell the user about MueAI's training programs.")
        result = crew.run(task)
        bot.send_message(chat_id=chat_id, text=result)
    else:
        bot.send_message(chat_id=chat_id, text="Hi! I'm MueAI's assistant 🤖. Ask me about our training courses, timings, or fees!")

    return "ok"

# --- Run Flask App ---
if __name__ == "__main__":
    app.run(port=5000)
