from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ValidationError
from .models import EmailVerification
import logging

logger = logging.getLogger(__name__)
        
def send_verification_email(user):
    try:
        # Удаляем старые неподтвержденные коды
        EmailVerification.objects.filter(
            user=user,
            is_verified=False
        ).delete()
        
        # Генерируем код подтверждения
        code = EmailVerification.generate_code()
        
        # Создаем запись в базе данных
        verification = EmailVerification.objects.create(
            user=user,
            code=code
        )
        
        # Формируем сообщение
        subject = 'Подтверждение регистрации'
        message = f'''
        Здравствуйте, {user.username}!
        
        Спасибо за регистрацию. Для подтверждения вашего email, пожалуйста, введите следующий код:
        
        {code}
        
        Код действителен в течение 24 часов.
        
        С уважением,
        Команда ToDoRun
        '''
        
        # Отправляем email
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        
        logger.info(f"Verification email sent to {user.email}")
        return verification
    except Exception as e:
        # Если произошла ошибка при отправке, удаляем запись о верификации
        if 'verification' in locals():
            verification.delete()
        logger.error(f"Error sending verification email to {user.email}: {str(e)}")
        raise ValidationError(f'Ошибка при отправке email: {str(e)}') 