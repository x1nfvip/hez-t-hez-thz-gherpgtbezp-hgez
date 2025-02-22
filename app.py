from flask import Flask, render_template, request, jsonify
import random
from datetime import datetime, timedelta
from flask_login import LoginManager, UserMixin, login_required, current_user, login_user

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id, username, role, last_generation=None):
        self.id = id
        self.username = username
        self.role = role
        self.last_generation = last_generation

@login_manager.user_loader
def load_user(user_id):
    # Creating a test user - replace with database lookup in production
    test_user = User(
        id=1,
        username="test_user",
        role="Basic",
        last_generation=None
    )
    login_user(test_user)
    return test_user

def generate_valid_card(card_type):
    bin_prefixes = {
        1: ("60457811425", 5),
        2: ("604578114", 7),
        3: ("604578118", 7),
        4: ("6045781123", 6)
    }
    
    bin_prefix, remaining_length = bin_prefixes[card_type]
    
    while True:
        base = bin_prefix + ''.join(random.choice('0123456789') for _ in range(remaining_length - 1))
        
        total = 0
        for i, digit in enumerate(reversed(base)):
            digit = int(digit)
            if i % 2 == 0:
                digit *= 2
                if digit > 9:
                    digit -= 9
            total += digit
        
        check_digit = (10 - (total % 10)) % 10
        card = base + str(check_digit)
        
        formatted_card = ' '.join([card[i:i+4] for i in range(0, len(card), 4)])
        return formatted_card

@app.route('/')
def home():
    # Auto-login test user
    test_user = User(1, "test_user", "Basic", None)
    login_user(test_user)
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        card_type = int(request.form.get('card_type', 1))
        card = generate_valid_card(card_type)
        
        return jsonify({
            'success': True,
            'card': card,
            'card_raw': card.replace(' ', '')
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/check_cooldown')
def check_cooldown():
    # Implement your cooldown logic here
    return jsonify({
        'can_generate': True,
        'wait_time': 0
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
