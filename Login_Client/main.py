from flask import Flask, render_template, request, flash
from radius_login import r_login
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        google_auth = request.form.get("google_auth")
        login_success = r_login(email, password, google_auth)
        if login_success:
            flash('You were successfully logged in')
        else:
            error = 'Invalid credentials'
    return render_template('login.html', error=error)


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run()