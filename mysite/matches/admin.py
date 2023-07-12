from django.contrib import admin
from .models import Series,Match,Hurt,Player
# Register your models here.
admin.site.register(Series)
admin.site.register(Match)
admin.site.register(Hurt)
admin.site.register(Player)