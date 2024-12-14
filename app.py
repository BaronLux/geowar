from flask import Flask, render_template, request, redirect, url_for
from game import game_state, game

app = Flask(__name__)


# Список для хранения сообщений

# рендерит главную страницу сайта
@app.route('/')
def index():
    state = next(game_state)
    while not game.wait_for_input:
        game.messages += [state]
        state = next(game_state)
    return render_template('index.html', messages=game.messages)


# обрпбатывает сообщения пользователя
@app.route('/send', methods=['POST'])
def send():
    message = request.form['message']
    game.messages += [message]
    game.get_user_message(message)
    return redirect(url_for('index'))


if __name__ == '__main__':
    # запуск приложения
    app.run(debug=True, host='0.0.0.0', port=8000)
