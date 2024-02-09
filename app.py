from flask import Flask, request, jsonify
from resumeparse import resumeparse
from flask_cors import CORS
import io
from flask_socketio import SocketIO, emit
import os
import re
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_cors import CORS
from subprocess import check_output
import json
import subprocess

app = Flask(__name__)
CORS(app, origins="http://localhost:3000")
socketio = SocketIO(app, cors_allowed_origins="*")  

class ResumeParser:
    @staticmethod
    def parse_resume(resume_file_path, count, count2, count3, email):
        print("54")
        parser_obj = resumeparse()
        parsed_resume_data = parser_obj.read_file(resume_file_path, count, count2, count3, email)
        print(parsed_resume_data, "99")
        return parsed_resume_data

@app.route('/resumeparse', methods=['POST'])
def parse_resume():
    is_folder_upload = request.form.get('isFolderUpload', False)
    count = 0
    count2 = 0
    count3 = 0
    batch_count = 0 
    email = []

    if is_folder_upload:
        uploaded_files = request.files.getlist('resumes[]')
        parsed_resume_data_list = []

        for i, resume_file in enumerate(uploaded_files, start=1):
            try:
                resume_file_path = new_filename(secure_filename(resume_file.filename), resume_file)
                resume_file.save(resume_file_path)

                parser_obj = resumeparse()
                parsed_resume_data = parser_obj.read_file(resume_file_path, count, count2, count3, email)
                parsed_resume_json = json.dumps(parsed_resume_data)

                php_script_path = "./htdocs/database_script.php"  # Update the path accordingly

                try:
                    result_json = check_output(["php", php_script_path], input=parsed_resume_json, text=True)
                except subprocess.CalledProcessError as e:
                    print("Error executing PHP script:")
                    print("Exit Code:", e.returncode)
                    print("Error Output:", e.stderr)
                    result_json = None  # Handle this as needed
                if result_json is not None:
                    result = json.loads(result_json)
                else:
                    result = {'error': 'PHP script execution failed'}
                # result = json.loads(result_json)

                os.remove(resume_file_path)

                parsed_resume_data = ResumeParser.parse_resume(resume_file_path, count, count2, count3, email)
                count = parsed_resume_data['row_newfile']
                count2 = parsed_resume_data['row_oldfile']
                count3 = parsed_resume_data['row_dublicate']
                if os.path.exists(resume_file_path):
                    os.remove(resume_file_path)
                # os.remove(resume_file_path)
                parsed_resume_data_list.append(parsed_resume_data)

                if i % 10 == 0:
                    progress_data = {
                        'current_count': i,
                        'total_count': len(uploaded_files),
                        'new_count': count,
                        'old_count': count2,
                        'dublicate_count': count3
                    }
                    socketio.emit('progress_update', progress_data)

            except subprocess.CalledProcessError as e:
                print("Error processing resume file:", e)

        if (i % 10 != 0) or (batch_count * 10 < len(uploaded_files)):
            progress_data = {
                'current_count': len(uploaded_files),
                'total_count': len(uploaded_files),
                'new_count': count,
                'old_count': count2,
                'dublicate_count': count3
            }
            socketio.emit('progress_update', progress_data)

        socketio.emit('parse_complete', {
            'new_count': count,
            'old_count': count2,
        })

    return jsonify({
        'new_count': count,
        'old_count': count2,
    })

def new_filename(org_filename, file):
    time = datetime.now()
    timestamp = time.strftime("%Y%m%d%H%M%S%f")
    unique_filename = f"{timestamp}_{org_filename}"
    return secure_filename(unique_filename)

@app.route('/greet', methods=['POST'])
def greet_user():
    print("hii")
    return jsonify({'message': 'hello'})

if __name__ == '__main__':
    app.run(debug=True)



# from flask import Flask, request, jsonify
# from resumeparse import resumeparse
# from flask_cors import CORS
# import io
# from flask_socketio import SocketIO, emit
# import os
# import re
# import docx2txt
# from datetime import datetime
# from werkzeug.utils import secure_filename
# from flask_cors import CORS

# #from io import BytesIO

# app = Flask(__name__)
# CORS(app)
# socketio = SocketIO(app, cors_allowed_origins="*")  
# class ResumeParser:
#     @staticmethod
#     def parse_resume(resume_file_path, count, count2,count3, email):
#         print("54")
#         parser_obj = resumeparse()
#         parsed_resume_data = parser_obj.read_file(resume_file_path, count, count2, count3, email)
#         print(parsed_resume_data, "99")
#         return parsed_resume_data

# @app.route('/resumeparse', methods=['POST'])
# def parse_resume():

    
#     is_folder_upload = request.form.get('isFolderUpload', False)
#     count = 0
#     count2 = 0
#     count3 = 0
#     batch_count = 0 
#     email = []
#     if is_folder_upload:
#         uploaded_files = request.files.getlist('resumes[]')
#         parsed_resume_data_list = []

#         for i, resume_file in enumerate(uploaded_files, start=1):
#             resume_file_path = new_filename(secure_filename(resume_file.filename), resume_file)
#             resume_file.save(resume_file_path)

#             parsed_resume_data = ResumeParser.parse_resume(resume_file_path, count, count2,count3, email)
#             count = parsed_resume_data['row_newfile']
#             count2 = parsed_resume_data['row_oldfile']
#             count3 = parsed_resume_data['row_dublicate']

#             os.remove(resume_file_path)
#             parsed_resume_data_list.append(parsed_resume_data)
#             if i % 10 == 0:
#                 progress_data = {
#                     'current_count': i,
#                     'total_count': len(uploaded_files),
#                     'new_count': count,
#                     'old_count': count2,
#                     'dublicate_count': count3
#                 }
#                 socketio.emit('progress_update', progress_data)


#         if batch_count * 10 < len(uploaded_files):
#             progress_data = {
#                 'current_count': len(uploaded_files),
#                 'total_count': len(uploaded_files),
#                 'new_count': count,
#                 'old_count': count2,
#                 'dublicate_count': count3
#             }
#             socketio.emit('progress_update', progress_data)

#         socketio.emit('parse_complete', {
#             'new_count': count,
#             'old_count': count2,
#         })

#     return jsonify({
#         'new_count': count,
#         'old_count': count2,
#     })

# def new_filename(org_filename, file):
#     time = datetime.now()
#     timestamp = time.strftime("%Y%m%d%H%M%S%f")
#     unique_filename = f"{timestamp}_{org_filename}"
#     return secure_filename(unique_filename)
# @app.route('/greet', methods=['POST'])
# def greet_user():
#     print("hii")
#     return jsonify({'message':'hello'})


# if __name__ == '__main__':
#     app.run(debug=True)