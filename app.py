from flask import Flask, render_template, request, redirect, flash
from werkzeug.utils import secure_filename
from main import getPrediction
import os

# Save images to the 'static' folder

app = Flask(__name__, static_folder="static")


app.secret_key = "secret key"

UPLOAD_FOLDER = 'static/images/'

# Define the upload folder to save images uploaded by the user.
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

# Post method to the decorator to allow for form submission.


@app.route('/', methods=['POST'])
def submit_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            label = getPrediction(filename)
            flash(label)
            full_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            flash(full_filename)
            return redirect('/')


if __name__ == "__main__":
    # Define port and map container port to localhost
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)  # Define 0.0.0.0 for Docker
