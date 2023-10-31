# Trimark Upload Platform

## Overview

The Trimark Upload Platform is a Flask-based web application designed to 
facilitate the upload and processing of Excel files. The application 
provides a user-friendly drag-and-drop interface for file uploads, 
executes a specified processing application, and displays the results to the user.

## Features

- **File Upload**: Easily upload Excel files for processing.
- **Excel File Processing**: Automatically processes uploaded Excel files.
- **Result Display**: Displays the results of the Excel file processing.
- **Batch File Execution**: Executes a Windows batch file for additional processing tasks.

## Prerequisites
- Python 3.x
- Flask
- Pandas
- openpyxl
- python_decouple
- pyodbc

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/jcarter62/trimark-upload-platform.git
    ```

2. **Navigate to Project Directory**

    ```bash
    cd trimark-upload-platform
    ```

3. **Install Required Packages**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the Flask Application**

    ```bash
    \venv\Scripts\python.exe -m flask run 
    ```

2. **Access the Web Interface**

    Open your web browser and navigate to `http://127.0.0.1:5000/`.

3. **Upload Excel File**

    Select an Excel file into the designated upload area.

4. **Execute Processing**

    Click the "Process" button to execute the processing application.

5. **View Results**

    The results of the processing will be displayed on the web interface.

## License

This project is licensed under the MIT License. See the [LICENSE.md](LICENSE.md) file for details.
