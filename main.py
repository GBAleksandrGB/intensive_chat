from datetime import datetime
from flask import Flask, render_template, request
import json

application = Flask(__name__)

# Путь к файлу с сообщениями
DB_FILE = './data/db.json'

# Чтение сообщения
db = open(DB_FILE, 'rb')
data = json.load(db)
messages = data['messages']


# Сохранение сообщения в файл
def safe_messages_to_file():
    db = open(DB_FILE, 'w')
    data = {
        'messages': messages
    }
    json.dump(data, db)


# Добавить сообщение в список
def add_message(text, sender):
    new_message = {
        'text': text,
        'sender': sender,
        'time': datetime.now().strftime('%H:%M'),
    }
    messages.append(new_message)
    safe_messages_to_file()


# for msg in messages:
#     print(f"[{msg['sender']}]:  {msg['text']}  /  {msg['time']}")


# Главная страница
@application.route('/')
def index_page():
    return f'Здравствуйте, Вас приветствует Чат-2022'


# Показать все сообщения
@application.route('/get_messages')
def get_messages():
    return {'messages': messages}


# Показать форму чата
@application.route('/form')
def form():
    return render_template('form.html')


@application.route('/send_message')
def send_message():
    # Получить данные пользователя
    try:
        name = request.args['name']
        text = request.args['text']
        if 3 >= len(name) <= 100:
            raise Exception('Имя должно быть не короче 3 и не длиннее 100 символов')
        if 1 >= len(text) <= 3000:
            raise Exception('Сообщение должно быть не короче 1 и не длиннее 3000 символов')
    except Exception as e:
        return e.__str__()
    else:
        # Добавление сообщения
        add_message(text, name)
        return 'OK'


application.run()
