from django.contrib import admin
from .models import GenZ
from .models import YoungPeople
# Register your models here.

class GenZAdmin(admin.ModelAdmin):
    list_display = ('_id', 'date', 'category', 'sentence', 'sentence_short', 'sentence_keywords', 'sentence_sentiment', 'sentence_sentiment_net', 'sentence_sent_score', 'sentence_sentiment_label', 'sentence_entities', 'sentence_non_entities')

class YoungPeopleAdmin(admin.ModelAdmin):
    list_display = ('_id', 'date', 'logits', 'net_sent', 'logits_mean', 'net_sent_mean', 'MA_logits', 'MA_net_sent', 'MA_net_sent_ema_alpha_01', 'MA_net_sent_ema_alpha_03', 'MA_net_sent_ema_alpha_05')

# Register your models here.
admin.site.register(GenZ, GenZAdmin)
admin.site.register(YoungPeople, YoungPeopleAdmin)