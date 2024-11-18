#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from pynamodb.models import Model
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    Table,
    Boolean,
)
from sqlalchemy.orm import backref, relationship
from pynamodb.attributes import (
    UnicodeAttribute,
    NumberAttribute,
)
import os

# from pynamodb.indexes import GlobalSecondaryIndex, LocalSecondaryIndex, AllProjection

__author__ = "bl"

Base = declarative_base()

class AppVersionModel(Base):
    __tablename__ = "app_version"
    id = Column(Integer, primary_key=True, autoincrement=True)
    android_version = Column(String)
    is_version = Column(String)
    android_show = Column(String)
    is_show = Column(String)
    is_content_en = Column(String)
    android_content_en = Column(String)
    is_content_zh = Column(String)
    android_content_zh = Column(String)
    is_url = Column(String)
    android_url = Column(String)

class BaseModel(Model):
    class Meta:
        billing_mode = "PAY_PER_REQUEST"
        region = os.getenv("REGIONNAME")


class NotificationModel(BaseModel):
    class Meta(BaseModel.Meta):
        table_name = "se-notifications"

    apply_to = UnicodeAttribute(hash_key=True)
    type = UnicodeAttribute(range_key=True)
    changed_at = NumberAttribute(default=0)
