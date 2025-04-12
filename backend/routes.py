from flask import Blueprint, request

from realtime_agents.model_prompts import query_rag

api = Blueprint('api', __name__)

@api.route('/')
def hello():
    return "Welcome to flask api!"

# This are some sample routes
@api.route('/users', methods=['GET'])
def get_users():
    return {"message": "List of users"}

@api.route('/chat', methods=['GET'])
def get_chat():
    args = request.args
    prompt = args.get("prompt")
    user_id = args.get("user_id")
    return query_rag(prompt, user_id)

@api.route('/posts', methods=['GET'])
def get_posts():
    return {"message": "List of posts"}
