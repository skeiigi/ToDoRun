from django.apps import AppConfig


class OrganConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'organ'
    
    def ready(self):
        from .models import TaskCategory
        categories = [
            ('important_urgent', 'Важное срочное'),
            ('important_not_urgent', 'Важное не срочное'),
            ('not_important_urgent', 'Не важное срочное'),
            ('not_important_not_urgent', 'Не важное не срочное'),
        ]
        
        for code, name in categories:
            TaskCategory.objects.get_or_create(name=code)

