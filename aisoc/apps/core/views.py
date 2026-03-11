import json
import logging
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Conversation, Message, Role, Group, Task, Vulnerability, AttackChain, BatchTask
from .config import get_config

logger = logging.getLogger(__name__)


def health(request):
    return JsonResponse({'status': 'ok', 'version': get_config().config.version})


@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    data = json.loads(request.body)
    username = data.get('username', 'admin')
    password = data.get('password', '')
    
    config = get_config()
    if config.config.auth.password and password != config.config.auth.password:
        return JsonResponse({'error': 'Invalid password'}, status=401)
    
    user = authenticate(request, username=username, password=password)
    if user is None:
        user = authenticate(request, username=username)
        if user is None:
            from django.contrib.auth.models import User
            user = User.objects.create_user(username=username, password=password if password else 'admin')
    
    login(request, user)
    return JsonResponse({'message': 'Login successful', 'user': {'username': user.username, 'role': user.role}})


@login_required
def logout(request):
    django_logout(request)
    return JsonResponse({'message': 'Logout successful'})


@login_required
def current_user(request):
    return JsonResponse({
        'username': request.user.username,
        'role': request.user.role,
        'is_authenticated': request.user.is_authenticated,
    })


@login_required
def conversations(request):
    if request.method == 'GET':
        convs = Conversation.objects.filter(user=request.user)[:50]
        return JsonResponse({
            'conversations': [
                {'id': str(c.id), 'title': c.title, 'created_at': c.created_at.isoformat(), 'updated_at': c.updated_at.isoformat()}
                for c in convs
            ]
        })
    elif request.method == 'POST':
        data = json.loads(request.body)
        conv = Conversation.objects.create(user=request.user, title=data.get('title', 'New Conversation'))
        return JsonResponse({'id': str(conv.id), 'title': conv.title})


@login_required
def conversation_detail(request, conversation_id):
    try:
        conv = Conversation.objects.get(id=conversation_id, user=request.user)
    except Conversation.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)
    
    if request.method == 'GET':
        return JsonResponse({
            'id': str(conv.id),
            'title': conv.title,
            'created_at': conv.created_at.isoformat(),
            'updated_at': conv.updated_at.isoformat(),
        })
    elif request.method == 'PUT':
        data = json.loads(request.body)
        conv.title = data.get('title', conv.title)
        conv.save()
        return JsonResponse({'message': 'Updated'})
    elif request.method == 'DELETE':
        conv.delete()
        return JsonResponse({'message': 'Deleted'})


@login_required
def messages(request, conversation_id):
    try:
        conv = Conversation.objects.get(id=conversation_id, user=request.user)
    except Conversation.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)
    
    if request.method == 'GET':
        msgs = conv.messages.all()
        return JsonResponse({
            'messages': [
                {
                    'id': str(m.id),
                    'role': m.role,
                    'content': m.content,
                    'tool_calls': m.tool_calls,
                    'tool_results': m.tool_results,
                    'created_at': m.created_at.isoformat(),
                }
                for m in msgs
            ]
        })
    elif request.method == 'POST':
        data = json.loads(request.body)
        msg = Message.objects.create(
            conversation=conv,
            role=data.get('role', 'user'),
            content=data.get('content', ''),
            tool_calls=data.get('tool_calls', []),
            tool_results=data.get('tool_results', []),
        )
        return JsonResponse({'id': str(msg.id)})


@login_required
def roles(request):
    if request.method == 'GET':
        roles = Role.objects.all()
        return JsonResponse({
            'roles': [
                {'id': str(r.id), 'name': r.name, 'description': r.description, 'is_default': r.is_default}
                for r in roles
            ]
        })
    elif request.method == 'POST':
        data = json.loads(request.body)
        role = Role.objects.create(
            name=data.get('name'),
            description=data.get('description', ''),
            system_prompt=data.get('system_prompt', ''),
            tools=data.get('tools', []),
            is_default=data.get('is_default', False),
        )
        return JsonResponse({'id': str(role.id), 'name': role.name})


@login_required
def role_detail(request, role_id):
    try:
        role = Role.objects.get(id=role_id)
    except Role.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)
    
    if request.method == 'GET':
        return JsonResponse({
            'id': str(role.id),
            'name': role.name,
            'description': role.description,
            'system_prompt': role.system_prompt,
            'tools': role.tools,
            'is_default': role.is_default,
        })
    elif request.method == 'PUT':
        data = json.loads(request.body)
        role.name = data.get('name', role.name)
        role.description = data.get('description', role.description)
        role.system_prompt = data.get('system_prompt', role.system_prompt)
        role.tools = data.get('tools', role.tools)
        role.is_default = data.get('is_default', role.is_default)
        role.save()
        return JsonResponse({'message': 'Updated'})
    elif request.method == 'DELETE':
        role.delete()
        return JsonResponse({'message': 'Deleted'})


@login_required
def groups(request):
    if request.method == 'GET':
        groups = Group.objects.all()
        return JsonResponse({
            'groups': [
                {'id': str(g.id), 'name': g.name, 'description': g.description}
                for g in groups
            ]
        })
    elif request.method == 'POST':
        data = json.loads(request.body)
        group = Group.objects.create(
            name=data.get('name'),
            description=data.get('description', ''),
            created_by=request.user,
        )
        return JsonResponse({'id': str(group.id), 'name': group.name})


@login_required
def group_detail(request, group_id):
    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)
    
    if request.method == 'GET':
        return JsonResponse({
            'id': str(group.id),
            'name': group.name,
            'description': group.description,
        })
    elif request.method == 'DELETE':
        group.delete()
        return JsonResponse({'message': 'Deleted'})


@login_required
def tasks(request):
    if request.method == 'GET':
        tasks = Task.objects.filter(user=request.user)[:50]
        return JsonResponse({
            'tasks': [
                {'id': str(t.id), 'name': t.name, 'status': t.status, 'progress': t.progress}
                for t in tasks
            ]
        })
    elif request.method == 'POST':
        data = json.loads(request.body)
        task = Task.objects.create(
            user=request.user,
            name=data.get('name', ''),
            status='pending',
        )
        return JsonResponse({'id': str(task.id)})


@login_required
def task_detail(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user=request.user)
    except Task.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)
    
    if request.method == 'GET':
        return JsonResponse({
            'id': str(task.id),
            'name': task.name,
            'status': task.status,
            'progress': task.progress,
            'result': task.result,
            'error': task.error,
        })
    elif request.method == 'DELETE':
        task.delete()
        return JsonResponse({'message': 'Deleted'})


@login_required
def vulnerabilities(request):
    if request.method == 'GET':
        vulns = Vulnerability.objects.filter(created_by=request.user)[:50]
        return JsonResponse({
            'vulnerabilities': [
                {'id': str(v.id), 'name': v.name, 'severity': v.severity, 'url': v.url}
                for v in vulns
            ]
        })
    elif request.method == 'POST':
        data = json.loads(request.body)
        vuln = Vulnerability.objects.create(
            name=data.get('name', ''),
            severity=data.get('severity', 'info'),
            description=data.get('description', ''),
            url=data.get('url', ''),
            parameters=data.get('parameters', {}),
            payload=data.get('payload', ''),
            evidence=data.get('evidence', ''),
            created_by=request.user,
        )
        return JsonResponse({'id': str(vuln.id)})


@login_required
def vulnerability_detail(request, vuln_id):
    try:
        vuln = Vulnerability.objects.get(id=vuln_id, created_by=request.user)
    except Vulnerability.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)
    
    if request.method == 'GET':
        return JsonResponse({
            'id': str(vuln.id),
            'name': vuln.name,
            'severity': vuln.severity,
            'description': vuln.description,
            'url': vuln.url,
        })
    elif request.method == 'DELETE':
        vuln.delete()
        return JsonResponse({'message': 'Deleted'})


@login_required
def attack_chains(request):
    if request.method == 'GET':
        chains = AttackChain.objects.filter(created_by=request.user)[:50]
        return JsonResponse({
            'attack_chains': [
                {'id': str(c.id), 'name': c.name, 'status': c.status}
                for c in chains
            ]
        })
    elif request.method == 'POST':
        data = json.loads(request.body)
        chain = AttackChain.objects.create(
            name=data.get('name', ''),
            description=data.get('description', ''),
            steps=data.get('steps', []),
            status='pending',
            created_by=request.user,
        )
        return JsonResponse({'id': str(chain.id)})


@login_required
def attack_chain_detail(request, chain_id):
    try:
        chain = AttackChain.objects.get(id=chain_id, created_by=request.user)
    except AttackChain.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)
    
    if request.method == 'GET':
        return JsonResponse({
            'id': str(chain.id),
            'name': chain.name,
            'description': chain.description,
            'steps': chain.steps,
            'status': chain.status,
        })
    elif request.method == 'DELETE':
        chain.delete()
        return JsonResponse({'message': 'Deleted'})


@login_required
def batch_tasks(request):
    if request.method == 'GET':
        tasks = BatchTask.objects.filter(created_by=request.user)[:50]
        return JsonResponse({
            'batch_tasks': [
                {'id': str(t.id), 'name': t.name, 'status': t.status, 'progress': t.progress, 'total': t.total}
                for t in tasks
            ]
        })
    elif request.method == 'POST':
        data = json.loads(request.body)
        task = BatchTask.objects.create(
            name=data.get('name', ''),
            target_list=data.get('target_list', []),
            tool_name=data.get('tool_name', ''),
            tool_config=data.get('tool_config', {}),
            total=len(data.get('target_list', [])),
            created_by=request.user,
        )
        return JsonResponse({'id': str(task.id)})


@login_required
def batch_task_detail(request, task_id):
    try:
        task = BatchTask.objects.get(id=task_id, created_by=request.user)
    except BatchTask.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)
    
    if request.method == 'GET':
        return JsonResponse({
            'id': str(task.id),
            'name': task.name,
            'status': task.status,
            'progress': task.progress,
            'total': task.total,
            'results': task.results,
        })
    elif request.method == 'DELETE':
        task.delete()
        return JsonResponse({'message': 'Deleted'})


@login_required
def config(request):
    config = get_config()
    return JsonResponse({
        'version': config.config.version,
        'server': {'host': config.config.server.host, 'port': config.config.server.port},
        'auth': {'session_duration_hours': config.config.auth.session_duration_hours},
        'openai': {
            'base_url': config.config.openai.base_url,
            'model': config.config.openai.model,
        },
    })


@login_required
def update_config(request):
    return JsonResponse({'message': 'Config update not implemented in this version'})


@login_required
def openapi_spec(request):
    return JsonResponse({
        'openapi': '3.0.0',
        'info': {'title': 'AISOC API', 'version': get_config().config.version},
        'paths': {},
    })
