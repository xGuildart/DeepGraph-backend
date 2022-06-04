# Generated by Django 4.0.5 on 2022-06-03 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GenZ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_id', models.TextField()),
                ('date', models.TextField()),
                ('category', models.TextField()),
                ('sentence', models.TextField()),
                ('sentence_short', models.TextField()),
                ('sentence_keywords', models.TextField()),
                ('sentence_sentiment', models.TextField()),
                ('sentence_sentiment_net', models.TextField()),
                ('sentence_sent_score', models.TextField()),
                ('sentence_sentiment_label', models.TextField()),
                ('sentence_entities', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='YoungPeople',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_id', models.TextField()),
                ('date', models.TextField()),
                ('logits', models.TextField()),
                ('net_sent', models.TextField()),
                ('logits_mean', models.TextField()),
                ('net_sent_mean', models.TextField()),
                ('MA_logits', models.TextField()),
                ('MA_net_sent', models.TextField()),
                ('MA_net_sent_ema_alpha_01', models.TextField()),
                ('MA_net_sent_ema_alpha_03', models.TextField()),
                ('MA_net_sent_ema_alpha_05', models.TextField()),
            ],
        ),
    ]
