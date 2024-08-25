import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
import subprocess
from pathlib import Path

app = Flask(__name__)
app_root = Path(__file__).resolve().parent
app_root = app_root.as_posix()
UPLOAD_FOLDER = app_root + "/" + 'static/uploads/'
TXT_FOLDER = app_root + "/" + 'static/txt/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TXT_FOLDER'] = TXT_FOLDER

# Tạo thư mục nếu chưa tồn tại
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['TXT_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file1' not in request.files or 'file2' not in request.files:
        return "No file part", 400

    file1 = request.files.get('file1')
    file2 = request.files.get('file2')

    if file1 and file1.filename:
        file1_path = os.path.join(app.config['UPLOAD_FOLDER'], "file1.png")
        file1.save(file1_path)

    if file2 and file2.filename:
        file2_path = os.path.join(app.config['UPLOAD_FOLDER'], "file2.png")
        file2.save(file2_path)

    # Tạo tệp văn bản chứa đường dẫn hai tệp ảnh
    txt_file_path = os.path.join(app.config['TXT_FOLDER'], 'image_paths.txt')
    with open(txt_file_path, 'w') as txt_file:
        if file1 and file1.filename:
            txt_file.write(f"{file1_path}\n")
        if file2 and file2.filename:
            txt_file.write(f"{file2_path}\n")

    return redirect(url_for('index'))

@app.route('/download-txt')
def download_txt():
    return send_from_directory(app.config['TXT_FOLDER'], 'image_paths.txt', as_attachment=True)

@app.route('/run-script', methods=['POST'])
def run_script():
    # try:
        # Execute the shell script
    result = subprocess.run(["C:/Program Files/Git/bin/bash.exe", app_root + '/'+ "test.sh"], text=True)
    # except subprocess.CalledProcessError as e:
    #     result = f"An error occurred: {e}"
    with open(app_root + '/' + 'final_predict.txt', 'r') as result_file:
        result_content = result_file.read()
    
    return jsonify({'result': result_content})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
