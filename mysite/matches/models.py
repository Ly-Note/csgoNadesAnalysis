from django.db import models

# Create your models here.
class Series(models.Model):
    #需要改，最好选用下拉框
    seriesName= models.CharField(max_length=100)
    def __str__(self):
        return self.seriesName

class Match(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    matchId = models.CharField(max_length=100)
    matchName =  models.CharField(max_length=100)
    dateTime = models.DateField()
    duration = models.FloatField()
    ticks  = models.IntegerField()
    team1Name = models.CharField(max_length=100)
    team2Name = models.CharField(max_length=100)
    team1Score = models.IntegerField()
    team2Score = models.IntegerField()
    
    
class Hurt(models.Model):
    # 链接主键
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    steamid = models.CharField(max_length=100)
    name= models.CharField(max_length=100)
    nadeDamage = models.IntegerField()
    molotovDamage = models.IntegerField()
    incendiaryDamage = models.IntegerField()
    roundNumber = models.IntegerField()
    tick = models.IntegerField()
    hurtedSteamid =models.CharField(max_length=100)
    
    