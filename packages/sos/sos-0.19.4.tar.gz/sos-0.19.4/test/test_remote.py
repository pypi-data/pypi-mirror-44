#!/usr/bin/env python3
#
# Copyright (c) Bo Peng and the University of Texas MD Anderson Cancer Center
# Distributed under the terms of the 3-clause BSD License.

import os
import subprocess
import unittest

from sos.hosts import Host
from sos.targets import file_target
from sos.utils import env

has_docker = True
try:
    subprocess.check_output('docker ps | grep test_sos', shell=True).decode()
except subprocess.CalledProcessError:
    subprocess.call('sh build_test_docker.sh', shell=True)
    try:
        subprocess.check_output(
            'docker ps | grep test_sos', shell=True).decode()
    except subprocess.CalledProcessError:
        print('Failed to set up a docker machine with sos')
        has_docker = False

# if sys.platform == 'win32':
#    with open('~/docker.yml', 'r') as d:
#        cfg = d.read()
#    with open('~/docker.yml', 'w') as d:
#        d.write(cfg.replace('/home/', 'c:\\Users\\'))


class TestRemote(unittest.TestCase):
    def setUp(self):
        env.reset()
        # self.resetDir('~/.sos')
        self.temp_files = []
        Host.reset()
        # remove .status file left by failed workflows.
        subprocess.call('sos purge', shell=True)

    def tearDown(self):
        for f in self.temp_files:
            file_target(f).unlink()

    @unittest.skipIf(not has_docker, "Docker container not usable")
    def testRemoteExecute(self):
        if os.path.isfile('result_remote.txt'):
            os.remove('result_remote.txt')
        if os.path.isfile('local.txt'):
            os.remove('local.txt')
        with open('local.txt', 'w') as w:
            w.write('something')
        self.assertEqual(subprocess.call(
            'sos push local.txt -c ~/docker.yml --to docker', shell=True), 0)
        with open('test_remote.sos', 'w') as tr:
            tr.write('''
[10]
input: 'local.txt'
output: 'result_remote.txt'
task:

run:
  cp local.txt result_remote.txt
  echo 'adf' >> 'result_remote.txt'

''')
        self.assertEqual(subprocess.call(
            'sos run test_remote.sos -c ~/docker.yml -r docker -s force', shell=True), 0)
        self.assertFalse(file_target('result_remote.txt').target_exists())
        #self.assertEqual(subprocess.call('sos preview result_remote.txt -c ~/docker.yml -r docker', shell=True), 0)
        #self.assertNotEqual(subprocess.call('sos preview result_remote.txt', shell=True), 0)
        self.assertEqual(subprocess.call(
            'sos pull result_remote.txt -c ~/docker.yml --from docker', shell=True), 0)
        self.assertTrue(file_target('result_remote.txt').target_exists())
        #self.assertEqual(subprocess.call('sos preview result_remote.txt', shell=True), 0)
        with open('result_remote.txt') as w:
            content = w.read()
            self.assertTrue('something' in content, 'Got {}'.format(content))
            self.assertTrue('adf' in content, 'Got {}'.format(content))


if __name__ == '__main__':
    unittest.main()
