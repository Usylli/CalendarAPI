from django.db import models
from accounts import models as accounts_model

class Event(models.Model):
    user = models.ForeignKey(accounts_model.Users, verbose_name="User", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField() 
    ReminderTime = models.DateTimeField() 
    
