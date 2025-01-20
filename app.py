# app.py
from flask import Flask, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from models import db, User
from forms import RegistrationForm, LoginForm
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abc123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(id_card=form.id_card.data).first()
        if existing_user:
          flash('ID card already registered', 'danger')
          return render_template('register.html', form=form)
        user = User(name=form.name.data,
                    last_name=form.last_name.data,
                    role=form.role.data,
                    id_card=form.id_card.data,
                    id_card_type=form.id_card_type.data,
                    email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id_card=form.id_card.data, id_card_type=form.id_card_type.data, role=form.role.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            flash(f'Welcome, {user.name}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check your credentials', 'danger')
    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        return render_template('dashboard.html', user=user)
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
  session.pop('user_id', None)
  return redirect(url_for('login'))

@app.route('/')
def index():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
