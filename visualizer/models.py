from django.db import models

# Create your models here.

class GenZ(models.Model):
    _id = models.TextField()
    date = models.TextField()
    category = models.TextField()
    sentence = models.TextField()
    sentence_short = models.TextField()
    sentence_keywords = models.TextField()
    sentence_sentiment = models.TextField()
    sentence_sentiment_net = models.TextField()
    sentence_sent_score = models.TextField()
    sentence_sentiment_label = models.TextField()
    sentence_entities = models.TextField()
    sentence_non_entities = models.TextField()

    def _str_(self):
        return self._id
    
class YoungPeople(models.Model):
    _id = models.TextField()
    date = models.TextField()
    logits = models.TextField()
    net_sent = models.TextField()
    logits_mean = models.TextField()
    net_sent_mean = models.TextField()
    MA_logits = models.TextField()
    MA_net_sent = models.TextField()
    MA_net_sent_ema_alpha_01 = models.TextField()
    MA_net_sent_ema_alpha_03 = models.TextField()
    MA_net_sent_ema_alpha_05 = models.TextField()
    
    def _str_(self):
        return self._id