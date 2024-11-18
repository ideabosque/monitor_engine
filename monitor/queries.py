#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from monitor_engine.monitor.types import Notification
from monitor_engine.monitor.models import NotificationModel


__author__ = "bl"


def resolve_notifications(info, **kwargs):
    arguments = {
        "hash_key": str(info.context.get("channel")).strip().lower(),
    }

    # Read data from dynamodb
    notifications = [
        Notification(**dict(**notification.__dict__["attribute_values"]))
        for notification in NotificationModel.query(**arguments)
    ]

    return notifications
