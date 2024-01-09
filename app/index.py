from flask import render_template, request, redirect
from flask_login import login_user, login_required, logout_user

from app import app, dao, login

from app.staff import *


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/index.html', methods=['GET'])
def home1():
    return render_template('index.html')


@app.route("/admin/login", methods=['GET', 'POST'])
def login_admin():
    error = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.authenticate_user(username, password)
        if user is not None:
            login_user(user)
            return redirect('/admin')
        else:
            error = 'Thong tin dang nhap sai'

    return render_template('login.html', error=error)



@app.route('/about.html', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/testimonial.html', methods=['GET'])
def testimonial():
    return render_template('testimonial.html')


@app.route('/team.html', methods=['GET'])
def team():
    return render_template('team.html')


@app.route('/contact.html', methods=['GET'])
def contact():
    return render_template('contact.html')


@app.route('/service.html', methods=['GET'])
def service():
    return render_template('service.html')


@app.route('/booking.html', methods=['GET'])
def booking():
    return render_template('booking.html')


@app.route('/room.html', methods=['GET'])
def room():
    return render_template('room.html')


@app.route('/account.html', methods=['GET'])
def account():
    return render_template('account.html')


@login.user_loader
def get_user_by_id(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    app.run(debug=True)
