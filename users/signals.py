# users/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def send_protocol_config_update_email(sender, instance, **kwargs):
    if instance.protocol_config:
        # print(instance.protocol_config)

        subject = 'Configuration Updated'
        message = (
            f'Dear {instance.username},\n\n'
            f'Your configuration has been updated to "{instance.protocol_config}". You can view the assigned configuration details under "Profile".\n\n'    
            f'If you have any questions or need assistance, feel free to contact us.\n\n'
            f'Best regards,\n'
            f'Our Product Team'
        )

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,  # sender
            [instance.email],          # receiver
            fail_silently=False,
        )