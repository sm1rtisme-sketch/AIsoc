from django.apps import AppConfig


class SkillsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.skills'
    verbose_name = 'Skills'


class KnowledgeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.knowledge'
    verbose_name = 'Knowledge'


class SecurityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.security'
    verbose_name = 'Security'


class TerminalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.terminal'
    verbose_name = 'Terminal'


class RobotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.robot'
    verbose_name = 'Robot'
