from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-this-in-production'

# Store contact form submissions
contact_submissions = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Create submission entry
        submission = {
            'name': name,
            'email': email,
            'message': message,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Store submission
        contact_submissions.append(submission)
        
        flash('Thank you for your message! I will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    
    return redirect(url_for('contact'))

@app.route('/admin/submissions')
def admin_submissions():
    # Simple admin page to view submissions
    # In production, add authentication
    return f'''
    <html>
    <head>
        <title>Contact Submissions</title>
        <style>
            body {{ 
                font-family: Arial, sans-serif; 
                padding: 20px; 
                background: #1a1a2e;
                color: #fff;
            }}
            .submission {{ 
                background: #16213e; 
                padding: 15px; 
                margin: 10px 0; 
                border-radius: 5px;
                border-left: 3px solid #00d9ff;
            }}
            h1 {{ color: #00d9ff; }}
            a {{ color: #00d9ff; text-decoration: none; }}
            a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <h1>Contact Form Submissions</h1>
        <p><a href="/">← Back to Home</a></p>
        <p>Total submissions: {len(contact_submissions)}</p>
        {''.join([f'''
        <div class="submission">
            <p><strong>Name:</strong> {sub["name"]}</p>
            <p><strong>Email:</strong> <a href="mailto:{sub["email"]}">{sub["email"]}</a></p>
            <p><strong>Message:</strong> {sub["message"]}</p>
            <p><strong>Time:</strong> {sub["timestamp"]}</p>
        </div>
        ''' for sub in contact_submissions]) if contact_submissions else '<p>No submissions yet.</p>'}
    </body>
    </html>
    '''

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host = "0.0.0.0", port = port)