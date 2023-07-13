from django.db import models

# Create your models here.
class Series(models.Model):
    #改成唯一
    seriesName= models.CharField(max_length=100,primary_key=True)
    def __str__(self):
        return self.seriesName

class Match(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    matchId = models.CharField(max_length=100,primary_key=True)
    matchName =  models.CharField(max_length=100)
    dateTime = models.DateTimeField('date')
    duration = models.FloatField(default=0)
    ticks  = models.IntegerField(default=0)
    team1Name = models.CharField(max_length=100)
    team2Name = models.CharField(max_length=100)
    team1Score = models.IntegerField(default=0)
    team2Score = models.IntegerField(default=0)
    def __str__(self):
        return self.matchName
    
class Hurt(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    steamid = models.CharField(max_length=100)
    nadeDamage = models.IntegerField(default=0)
    molotovDamage = models.IntegerField(default=0)
    incendiaryDamage = models.IntegerField(default=0)
    roundNumber = models.IntegerField(default=0)
    tick = models.IntegerField(default=0)
    hurtedSteamid =models.CharField(max_length=100)
    
class Player(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    steamid = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    
    
    