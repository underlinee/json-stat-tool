from unittest import TestCase

import puller
import datetime
import os.path


class TestLogPuller(TestCase):

    def test_init(self):
        log_puller = puller.LogPuller("remote_file_paths")
        assert log_puller.date_format == "%Y_%m_%d"
        assert len(log_puller.remote_file_formats) == 10
        assert log_puller.local_file_format == "%Y_%m_%d.application.log.{}.gz"

    def test_local_file_name(self):
        log_puller = puller.LogPuller("remote_file_paths")
        assert log_puller._local_file_name(datetime.datetime(2018, 2, 9), 1) == "2018_02_09.application.log.1.gz"

    def test_remote_file_name(self):
        remote = "username@sample-server6.com:/service/logs/%Y_%m_%d.application.log.gz"
        log_puller = puller.LogPuller("remote_file_paths")
        assert log_puller._remote_file_path(remote, datetime.datetime(2018, 2,
                                                                      9)) == "username@sample-server6.com:/service/logs/2018_02_09.application.log.gz"

    def test_pull(self):
        log_puller = puller.LogPuller("remote_file_paths")
        files = log_puller.pull(datetime.datetime(2018, 1, 1))
        for file in files:
            assert os.path.isfile(file) == True
