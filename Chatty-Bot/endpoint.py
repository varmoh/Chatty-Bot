from flask import Flask, render_template, request, jsonify, Response
import pymongo
import yaml
import os
from bson import ObjectId

app = Flask(__name__, template_folder='web', static_folder='web/static')

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["chatbot_db"]

# Your Flask app with endpoints
# Add trigger, update trigger, delete trigger endpoints...

def get_triggers(language):
    collection = db[f"triggers_{language}"]
    triggers = list(collection.find({}, {"_id": 1, "trigger": 1, "response": 1}))

    # Convert ObjectId to string for serialization
    for trigger in triggers:
        trigger['_id'] = str(trigger['_id'])

    # Serialize triggers to YAML format
    yaml_triggers = yaml.dump({"triggers": triggers}, allow_unicode=True)

    return yaml_triggers

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/triggers', methods=['GET'])
def triggers():
    language = request.args.get('language', 'english')  # Default language to English if not specified
    yaml_triggers = get_triggers(language)
    return Response(yaml_triggers, mimetype='text/yaml')

@app.route('/add_trigger', methods=['POST'])
def add_trigger():
    data = request.json
    language = data.get("language", "english")  # Default to English if language not provided
    result = save_trigger_to_db(data, language)
    return result

@app.route('/update_trigger/<string:id>', methods=['PUT'])
def update_trigger(id):
    data = request.json
    language = data.get("language", "english")  # Default to English if language not provided
    collection = db[f"triggers_{language}"]
    result = collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    if result.modified_count > 0:
        return jsonify({'message': 'Trigger updated successfully'}), 200
    else:
        return jsonify({'message': 'No trigger found with the provided ID'}), 404

@app.route('/delete_trigger/<string:id>', methods=['DELETE'])
def delete_trigger(id):
    language = request.args.get('language', 'english')  # Default language to English if not specified
    collection = db[f"triggers_{language}"]
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count > 0:
        return jsonify({'message': 'Trigger deleted successfully'}), 200
    else:
        return jsonify({'message': 'No trigger found with the provided ID'}), 404

def save_trigger_to_db(trigger, language):
    collection = db[f"triggers_{language}"]
    existing_trigger = collection.find_one({"trigger": trigger["trigger"]})
    if existing_trigger:
        return jsonify({'message': 'Trigger already exists in the database'}), 400
    else:
        collection.insert_one(trigger)
        print("Trigger added to the database")
        return jsonify({'message': 'Trigger added successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)