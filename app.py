import os
from dotenv import load_dotenv

load_dotenv()
from flask import Flask, request, jsonify
from flask_mail import Mail
from communication import email
from emotional_analysis import emotion_classifier
from gpt import gpt4

MAIL_SERVER = os.getenv('MAIL_SERVER')
MAIL_PORT = int(os.getenv('MAIL_PORT'))
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_USE_TLS = os.getenv('MAIL_USE_TLS') == 'True'
MAIL_USE_SSL = os.getenv('MAIL_USE_SSL') == 'True'

app = Flask(__name__)

# Configuration
app.config['MAIL_SERVER'] = MAIL_SERVER
app.config['MAIL_PORT'] = MAIL_PORT
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
app.config['MAIL_USE_SSL'] = MAIL_USE_SSL

mail = Mail(app)

mailer = email.Mailer(mail, MAIL_SERVER, MAIL_USERNAME, MAIL_PASSWORD)
emotional_classifier = emotion_classifier.EmotionClassifier()
gpt_model = gpt4.GPT()


# All methods must be invokes via a sigle POST endpoint, because Protopie does not support multiple endpoints
@app.route('/post-endpoint', methods=['POST'])
def post_endpoint():
    data = request.json
    method = data['method']

    if method == 'send_mail':
        body = gpt_model.chat_to_mail(data['text'], data['lawyer_name'], data['recipient_name'])
        subject = gpt_model.chat_to_mail_subject(data['text'])
        mailer.send_mail(subject, data['recipients'], body)
        return jsonify({'message': 'Mail sent'})
    elif method == 'get_unread_emails':
        emails = mailer.get_unread_emails()
        return jsonify({'message': 'Emails received', 'emails': emails})
    elif method == 'predict_emotion':
        emotion_probabilities = emotional_classifier.predict_emotion(data['text'])
        return jsonify({'message': 'Emotion predicted', 'emotion_probabilities': emotion_probabilities})
    elif method == 'legal_explain':
        explanation = gpt_model.legal_explain(data['legal_term'], data['text'])
        return jsonify({'message': 'Legal term explained', 'explanation': explanation})

    return jsonify({'message': 'Method not found'})


if __name__ == '__main__':
    app.run(debug=True)
