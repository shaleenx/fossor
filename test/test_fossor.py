# Copyright 2017 LinkedIn Corporation. All rights reserved. Licensed under the BSD-2 Clause license.
# See LICENSE in the project root for license information.

import sys
import logging

from fossor.engine import Fossor

import fossor.variables.hostname
import fossor.checks.buddyinfo

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(__name__)


def test_convert_simple_type():
    f = Fossor()
    assert f._convert_simple_type('false') is False
    assert f._convert_simple_type('False') is False
    assert f._convert_simple_type(False) is False

    assert f._convert_simple_type('true') is True
    assert f._convert_simple_type('True') is True
    assert f._convert_simple_type(True) is True

    assert f._convert_simple_type('1.0') == 1.0
    assert type(f._convert_simple_type('1.0')) == float

    assert f._convert_simple_type('1') == 1
    assert type(f._convert_simple_type('1')) == int

    assert f._convert_simple_type('foo') == 'foo'
    assert type(f._convert_simple_type('foo')) == str


def test_variable_plugin_whitelist():
    f = Fossor()
    f.add_variable('timeout', 1)
    assert len(f.variable_plugins) > 2
    whitelist = ['Hostname', 'PidExe']
    f.run(variable_plugin_whitelist=whitelist)
    assert len(f.variable_plugins) == 2


def test_variable_plugin_blacklist():
    f = Fossor()
    f.add_variable('timeout', 1)
    assert fossor.variables.hostname.Hostname in f.variable_plugins
    blacklist = ['Hostname']
    f.run(variable_plugin_blacklist=blacklist)
    assert 'Hostname' not in f.variable_plugins
    assert len(f.variable_plugins) > 0


def test_check_plugin_whitelist():
    f = Fossor()
    f.add_variable('timeout', 1)
    assert len(f.check_plugins) > 2
    whitelist = ['BuddyInfo', 'LoadAvg']
    f.run(check_whitelist=whitelist)
    assert len(f.check_plugins) == 2
    assert fossor.checks.buddyinfo.BuddyInfo in f.check_plugins


def test_check_plugin_blacklist():
    f = Fossor()
    f.add_variable('timeout', 1)
    assert len(f.check_plugins) > 2
    assert fossor.checks.buddyinfo.BuddyInfo in f.check_plugins
    blacklist = ['BuddyInfo', 'LoadAvg']
    f.run(check_blacklist=blacklist)
    assert fossor.checks.buddyinfo.BuddyInfo not in f.check_plugins
    assert len(f.check_plugins) > 1
