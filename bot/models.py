from django.db import models

# Create your models here.
class person(models.Model):
    fbid = models.CharField(max_length = 250)
    location_lat = models.CharField(max_length = 250 , default = 'NULL')
    location_long = models.CharField(max_length = 250 , default = 'NULL')
    # time = models.CharField(max_length = 1000)
    state = models.CharField(max_length = 1000, default = 'NULL')
    name = models.CharField(max_length = 1000, default = 'NULL')
    issue = models.CharField(max_length = 1000, default = 'NULL')
    # emailid= models.CharField(max_length = 1000, default = 'NULL')
    # dp = models.CharField(max_length = 1000, default = 'NULL')
    # ppl = models.CharField(max_length = 1000, default = 'NULL')
    # requests =  models.CharField(max_length = 1000, default = 'NULL')

    def __str__(self):
        return self.fbid
