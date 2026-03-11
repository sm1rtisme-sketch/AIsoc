from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('health', views.health, name='health'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('me', views.current_user, name='current_user'),
    path('conversations', views.conversations, name='conversations'),
    path('conversations/<uuid:conversation_id>', views.conversation_detail, name='conversation_detail'),
    path('conversations/<uuid:conversation_id>/messages', views.messages, name='messages'),
    path('roles', views.roles, name='roles'),
    path('roles/<uuid:role_id>', views.role_detail, name='role_detail'),
    path('groups', views.groups, name='groups'),
    path('groups/<uuid:group_id>', views.group_detail, name='group_detail'),
    path('tasks', views.tasks, name='tasks'),
    path('tasks/<uuid:task_id>', views.task_detail, name='task_detail'),
    path('vulnerabilities', views.vulnerabilities, name='vulnerabilities'),
    path('vulnerabilities/<uuid:vuln_id>', views.vulnerability_detail, name='vulnerability_detail'),
    path('attack-chains', views.attack_chains, name='attack_chains'),
    path('attack-chains/<uuid:chain_id>', views.attack_chain_detail, name='attack_chain_detail'),
    path('batch-tasks', views.batch_tasks, name='batch_tasks'),
    path('batch-tasks/<uuid:task_id>', views.batch_task_detail, name='batch_task_detail'),
    path('config', views.config, name='config'),
    path('config/update', views.update_config, name='update_config'),
    path('openapi.json', views.openapi_spec, name='openapi_spec'),
]
