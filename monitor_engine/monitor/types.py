#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from graphene import ObjectType, String

__author__ = "bl"


class Notification(ObjectType):
    apply_to = String()
    type = String()
    changed_at = String()
