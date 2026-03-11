import json
import logging
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from apps.core.config import get_config
from apps.agent.agent import Agent

logger = logging.getLogger(__name__)


@login_required
@require_http_methods(["POST"])
def chat(request):
    data = json.loads(request.body)
    conversation_id = data.get('conversation_id')
    message = data.get('message', '')
    role = data.get('role', 'default')
    
    config = get_config()
    agent = Agent(config)
    
    response = agent.chat(conversation_id, message, role)
    return JsonResponse(response)


@login_required
@require_http_methods(["POST"])
def stream_chat(request):
    data = json.loads(request.body)
    conversation_id = data.get('conversation_id')
    message = data.get('message', '')
    role = data.get('role', 'default')
    
    config = get_config()
    agent = Agent(config)
    
    def generate():
        for chunk in agent.stream_chat(conversation_id, message, role):
            yield f"data: {json.dumps(chunk)}\n\n"
    
    from django.http import StreamingHttpResponse
    return StreamingHttpResponse(generate(), content_type='text/event-stream')
