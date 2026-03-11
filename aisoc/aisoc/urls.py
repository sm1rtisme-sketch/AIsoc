from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.core.urls')),
    path('api/agent/', include('apps.agent.urls')),
    path('api/mcp/', include('apps.mcp.urls')),
    path('api/skills/', include('apps.skills.urls')),
    path('api/knowledge/', include('apps.knowledge.urls')),
    path('api/security/', include('apps.security.urls')),
    path('api/terminal/', include('apps.terminal.urls')),
    path('api/robot/', include('apps.robot.urls')),
]
