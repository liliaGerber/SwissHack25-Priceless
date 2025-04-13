from bson.json_util import dumps
from flask import Blueprint, Response, jsonify
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "raiffeisen"
COLLECTION_NAME = "summaries"

meeting_api = Blueprint('meeting_api', __name__)

@meeting_api.route('/', methods=['GET'])
def api_get_all_meetings():
    return Response(dumps(get_all_meetings()), mimetype='application/json')

@meeting_api.route('/customer/<customer_id>', methods=['GET'])
def api_get_meetings_by_customer(customer_id):
    return Response(dumps(get_meetings_by_customer(customer_id)), mimetype='application/json')

@meeting_api.route('/advisor/<advisor_id>', methods=['GET'])
def api_get_meetings_by_advisor(advisor_id):
    return Response(dumps(get_meetings_by_advisor(advisor_id)), mimetype='application/json')

@meeting_api.route('/clear', methods=['DELETE'])
def api_clear_meetings():
    clear_meetings()
    return jsonify({"status": "success", "message": "All meetings deleted."})


def get_meeting_collection():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    return db[COLLECTION_NAME]

def clear_meetings():
    collection = get_meeting_collection()
    result = collection.delete_many({})
    print(f"✅ Deleted {result.deleted_count} meeting(s).")

def get_all_meetings():
    collection = get_meeting_collection()
    return list(collection.find())

def get_meetings_by_customer(customer_id: str):
    collection = get_meeting_collection()
    return list(collection.find({"customerId": customer_id}))

def get_meetings_by_advisor(advisor_id: str):
    collection = get_meeting_collection()
    return list(collection.find({"advisorId": advisor_id}))
