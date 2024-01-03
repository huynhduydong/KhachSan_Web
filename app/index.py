from flask import render_template

from app import app


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/index.html', methods=['GET'])
def home1():
    return render_template('index.html')


@app.route('/about.html', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/contact.html', methods=['GET'])
def contact():
    return render_template('contact.html')


@app.route('/gallery.html', methods=['GET'])
def gallery():
    return render_template('gallery.html')


@app.route('/room.html', methods=['GET'])
def room():
    return render_template('room.html')
@app.route('/account.html', methods=['GET'])
def account():
    return render_template('account.html')


if __name__ == '__main__':
    app.run(debug=True)
