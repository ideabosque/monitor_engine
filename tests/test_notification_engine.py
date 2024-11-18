#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bl"

import logging, sys, unittest, os
from dotenv import load_dotenv

load_dotenv()

setting = {
    "region_name": os.getenv("REGION_NAME"),
    "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
    "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
}

sys.path.insert(0, "/var/www/projects/monitor_engine")

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()

from monitor_engine import Monitor


class MonitorEngineTest(unittest.TestCase):
    def setUp(self):
        self.monitor = Monitor(logger, **setting)
        logger.info("Initiate MonitorEngineTest ...")

    def tearDown(self):
        logger.info("Destory MonitorEngineTest ...")

    @unittest.skip("demonstrating skipping")
    def test_save_notification(self):
        result = self.monitor.save_notification(
            notifiction_type="seller", channel="ss3"
        )
        logger.info(result)

    @unittest.skip("demonstrating skipping")
    def test_notificatin_engine_graphql(self):
        query = """
            query notifications{
                monitor{
                    applyTo
                    type
                    changedAt
                }
            }
        """

        variables = {
            "evnet_log_id": "test",
        }

        payload = {"query": query, "variables": variables}
        response = self.monitor.monitor_engine_graphql(**payload)
        logger.info(response)

    # @unittest.skip("demonstrating skipping")
    def test_get_event_logs(self):
        query = """
            query eventLogs(
                $pageSize: Int
                $pageNumber: Int
                $subjectType: [String]
                $subjectId: [String]
                $descriptions: [String]
                $duration: [DateTime]
            ) {
                eventLogs(
                    pageSize: $pageSize
                    pageNumber: $pageNumber
                    subjectType: $subjectType
                    subjectId: $subjectId
                    descriptions: $descriptions
                    duration: $duration
                ) {
                    items {
                        logId
                        # subjectType
                        # createdAt
                        # subjectId
                    }
                    pageSize
                    pageNumber
                    total
                }
            }
        """
        # variables = {
        #     "pageSize": 2,
        #     "pageNumber": 2,

        #     # "descriptions": [
        #     #     "A product packaging toggled status.",
        #     #     "New product price list created.",
        #     # ],
        #     # # "subjectType": "user",
        #     # "subjectId": "5811",
        #     # "duration": ["2021-08-01T00:00:00Z", "2021-08-29T23:59:59Z"],
        # }
        variables = {
            "pageSize": 10,
            "pageNumber": 91,
            # "subjectType": ["user"],
            # "subjectId": [5811],
            # "descriptions": [
            #     "User updated.",
            #     "A product packaging toggled status.",
            # ],
            # "duration": ["2021-08-01T00:00:00Z", "2021-08-30T23:59:59Z"],
        }

        payload = {"query": query, "variables": variables}
        response = self.monitor.monitor_engine_graphql(**payload)
        logger.info(response)

    @unittest.skip("demonstrating skipping")
    def test_get_event_logs_by_backend(self):
        payload = {
            "operation_type": 1,
            "start_at": "2021-09-15T05:03:58Z",
            "end_at": "2021-09-16T05:03:58Z",
            "limit": 1000,
            "last_evaluated_key": None,
        }
        response = self.monitor.get_event_logs("product", **payload)
        logger.info(response)


if __name__ == "__main__":
    unittest.main()
