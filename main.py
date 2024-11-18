#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from graphene import Schema
from silvaengine_utility import Utility
from monitor_engine.monitor.schema import Query, type_class
from monitor_engine.monitor.enumerations import ClientType
from monitor_engine.monitor.handlers import save_notification, get_app_version
from monitor_engine.monitor.models import Base
import jsonpickle


__author__ = "bl"


# Hook function applied to deployment
def deploy() -> list:
    return [
        {
            "service": "monitor",
            "class": "Monitor",
            "functions": {
                "monitor_engine_graphql": {
                    "is_static": False,
                    "label": "Monitor Engine",
                    "query": [
                        {
                            "action": "notifications",
                            "label": "View Monitors",
                        },
                    ],
                    "type": "RequestResponse",
                    "support_methods": ["POST"],
                    "is_auth_required": False,
                    "is_graphql": True,
                    "settings": "beta_core_ss3",
                    "disabled_in_resources": True,
                },
                "app_version": {
                    "is_static": False,
                    "label": "Get APP Version",
                    "type": "RequestResponse",
                    "support_methods": ["POST"],
                    "is_auth_required": False,
                    "is_graphql": False,
                    "settings": "beta_core_ss3",
                    "disabled_in_resources": True,
                    "query": [],
                    "mutation": [],
                },
            },
        }
    ]


class Monitor(object):
    def __init__(self, logger, **setting):
        self.logger = logger
        self.setting = setting
        self.db_session = Utility.create_database_session(setting)
        Base.query = self.db_session.query_property()

    # Add new log
    def save_notification(
        self,
        notifiction_type,
        channel,
    ):
        try:
            return save_notification(notifiction_type=notifiction_type, channel=channel)
        except Exception as e:
            raise e

    # Event log recorder entry.
    def monitor_engine_graphql(self, **params):
        try:
            channel = params.get("endpoint_id", ClientType.SS3.value)

            if not channel:
                raise Exception("Unrecognized request origin", 401)

            schema = Schema(
                query=Query,
                types=type_class(),
            )
            context = {
                "logger": self.logger,
                "channel": str(channel).strip(),
            }
            variables = params.get("variables", {})
            operations = params.get("query")
            response = {
                "errors": "Invalid operations.",
                "status_code": 400,
            }

            if not operations:
                return jsonpickle.encode(response, unpicklable=False)

            execution_result = schema.execute(
                operations, context_value=context, variable_values=variables
            )

            if not execution_result:
                response = {
                    "errors": "Invalid execution result.",
                }
            elif execution_result.errors:
                response = {
                    "errors": [
                        Utility.format_error(e) for e in execution_result.errors
                    ],
                }
            elif execution_result.invalid:
                response = execution_result
            elif execution_result.data:
                response = {"data": execution_result.data, "status_code": 200}
            else:
                response = {
                    "errors": "Uncaught execution error.",
                }

            return jsonpickle.encode(response, unpicklable=False)
        except Exception as e:
            raise e

    def app_version(self, **params):
        return jsonpickle.encode(get_app_version(self.db_session), unpicklable=False)
