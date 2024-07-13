from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

# Initialize Flask application
app = Flask(__name__)

# MySQL database configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",  # Replace with your MySQL password
    database="myntra"
)
cursor = db.cursor()

# Routes

@app.route('/')
def index():
    return render_template('gamification.html')

@app.route('/FashionChallenge.html')
def fashion_challenge():
    return render_template('FashionChallenge.html')

@app.route('/participate.html', methods=['GET', 'POST'])
def participate():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        outfit_description = request.form['outfit-description']

        insert_query = "INSERT INTO participant (Name, Email, `Outfit Description`) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (name, email, outfit_description))
        db.commit()

        return redirect(url_for('thank_you'))

    return render_template('participate.html')

@app.route('/thankyou')
def thank_you():
    return render_template('thankyou.html')

@app.route('/profile.html')
def profile():
    return render_template('profile.html')

@app.route('/admin.html', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        # Get form data correctly using the field names from admin.html
        challenge_title = request.form['challengeTitle']
        theme = request.form['theme']
        start_date = request.form['startDate']

        # Insert data into database
        insert_query = "INSERT INTO Challenge (ChallengeTitle, Theme, StartDate) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (challenge_title, theme, start_date))
        db.commit()

        # Optionally, you can redirect to a success page or back to the dashboard
        return redirect(url_for('admin'))

    # Render admin.html template for GET request
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)
