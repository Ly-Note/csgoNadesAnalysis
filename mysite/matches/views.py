from django.shortcuts import render
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect,JsonResponse,HttpResponse
from .forms import NameForm,ContactForm,UploadFileForm
from django.forms import ModelForm
from django.views.decorators.csrf import csrf_exempt
from .models import Series,Match,Hurt,Player
import json
import datetime

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def sucess(request):
    return render(request, "matches/uploads_sucess.html")

@csrf_exempt
def upload_json(request):
    if request.method == 'POST':
        str_series = request.GET.get('extra_param', None)
        if(str_series is None):
          return JsonResponse({'error': 'extra_param is null'}, status=400)

        str_data = request.body.decode('utf-8') 
        
        
        data = json.loads(str_data)
        s=createSeries(str_series)
        
        exists = Match.objects.filter(matchId=data['id']).exists()
        if exists:
            print("Blog object exists")
        else:
            m = createMatch(data,s)
            createHurt(data,m)
            createPlayer(data,m)
            print("Blog object does not exist")
        
        
        

        return JsonResponse({'message': 'Created'}, status=201)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

def createSeries(str_series):
    series = Series(seriesName = str_series)
    series.save()
    return series

def createMatch(data,s):
    t= datetime.datetime.fromisoformat(data['date'])
    m = Match(series = s,matchId = data['id'],
                  matchName=data['NameWithoutExtension'],dateTime = t,
                  duration = data['duration'],team1Name = data['team_ct']['team_name'],
                  team2Name = data['team_t']['team_name'],team1Score = data['team_ct']['score'],
                  team2Score = data['team_t']['score'],ticks = data['ticks']
                  )
    m.save()
    return m 

def createHurt(data,m):
        playerHurted = data['player_hurted']
        for h in playerHurted :
            # molotov 502
            if h['weapon']['element'] == 502  :
                hurt = Hurt(match=m,steamid = h['attacker_steamid'],nadeDamage =0,
                                molotovDamage=h['health_damage'],incendiaryDamage=0,
                                roundNumber = h['round_number'],
                                tick=h['tick'],hurtedSteamid=h['hurted_steamid'])
            # 燃烧弹503 
            elif h['weapon']['element']==503:
                hurt = Hurt(match=m,steamid = h['attacker_steamid'],nadeDamage =0,
                                molotovDamage=0,incendiaryDamage=h['health_damage'],
                                roundNumber = h['round_number'],
                                tick=h['tick'],hurtedSteamid=h['hurted_steamid'])
            # 手雷506
            elif h['weapon']['element']==506:
                hurt = Hurt(match=m,steamid = h['attacker_steamid'],incendiaryDamage =0,
                                molotovDamage=0,nadeDamage=h['health_damage'],
                                roundNumber = h['round_number'],
                                tick=h['tick'],hurtedSteamid=h['hurted_steamid'])
                
            else:
                continue
            hurt.save()
                
        return 

def createPlayer(data,m):
    players = data['players']
    for p in players:
        player = Player(match = m,steamid = p['steamid'],name = p['name'])
        player.save()
    return 
    
    
    