from datetime import datetime
from flask import Flask, request, render_template, jsonify
import pandas as pd
import os
from decouple import config
from process_file import Process_File

#
# ref: https://chat.openai.com/share/eb7a430c-e5bb-4294-8c91-adbb3ade4d13
#

app = Flask(__name__)
upload_folder = config('UPLOAD_FOLDER')
file_path = ''

@app.route('/', methods=['GET', 'POST'])
def index():
    global file_path
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            file_path = os.path.join(upload_folder, uploaded_file.filename)
            uploaded_file.save(file_path)
            # Process the Excel file
            df = pd.read_excel(file_path)
            # Dummy processing: Count the number of rows and columns
            rows, cols = df.shape
            context = {
                "rows": rows,
                "cols": cols,
                "file_path": file_path,
                "recent_files": recent_processed_files()
            }
            return render_template('index.html', context=context)
    context = {
        "recent_files": recent_processed_files()
    }
    return render_template('index.html', context=context)

@app.route('/process', methods=['POST'])
def process():
    pf = Process_File()
    try:
        pf.exec(file_path)
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"result": "Processing failed."})

    return jsonify({"result": "Processing completed successfully."})


# create list of 10 most recent files in the destination folder.
def recent_processed_files():
    recent_files = []
    # get list of files in the folder
    dest_folder = config('DESTINATION_FOLDER')
    files = os.listdir(dest_folder)
    files.sort(reverse=True)
    files_w_details = []
    for f in files:
        # get file modify date and size in MB
        dtls = os.stat(os.path.join(dest_folder, f))
        # add file name to details
        mtime = dtls.st_mtime
        # convert mtime to yyyy-mm-dd hh:mm:ss
        modified = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
        dtls = {"name": f, "modified": modified}
        # add details to list
        files_w_details.append(dtls)
    # get 10 most recent files
    recent_files = files_w_details[:10]

    # for f in recent_files:
    #     # open each file, and determine the last meterreadingdate and the number of rows
    #     df = pd.read_excel(os.path.join(dest_folder, f["name"]))
    #     # get the last meterreadingdate
    #     last_meterreadingdate = df["Meter Reading Date"].max()
    #     # get the number of rows
    #     rows, cols = df.shape
    #     # add last_meterreadingdate and rows to the file details
    #     f["last_meterreadingdate"] = last_meterreadingdate
    #     f["rows"] = rows
    #     #
    return recent_files


@app.route('/fileinfo/<filename>', methods=['GET'])
def file_info(filename):
    # determine file date information for the file name
    dest_folder = config('DESTINATION_FOLDER')
    full_path = os.path.join(dest_folder, filename)

    df = pd.read_excel(full_path)
    # get the last meterreadingdate
    last_meterreadingdate = df["Meter Reading Date"].max()
    # get the number of rows
    rows, cols = df.shape
    # add last_meterreadingdate and rows to the file details

    dtls = os.stat(full_path)
    # add file name to details
    mtime = dtls.st_mtime
    # convert mtime to yyyy-mm-dd hh:mm:ss
    modified = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')

    return jsonify({"modified": modified, "rows": rows, "last_meterreadingdate": last_meterreadingdate})


if __name__ == '__main__':
    port = config('PORT')
    ip = config('IP')
    app.run(ip, port=port)

