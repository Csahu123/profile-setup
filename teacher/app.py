from flask import Flask, jsonify, request, render_template
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS
from db import create_user,update_user,get_user

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'

@app.route('/')
def home():
    return render_template('index.html')



@app.route('/create_user', methods=['GET', 'POST'])
def create_profile():
    username = request.form.get('username', '')
    # user_class = request.form.get('user_class', '')
    language = request.form.get('language','')
    call_icon = request.form.get('call_icon','')
    message_icon = request.form.get('message_icon','')
    
    user_designation = request.form.get('user_designation', '')
    user_description = request.form.get('user_description', '')
    about = request.form.get('user_about', '')
    useridname = request.form.get('useridname', '')
    password = request.form.get('password', '')
    
    phone = request.form.get('phone', '')
    email = request.form.get('email', '')
    address = request.form.get('address', '')
    department = request.form.get('department', '')
    experience = request.form.get('experience', '')
    specialization = request.form.get('specialization', '')
    totalClasses = request.form.get('totalClasses', '')
    attendedClasses = request.form.get('attendedClasses', '')
    Topic1 = request.form.get('topic1', '')
    Topic2 = request.form.get('topic2', '')
    award = request.form.get('award', '')
    hobbies = request.form.get('hobbies', '')
    favoriteTopic = request.form.get('favoriteTopic', '')


    user_image = request.files['file']
    if user_image:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(user_image.filename))
        user_image.save(filename)

    personal_info = {
        'status':{
            'user_designation':user_designation,
            'user_description':user_description
        },
        'about': about,
        'useridpassword':{
            'useridname':useridname,
            'password':password
        },
        'contact': {
            'phone': phone,
            'email': email,
            'address': address
        }
    }
    academic = {
        'department': department,
        'experience': experience,
        'specialization': specialization
    },
    attendence= {
        'totalClasses': totalClasses,
        'attendedClasses': attendedClasses,
    }
    performance={
            'classGrades': {
                'topic1': Topic1,
                'topic2': Topic2
            },
            'award':award
    }
    interest={
        'hobbies': hobbies,
        'favoriteTopic': favoriteTopic,
    }
    user_data = {
        'username': username,
        'language':language,
        'call_icon':call_icon,
        'message_icon':message_icon,
        # 'user_class': user_class,
        'user_image': filename,
        'user_designation': user_designation,
        'user_description': user_description,
        'personal_info': personal_info,
        'academic':academic,
        'attendence': attendence,
        'performance':performance,
        'interest':interest
    }

    create_user(username,language, call_icon, message_icon, filename, user_designation, user_description, about,useridname, password, phone, email, address, department,
                    experience, specialization,totalClasses,attendedClasses,Topic1,Topic2,award,hobbies,favoriteTopic)

    # return jsonify({'user_data': user_data})
    return jsonify(user_data)

@app.route('/get_user/<string:user_id>', methods=['GET'])
def get_user_profile(user_id):
    # Call the get_user function to retrieve the user's profile by user ID
    user = get_user(user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    return jsonify(user)

@app.route('/update_user/<string:user_id>', methods=['PUT', 'POST'])
def update_user_profile(user_id):
    user_data = get_user(user_id)

    if not user_data:
        return jsonify({"error": "User not found"}), 404

    username = request.form.get('username', user_data['username'])
    language = request.form.get('language', user_data['language'])
    call_icon = request.form.get('call_icon', user_data['call_icon'])
    message_icon = request.form.get('message_icon', user_data['message_icon'])

    user_designation = request.form.get('user_designation', user_data['personal_info']['status']['user_designation'])
    user_description = request.form.get('user_description', user_data['personal_info']['status']['user_description'])
    about = request.form.get('user_about', user_data['personal_info']['about'])
    useridname = request.form.get('useridname', user_data['personal_info']['useridpassword']['useridname'])
    password = request.form.get('password', user_data['personal_info']['useridpassword']['password'])
    phone = request.form.get('phone', user_data['personal_info']['contact']['phone'])
    email = request.form.get('email', user_data['personal_info']['contact']['email'])
    address = request.form.get('address', user_data['personal_info']['contact']['address'])
    department = request.form.get('department', user_data['academic']['department'])
    experience = request.form.get('experience', user_data['academic']['experience'])
    specialization = request.form.get('specialization', user_data['academic']['specialization'])
    totalClasses = request.form.get('totalClasses', user_data['attendence']['totalClasses'])
    attendedClasses = request.form.get('attendedClasses', user_data['attendence']['attendedClasses'])
    Topic1 = request.form.get('topic1', user_data['performance']['classGrades']['topic1'])
    Topic2 = request.form.get('topic2', user_data['performance']['classGrades']['topic2'])
    award = request.form.get('award', user_data['performance']['award'])
    hobbies = request.form.get('hobbies', user_data['interest']['hobbies'])
    favoriteTopic = request.form.get('favoriteTopic', user_data['interest']['favoriteTopic'])

    user_image = request.files.get('file')
    filename = user_data.get('user_image')  # Get the existing filename

    if user_image:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(user_image.filename))
        user_image.save(filename)

    update_user(user_id, username, language, call_icon, message_icon, filename, user_designation, user_description, about,
                useridname, password, phone, email, address, department, experience, specialization, totalClasses,
                attendedClasses, Topic1, Topic2, award, hobbies, favoriteTopic)

    updated_user = get_user(user_id)
    updated_user['_id'] = str(updated_user['_id'])

    return jsonify(updated_user)



if __name__ == '__main__':
    app.run(debug=True,port=5001)