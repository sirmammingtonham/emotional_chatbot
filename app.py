import os
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, jsonify, request, session
import base64

from src.tone_analyzer import ToneAnalyzer
from src.emotion_detection import EmotionDetector
from src.chatbot import ChatBot

load_dotenv(find_dotenv('ibm-credentials.env'))

app = Flask('Emotionally Intelligent Chatbot')
app.secret_key = os.environ.get('ASSISTANT_APIKEY') # just a long fixed string
app.config['TEMPLATES_AUTO_RELOAD'] = True

tone_analyzer = ToneAnalyzer()
emotion_detector = EmotionDetector()
chatbot = ChatBot()


@app.route("/")
def home():
    if 'session_id' in session:
        session.pop('session_id', None)
    return render_template("index.html")


@app.route("/parse_text")
def test():
    userText = request.args.get('msg')

    if 'emotion' not in session:
        session['emotion'] = ('Neutral', 1.0)
    current_emotion = session['emotion']
    print(current_emotion)
    tone = tone_analyzer.analyze(userText)
    response = chatbot.processMessage(userText, tone, current_emotion, session)

    return jsonify(response=response, tone=tone.getTone(), emotion=current_emotion[0])


@app.route("/parse_image", methods=['POST'])
def parse_image():
    try:
        imgdata = base64.b64decode(request.data.split(b',')[1])
        current_emotion = emotion_detector.run_detection_bytes(imgdata)
        if current_emotion is None:
            current_emotion = ('Neutral', 1.0)
        session['emotion'] = current_emotion
        return f'successfully updated emotion to {current_emotion[0]}'

    except Exception as e:
        print(e)
        return f'error! {e}'


if __name__ == "__main__":
    app.run()
