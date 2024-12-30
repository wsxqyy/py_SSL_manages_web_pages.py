import os
import shutil
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, render_template_string
from werkzeug.utils import secure_filename
import OpenSSL
import zipfile
import webbrowser
from threading import Timer

# 嵌入CSS样式
STYLES_CSS = """
body {
    font-family: Arial, sans-serif;
}
.container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
h1 {
    text-align: center;
}
.upload-btn, .back-btn {
    display: block;
    margin: 20px auto;
    padding: 10px 20px;
    background-color: #007bff;
    color: #fff;
    text-align: center;
    border-radius: 8px;
    text-decoration: none;
    box-shadow: 0 4px 8px rgba(0, 123, 255, 0.2);
    transition: background-color 0.3s;
}
.upload-btn:hover, .back-btn:hover {
    background-color: #0056b3;
}
table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
}
thead th {
    background-color: #007bff;
    color: #fff;
}
th, td {
    padding: 10px;
    text-align: left;
    border: 1px solid #ddd;
}
a {
    color: #007bff;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}
.form-group {
    margin-bottom: 20px;
}
label {
    display: block;
    margin-bottom: 5px;
}
textarea {
    width: 100%;
    height: 200px;
    padding: 10px;
    border-radius: 8px;
    border: 1px solid #ddd;
    resize: none;
}
button {
    display: block;
    width: 100%;
    padding: 10px;
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 4px 8px rgba(0, 123, 255, 0.2);
    transition: background-color 0.3s;
}
button:hover {
    background-color: #0056b3;
}
.cert-container {
    display: flex;
    justify-content: space-between;
    gap: 20px;
}
.cert-box {
    width: 48%;
}
"""

# 嵌入HTML模板
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="shortcut icon" href="fanx.ico" type="image/x-icon">
    <link rel="icon" href="fanx.ico" type="image/x-icon">
    <title>SSL证书管理</title>
    <style>
    {{ styles|safe }}
    </style>
</head>
<body>
    <div class="container">
        <h1>SSL证书管理</h1>
        <a href="{{ url_for('upload_file') }}" class="upload-btn">上传证书</a>
        <table>
            <thead>
                <tr>
                    <th>文件夹</th>
                    <th>文件名</th>
                    <th>域名</th>
                    <th>到期时间</th>
                    <th>操作</th>
                </tr>
            </thead>
            <tbody>
                {% for cert in certs %}
                <tr>
                    <td>{{ cert.folder }}</td>
                    <td>{{ cert.filename }}</td>
                    <td>{{ cert.domain }}</td>
                    <td>{{ cert.expire_date }}</td>
                    <td>
                        <a href="{{ url_for('view_file', folder=cert.folder) }}">查看</a>
                        <a href="{{ url_for('download_folder', folder=cert.folder) }}">下载</a>
                        <a href="{{ url_for('delete_file', folder=cert.folder) }}">删除</a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</body>
</html>
"""

UPLOAD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="shortcut icon" href="fanx.ico" type="image/x-icon">
    <link rel="icon" href="fanx.ico" type="image/x-icon">
    <title>上传SSL证书</title>
    <style>
    {{ styles|safe }}
    </style>
</head>
<body>
<div class="container">
    <h1>上传SSL证书</h1>
    <form method="post" enctype="multipart/form-data">
        <div class="form-group">
            <label for="key_file">上传KEY文件:</label>
            <input type="file" id="key_file" name="key_file">
            <textarea name="key_content" placeholder="或粘贴KEY文件内容"></textarea>
        </div>
        <div class="form-group">
            <label for="pem_file">上传PEM文件:</label>
            <input type="file" id="pem_file" name="pem_file">
            <textarea name="pem_content" placeholder="或粘贴PEM文件内容"></textarea>
        </div>
        <button type="submit">上传</button>
    </form>
</div>
</body>
</html>
"""

VIEW_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="shortcut icon" href="fanx.ico" type="image/x-icon">
    <link rel="icon" href="fanx.ico" type="image/x-icon">
    <title>查看SSL证书</title>
    <style>
    {{ styles|safe }}
    </style>
</head>
<body>
<div class="container">
    <h1>查看SSL证书</h1>
    <div class="cert-container">
        <div class="cert-box">
            <h2>PEM 文件</h2>
            <textarea readonly>{{ pem_content }}</textarea>
        </div>
        <div class="cert-box">
            <h2>KEY 文件</h2>
            <textarea readonly>{{ key_content }}</textarea>
        </div>
    </div>
    <a href="{{ url_for('index') }}" class="back-btn">返回</a>
</div>
</body>
</html>
"""

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
    return render_template_string(INDEX_HTML, styles=STYLES_CSS, certs=certs)

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

    return render_template_string(UPLOAD_HTML, styles=STYLES_CSS)

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

    return render_template_string(VIEW_HTML, styles=STYLES_CSS, pem_content=pem_content, key_content=key_content, folder=folder)

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