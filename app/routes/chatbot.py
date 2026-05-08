from flask import Blueprint, render_template, request, jsonify
from app.services.chatbot import get_chatbot_response

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/chatbot')
def chatbot_page():
    return render_template('chatbot.html')

@chatbot_bp.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({'error': 'Message vide'}), 400
    
    response = get_chatbot_response(user_message)
    return jsonify({'response': response})
