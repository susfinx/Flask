from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash
from models import db, User, RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)


@app.route('/', methods=['GET', 'POST'])

def register():
    form = RegistrationForm()

    if form.validate_on_submit():

        hashed_password = generate_password_hash(form.password.data, method='sha256')

        new_user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        return 'Вы успешно зарегистрированы!'

    return render_template('register.html', form=form)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
