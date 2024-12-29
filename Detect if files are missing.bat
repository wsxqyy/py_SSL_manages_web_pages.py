@echo off
chcp 65001
setlocal enabledelayedexpansion

:: 定义文件和文件夹列表
set "folders=static templates"
set "files=SSL_manages_web_pages.py pip_depend.bat"
set "static_files=styles.css"
set "templates_files=index.html upload.html view.html"

:: 检查文件夹
for %%f in (%folders%) do (
    if not exist "%%f\" (
        echo Missing folder: %%f, 缺失文件夹：%%f
    )
)

:: 检查文件
for %%f in (%files%) do (
    if not exist "%%f" (
        echo Missing file: %%f, 缺失文件：%%f
    )
)

:: 检查static文件夹中的文件
for %%f in (%static_files%) do (
    if not exist "static\%%f" (
        echo Missing file in static folder: %%f, 静态文件夹中缺失文件：%%f
    )
)

:: 检查templates文件夹中的文件
for %%f in (%templates_files%) do (
    if not exist "templates\%%f" (
        echo Missing file in templates folder: %%f, 模板文件夹中缺失文件：%%f
    )
)

echo Check completed. 检查完成没有缺失。
pause