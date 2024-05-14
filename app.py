from flask import Flask, render_template, request, redirect, url_for, session
import random
import string
import sqlite3
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Function to generate a random password
def generate_random_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(8))

# Function to create the users table if it doesn't exist
def create_users_table():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            email TEXT,
            phone_number TEXT,
            generated_username TEXT,
            generated_password TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to create the results table if it doesn't exist
def create_results_table():
    conn = sqlite3.connect('results.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY,
            username TEXT,
            test_score INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Ensure the users and results tables are created when the application starts
create_users_table()
create_results_table()

# Registration route
@app.route('/')
def registration_form():
    return render_template('registration_form.html')

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone_number = request.form['phone_number']

        # Generate a random username using the first three characters of the email and a random 4-digit number
        email_prefix = email.split('@')[0][:3]
        random_number = ''.join(random.choices(string.digits, k=4))
        generated_username = email_prefix + random_number

        # Generate a random password
        generated_password = generate_random_password()

        # Store the user data in the database
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, email, phone_number, generated_username, generated_password) VALUES (?, ?, ?, ?, ?)", (username, email, phone_number, generated_username, generated_password))
        conn.commit()
        conn.close()

        return render_template('registration_result.html', username=generated_username, password=generated_password)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        input_username = request.form['username']
        input_password = request.form['password']

        # Check if the username and password match the data in the database
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE generated_username = ? AND generated_password = ?", (input_username, input_password))
        user = cursor.fetchone()
        conn.close()

        if user:
            # Store the username in the session
            session['username'] = user[1]
            return render_template('welcome.html', username=session['username'])
        else:
            return "Invalid username or password. Please try again."

    return render_template('login_form.html')

# Add a route for the TEST page
@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        # Handle the form submission
        test_option = request.form['test_option']
        if test_option == 'Aptitude':
            # Redirect to the aptitude test page
            return redirect(url_for('aptitude_test'))
        elif test_option == 'Programming':
            # Redirect to the programming test page
            return redirect(url_for('programming_test'))
    
    return render_template('test_options.html')

# Add routes for the aptitude and programming test pages
@app.route('/aptitude_test', methods=['GET', 'POST'])
def aptitude_test():
    aptitude_questions = []
    if request.method == 'POST':
        # Validate the answers and calculate test score
        user_answers = {}
        for i in range(1, 16):
            user_answers[f'answer{i}'] = request.form.get(f'answer{i}', '')

        # Fetch random aptitude questions from the API
        response = requests.get('https://aptitude-api.vercel.app/Age')
        if response.status_code == 200:
            aptitude_questions = response.json()
        else:
            # Use placeholder questions if API request fails
            aptitude_questions = [{'question': 'Placeholder question'}] * 15

        # Calculate test score (for demonstration)
        test_score = random.randint(0, 100)

        if 'username' in session:
            username = session['username']
            
            # Store the test results in the results database
            conn = sqlite3.connect('results.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO results (username, test_score) VALUES (?, ?)", (username, test_score))
            conn.commit()
            conn.close()

            return redirect(url_for('results'))

    return render_template('aptitude_test.html', questions=aptitude_questions)

@app.route('/programming_test')
def programming_test():
    # Fetch programming test questions from the database
    # Add code to fetch programming test questions from the database and render the template
    return render_template('programming_test.html')

# Add routes to handle submitting the test results
@app.route('/submit_test_results', methods=['POST'])
def submit_test_results():
    # Handle the form submission and store the test results in the database
    if 'username' in session:
        username = session['username']
        # Fetch other details of the user from the database if needed
        # Process and store the test results in a new database table
        # Pass user_answers, correct_answers, and total_result to the results template
        user_answers = {}  # Placeholder, fetch user answers from the form
        correct_answers = {}  # Placeholder, fetch correct answers from the database
        total_result = 0  # Placeholder, calculate total result
        return render_template('results.html', username=username, email="user@example.com", phone_number="1234567890", user_answers=user_answers, correct_answers=correct_answers, total_result=total_result)
    else:
        return redirect(url_for('login'))

# Add a route to fetch and display the test results
@app.route('/results')
def results():
    if 'username' in session:
        username = session['username']
        
        # Fetch test results for the logged-in user
        conn = sqlite3.connect('results.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM results WHERE username = ?", (username,))
        test_results = cursor.fetchall()
        conn.close()

        return render_template('results.html', username=username, test_results=test_results)
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
