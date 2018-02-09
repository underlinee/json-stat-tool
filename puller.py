#!/usr/bin/python

import os
import subprocess
import re


class LogPuller:

    def __init__(self, paths_file):
        with open(paths_file) as f:
            self.remote_file_formats = [line.strip() for line in f.readlines() if line.strip()]

            filename = self.remote_file_formats[0].split("/")[-1].strip()
            last_dot_index = filename.rfind('.')
            self.local_file_format = filename[:last_dot_index] + '.{}.' + filename[last_dot_index + 1:]

            p = re.compile('%[%Ymd_\-]+')
            self.date_format = p.findall(self.local_file_format)[0]

    def pull(self, date):
        curdir = os.path.dirname(os.path.abspath(__file__))
        files = []
        processes = []

        for idx, remote in enumerate(self.remote_file_formats):
            local_file = curdir + "/" + self._local_file_name(date, idx + 1)
            remote_file = self._remote_file_path(remote, date)

            files.append(local_file)

            if not os.path.isfile(local_file):
                scp_cmd = "scp -o StrictHostKeyChecking=no " + remote_file + " " + local_file
                p = subprocess.Popen(scp_cmd, shell=True)
                processes.append(p)

        [p.wait() for p in processes]
        return files

    def _local_file_name(self, date, idx):
        return self.local_file_format.replace(self.date_format, date.strftime(self.date_format)).format(idx)

    def _remote_file_path(self, remote, date):
        return remote.replace(self.date_format, date.strftime(self.date_format))
