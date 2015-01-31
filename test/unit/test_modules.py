#
# Copyright (c) 2014, Arista Networks, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#   Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
#   Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#
#   Neither the name of Arista Networks nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL ARISTA NETWORKS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
import os
import re
import subprocess
import unittest
import json
import pprint

from string import Template

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../lib'))

import yaml

from testlib import random_vlan, random_string
from systestlib import DutSystemTest, get_fixture

FUNC_RE = re.compile(r'(?P<function>[\w_]+)(?=\(\))')

DEFAULT_TEST = 'change'
DEFAULT_BINARY = 'ansible'


class AnsibleModuleSystemTest(DutSystemTest):

    def __init__(self, testname, module, **kwargs):
        self.module = module
        self.longMessage = True
        self.maxDiff = None

        super(AnsibleModuleSystemTest, self).__init__(testname)

    @property
    def command(self):
        return ' '.join(self.module.command)

    @property
    def tag(self):
        return 'cmd=%s' % self.command

    def fail_idempotent_check(self, dut):
        return 'idempotent check failed for %s (%s)' % (dut, self.module.name)

    def run_test(self, dut):
        proc = subprocess.Popen(self.module.command, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        (out, err) = proc.communicate()
        self.assertEqual(err, '', self.tag)
        (result, data) = out.split(' >> ')
        (host, result) = result.split(' | ')
        data = json.loads(data)
        return (host, result, data)

    def module_test(self, dut):
        (host, result, data) = self.run_test(dut)
        self.assertEqual(result.upper(), 'SUCCESS', 'msg=%s' % data.get('msg'))
        for key in ['changed', 'removed', 'created', 'changes', 'instance']:
            self.assertIn(key, data, self.tag)
        return (host, result, data)

    def module_test_create(self):
        for name, dut in self.duts.items():
            if self.module.setup:
                dut.config(self.module.setup)

            self.module.host = name
            self.module.substitution(dict(dut_name=name))

            (host, result, data) = self.module_test(name)

            self.assertTrue(data['created'], self.tag)
            self.assertFalse(data['changed'], self.tag)
            self.assertFalse(data['removed'], self.tag)

            self.idempotent_check(dut)

    def module_test_change(self):
        for name, dut in self.duts.items():
            if self.module.setup:
                dut.config(self.module.setup)

            self.module.host = name
            self.module.substitution(dict(dut_name=name))

            (host, result, data) = self.module_test(name)

            self.assertTrue(data['changed'], self.tag)
            self.assertFalse(data['created'], self.tag)
            self.assertFalse(data['removed'], self.tag)

            self.idempotent_check(dut)

    def module_test_remove(self):
        for name, dut in self.duts.items():
            if self.module.setup:
                dut.config(self.module.setup)

            self.module.host = name
            self.module.substitution(dict(dut_name=name))

            (host, result, data) = self.module_test(name)

            self.assertTrue(data['removed'], self.tag)
            self.assertFalse(data['changed'], self.tag)
            self.assertFalse(data['created'], self.tag)

            self.idempotent_check(dut)

    def idempotent_check(self, dut):
        (host, result, data) = self.module_test(dut)

        for key in ['created', 'changed', 'removed']:
            self.assertFalse(data[key], '%s [%s]' % (data, self.tag))

        self.assertEqual(data['changes'], {}, data)


class AnsibleModuleTestCase(object):

    def __init__(self, **kwargs):
        self.binary = kwargs.get('binary', DEFAULT_BINARY)
        self.name = kwargs.get('name')
        self.module = kwargs.get('module')
        self.path = kwargs.get('path')
        self.hostsfile = kwargs.get('hostsfile')
        self.args = kwargs.get('args')
        self.setup = kwargs.get('setup', list())
        self.host = kwargs.get('host')
        self.local_connection = kwargs.get('local_connection', True)
        self.variables = kwargs.get('variables')

        self.compile()
        self.substitution(self.variables)

    @property
    def command(self):
        return self.build_command()

    def compile(self):
        for key, value in self.variables.items():
            match = FUNC_RE.match(str(value))
            if match:
                func = match.group('function')
                if func not in globals():
                    raise TypeError('invalid function name')
                self.variables[key] = globals().get(func)()

    def substitution(self, values):

        # handle variable substitution for args
        self.args = dict([(key, Template(str(value)).safe_substitute(values))
                          for key, value in self.args.items()])

        # handle variable substituton for setup
        cmds = [Template(str(value)).safe_substitute(values) for value in
                self.setup]
        self.setup = cmds

        # handle variable substitution for name
        self.name = Template(str(self.name)).safe_substitute(values)


    def add_argument(self, value):
        self.args.append(value)

    def build_command(self):
        command = [self.binary]

        # add module name
        command.extend(['-m', self.module])

        # add module path (if necessary)
        if self.path:
            command.extend(['-M', self.path])

        # add host file (if necessary)
        if self.hostsfile:
            command.extend(['-i', self.hostsfile])

        # add module arguments
        if self.args:
            args = ' '
            for key, value in self.args.items():
                if isinstance(value, bool):
                    value = str(value).lower()
                args += '%s=%s ' % (key, value)
            command.extend(['-a', '%s' % args])

        if self.local_connection:
            command.extend(['--connection', 'local'])

        # add host
        command.append(self.host)
        return command




def get_tests(filepath):
    testfiles = [os.path.join(filepath, f) for f in os.listdir(filepath)
                 if f.endswith('yaml')]
    return testfiles


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    tests = get_tests(os.path.join(os.path.dirname(__file__), '../testcases'))

    for test in tests:
        harness = yaml.load(open(test))

        testcases = harness.get('testcases')
        for testcase in testcases:
            kwargs = dict([(k, v) for k, v in harness.items()
                           if k != 'testcases'])

            kwargs.update(dict([(k, v) for k, v in testcase.items()]))

            kwargs['variables'] = harness.get('variables', dict())
            kwargs['variables'].update(testcase.get('variables', dict()))

            module = AnsibleModuleTestCase(**kwargs)
            testname = 'module_test_%s' % testcase.get('test', DEFAULT_TEST)
            suite.addTest(AnsibleModuleSystemTest(testname, module))

    return suite

if __name__ == '__main__':
    unittest.main()


