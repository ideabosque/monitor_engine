#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from graphene import ObjectType, List
from monitor_engine.monitor.types import Notification
from monitor_engine.monitor.queries import (
    resolve_notifications,
)

__author__ = "bl"


def type_class():
    return [Notification]


# Query resource or role list
class Query(ObjectType):
    notifications = List(Notification)

    def resolve_notifications(self, info, **kwargs):
        return resolve_notifications(info, **kwargs)
