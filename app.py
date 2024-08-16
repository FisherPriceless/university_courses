from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

@app.after_request
def remove_cors_headers(response):
    response.headers.pop('Access-Control-Allow-Origin', None)  # Remove the header
    return response

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['university_courses']
collection = db['courses']

# GET /courses - Get all courses
@app.route('/courses', methods=['GET'])
def get_courses():
    try:
        courses = list(collection.find())
        for course in courses:
            course['_id'] = str(course['_id'])  # Convert ObjectId to string for JSON serialization
        return jsonify(courses), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# DELETE /courses/<id> - Delete a course by ID
@app.route('/courses/<id>', methods=['DELETE'])
def delete_course(id):
    try:
        result = collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            return jsonify({"error": "Course not found"}), 404
        return jsonify({"message": "Course deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# POST /courses - Add a new course
@app.route('/courses', methods=['POST'])
def add_course():
    try:
        data = request.json
        course_id = collection.insert_one(data).inserted_id
        return jsonify({"message": "Course added successfully", "course_id": str(course_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# PUT /courses/<id> - Update a course by ID
@app.route('/courses/<id>', methods=['PUT'])
def update_course(id):
    try:
        data = request.json
        result = collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        if result.matched_count == 0:
            return jsonify({"error": "Course not found"}), 404
        return jsonify({"message": "Course updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
