from flask import Flask, jsonify, request, render_template
from werkzeug.utils import secure_filename
import os
import re
from db import *
import hashlib

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'

@app.route('/')
def home():
    return render_template('index.html')

def is_user_id_unique(user_id):
    # Query your database to check if the user_id already exists
    user = get_student(user_id)
    return user is None

def hash_password(password):
    # Create a new SHA-256 hash object
    sha256 = hashlib.sha256()

    # Update the hash object with the password bytes (encoded as UTF-8)
    sha256.update(password.encode('utf-8'))

    # Get the hexadecimal representation of the hash
    hashed_password = sha256.hexdigest()

    return hashed_password  


@app.route('/create_student_profile', methods=['GET', 'POST'])
def create_student_profile():
    user_id = request.form.get('user_id', '')
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    hashed_password = hash_password(password)

    user_class = request.form.get('user_class', '')
    # unknown_field = request.form.get('do not know yet')
    user_designation = request.form.get('user_designation', '')
    user_description = request.form.get('user_description', '')
    about = request.form.get('user_about', '')
    phone = request.form.get('phone', '')
    email = request.form.get('email', '')
    address = request.form.get('address', '')
    parents = request.form.get('parents', '')
    

    if not is_user_id_unique(user_id):
        return jsonify({'error': 'User ID already exists'}), 400
    
    
    # if not re.match(r'^[\w\.-]+@[\w\.-]+$', email):
    #     return "Invalid email address."
    
    
    # if not re.match(r'^\d{10}$', phone):
        # return "Invalid mobile number"
        # return render_template('index.html') + '<script>showAlert("phone", "Invalid phone number. It should be exactly 10 digits.");</script>'

    user_image = request.files['file']
    if user_image:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(user_image.filename))
        user_image.save(filename)

    personal_info = {
        'about': about,
        'contact': {
            'phone': phone,
            'email': email,
            'address': address
        }
    }

    performance = {
        
    }

    Attendance = {

    }

    Interest = {

    }

    parents = {

    }
    user_data = {
        'user_id': user_id,
        'username': username,
        'password':hashed_password,
        'user_class': user_class,
        'user_image': filename,
        'user_designation': user_designation,
        'user_description': user_description,
        'personal_info': personal_info,
        'performance':performance,
        'Attendance':Attendance,
        'Interest':Interest,
        'parents':parents
    }

    create_student_profile_db(user_id, username,password, user_class, filename, user_designation, user_description, about, phone, email, address)

    # return jsonify({'user_data': user_data})
    return jsonify(user_data)

@app.route('/get_user/<string:user_id>', methods=['GET'])
def get_user_profile(user_id):
    user = get_student(user_id)
    print(user)
    if user:
        user['_id'] = str(user['_id'])
        return jsonify(user)
    else:
        return jsonify({'error': 'User does not exists!!'})
    
    # return jsonify(user)



@app.route('/update_user', methods=['PUT', 'POST'])
def update_student_profile():
    
    user_data = get_student(user_id)

    if not user_data:
        return jsonify({"error": "User not found"}), 404
    
    # Get user data from the request
    user_id = request.form.get('user_id', user_data['user_id'])  # You may need to provide a user ID to identify the user to update
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    
    username = request.form.get('username', user_data['username'])
    password = request.form.get('password', user_data['password'])
    hashed_password = hash_password(password)

    user_class = request.form.get('user_class', user_data['user_class'])
    user_designation = request.form.get('user_designation', user_data['user_designation'])
    user_description = request.form.get('user_description', user_data['user_description'])
    about = request.form.get('user_about', user_data['user_about'])
    phone = request.form.get('phone', user_data['phone'])
    email = request.form.get('email', user_data['email'])
    address = request.form.get('address', user_data['address'])
    performance = request.form.get('performance', user_data['performance'])
    Interest = request.form.get('Interest', user_data['Interest'])
    Attendance = request.form.get('Attendance', user_data['Attendance'])
    parents = request.form.get('parents', user_data['parents'])
    user_image = request.files.get('file')

    # Optional: Handle the user image update
    if user_image:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(user_image.filename))
        user_image.save(filename)
    else:
        filename = None  # No new image provided

   

    # Call a function to update the user in the database
    update_student_profile_db(
        user_id,
        username,
        password,
        user_class,
        filename,  # Use None if no new image is provided
        user_designation,
        user_description,
        about,
        phone,
        email,
        address,
        performance,
        Interest,
        Attendance,
        parents
    )
    updated_user = get_student(user_id)
    updated_user['_id'] = str(updated_user['_id'])

    
    return jsonify(updated_user)

def search_by_mobile_number():
    pass

def search_by_email():
    pass

def search_by_username_or_user_id():
    pass

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip()

    if query:
        # Check if the query is a valid mobile number (all digits)
        if query.isdigit() and len(query) == 10:
            # Search for mobile number in all collections (student, parents, teacher)
            result = search_by_mobile_number(query)
        elif '@' in query:
            # Check if the query contains "@" (likely an email)
            # Search for email in all collections
            result = search_by_email(query)
        else:
            # Search for username or user ID in all collections
            result = search_by_username_or_user_id(query)

        return render_template('search_results.html', query=query, result=result)

    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)