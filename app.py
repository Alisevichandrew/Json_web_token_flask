from functools import wraps
from flask import Flask, request, jsonify, make_response, render_template, session
import jwt
from datetime import datetime, timedelta

# app = Flask(__name__)
# app.config['SECRET_kEY'] = 'b'SO\x07\xfd\x7fDh\xc4`\x16\xa6\xbd\xd7T\xe1&'
app = Flask(__name__)
app.secret_key = b'Z\x864\x94\x8a\xf2\x92\x1c\xb1&\xda\xff\x84\xdfc\x8c'
#generation by command in terminal:> python -c 'import os; print(os.urandom(16))'


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
@app.route('/login', methods=['POST'])
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
