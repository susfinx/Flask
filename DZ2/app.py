from flask import Flask, render_template, request, redirect, url_for, make_response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/welcome', methods=['POST'])
def welcome():
    # Получаем данные из формы
    name = request.form.get('name')
    email = request.form.get('email')

    # Создаем cookie с данными пользователя
    response = make_response(redirect(url_for('greet')))
    response.set_cookie('name', name)
    response.set_cookie('email', email)
    return response

@app.route('/greet')
def greet():
    # Получаем данные из cookie
    name = request.cookies.get('name')

    if name:
        return render_template('welcome.html', name=name)
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    # Удаляем cookie и перенаправляем на страницу ввода
    response = make_response(redirect(url_for('index')))
    response.delete_cookie('name')
    response.delete_cookie('email')
    return response

if __name__ == '__main__':
    app.run(debug=True)
