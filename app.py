from flask import Flask, render_template, request, redirect, url_for
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    subprocess.run(['python', 'person.py'])
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
