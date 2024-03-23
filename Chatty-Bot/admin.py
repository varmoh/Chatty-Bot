import yaml
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["chatbot_db"]

def add_trigger(trigger):
    collection = db["triggers"]
    collection.insert_one(trigger)
    print("Trigger added successfully")

def update_trigger(trigger_id, new_trigger):
    collection = db["triggers"]
    result = collection.update_one({"_id": trigger_id}, {"$set": new_trigger})
    if result.modified_count > 0:
        print("Trigger updated successfully")
    else:
        print("No trigger found with the provided ID")

def delete_trigger(trigger_id):
    collection = db["triggers"]
    result = collection.delete_one({"_id": trigger_id})
    if result.deleted_count > 0:
        print("Trigger deleted successfully")
    else:
        print("No trigger found with the provided ID")

def main():
    print("Welcome to the ChatBot Admin Panel!")
    print("1. Add Trigger")
    print("2. Update Trigger")
    print("3. Delete Trigger")
    choice = input("Enter your choice (1/2/3): ")

    if choice == "1":
        trigger = {
            "trigger": input("Enter the trigger: "),
            "response": input("Enter the response: ")
        }
        add_trigger(trigger)
    elif choice == "2":
        trigger_id = input("Enter the ID of the trigger to update: ")
        new_trigger = {
            "trigger": input("Enter the updated trigger: "),
            "response": input("Enter the updated response: ")
        }
        update_trigger(trigger_id, new_trigger)
    elif choice == "3":
        trigger_id = input("Enter the ID of the trigger to delete: ")
        delete_trigger(trigger_id)
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
