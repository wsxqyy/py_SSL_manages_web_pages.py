import os
import shutil
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename
import OpenSSL
import zipfile
import webbrowser
from threading import Timer

UPLOAD_FOLDER = 'ssl_files'
ALLOWED_EXTENSIONS = {'pem', 'key'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'supersecretkey'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_cert_info(cert_path):
    with open(cert_path, 'rt') as f:
        cert = f.read()
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    domain = x509.get_subject().CN
    expire_date = x509.get_notAfter().decode('utf-8')
    expire_date = f"{expire_date[:4]}-{expire_date[4:6]}-{expire_date[6:8]}"
    return domain, expire_date

@app.route('/')
def index():
    certs = []
    for domain_folder in os.listdir(app.config['UPLOAD_FOLDER']):
        domain_folder_path = os.path.join(app.config['UPLOAD_FOLDER'], domain_folder)
        if os.path.isdir(domain_folder_path):
            for filename in os.listdir(domain_folder_path):
                if filename.endswith('.pem'):
                    domain, expire_date = get_cert_info(os.path.join(domain_folder_path, filename))
                    certs.append({'folder': domain_folder, 'filename': filename, 'domain': domain, 'expire_date': expire_date})
    return render_template('index.html', certs=certs)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        key_file = request.files.get('key_file')
        pem_file = request.files.get('pem_file')
        key_content = request.form.get('key_content')
        pem_content = request.form.get('pem_content')

        domain_folder = None

        if pem_file and allowed_file(pem_file.filename):
            pem_filename = secure_filename(pem_file.filename)
            pem_file_path = os.path.join(app.config['UPLOAD_FOLDER'], pem_filename)
            pem_file.save(pem_file_path)
            domain, _ = get_cert_info(pem_file_path)
            domain_folder = os.path.join(app.config['UPLOAD_FOLDER'], domain)
            if not os.path.exists(domain_folder):
                os.makedirs(domain_folder)
            os.rename(pem_file_path, os.path.join(domain_folder, 'uploaded_cert.pem'))
            print(f"PEM file saved to {os.path.join(domain_folder, 'uploaded_cert.pem')}")
        elif pem_content:
            pem_filename = secure_filename('uploaded_cert.pem')
            pem_file_path = os.path.join(app.config['UPLOAD_FOLDER'], pem_filename)
            with open(pem_file_path, 'w') as f:
                f.write(pem_content)
            domain, _ = get_cert_info(pem_file_path)
            domain_folder = os.path.join(app.config['UPLOAD_FOLDER'], domain)
            if not os.path.exists(domain_folder):
                os.makedirs(domain_folder)
            os.rename(pem_file_path, os.path.join(domain_folder, 'uploaded_cert.pem'))
            print(f"PEM file saved to {os.path.join(domain_folder, 'uploaded_cert.pem')}")

        if key_file and allowed_file(key_file.filename):
            key_filename = secure_filename(key_file.filename)
            key_file_path = os.path.join(domain_folder, 'uploaded_key.key')
            key_file.save(key_file_path)
            print(f"KEY file saved to {key_file_path}")
        elif key_content:
            key_filename = secure_filename('uploaded_key.key')
            key_file_path = os.path.join(domain_folder, key_filename)
            with open(key_file_path, 'w') as f:
                f.write(key_content)
            print(f"KEY file saved to {key_file_path}")

        flash('文件上传成功')
        return redirect(url_for('index'))

    return render_template('upload.html')

@app.route('/view/<folder>')
def view_file(folder):
    pem_path = os.path.join(app.config['UPLOAD_FOLDER'], folder, 'uploaded_cert.pem')
    key_path = os.path.join(app.config['UPLOAD_FOLDER'], folder, 'uploaded_key.key')
    
    if not os.path.exists(pem_path):
        flash(f"PEM文件未找到: {pem_path}")
        return redirect(url_for('index'))

    with open(pem_path, 'r') as pem_file:
        pem_content = pem_file.read()
    
    if os.path.exists(key_path):
        with open(key_path, 'r') as key_file:
            key_content = key_file.read()
    else:
        key_content = "KEY文件未找到"

    return render_template('view.html', pem_content=pem_content, key_content=key_content, folder=folder)

@app.route('/delete/<folder>')
def delete_file(folder):
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder)
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        flash('目录及其内容删除成功')
    else:
        flash('目录未找到')
    return redirect(url_for('index'))

@app.route('/download/<folder>')
def download_folder(folder):
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder)
    zip_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{folder}.zip")
    
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                zipf.write(os.path.join(root, file), arcname=os.path.join(folder, file))
    
    return send_from_directory(app.config['UPLOAD_FOLDER'], f"{folder}.zip", as_attachment=True)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    # 使用计时器来延迟打开浏览器，确保Flask服务器已经启动
    Timer(1, open_browser).start()
    app.run(debug=True)