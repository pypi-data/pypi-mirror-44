# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-04-19 11:57
from __future__ import unicode_literals
import os

from django.db import migrations
from django.conf import settings


def insert_channels(apps, schema_editor):

    default = True

    Channel = apps.get_model("message_sender.channel")

    if settings.MESSAGE_BACKEND_TEXT == "vumi":
        if not Channel.objects.filter(channel_id="VUMI_TEXT").exists():
            vumi_url = os.environ.get("MESSAGE_SENDER_VUMI_API_URL_TEXT")
            vumi_account_key = os.environ.get("MESSAGE_SENDER_VUMI_ACCOUNT_KEY_TEXT")
            vumi_conv_key = os.environ.get("MESSAGE_SENDER_VUMI_CONVERSATION_KEY_TEXT")
            vumi_acc_token = os.environ.get("MESSAGE_SENDER_VUMI_ACCOUNT_TOKEN_TEXT")

            if vumi_url and vumi_account_key and vumi_conv_key and vumi_acc_token:
                channel = Channel()
                channel.channel_id = "VUMI_TEXT"
                channel.default = default
                channel.channel_type = "vumi"
                channel.concurrency_limit = settings.CONCURRENT_TEXT_LIMIT
                channel.message_delay = settings.TEXT_MESSAGE_DELAY
                channel.message_timeout = settings.TEXT_MESSAGE_TIMEOUT
                channel.configuration = {
                    "VUMI_API_URL": vumi_url,
                    "VUMI_ACCOUNT_KEY": vumi_account_key,
                    "VUMI_CONVERSATION_KEY": vumi_conv_key,
                    "VUMI_ACCOUNT_TOKEN": vumi_acc_token,
                }

                channel.save()

                default = False

    elif settings.MESSAGE_BACKEND_TEXT == "junebug":
        if not Channel.objects.filter(channel_id="JUNEBUG_TEXT").exists():
            june_url = os.environ.get("MESSAGE_SENDER_JUNEBUG_API_URL_TEXT")
            june_auth = os.environ.get("MESSAGE_SENDER_JUNEBUG_API_AUTH_TEXT")
            june_from = os.environ.get("MESSAGE_SENDER_JUNEBUG_API_FROM_TEXT")

            if june_url and june_auth and june_from:
                channel = Channel()
                channel.channel_id = "JUNEBUG_TEXT"
                channel.default = default
                channel.channel_type = "junebug"
                channel.concurrency_limit = settings.CONCURRENT_TEXT_LIMIT
                channel.message_delay = settings.TEXT_MESSAGE_DELAY
                channel.message_timeout = settings.TEXT_MESSAGE_TIMEOUT
                channel.configuration = {
                    "JUNEBUG_API_URL": june_url,
                    "JUNEBUG_API_AUTH": june_auth,
                    "JUNEBUG_API_FROM": june_from,
                }
                channel.save()

                default = False

    if settings.MESSAGE_BACKEND_VOICE == "vumi":
        if not Channel.objects.filter(channel_id="VUMI_VOICE").exists():
            vumi_url = os.environ.get("MESSAGE_SENDER_VUMI_API_URL_VOICE")
            vumi_account_key = os.environ.get("MESSAGE_SENDER_VUMI_ACCOUNT_KEY_VOICE")
            vumi_conv_key = os.environ.get("MESSAGE_SENDER_VUMI_CONVERSATION_KEY_VOICE")
            vumi_acc_token = os.environ.get("MESSAGE_SENDER_VUMI_ACCOUNT_TOKEN_VOICE")

            if vumi_url and vumi_account_key and vumi_conv_key and vumi_acc_token:
                channel = Channel()
                channel.channel_id = "VUMI_VOICE"
                channel.default = default
                channel.channel_type = "vumi"
                channel.concurrency_limit = settings.CONCURRENT_VOICE_LIMIT
                channel.message_delay = settings.VOICE_MESSAGE_DELAY
                channel.message_timeout = settings.VOICE_MESSAGE_TIMEOUT
                channel.configuration = {
                    "VUMI_API_URL": vumi_url,
                    "VUMI_ACCOUNT_KEY": vumi_account_key,
                    "VUMI_CONVERSATION_KEY": vumi_conv_key,
                    "VUMI_ACCOUNT_TOKEN": vumi_acc_token,
                }
                channel.save()

                default = False

    elif settings.MESSAGE_BACKEND_VOICE == "junebug":
        if not Channel.objects.filter(channel_id="JUNEBUG_VOICE").exists():
            june_url = os.environ.get("MESSAGE_SENDER_JUNEBUG_API_URL_VOICE")
            june_auth = os.environ.get("MESSAGE_SENDER_JUNEBUG_API_AUTH_VOICE")
            june_from = os.environ.get("MESSAGE_SENDER_JUNEBUG_API_FROM_VOICE")

            if june_url and june_auth and june_from:
                channel = Channel()
                channel.channel_id = "JUNEBUG_VOICE"
                channel.default = default
                channel.channel_type = "junebug"
                channel.concurrency_limit = settings.CONCURRENT_VOICE_LIMIT
                channel.message_delay = settings.VOICE_MESSAGE_DELAY
                channel.message_timeout = settings.VOICE_MESSAGE_TIMEOUT
                channel.configuration = {
                    "JUNEBUG_API_URL": june_url,
                    "JUNEBUG_API_AUTH": june_auth,
                    "JUNEBUG_API_FROM": june_from,
                }
                channel.save()


class Migration(migrations.Migration):

    dependencies = [("message_sender", "0011_channel")]

    operations = [migrations.RunPython(insert_channels)]
