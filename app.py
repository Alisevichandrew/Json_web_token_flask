from functools import wraps
from flask import Flask, request, jsonify, make_response, render_template, session
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_kEY'] = 'af0caf1cfd904b52abd29c893500a19b'

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 401
        
        try:
            # why 'data'?
            token = jwt.decode(token, app.config['SECRET KEY'])
        except:
            return jsonify({'Message': 'Invalid Token'}), 403
        
        return func(*args, **kwargs)
    return decorated
    

#Home
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return 'Logged in currently!'

#Public
@app.route('/public')
def public():
    return 'For Public'

#Authenticated
@app.route('/auth')
@token_required
def auth():
    return 'JWT is verified. Welcome to you dashboard!' 

# Login
@app.route('/Login', methods=['POST'])
def login():
    if request.form['username'] and request.form['password'] == '123456':
        session['logged_in'] = True
        token = jwt.encode({
            'user': request.form['username'],
            'expiration': str(datetime.utcnow() + timedelta(seconds=60))
        },
            app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('utf-8')})

    else:
        return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: "Authentication Failed!"'})


if __name__ == "__main__":
    app.run(debug=True)
