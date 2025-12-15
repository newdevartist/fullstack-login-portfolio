from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  # Κλειδί για την ασφάλεια

# Παράδειγμα χρηστών (σε πραγματική εφαρμογή, θα χρησιμοποιήσεις βάση δεδομένων)
users = {}

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data['email']
    password = data['password']
    
    if email in users:
        return jsonify({'message': 'User already exists'}), 400  # Αν ο χρήστης υπάρχει ήδη
    
    hashed_password = generate_password_hash(password)  # Κρυπτογράφηση του κωδικού
    users[email] = hashed_password
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    
    if email not in users:
        return jsonify({'message': 'User not found'}), 404  # Αν δεν βρεθεί ο χρήστης
    
    if not check_password_hash(users[email], password):  # Επαλήθευση του κωδικού
        return jsonify({'message': 'Invalid credentials'}), 400
    
    return jsonify({'message': 'Login successful'}), 200

if __name__ == '__main__':
    app.run(debug=True)  # Εκκίνηση του server
