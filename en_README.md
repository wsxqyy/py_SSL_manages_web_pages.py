# 🌐 py_SSL_manages_web_pages.py README

## 🚀 Introduction

The `py_SSL_manages_web_pages.py` project is a Python script based on the Flask framework, designed to manage SSL certificate files. It provides a simple web interface that allows users to upload, view, download, and delete SSL certificate files in PEM and KEY formats.

## ✨ Features

- **Upload Certificates**: You can upload PEM and KEY files through the web interface.
- **View Certificate Information**: After uploading, you can view detailed information about the certificates, including the domain name and expiration date.
- **Download Certificates**: You can download the entire certificate folder, compressed in ZIP format.
- **Delete Certificates**: You can delete certificate folders that are no longer needed.

## 🛠️ Technology Stack

- **Flask**: Used for building the web server and handling HTTP requests.
- **OpenSSL**: Used for parsing certificate information from PEM files.
- **Werkzeug**: Used for handling file uploads and secure file naming.
- **Zipfile**: Used for creating ZIP compressed files.

## 📝 How to Use

### Environment Setup

Ensure that the Python environment is installed and the required Python libraries are installed. If you have trouble remembering the commands, you can run the `pip_depend.bat` file in the project to install dependencies:

```bash
pip install flask openssl werkzeug zipfile
```

### Running the Script

Run the following command in the terminal or command prompt:

```bash
python SSL_manages_web_pages.py
```

If the script does not automatically open a browser, you can manually open a browser and visit:

```
http://127.0.0.1:5000/
```

Please note that due to network issues, the parsing of the above web page was not successful. If you need the content of this web page, please check the legitimacy of the web page link and retry appropriately. If the parsing of this link is not necessary for your question, I can still answer your question as normal.

### Uploading Certificates

Select PEM and KEY files to upload through the web interface. You can also input the content of PEM and KEY through the form.

### Viewing and Manipulating Certificates

- After uploading, click on the corresponding links to view the certificate content.
- Click the download or delete button to perform the respective actions.

## ⚠️ Notes

- Please ensure that the files you upload are valid PEM and KEY files.
- The script, when running, uses the `ssl_files` folder as the default upload directory. Make sure you have the appropriate read and write permissions.
- The script will automatically create the `ssl_files` folder if it does not exist; otherwise, it will throw an error.
- If there are missing files, you can run the `Detect if files are missing.bat` in the project to check for missing files.

## 📊 Version History

- **v1.0**: Initial version, providing basic functions for uploading, viewing, downloading, and deleting.
- **v1.0.1**: Updated the instant-on dependent exe and updated the single-file version of the program script. 
## 🤝 Contributions

Contributions to this project are welcome. If you have any suggestions for improvement or find any issues, you can submit them through GitHub's Issue or Pull Request.

## 📜 License

This project is licensed under the [MIT License](LICENSE).
