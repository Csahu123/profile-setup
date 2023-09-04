from bson import ObjectId
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
profile_db = client.get_database('ProfileApp')

profile_collection = profile_db.get_collection('profile')

# Create unique indexes for user_id, personal_info.contact.phone, and personal_info.contact.email
profile_collection.create_index([("user_id", 1)], unique=True)
profile_collection.create_index([("personal_info.contact.phone", 1)], unique=True, partialFilterExpression={"personal_info.contact.phone": {"$exists": True}})
profile_collection.create_index([("personal_info.contact.email", 1)], unique=True, partialFilterExpression={"personal_info.contact.email": {"$exists": True}})


def create_student_profile_db(user_id,username,hash_password, user_class, user_image, user_designation, user_description, about, phone, email, address):
 
    user = profile_collection.insert_one({
        'user_id':user_id,
        'password': hash_password,
        'username': username,
        'user_class': user_class,
        'user_image': user_image,
        'user_designation': user_designation,
        'user_description': user_description,
        'personal_info': {
            'about': about,
            'contact': {
                'phone': phone,
                'email': email,
                'address': address
            }
        
        },
        'performance':{},
        'Attendance':{},
        'Interest':{},
        'parents':{}
    })
    return user

def get_students():
    return list(profile_collection.find({}))


def get_student(user_id):
    
    user = profile_collection.find_one({'user_id': user_id})
    # print(f"\nuser{user}")
    if user:
        user['_id'] = str(user['_id'])  # Convert ObjectId to a string
    
    return user

def update_student_profile_db(user_id, username,hash_password, user_class, filename, user_designation, user_description, about, phone, email, address):
    profile_collection.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': {
            'user_id':user_id,
            'username': username,
            'password':hash_password,
            'user_class': user_class,
            'user_image': filename,
            'user_designation': user_designation,
            'user_description': user_description,
            'personal_info': {
                'about': about,
                'contact': {
                    'phone': phone,
                    'email': email,
                    'address': address
                }
            },
            'performance':{},
            'Attendance':{},
            'Interest':{},
            'parents':{}
        }}
    )

