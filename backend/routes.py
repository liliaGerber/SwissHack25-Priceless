from bson.json_util import dumps
from flask import Blueprint, request, Response
from pymongo import MongoClient

from realtime_agents.context_agents import InteractionAdvisorRAGAgent, VisionRAGAgent, SummaryRAGAgent, \
    RetirementRAGAgent, InvestmentRAGAgent, RealTimeAgent, PlanMyMeetingAgent

api = Blueprint('api', __name__)
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
    agent = InteractionAdvisorRAGAgent()
    return agent.query(prompt, user_id)


@api.route('/rag/investment', methods=['GET'])
def investment():
    prompt = request.args.get("prompt")
    user_id = request.args.get("user_id")
    agent = InvestmentRAGAgent()
    return agent.query(prompt, user_id)


@api.route('/rag/retirement', methods=['GET'])
def retirement():
    prompt = request.args.get("prompt")
    user_id = request.args.get("user_id")
    agent = RetirementRAGAgent()
    return agent.query(prompt, user_id)


@api.route('/rag/summary', methods=['GET'])
def summary():
    prompt = request.args.get("prompt")
    user_id = request.args.get("user_id")
    agent = SummaryRAGAgent()
    return agent.query(prompt, user_id)


@api.route('/rag/interaction', methods=['GET'])
def interaction():
    prompt = request.args.get("prompt")
    user_id = request.args.get("user_id")
    agent = InteractionAdvisorRAGAgent()
    return agent.query(prompt, user_id)


@api.route('/rag/vision', methods=['GET'], endpoint='vision_route')
def vision():
    prompt = request.args.get("prompt")
    user_id = request.args.get("user_id")
    agent = VisionRAGAgent()
    return agent.query(prompt, user_id)


@api.route('/rag/meeting', methods=['GET'])
def meeting():
    prompt = request.args.get("prompt")
    user_id = request.args.get("user_id")
    agent = RealTimeAgent()
    return agent.query(prompt, user_id)


@api.route('/rag/plan', methods=['GET'])
def plan():
    prompt = request.args.get("prompt")
    user_id = request.args.get("user_id")
    agent = PlanMyMeetingAgent()
    return agent.query(prompt, user_id)

