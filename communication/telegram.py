import requests


class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.url = "https://api.telegram.org/bot{}/".format(token)
        self.telegram_client_first_name = None
        self.telegram_client_last_name = None
        self.telegram_chat_id = None
        self.offset = None

    def set_telegram_client(self, telegram_client_first_name, telegram_client_last_name):
        self.telegram_client_first_name = telegram_client_first_name
        self.telegram_client_last_name = telegram_client_last_name

    def get_updates(self):
        method = "getUpdates"
        params = {"offset": self.offset}
        resp = requests.get(self.url + method, params)
        result_json = resp.json()["result"]

        messages_from_client = []
        for message in result_json:
            if (message["message"]["from"]["first_name"] == self.telegram_client_first_name
                    and (not self.telegram_client_last_name
                         or message["message"]["from"]["last_name"] == self.telegram_client_last_name)
                    and message["message"]["text"] != "/start"):
                messages_from_client.append(message)

        if len(messages_from_client) > 0:
            self.telegram_chat_id = messages_from_client[0]["message"]["chat"]["id"]
            self.offset = messages_from_client[0]["update_id"] + 1

        text_messages_from_client = [message["message"]["text"] for message in messages_from_client]

        return [{'from': f"{self.telegram_client_first_name} {self.telegram_client_last_name}",
                 'body': message, "written_from_lawyer": 0} for message in text_messages_from_client]

    def send_message(self, text):
        method = "sendMessage"
        params = {"chat_id": self.telegram_chat_id, "text": text}
        resp = requests.post(self.url + method, params)
        return resp
