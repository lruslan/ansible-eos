#!/usr/bin/python
#
# Copyright (c) 2015, Arista Networks, Inc.
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
DOCUMENTATION = """
---
module: eos_vrrp
short_description: Manage EOS VRRP resources
description:
  - This module will manage VRRP configurations on EOS nodes
version_added: 1.2.0
category: XXX
author: Arista EOS+
requirements:
  - Arista EOS 4.13.7M or later with command API enabled
  - Python Client for eAPI 0.4.0 or later
notes: XXX
  - All configuration is idempotent unless otherwise specified
  - Supports eos metaparameters for using the eAPI transport
  - Supports stateful resource configuration.
options:
  interface:
    description:
      - The interface on which the VRRP is configured
    required: true
    default: null
    choices: []
    aliases: []
    version_added: 1.2.0
  vrid:
    description:
      - The unique identifying ID of the VRRP on its interface
    required: true
    default: null
    choices: []
    aliases: []
    version_added: 1.2.0
  enable:
    description:
      - The state of the VRRP
    required: false
    default: false
    choices: [True, False]
    aliases: []
    version_added: 1.2.0
  primary_ip:
    description:
      - The ip address of the virtual router
    required: false
    default: '0.0.0.0'
    choices: []
    aliases: []
    version_added: 1.2.0
  priority:
    description:
      - The priority setting for the virtual router
    required: false
    default: 100
    choices: []
    aliases: []
    version_added: 1.2.0
  description:
    description:
      - Text description of the virtual router
    required: false
    default: null
    choices: []
    aliases: []
    version_added: 1.2.0
  secondary_ip:
    description:
      - Array of secondary ip addresses assigned to the VRRP
    required: false
    default: null
    choices: []
    aliases: []
    version_added: 1.2.0
  ip_version:
    description:
      - VRRP version in place on the virtual router
    required: false
    default: 2
    choices: [2, 3]
    aliases: []
    version_added: 1.2.0
  timers_advertise:
    description:
      - Interval between advertisement messages to virtual router group
    required: false
    default: 1
    choices: []
    aliases: []
    version_added: 1.2.0
  mac_addr_adv_interval:
    description:
      - Interval between advertisement messages to virtual router group
    required: false
    default: 30
    choices: []
    aliases: []
    version_added: 1.2.0
  preempt:
    description:
      - Preempt mode setting for the virtual router
    required: false
    default: true
    choices: [true, false]
    aliases: []
    version_added: 1.2.0
  preempt_delay_min:
    description:
      - Interval between a preempt event and takeover
    required: false
    default: 0
    choices: []
    aliases: []
    version_added: 1.2.0
  preempt_delay_reload:
    description:
      - Interval between a preempt event and takeover after reload
    required: false
    default: 0
    choices: []
    aliases: []
    version_added: 1.2.0
  delay_reload:
    description:
      - Delay between switch reload and VRRP initialization
    required: false
    default: 0
    choices: []
    aliases: []
    version_added: 1.2.0
  authentication:
    description:
      - Authentication key for packets received from router group
    required: false
    default: null
    choices: []
    aliases: []
    version_added: 1.2.0
  authentication_type:
    description:
      - Type of authentication key in effect on the virtual router
    required: false
    default: null
    choices: []
    aliases: []
    version_added: 1.2.0
  track:
    description:
      - Name of an interface to track
    required: false
    default: null
    choices: []
    aliases: []
    version_added: 1.2.0
  track_action:
    description:
      - Action to take on state-change of the tracked interface
    required: false
    default: null
    choices: [shutdown, decrement]
    aliases: []
    version_added: 1.2.0
  track_amount:
    description:
      - Amount to decrement priority for 'decrement' track_action
    required: false
    default: null
    choices: []
    aliases: []
    version_added: 1.2.0
  bfd_ip:
    description:
      - BFD ip address for the VRRP
    required: false
    default: null
    choices: []
    aliases: []
    version_added: 1.2.0
"""

EXAMPLES = """

- XXX
- eos_routemap: name=rm1 action=permit seqno=10
                description='this is a great routemap'
                match='as 50,interface Ethernet2'
                set='tag 100,weight 1000'
                continue=20
"""
#<<EOS_COMMON_MODULE_START>>

import syslog
import collections

from ansible.module_utils.basic import *

try:
    import pyeapi
    PYEAPI_AVAILABLE = True
except ImportError:
    PYEAPI_AVAILABLE = False

DEFAULT_SYSLOG_PRIORITY = syslog.LOG_NOTICE
DEFAULT_CONNECTION = 'localhost'
TRANSPORTS = ['socket', 'http', 'https', 'http_local']

class EosAnsibleModule(AnsibleModule):

    meta_args = {
        'config': dict(),
        'username': dict(),
        'password': dict(),
        'host': dict(),
        'connection': dict(default=DEFAULT_CONNECTION),
        'transport': dict(choices=TRANSPORTS),
        'port': dict(),
        'debug': dict(type='bool', default='false'),
        'logging': dict(type='bool', default='true')
    }

    stateful_args = {
        'state': dict(default='present', choices=['present', 'absent']),
    }

    def __init__(self, stateful=True, *args, **kwargs):
        kwargs['argument_spec'].update(self.meta_args)

        self._stateful = stateful
        if stateful:
            kwargs['argument_spec'].update(self.stateful_args)
        super(EosAnsibleModule, self).__init__(*args, **kwargs)

        self.result = dict(changed=False, changes=dict())

        self._debug = kwargs.get('debug') or self.boolean(self.params['debug'])
        self._logging = kwargs.get('logging') or self.params['logging']

        self.log('DEBUG flag is %s' % self._debug)

        self.debug('pyeapi_version', self.check_pyeapi())
        self.debug('stateful', self._stateful)
        self.debug('params', self.params)

        self._attributes = self.map_argument_spec()
        self.validate()

        self._node = self.connect()
        self._instance = None

        self.desired_state = self.params['state'] if self._stateful else None
        self.exit_after_flush = kwargs.get('exit_after_flush')

    @property
    def instance(self):
        if self._instance:
            return self._instance

        func = self.func('instance')
        if not func:
            self.fail('Module does not support "instance"')

        try:
            self._instance = func(self)
        except Exception as exc:
            self.fail('instance[error]: %s' % exc.message)

        self.log("called instance: %s" % self._instance)
        return self._instance

    @property
    def attributes(self):
        return self._attributes

    @property
    def node(self):
        if self._node:
            return self._node
        self._node = self.connect()
        return self._node

    def check_pyeapi(self):
        if not PYEAPI_AVAILABLE:
            self.fail('Unable to import pyeapi, is it installed?')
        return pyeapi.__version__

    def map_argument_spec(self):
        """map_argument_spec maps only the module argument spec to attrs

        This method will map the argumentspec minus the meta_args to attrs
        and return the attrs.  This returns a dict object that includes only
        the original argspec plus the stateful_args (if self._stateful=True)

        Returns:
            dict: Returns a dict object that includes the original
                argument_spec plus stateful_args with values minus meta_args

        """
        keys = set(self.params).difference(self.meta_args)
        attrs = dict()
        attrs = dict([(k, self.params[k]) for k in self.params if k in keys])
        if 'CHECKMODE' in attrs:
            del attrs['CHECKMODE']
        return attrs

    def validate(self):
        for key, value in self.attributes.iteritems():
            func = self.func('validate_%s' % key)
            if func:
                self.attributes[key] = func(value)

    def create(self):
        if not self.check_mode:
            func = self.func('create')
            if not func:
                self.fail('Module must define "create" function')
            return self.invoke(func, self)

    def remove(self):
        if not self.check_mode:
            func = self.func('remove')
            if not func:
                self.fail('Module most define "remove" function')
            return self.invoke(func, self)

    def flush(self, exit_after_flush=False):
        self.exit_after_flush = exit_after_flush

        if self.desired_state == 'present' or not self._stateful:
            if self.instance.get('state') == 'absent':
                changed = self.create()
                self.result['changed'] = changed or True
                self.refresh()

            changeset = self.attributes.viewitems() - self.instance.viewitems()

            if self._debug:
                self.debug('desired_state', self.attributes)
                self.debug('current_state', self.instance)

            changes = self.update(changeset)
            if changes:
                self.result['changes'] = changes
                self.result['changed'] = True

            self._attributes.update(changes)

            flush = self.func('flush')
            if flush:
                self.invoke(flush, self)

        elif self.desired_state == 'absent' and self._stateful:
            if self.instance.get('state') == 'present':
                changed = self.remove()
                self.result['changed'] = changed or True

        elif self._stateful:
            if self.desired_state != self.instance.get('state'):
                changed = self.invoke(self.instance.get('state'))
                self.result['changed'] = changed or True

        self.refresh()
        self.result['instance'] = self.instance

        if self.exit_after_flush:
            self.exit()

    def update(self, changeset):
        changes = dict()
        for key, value in changeset:
            if value is not None:
                changes[key] = value
                func = self.func('set_%s' % key)
                if func and not self.check_mode:
                    try:
                        self.invoke(func, self)
                    except Exception as exc:
                        self.fail(exc.message)
        return changes

    def connect(self):
        if self.params['config']:
            pyeapi.load_config(self.params['config'])

        config = dict()

        if self.params['connection']:
            config = pyeapi.config_for(self.params['connection'])
            if not config:
                msg = 'Connection name "%s" not found' % self.params['connection']
                self.fail(msg)

        if self.params['username']:
            config['username'] = self.params['username']

        if self.params['password']:
            config['password'] = self.params['password']

        if self.params['transport']:
            config['transport'] = self.params['transport']

        if self.params['port']:
            config['port'] = self.params['port']

        if self.params['host']:
            config['host'] = self.params['host']

        if 'transport' not in config:
            self.fail('Connection must define a transport')

        connection = pyeapi.client.make_connection(**config)
        node = pyeapi.client.Node(connection, **config)

        try:
            resp = node.enable('show version')
            self.debug('eos_version', resp[0]['result']['version'])
            self.debug('eos_model', resp[0]['result']['modelName'])
        except (pyeapi.eapilib.ConnectionError, pyeapi.eapilib.CommandError):
            self.fail('unable to connect to %s' % node)
        else:
            self.log('Connected to node %s' % node)
            self.debug('node', str(node))

        return node

    def config(self, commands):
        self.result['changed'] = True
        if not self.check_mode:
            self.node.config(commands)

    def api(self, module):
        return self.node.api(module)

    def func(self, name):
        return globals().get(name)

    def invoke(self, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            self.fail(exc.message)

    def invoke_function(self, name, *args, **kwargs):
        func = self.func(name)
        if func:
            return self.invoke(func, *args, **kwargs)

    def fail(self, msg):
        self.invoke_function('on_fail', self)
        self.log('ERROR: %s' % msg, syslog.LOG_ERR)
        self.fail_json(msg=msg)

    def exit(self):
        self.invoke_function('on_exit', self)
        self.log('Module completed successfully')
        self.exit_json(**self.result)

    def refresh(self):
        self._instance = None

    def debug(self, key, value):
        if self._debug:
            if 'debug' not in self.result:
                self.result['debug'] = dict()
            self.result['debug'][key] = value

    def log(self, message, priority=None):
        if self._logging:
            syslog.openlog('ansible-eos')
            priority = priority or DEFAULT_SYSLOG_PRIORITY
            syslog.syslog(priority, str(message))

    @classmethod
    def add_state(cls, name):
        cls.stateful_args['state']['choices'].append(name)

#<<EOS_COMMON_MODULE_END>>


def instance(module):
    """ Returns an instance of Vrrp based on interface
    """
    interface = module.attributes['interface']
    vrid = module.attributes['vrid']
    _instance = dict(interface=interface, vrid=vrid, state='absent')

    try:
        result = module.node.api('vrrp').get(interface)[vrid]
    except:
        result = None

    if result:
        _instance['state'] = 'present'

        _instance['enable'] = result['enable']
        _instance['primary_ip'] = result['primary_ip']
        _instance['priority'] = str(result['priority'])
        _instance['description'] = result['description']
        _instance['ip_version'] = str(result['ip_version'])
        _instance['timers_advertise'] = str(result['timers_advertise'])
        _instance['preempt'] = result['preempt']
        _instance['preempt_delay_min'] = str(result['preempt_delay_min'])
        _instance['preempt_delay_reload'] = str(result['preempt_delay_reload'])
        _instance['delay_reload'] = str(result['delay_reload'])
        _instance['mac_addr_adv_interval'] = \
            str(result['mac_addr_adv_interval'])



        sec_ips = ','.join(sorted(result['secondary_ip']))
        _instance['secondary_ip'] = ','.join(sorted(result['secondary_ip']))

        tracks = result['track']
        track_list = []
        for track in tracks:
            tr_obj = track['name']
            action = track['action']
            amount = track.get('amount', '__NONE__')
            track_list.append("%s--%s--%s" % (tr_obj, action, amount))

        tracks = ','.join(sorted(track_list))
    return _instance


def create(module):
    interface = module.attributes['interface']
    vrid = module.attributes['vrid']
    module.node.api('vrrp').create(interface, vrid)


def validate_enable(value):
    """Validates the enable argument is True or False.
    """
    if value is None:
        return None
    if value == 'True':
        return True
    if value == 'False':
        return False
    raise ValueError("vrrp argument 'enable' must be True or False")


def set_enable(module):
    """Configures the enable attribute for the vrrp.
    """
    interface = module.attributes['interface']
    vrid = module.attributes['vrid']
    value = module.attributes['enable']
    module.node.api('vrrp').set_enable(interface, vrid, value=value)


def set_primary_ip(module):
    """Configures the primary ip attribute for the vrrp.
    """
    interface = module.attributes['interface']
    vrid = module.attributes['vrid']
    value = module.attributes['primary_ip']
    module.node.api('vrrp').set_primary_ip(interface, vrid, value=value)


def set_priority(module):
    """Configures the priority attribute for the vrrp
    """
    interface = module.attributes['interface']
    vrid = module.attributes['vrid']
    value = module.attributes['priority']
    if not value.isdigit():
        raise ValueError("vrrp argument 'priority' must be an integer")
    module.node.api('vrrp').set_priority(interface, vrid, value=int(value))


def set_description(module):
    """Configures the description attribute for the vrrp
    """
    interface = module.attributes['interface']
    vrid = module.attributes['vrid']
    value = module.attributes['description']
    if value == '':
        # Empty string passed in - disable description on the vrrp
        module.node.api('vrrp').set_description(interface, vrid, disable=True)
    module.node.api('vrrp').set_description(interface, vrid, value=value)


def set_ip_version(module):
    """Configures the ip version attribute for the vrrp
    """
    interface = module.attributes['interface']
    vrid = module.attributes['vrid']
    value = module.attributes['ip_version']
    if not value.isdigit():
        raise ValueError("vrrp argument 'ip_version' must be an integer")
    module.node.api('vrrp').set_ip_version(interface, vrid, value=int(value))


def validate_secondary_ip(value):
    """Converts the secondary ip array argument into a matchable string
    """
    if value is None:
        return None
    split = value.split(',')
    trimmed = []
    for item in split:
        item = item.strip(" []")
        trimmed.append(item)
    joined = ','.join(sorted(trimmed))
    return joined


def set_secondary_ip(module):
    """Configures the secondary ip attribute for the vrrp
    """
    interface = module.attributes['interface']
    vrid = module.attributes['vrid']
    value = module.attributes['secondary_ip']
    if value == '':
        value = []
    else:
        value = value.split(',')
    module.node.api('vrrp').set_secondary_ips(interface, vrid, value)


def set_timers_advertise(module):
    """Configures the timers advertise attribute for the vrrp
    """
    interface = module.attributes['interface']
    vrid = module.attributes['vrid']
    value = module.attributes['timers_advertise']
    if not value.isdigit():
        raise ValueError("vrrp argument 'timers_advertise' must be an integer")
    module.node.api('vrrp').set_timers_advertise(interface, vrid,
                                                 value=int(value))


def validate_preempt(value):
    """Validates the preempt argument is True or False.
    """
    if value is None:
        return None
    if value == 'True':
        return True
    if value == 'False':
        return False
    raise ValueError("vrrp argument 'preempt' must be True or False")


def set_preempt(module):
    """Configures the preempt attribute for the vrrp.
    """
    interface = module.attributes['interface']
    vrid = module.attributes['vrid']
    value = module.attributes['preempt']
    module.node.api('vrrp').set_preempt(interface, vrid, value=value)


def set_preempt_delay_min(module):
    """Configures the preempt delay minimum attribute for the vrrp
    """
    interface = module.attributes['interface']
    vrid = module.attributes['vrid']
    value = module.attributes['preempt_delay_min']
    if not value.isdigit():
        raise ValueError("vrrp argument 'preempt_delay_min' must "
                         "be an integer")
    module.node.api('vrrp').set_preempt_delay_min(interface, vrid,
                                                  value=int(value))


def set_preempt_delay_reload(module):
    """Configures the preempt delay reload attribute for the vrrp
    """
    interface = module.attributes['interface']
    vrid = module.attributes['vrid']
    value = module.attributes['preempt_delay_reload']
    if not value.isdigit():
        raise ValueError("vrrp argument 'preempt_delay_reload' must "
                         "be an integer")
    module.node.api('vrrp').set_preempt_delay_reload(interface, vrid,
                                                     value=int(value))


def set_delay_reload(module):
    """Configures the delay reload attribute for the vrrp
    """
    interface = module.attributes['interface']
    vrid = module.attributes['vrid']
    value = module.attributes['delay_reload']
    if not value.isdigit():
        raise ValueError("vrrp argument 'delay_reload' must "
                         "be an integer")
    module.node.api('vrrp').set_delay_reload(interface, vrid,
                                             value=int(value))


def set_mac_addr_adv_interval(module):
    """Configures the mac-address advertisement-interval attribute for the vrrp
    """
    interface = module.attributes['interface']
    vrid = module.attributes['vrid']
    value = module.attributes['mac_addr_adv_interval']
    if not value.isdigit():
        raise ValueError("vrrp argument 'mac_addr_adv_interval' must "
                         "be an integer")
    module.node.api('vrrp').set_mac_addr_adv_interval(interface, vrid,
                                                      value=int(value))


# XXX
# def validate_track(value):
#     pass


def main():
    """ The main module routine called when the module is run by Ansible
    """

    argument_spec = dict(
        interface=dict(required=True),
        vrid=dict(required=True, type='int'),
        enable=dict(),
        primary_ip=dict(),
        priority=dict(),
        description=dict(),
        # secondary_ip=dict(type='list'),
        secondary_ip=dict(),
        ip_version=dict(),
        timers_advertise=dict(),
        mac_addr_adv_interval=dict(),
        preempt=dict(),
        preempt_delay_min=dict(),
        preempt_delay_reload=dict(),
        delay_reload=dict(),
        authentication_type=dict(),
        # track=dict(type='list'),
        track=dict(),
        bfd_ip=dict(),
    )

    # argument_spec = module.node.api('vrrp').vrrp_format(argument_spec)

    argument_spec['continue'] = dict()

    module = EosAnsibleModule(argument_spec=argument_spec,
                              supports_check_mode=True)

    module.flush(True)

main()
