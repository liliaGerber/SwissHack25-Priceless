from bson.json_util import dumps
from flask import Blueprint, request, Response
from pymongo import MongoClient

from realtime_agents.model_prompts import query_rag

api = Blueprint('api', __name__)
LLM_MODEL = 'gemma3:1b'
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "raiffeisen"
COLLECTION_NAME = "customers"
customer_collection = MongoClient(MONGO_URI)[DB_NAME][COLLECTION_NAME]

@api.route('/')
def hello():
    return "Welcome to flask api!"

@api.route('/customers', methods=['GET'])
def get_customers():
    customers = customer_collection.find()
    return Response(dumps(customers), mimetype='application/json')

@api.route('/chat', methods=['GET'])
def get_chat():
    args = request.args
    prompt = args.get("prompt")
    user_id = args.get("user_id")
    return query_rag(prompt, user_id)

@api.route('/posts', methods=['GET'])
def get_posts():
    return {"message": "List of posts"}

# functions

def get_all_customers():
    return  customer_collection.find()
