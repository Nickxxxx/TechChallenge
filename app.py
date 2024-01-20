import os
from dotenv import load_dotenv

load_dotenv()
from flask import Flask, request, jsonify
from flask_mail import Mail
from communication import email, telegram
from emotional_analysis import emotion_classifier
from gpt import gpt4

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
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
telegram_bot = telegram.TelegramBot(TELEGRAM_BOT_TOKEN)

default_communication_method = "mail"


# All methods must be invokes via a sigle POST endpoint, because Protopie does not support multiple endpoints
@app.route('/post-endpoint', methods=['POST'])
def post_endpoint():
    global default_communication_method
    data = request.json
    method = data['method']

    if method == 'send_mail':
        if default_communication_method == "mail":
            body = gpt_model.chat_to_mail(data['text'], mailer.lawyer_name, mailer.test_client_name)
            subject = gpt_model.chat_to_mail_subject(data['text'])
            mailer.send_mail(subject, body)
            return jsonify({'message': 'Mail sent'})
        if default_communication_method == "telegram":
            text = gpt_model.chat_to_telegram(data['text'], mailer.lawyer_name, mailer.test_client_name)
            telegram_bot.send_message(text)
            return jsonify({'message': 'Message sent'})

    elif method == 'get_unread_emails':
        emails = mailer.get_unread_emails()
        if len(emails) > 0:
            default_communication_method = "mail"
            return jsonify({'message': 'Emails received', 'emails': emails, "from_lawyer": data['from_lawyer']})

        if not telegram_bot.telegram_client_first_name:
            return jsonify({'message': 'Emails received', 'emails': [], "from_lawyer": data['from_lawyer']})
        telegram_messages = telegram_bot.get_updates()
        if len(telegram_messages) > 0:
            default_communication_method = "telegram"
            return jsonify({'message': 'Emails received', 'emails': telegram_messages, "from_lawyer": data['from_lawyer']})

    elif method == 'predict_emotion':
        emotion_probabilities = emotional_classifier.predict_emotion(data['text'])
        emotional_suggestions = gpt_model.emotional_suggestions(emotion_probabilities, data['text'])
        answer_suggestion = gpt_model.answer_suggestion(data['text'])
        return jsonify({'message': 'Emotion predicted', 'emotion_probabilities': emotion_probabilities,
                        'emotional_suggestions': emotional_suggestions, 'answer_suggestion': answer_suggestion})

    elif method == 'legal_explain':
        explanation = gpt_model.legal_explain(data['legal_term'], data['text'])
        return jsonify({'message': 'Legal term explained', 'explanation': explanation})

    elif method == 'set_test_client':
        mailer.set_test_client(data['name'], data['email'])
        telegram_bot.set_telegram_client(data['telegram_first_name'], data['telegram_last_name'])
        return jsonify({'message': 'Test client set'})

    elif method == 'set_lawyer_name':
        mailer.set_lawyer_name(data['name'])
        return jsonify({'message': 'Lawyer name set'})

    return jsonify({'message': 'Method not found'})


if __name__ == '__main__':
    app.run(debug=True)
