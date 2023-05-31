from flask import Flask, request, jsonify
import psycopg2
import telebot
from datetime import datetime

if __name__ == "__main__":

        connection = psycopg2.connect(user = "postgres",
                              password = "Akadem53",
                              host = "127.0.0.1",
                              port = "5432",
                              database = "telegram_bot")
        cursor = connection.cursor()
        API_TOKEN = 'token'

        bot = telebot.TeleBot(API_TOKEN)

        def send_message(json_data):            
                sending_ids = json_data["uids"]
                message = json_data["message"]
                if type(sending_ids) != type(str(" ")):
                        for id in sending_ids:
                                cheking_user_chat_by_id = """SELECT chat_id from private_message where destination_id = %s"""
                                id = int(id)
                                try:
                                        cursor.execute(cheking_user_chat_by_id, [id])
                                        chat_id = cursor.fetchall()
                                        if len(chat_id) == 0:
                                                pass
                                        else:
                                                bot.send_message(chat_id=chat_id[0], text=message)
                                except None:
                                        pass
                else:
                        cheking_user_chat_by_id = """SELECT chat_id from private_message where destination_id = %s"""
                        sending_ids = int(sending_ids)
                        try:
                                cursor.execute(cheking_user_chat_by_id, [sending_ids])
                                chat_id = cursor.fetchall()
                                if len(chat_id) == 0:
                                        pass
                                else:
                                        bot.send_message(chat_id=chat_id[0][0], text=message)
                        except AttributeError:
                                pass
                cursor.close()
        


        app = Flask(__name__)

        @app.route('/SendMessage', methods=['POST'])
        def message():
            json_data = request.get_json()
            send_message(json_data)
            return"Succes"

        @app.route('/GetUpdate', methods=['GET'])
        def request():
                with open("request_time.txt", 'r') as file:
                    last_check_date = str(file.read())
                cursor.execute("""SELECT id FROM destination""")
                all_user_ids = cursor.fetchall()
                for id in all_user_ids[0]:
                        selecting_messages_by_id = """SELECT destination_id, text from private_message where destination_id = %s and date - timestamp %s > interval '0 day 1 second'"""
                        id = int(id)
                        function_tuple = (id, last_check_date)
                        cursor.execute(selecting_messages_by_id, function_tuple)
                        message_tuple = cursor.fetchall()
                with open("request_time.txt", 'w') as file:
                        to_write = str(datetime.now()).split(".")
                        file.write(to_write[0])
                return jsonify(message_tuple)
        
        app.run(debug=True)