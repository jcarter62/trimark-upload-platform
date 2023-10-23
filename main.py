from flask import Flask, request, render_template, jsonify
import pandas as pd
import os
from decouple import config
import subprocess

#
# ref: https://chat.openai.com/share/eb7a430c-e5bb-4294-8c91-adbb3ade4d13
#

app = Flask(__name__)
upload_folder = config('UPLOAD_FOLDER')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            file_path = os.path.join(upload_folder, uploaded_file.filename)
            uploaded_file.save(file_path)
            # Process the Excel file
            df = pd.read_excel(file_path)
            # Dummy processing: Count the number of rows and columns
            rows, cols = df.shape
            return render_template('index.html', rows=rows, cols=cols)
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    try:
        batch_file_path = config('CMD')

        subprocess.run([batch_file_path], shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        return jsonify({"result": "Processing failed."})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"result": "Processing failed."})

    return jsonify({"result": "Processing completed successfully."})


if __name__ == '__main__':
    port = config('PORT')
    app.run(debug=True, port=port)

