from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives

from .models import UserResponse, Post


@receiver(post_save, sender=Post)
def post_created(instance, created, **kwargs):
    if not created:
        return

    emails = UserResponse.objects.filter(
        user__response=instance.response
    ).values_list('email', flat=True)

    subject = f'Новый отклик{instance.response}'

    text_content = (
        f'Автор: {instance.author}\n\n'
        f'Ссылка на пост: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'Автор: {instance.author}<br><br>'
        f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
        f'Ссылка на пост</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
