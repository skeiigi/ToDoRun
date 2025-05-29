from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_default_categories(sender, **kwargs):
    from .models import TaskCategory
    categories = [
        ('important_urgent', 'Важное срочное'),
        ('important_not_urgent', 'Важное не срочное'),
        ('not_important_urgent', 'Не важное срочное'),
        ('not_important_not_urgent', 'Не важное не срочное'),
    ]
    
    for name, display_name in categories:
        TaskCategory.objects.get_or_create(name=name)

class OrganConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'organ'
    
    def ready(self):
        post_migrate.connect(create_default_categories, sender=self)
