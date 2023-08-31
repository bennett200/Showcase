from django.db import models

# Create your models here.

class Email(models.Model):
    BOOL_CHOICES = ((True, 'All USERS'), (False, 'SELECTED USERS'))
    title = models.CharField(max_length=150, null=True, blank=True, default='Title for Email')
    subject = models.CharField(max_length=150, null=True, blank=True, default='Store Subject')
    body = models.TextField(max_length='600', null=True, blank=True, default='Body message')
    message_sender = models.EmailField(max_length=254, null=True, blank=False, default='mystore@example.net')
    all_users = models.BooleanField(default=False, choices=BOOL_CHOICES, null=True, blank=True)

    message_recipients = models.TextField(max_length=300, null=True, blank=False, default='testuser@example.net')
    
    def __str__(self):
        return self.id
    
    @property
    def message_receivers(self):
        final_list = self.message_recipients.split(', ')
        return final_list