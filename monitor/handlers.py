#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from time import time
from monitor_engine.monitor.models import NotificationModel, AppVersionModel
from monitor_engine.monitor.utils import asynchronous, convert_object_to_dict

__author__ = "bl"


@asynchronous
def save_notification(notifiction_type, channel):
    try:
        if not notifiction_type or not channel:
            raise Exception("Monitor type and channel are required")

        NotificationModel(
            str(channel).strip().lower(),
            str(notifiction_type).strip().lower(),
            **{"changed_at": int(round(time() * 1000))},
        ).save()

        return True
    except Exception as e:
        raise e


def get_app_version(db_session):
    try:
        return convert_object_to_dict(db_session.query(AppVersionModel).first())
    except Exception as e:
        raise e
