from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
app.secret_key = os.urandom(24)

# In-memory storage for simplicity
users = {}
problems = [
    {"id": 1, "question": "What is 2 + 2?", "options": ["3", "4", "5"], "correct": "4"},
    {"id": 2, "question": "What is the capital of France?", "options": ["London", "Paris", "Berlin"], "correct": "Paris"}
]

@app.route('/')
def index():
    if 'user' in session:
        return render_template('index.html', problems=problems)
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form['email']
    session['user'] = email
    if email not in users:
        users[email] = {"email": email, "score": 0}
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    print(f"Received data: {data}")  # Debug print
    user = session.get('user')
    if user:
        problem_id = data.get('problem_id')
        answer = data.get('answer')
        print(f"User: {user}, Problem ID: {problem_id}, Answer: {answer}")  # Debug print
        problem = next((p for p in problems if p['id'] == problem_id), None)
        if problem:
            if problem['correct'] == answer:
                users[user]['score'] += 1
                print(f"Updated user score: {users[user]}")  # Debug print
            else:
                print("Incorrect answer")  # Debug print
            return jsonify({"score": users[user]['score']})
        print("Problem not found")  # Debug print
        return jsonify({"error": "Problem not found"}), 404
    print("User not logged in")  # Debug print
    return jsonify({"error": "Not logged in"}), 403

@app.route('/leaderboard')
def leaderboard():
    sorted_users = sorted(users.values(), key=lambda x: x['score'], reverse=True)
    return render_template('leaderboard.html', users=sorted_users)

@app.route('/get_leaderboard', methods=['GET'])
def get_leaderboard():
    sorted_users = sorted(users.values(), key=lambda x: x['score'], reverse=True)
    return jsonify(sorted_users)

if __name__ == '__main__':
    app.run(debug=True)
