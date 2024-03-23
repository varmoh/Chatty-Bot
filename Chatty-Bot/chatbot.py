import pymongo
import yaml
import os
import random
import requests
from Levenshtein import distance
from fuzzywuzzy import fuzz
from bson import ObjectId
from flask import Flask, render_template, request, jsonify
from bson import ObjectId

app = Flask(__name__)

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["chatbot_db"]

def get_response(user_input, language):
    collection = db[f"triggers_{language}"]
    
    # Check if user input matches any trigger in the database
    trigger = collection.find_one({"trigger": user_input.lower()})
    if trigger:
        response = trigger["response"]
        if isinstance(response, list):
            return random.choice(response)  # Randomly select a response from list
        elif isinstance(response, str):
            return response  # Return single response directly

    # Check if similar trigger already exists using Levenshtein with a threshold of 1
    similar_triggers = collection.find()
    for similar_trigger in similar_triggers:
        if distance(user_input.lower(), similar_trigger["trigger"]) <= 1:
            response = similar_trigger["response"]
            if isinstance(response, list):
                return random.choice(response)  # Randomly select a response from list
            elif isinstance(response, str):
                return response  # Return single response directly

    # Check if similar trigger already exists using fuzzywuzzy with a threshold of 85
    similar_triggers = collection.find()
    for similar_trigger in similar_triggers:
        if fuzz.ratio(user_input.lower(), similar_trigger["trigger"]) >= 85:
            response = similar_trigger["response"]
            if isinstance(response, list):
                return random.choice(response)  # Randomly select a response from list
            elif isinstance(response, str):
                return response  # Return single response directly

    # Return a generic unknown response
    return "Sorry, I don't understand that."

def main():
    print("Welcome to the ChatBot!")
    
    language = ""
    while language not in ["estonian", "english", "lithuanian"]:
        language = input("Please choose a language (estonian/english/lithuanian): ").lower()

        if language in ["estonian", "english", "lithuanian"]:
            load_triggers(language)
            print(f"Language set to {language.capitalize()}")
        else:
            print("Invalid language. Please choose estonian, english, or lithuanian.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response = get_response(user_input, language)
        print("Bot:", response.format(name=user_input))  # Format response with user input

def load_triggers(language):
    collection = db[f"triggers_{language}"]

    # Load triggers from YAML file based on language
    yaml_file = f"bot/triggers/{language}.yaml"
    with open(yaml_file, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
        triggers = data["triggers"]
        for trigger, responses in triggers.items():
            db_trigger = {
                "trigger": trigger.lower(),
                "response": responses
            }
            # Update existing trigger or insert new trigger
            collection.update_one({"trigger": trigger.lower()}, {"$set": db_trigger}, upsert=True)

    print(f"Triggers loaded for {language.capitalize()}")

if __name__ == "__main__":
    main()
