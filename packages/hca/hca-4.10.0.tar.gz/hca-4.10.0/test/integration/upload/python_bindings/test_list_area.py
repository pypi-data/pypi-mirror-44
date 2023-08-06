#!/usr/bin/env python
# coding: utf-8

import os
import sys
import unittest

import responses

pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))  # noqa
sys.path.insert(0, pkg_root)  # noqa

from hca import upload
from test.integration.upload import UploadTestCase


class TestUploadListArea(UploadTestCase):

    def setUp(self):
        super(self.__class__, self).setUp()
        self.area = self.mock_current_upload_area()
        self.upload_bucket.Object('/'.join([self.area.uuid, 'bogofile'])).put(Body="foo")

    @responses.activate
    def test_list_current_area(self):
        self.simulate_credentials_api(area_uuid=self.area.uuid)

        file_list = list(upload.list_current_area())

        self.assertEqual(file_list, [{'name': 'bogofile'}])

    @responses.activate
    def test_list_current_area_with_detail(self):
        self.simulate_credentials_api(area_uuid=self.area.uuid)

        list_url = 'https://upload.{stage}.data.humancellatlas.org/v1/area/{uuid}/files_info'.format(
            stage=self.deployment_stage,
            uuid=self.area.uuid)
        responses.add(responses.PUT, list_url, json=[{"name": "bogofile", "size": 1234}], status=200)

        file_list = list(upload.list_current_area(detail=True))

        self.assertEqual(file_list, [{'name': 'bogofile', 'size': 1234}])


if __name__ == "__main__":
    unittest.main()
