from flask import Flask, redirect, url_for, session, render_template, request
from flask_oauthlib.client import OAuth
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

oauth = OAuth(app)

webflow_oauth = oauth.remote_app(
    'webflow',
    consumer_key='e6f544aae5938dc537b7329093bd986464c9a0c6aed139979fe6e3ac1645901a',
    consumer_secret='356a7f9b006b09c4f54817d3d76892991050b627d54a291197af37e99027f4b2',
    request_token_params={},
    base_url='https://api.webflow.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://api.webflow.com/oauth/token',
    authorize_url='https://webflow.com/oauth/authorize'
)

@app.route('/callback')
@webflow_oauth.authorized_handler
def callback(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token
    return redirect(url_for('profile'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        return redirect(url_for('profile'))
    else:
        return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return redirect(url_for('login'))
    else:
        return render_template('signup.html')

@app.route('/profile')
def profile():
    access_token = session.get('access_token')
    if access_token:
        return f'Welcome to your profile page!'
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
