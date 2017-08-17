from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.conf import settings

from rest_framework.authtoken.models import Token

from authtools.models import AbstractEmailUser
# Create your models here.


class User(AbstractEmailUser):
    """
    Model to represent user in system
    """
    first_name = models.CharField(_('First name'), max_length=30)
    last_name = models.CharField(_('Last name'), max_length=30)
    is_manager = models.BooleanField(_('Is manager ?'), default=False)
    is_closed = models.BooleanField(_('Account closed ?'), default=False)
    passport_number = models.CharField(
        _('Passport number'),
        max_length=10,
        unique=True
    )
    balance = models.DecimalField(
        _('Balance'),
        max_digits=10,
        decimal_places=2,
        default=0,
        editable=False
    )

    email = models.EmailField(_('Email'), unique=True)

    @property
    def token(self):
        return Token.objects.get(user=self)

    @property
    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    @property
    def is_client(self):
        return not self.is_manager and not self.is_staff and not self.is_superuser


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        # creating Token for user (CustomUser model)
        Token.objects.create(user=instance)

        # sending mails to managers
        if instance.is_client:
            all_managers = User.objects.filter(is_manager=True)

            if all_managers:
                managers_emails = [manager.email for manager in all_managers]
                subject = 'Created New User with id: %d' % (instance.id)
                message = 'Was created new user: %s with id %d' % (instance.get_full_name, instance.id)
                send_mail(
                    subject=subject,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=managers_emails,
                    message=message
                )


            # sending mail to client

            message = 'Dear %s, Thank You for registration in our service, in the nearest future' \
                      'we activate your account and You can work with us' % (instance.get_full_name)

            send_mail(
                subject='Thank You for registration',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.email, ],
                message=message
            )
