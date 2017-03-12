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
    location = models.CharField(max_length = 1000, default = 'NULL')
    # emailid= models.CharField(max_length = 1000, default = 'NULL')
    # dp = models.CharField(max_length = 1000, default = 'NULL')
    # ppl = models.CharField(max_length = 1000, default = 'NULL')
    # requests =  models.CharField(max_length = 1000, default = 'NULL')

    def __str__(self):
        return self.fbid


class constituency(models.Model):
    constituencyName = models.CharField(max_length = 250 , default = 'NULL')
    problemHits = models.CharField(max_length = 250 , default = 'NULL')

    def __str__(self):
        return self.constituencyName




class issue(models.Model):
    constituencyName = models.ForeignKey(constituency, on_delete=models.CASCADE)
    problem = models.CharField(max_length = 250 , default = 'NULL')
    problemTag1 = models.CharField(max_length = 250 , default = 'NULL')
    problemTag2 = models.CharField(max_length = 250 , default = 'NULL')

    def __str__(self):
        return self.problem




class mla(models.Model):
    constituencyName = models.ForeignKey(constituency, on_delete=models.CASCADE)
    candidateName = models.CharField(max_length = 250 , default = 'NULL')
    contactDetails = models.CharField(max_length = 250 , default = 'NULL')
    crimalCases = models.CharField(max_length = 250 , default = 'NULL')
    educationalQualifications = models.CharField(max_length = 250 , default = 'NULL')

    def __str__(self):
        return self.candidateName        
