from django.db import models
from accounts import models as accounts_model
from datetime import timedelta
from django.utils import timezone

class Event(models.Model):
    user = models.ForeignKey(accounts_model.Users, verbose_name="User", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField() #auto_now = True
    end_date = models.DateTimeField() #default = timezone.now().replace(hour=23, minute=59, second=59, microsecond=999999)
    ReminderTime = models.DateTimeField() #default = timedelta(hours=1)
    
#u.event_set.create(name='event_name', start_date=(timezone.now()+timedelta(days=1)))
#from accounts.models import Users
#from events.models import Event