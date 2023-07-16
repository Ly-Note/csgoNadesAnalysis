from django.shortcuts import render
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect,JsonResponse,HttpResponse
from .forms import NameForm,ContactForm,UploadFileForm
from django.forms import ModelForm
from django.views.decorators.csrf import csrf_exempt
from .models import Series,Match,Hurt,Player
import json
import datetime
from django.views.generic import DetailView,ListView
from django.db.models import Sum

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def sucess(request):
    hurts = Hurt.objects.values('steamid').annotate(total_damage=Sum('nadeDamage'))
    players = Player.objects.all()
    player_dict = {player.steamid: player for player in players}
    for hurt in hurts:
        steamid = hurt['steamid']
        player = player_dict.get(steamid)
        if player is not None:
            hurt['steamid'] = player.name
        else:
            hurt['steamid'] = 'Unknown'
            
    
    id = "de_ancient_6001606039256035681662955289451887704"
    m = Match.objects.get(matchId=id)   
    #回合道具伤害（手雷，燃烧弹，道具伤害）
    m.hurt_set.values('steamid', 'roundNumber').annotate(total_Damage=Sum('nadeDamage'))
    m.hurt_set.values('steamid', 'roundNumber').annotate(total_Damage=Sum('molotovDamage')+Sum('incendiaryDamage'))
    m.hurt_set.values('steamid', 'roundNumber').annotate(total_Damage=Sum('nadeDamage')+Sum('molotovDamage')+Sum('incendiaryDamage'))
   
    #单颗手雷道具（手雷）
    m.hurt_set.values('steamid', 'tick','roundNumber').annotate(total_Damage=Sum('nadeDamage'))
    
    #受道具伤害（手雷，燃烧弹，道具伤害）
    m.hurt_set.values('hurtedSteamid', 'roundNumber').annotate(total_nadeHurt=Sum('nadeDamage'))
    m.hurt_set.values('hurtedSteamid', 'roundNumber').annotate(total_molotovIncendiaryHurt=Sum('molotovDamage')+Sum('incendiaryDamage'))
    m.hurt_set.values('hurtedSteamid', 'roundNumber').annotate(total_wholeHurt=Sum('nadeDamage')+Sum('molotovDamage')+Sum('incendiaryDamage'))

    #整场比赛（手雷，燃烧弹，道具伤害）
    m.hurt_set.values('steamid').annotate(total_Damage=Sum('nadeDamage'))
    m.hurt_set.values('steamid').annotate(total_Damage=Sum('molotovDamage')+Sum('incendiaryDamage'))
    m.hurt_set.values('steamid').annotate(total_Damage=Sum('nadeDamage')+Sum('molotovDamage')+Sum('incendiaryDamage'))


    #整场比赛承伤（手雷，燃烧弹，道具伤害）
    m.hurt_set.values('hurtedSteamid').annotate(total_Damage=Sum('nadeDamage'))
    m.hurt_set.values('hurtedSteamid').annotate(total_Damage=Sum('molotovDamage')+Sum('incendiaryDamage'))
    m.hurt_set.values('hurtedSteamid').annotate(total_Damage=Sum('nadeDamage')+Sum('molotovDamage')+Sum('incendiaryDamage'))
    #print(testm)
    
    return render(request, "matches/uploads_sucess.html")


def hurtsList(request,seriesName,matchId):
    s = Series.objects.get(seriesName=seriesName)
    m = s.match_set.get(matchId = matchId)
    # onds:one nade damages 
    #单颗手雷道具（按从大到小来排序）
    onds= m.hurt_set.values('steamid', 'tick','roundNumber').annotate(total_Damage=Sum('nadeDamage')).filter(total_Damage__gt=0).order_by('-total_Damage')
    
    # rnds:round nade damages
    # rmids:round molotovIncendiary damages
    # rwds:round nade and molotovIncendiary damages
    #回合道具伤害（手雷，燃烧弹，道具伤害）（按从大到小来排序）
    rnds  = m.hurt_set.values('steamid', 'roundNumber').annotate(total_Damage=Sum('nadeDamage')).order_by('-total_Damage').filter(total_Damage__gt=0)
    rmids = m.hurt_set.values('steamid', 'roundNumber').annotate(total_Damage=Sum('molotovDamage')+Sum('incendiaryDamage')).order_by('-total_Damage').filter(total_Damage__gt=0)
    rwds=m.hurt_set.values('steamid', 'roundNumber').annotate(total_Damage=Sum('nadeDamage')+Sum('molotovDamage')+Sum('incendiaryDamage')).order_by('-total_Damage').filter(total_Damage__gt=0)
   
    #整场比赛（手雷，燃烧弹，道具伤害）（按从大到小来排序）
    wnds = m.hurt_set.values('steamid').annotate(total_Damage=Sum('nadeDamage')).order_by('-total_Damage').filter(total_Damage__gt=0)
    wmids = m.hurt_set.values('steamid').annotate(total_Damage=Sum('molotovDamage')+Sum('incendiaryDamage')).order_by('-total_Damage').filter(total_Damage__gt=0)
    wwds = m.hurt_set.values('steamid').annotate(total_Damage=Sum('nadeDamage')+Sum('molotovDamage')+Sum('incendiaryDamage')).order_by('-total_Damage').filter(total_Damage__gt=0)
   
    #回合受道具伤害（手雷，燃烧弹，道具伤害）（按从大到小来排序）
    hrnds = m.hurt_set.values('hurtedSteamid', 'roundNumber').annotate(total_Damage=Sum('nadeDamage')).order_by('-total_Damage').filter(total_Damage__gt=0)
    hrmids =  m.hurt_set.values('hurtedSteamid', 'roundNumber').annotate(total_Damage=Sum('molotovDamage')+Sum('incendiaryDamage')).order_by('-total_Damage').filter(total_Damage__gt=0)
    hrwds = m.hurt_set.values('hurtedSteamid', 'roundNumber').annotate(total_Damage=Sum('nadeDamage')+Sum('molotovDamage')+Sum('incendiaryDamage')).order_by('-total_Damage').filter(total_Damage__gt=0)


    # hwwds:hurt of whole round whole damages
    #整场比赛承伤（手雷，燃烧弹，道具伤害）
    hwnds = m.hurt_set.values('hurtedSteamid').annotate(total_Damage=Sum('nadeDamage')).order_by('-total_Damage')
    hwmids = m.hurt_set.values('hurtedSteamid').annotate(total_Damage=Sum('molotovDamage')+Sum('incendiaryDamage')).order_by('-total_Damage')
    hwwds = m.hurt_set.values('hurtedSteamid').annotate(total_Damage=Sum('nadeDamage')+Sum('molotovDamage')+Sum('incendiaryDamage')).order_by('-total_Damage')
   
    

    players = Player.objects.all()
    player_dict = {player.steamid: player for player in players}
    
    steamId2SteamName(player_dict,onds,rnds,rmids,rwds,wnds,wmids,wwds)
    hurtedSteamid2SteamName(player_dict,hrnds,hrmids,hrwds,hwnds,hwmids,hwwds)

    
    return render(request, 'matches/hurts.html', 
                  {'onds': onds,
                   'rnds':rnds, 'rmids':rmids, 'rwds':rwds, 
                   'wnds':wnds,'wmids':wmids,'wwds':wwds,
                   'hrnds':hrnds,'hrmids':hrmids,'hrwds':hrwds,
                   'hwnds':hwnds,'hwmids':hwmids,'hwwds':hwwds,})

def steamId2SteamName(player_dict,*listDatas):
    for listData in listDatas:
        for d in listData:
            steamid = d['steamid']
            player = player_dict.get(steamid)
            if player is not None:
                d['steamid'] = player.name
            else:
                d['steamid'] = 'Unknown'
    return 

def hurtedSteamid2SteamName(player_dict,*listDatas):
    for listData in listDatas:
        for d in listData:
            steamid = d['hurtedSteamid']
            player = player_dict.get(steamid)
            if player is not None:
                d['hurtedSteamid'] = player.name
            else:
                d['hurtedSteamid'] = 'Unknown'
    return
    

class SeriesView(ListView):
    template_name = 'matches/index.html'
    context_object_name = 'series_list'
    def get_queryset(self):

        return Series.objects.all()
    
class MatchesView(ListView):
    template_name = 'matches/matches.html'
    context_object_name = 'matches_list'
    
    def get_queryset(self):
        name = self.kwargs.get('seriesName')
        s = Series.objects.get(seriesName=name)    
        return  s.match_set.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 获取URL中的参数，并且给context赋值，并在html展示{{sN}}
        # s = self.kwargs.get('seriesName')
        # print("s:",s)
        # context['sN'] = s
        return context
    

    
# class HurtsView(ListView):
#     template_name = 'matches/hurts.html'
#     context_object_name = 'hurt_list'
    
#     def get_queryset(self):
#         seriesName = self.kwargs.get('seriesName')
#         name = self.kwargs.get('matchId')
#         print(seriesName)
#         print(name)
#         name = "blastfall"
#         s = Series.objects.get(seriesName=name)    
#         return  s.match_set.all()
    

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
    
    
    