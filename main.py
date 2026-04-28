from flask import Flask, render_template

# Initialize Flask with the template folder
app = Flask(__name__, template_folder='template')

@app.route('/')
def index():
    # THIS FIXES KOYEB STARTING LOOP
    # When Koyeb pokes port 8080, it sees this and says "Healthy!"
    return "Bot Web Server is Running Successfully!", 200

@app.route('/dl/<file_id>')
def download_page(file_id):
    # This is where you would use your dl.html
    return render_template('dl.html', file_name="Your File", direct_link="#")
    
