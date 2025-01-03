<a href="https://github.com/wsxqyy/py_SSL_manages_web_pages.py/blob/main/en_README.md">Read through English documents</a>
# 🌐 py_SSL_manages_web_pages.py 自述文件

## 🚀 简介

`py_SSL_manages_web_pages.py` 项目是一个基于Flask框架的Python脚本，用于管理SSL证书文件。它提供了一个简单的Web界面，允许用户上传、查看、下载和删除SSL证书文件（PEM和KEY格式）。

## ✨ 功能

- **上传证书**：您可以通过Web界面上传PEM和KEY文件。
- **查看证书信息**：上传后，您可以查看证书的详细信息，包括域名和到期日期。
- **下载证书**：您可以下载整个证书文件夹，压缩为ZIP格式。
- **删除证书**：您可以删除不再需要的证书文件夹。

## 🛠️ 技术栈

- **Flask**：用于构建Web服务器和处理HTTP请求。
- **OpenSSL**：用于解析PEM文件中的证书信息。
- **Werkzeug**：用于处理文件上传和安全文件名。
- **Zipfile**：用于创建ZIP压缩文件。

## 📝 使用方法

### 环境准备

确保Python环境已安装，并安装所需的Python库。您如果记不住可以点击项目文件中的pip depend.bat来进行安装依赖：

```bash
pip install flask openssl werkzeug zipfile
```

### 运行脚本

在终端或命令提示符中运行：

```bash
python SSL_manages_web_pages.py
```

如果脚本没有自动打开浏览器，您可以自行打开浏览器访问：

```
http://127.0.0.1:5000/
```

### 上传证书

在Web界面中选择PEM和KEY文件上传。也可以通过表单输入PEM和KEY的内容。

### 查看和操作证书

- 上传后，点击相应的链接查看证书内容。
- 点击下载或删除按钮进行相应操作。

## ⚠️ 注意事项

- 请确保上传的文件是有效的PEM和KEY文件。
- 脚本运行时，默认的上传文件夹为 `ssl_files`，请确保有相应的读写权限。
- 脚本在启动时会自动创建 `ssl_files` 文件夹，如果不存在的话将报错。
- 如果文件有缺失，您可以点击项目中的Detect if files are missing.bat检查文件是否缺失。
## 📊 版本历史

- **v1.0**：初始版本，提供基本的上传、查看、下载和删除功能。
- **v1.0.1**：更新免安装依赖的exe，同时更新了单文件版本的程序脚本。 

## 🤝 贡献

欢迎对本项目进行贡献。如果你有任何改进建议或发现问题，可以通过GitHub的Issue或Pull Request提交。

## 📜 许可证

本项目采用[MIT许可证](LICENSE)。
