import pymongo
import yaml
from flask import Flask, request, jsonify
from jinja2 import FileSystemLoader, Environment
from Levenshtein import distance
from fuzzywuzzy import fuzz

app = Flask(__name__, template_folder='chat', static_folder='chat/static')

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["chatbot_db"]

# Define the template folder explicitly
template_loader = FileSystemLoader(searchpath="./chat/static/")
template_env = Environment(loader=template_loader)

def get_response_from_chatbot(user_input, language):
    languages = ['estonian', 'english', 'lithuanian']  # Adjust the order as needed

    for lang in languages:
        collection = db[f"triggers_{lang}"]
        
        # Check if user input matches any trigger in the database
        trigger = collection.find_one({"trigger": user_input.lower()})
        if trigger:
            return trigger["response"]  # Return the entire response list

        # Check if similar trigger already exists using Levenshtein with a threshold of 1
        similar_triggers = collection.find()
        for similar_trigger in similar_triggers:
            if distance(user_input.lower(), similar_trigger["trigger"]) <= 1:
                return similar_trigger["response"]  # Return the entire response list

        # Check if similar trigger already exists using fuzzywuzzy with a threshold of 85
        similar_triggers = collection.find()
        for similar_trigger in similar_triggers:
            if fuzz.ratio(user_input.lower(), similar_trigger["trigger"]) >= 85:
                return similar_trigger["response"]  # Return the entire response list

    # Load language-specific unknown response
    return ["Sorry, I couldn't get a response from the chatbot"]

@app.route('/')
def home():
    # Render the template using the explicitly set template environment
    template = template_env.get_template('index.html')
    return template.render()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('user_input', '')
    language = data.get('language', 'english')  # Default to English if language not provided

    if not user_input:
        return jsonify({'response': "Please provide user input"}), 400

    chatbot_response = get_response_from_chatbot(user_input, language)

    # Clear the input value after sending the message
    user_input = ''

    return jsonify({'response': chatbot_response, 'user_input': user_input})

if __name__ == '__main__':
    app.run(port=5001)
