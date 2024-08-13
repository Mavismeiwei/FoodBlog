from django.db import models

# Create your models here.

# 发送邮件
class Email(models.Model):
    nid = models.AutoField(primary_key=True)
    email = models.EmailField(verbose_name='Emails from sender')
    content = models.TextField(verbose_name='Send context')
    create_date = models.DateTimeField(verbose_name='Send time', auto_now=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = 'Email Sent'