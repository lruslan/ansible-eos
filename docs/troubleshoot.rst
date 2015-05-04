############
Troubleshoot
############

************
Introduction
************

The Ansible EOS role is developed by Arista EOS+ CS and supported by the Arista
EOS+ community.   Support for the modules as well as using Ansible with Arista
EOS nodes is provided on a best effort basis by the Arista EOS+ CS team and the
community.  

For customers that are looking for a premium level of support, please contact
your local account team or email eosplus@arista.com for help.

*****************
Submitting Issues
*****************

The Arista EOS+ CS development team uses Github Issues to track discovered
bugs and enhancement request to the Ansible EOS role.  The issues tracker can
be found at https://github.com/arista-eosplus/ansible-eos/issues.

For defect issues, please provide as much relevant data as possible as to what
is causing the issue, if and how it is reproducable, the version of EOS and
Ansible running.

For enhancement requests, please provide a brief description of the
enhancement request and the version of EOS to be supported.

The issue tracker is monitored by Arista EOS+ CS and issues submitted are
categorized and scheduled for inclusion in upcoming Ansible EOS role versions.

***********************
Debugging Module Output
***********************

All Ansible EOS role modules provide a consistent output and options for
troubleshooting the module operations.  Each module provides logging and debug
information tho help debugging the change the module is introducing.  Modules
provide two arguments for debugging: logging (default=on) and debug
(default=off).

When a module executes, the module output can be registered as a variable and
then used to display the output.  Below is an example task that configures a
logical Vxlan interface::

    - name: Configure Vxlan logical interface
      eos_vxlan: name={{ vxlan.name }}
             description={{ vxlan.description|default(omit) }}
             source_interface={{ vxlan.source_interface }}
             multicast_group={{ vxlan.multicast_group }}
             debug=no
             connection={{ inventory_hostname }}
      when: vxlan is defined
      register: eos_vxlan_output

Once the variable is registered, for instance eos_vxlan_output in the above
example, the Ansible `debug`_ module can be used to display the output.::

    - debug: var=eos_vxlan_output

When the debug module is added to the playbook, the eos_vxlan module will
display the followig output::

    TASK: [debug var=eos_vxlan_output] ********************************************
    ok: [veos02] => {
        "var": {
            "eos_vxlan_output": {
                "changed": false,
                "changes": {},
                "instance": {
                    "description": null,
                    "enable": true,
                    "multicast_group": "239.10.10.10",
                    "name": "Vxlan1",
                    "source_interface": "Loopback0",
                    "state": "present",
                    "udp_port": 4789
                },
                "invocation": {
                    "module_args": "name=Vxlan1 source_interface=Loopback0 multicast_group=239.10.10.10 debug=no connection=veos02",
                    "module_name": "eos_vxlan"
                }
            }
        }
    }

In the module output are the standard responses from Ansible task runs
including invocation and changed.  Invocation shows the name of the module that
was executed and the arguments passed to to module which should match the task
in the playbook.

The changed key displays true if any changes are made to the system or false if
no changes are required on the end system. 

The Ansible EOS role addes the keys for changes and instance.  The instance key
provides a view of the resource at the conclusion of the task execution.  When
compared to the nodes running-configuration, the instance should be displaying
configuration valus that are consistent with the nodes current configuration.

The changes key provides the set of key / value pairs that are changed during a
module execution.  Since the changed key has a value of false, no changes where
made in this instance.  The example below shows the output when changes are
made to the configuration.::

    TASK: [debug var=eos_vxlan_output] ********************************************
    ok: [veos02] => {
        "var": {
            "eos_vxlan_output": {
                "changed": true,
                "changes": {
                    "multicast_group": "239.10.10.10",
                    "source_interface": "Loopback0"
                },
                "instance": {
                    "description": null,
                    "enable": true,
                    "multicast_group": "239.10.10.10",
                    "name": "Vxlan1",
                    "source_interface": "Loopback0",
                    "state": "present",
                    "udp_port": 4789
                },
                "invocation": {
                    "module_args": "name=Vxlan1 source_interface=Loopback0 multicast_group=239.10.10.10 debug=no connection=veos02",
                    "module_name": "eos_vxlan"
                }
            }
        }
    }

The above example show the output from the same module; however, this time
changes are introducted as indicated by the changed key being set to true.  In
addition, the changes key shows which arguments where changed and the value the
keys were set to.  For all other arguments that are not included in the changes
key, no configuration updates were executed.

Thus far, the examples have shown the ouput for eos_* modules that is avaible
for every run without any changes.  All modules also provide a `debug` argument
that, when enabled, provides additional information about the execution of the
module.

Below is an example of the same module execution, only this time with debug
enabled::

    TASK: [debug var=eos_vxlan_output] ********************************************
    ok: [veos02] => {
        "var": {
            "eos_vxlan_output": {
                "changed": true,
                "changes": {
                    "multicast_group": "239.10.10.10",
                    "source_interface": "Loopback0"
                },
                "debug": {
                    "current_state": {
                        "description": null,
                        "enable": true,
                        "multicast_group": "",
                        "name": "Vxlan1",
                        "source_interface": "",
                        "state": "present",
                        "udp_port": 4789
                    },
                    "desired_state": {
                        "description": null,
                        "enable": true,
                        "multicast_group": "239.10.10.10",
                        "name": "Vxlan1",
                        "source_interface": "Loopback0",
                        "state": "present",
                        "udp_port": null
                    },
                    "node": "Node(connection=EapiConnection(transport=https://192.168.1.17:443//command-api))",
                    "params": {
                        "config": null,
                        "connection": "veos02",
                        "debug": true,
                        "description": null,
                        "enable": true,
                        "logging": true,
                        "multicast_group": "239.10.10.10",
                        "name": "Vxlan1",
                        "password": null,
                        "source_interface": "Loopback0",
                        "state": "present",
                        "udp_port": null,
                        "username": null
                    },
                    "pyeapi_version": "0.2.2",
                    "stateful": true
                },
                "instance": {
                    "description": null,
                    "enable": true,
                    "multicast_group": "239.10.10.10",
                    "name": "Vxlan1",
                    "source_interface": "Loopback0",
                    "state": "present",
                    "udp_port": 4789
                },
                "invocation": {
                    "module_args": "name=Vxlan1 source_interface=Loopback0 multicast_group=239.10.10.10 debug=yes connection=veos02",
                    "module_name": "eos_vxlan"
                }
            }
        }
    }

With the `debug` key set to `yes` the the module output provides an additional
keyword `debug` that provides additional information.  While the keys under
`debug` could vary from module to module, the following keys are in common
across all module implementations

    * current_state - shows the resource instance values at the beginning of
      the task run before any changes are attempted
    * desired_state - shows the desired state of the resource based on the
      input arguments from the task
    * node - shows the eAPI connection information 
    * params - shows all parameters used to build the module including
      arguments and metaparameters
    * pyeapi_version - shows the current version of pyeapi library used 
    * statful - shows whether or not the module is stateful

Using the `debug` argument provides a fair amount of detail about how the
module executes on the node. There is also logging information that also
provides some details about the changes the module is making to the end system.
Logging is enabled by default and can be disabled by configurating the
`logging` keyword argument to `false`.  

All logging information is sent to the local syslog on the device executing the
module.  When using the SSH transport, all logging information will be found in
the node's syslog and in the case of using the eAPI transport, the logging
information wil be found on the Ansible control hosts syslog.

From the same example as above, the `eos_vxlan` module provides logging
information in syslog as shown below::

    Apr 16 00:36:34 veos02 ansible-eos_vxlan: Invoked with username=None enable=True logging=True name=Vxlan1 connection=veos02 udp_port=None multicast_group=239.10.10.10 state=present source_interface=Loopback0 debug=True password=NOT_LOGGING_PASSWORD config=None description=None
    Apr 16 00:36:34 veos02 ansible-eos: DEBUG flag is True
    Apr 16 00:36:34 veos02 ansible-eos: Connected to node Node(connection=EapiConnection(transport=https://127.0.0.1:443//command-api))
    Apr 16 00:36:34 veos02 ansible-eos: called instance: {'multicast_group': '', 'state': 'present', 'enable': True, 'description': '', 'source_interface': '', 'udp_port': 4789, 'name': 'Vxlan1'}
    Apr 16 00:36:34 veos02 ansible-eos: Invoked set_source_interface for eos_vxlan[Vxlan1] with value Loopback0
    Apr 16 00:36:34 veos02 ansible-eos: Invoked set_multicast_group for eos_vxlan[Vxlan1] with value 239.10.10.10
    Apr 16 00:36:35 veos02 ansible-eos: called instance: {'multicast_group': '239.10.10.10', 'state': 'present', 'enable': True, 'description': '', 'source_interface': 'Loopback0', 'udp_port': 4789, 'name': 'Vxlan1'}
    Apr 16 00:36:35 veos02 ansible-eos: Module completed successfully

The log output diplays the invocation of the module by Ansible and includes
information about the execution process.  

Using both the `debug` and `logging` keywords provides a window into the
execution of the Ansible EOS role and should make troubleshooting undesired
results easier.


*********************************
Debugging EOS Connectivity Issues
*********************************

Sometimes it is difficult to quickly deduce what is causing a particular
playbook or task not to run without error.  While Ansible provids some verbose
details during the task execution, sometimes the problem relates to connecting
from the Ansible control host to the EOS node.  

This section provides some basic tips on troubleshooting connectvity issues
with Arista EOS nodes.

When starting to troubleshoot connectivity errors, the first place to start
is with some simple `ping` tests to ensure there is reachabilty between the
Ansible control host and the EOS node::

    $ ping -c 5 192.168.1.16
    PING 192.168.1.16 (192.168.1.16): 56 data bytes
    64 bytes from 192.168.1.16: icmp_seq=0 ttl=64 time=1.202 ms
    64 bytes from 192.168.1.16: icmp_seq=1 ttl=64 time=1.082 ms
    64 bytes from 192.168.1.16: icmp_seq=2 ttl=64 time=0.829 ms
    64 bytes from 192.168.1.16: icmp_seq=3 ttl=64 time=0.936 ms
    64 bytes from 192.168.1.16: icmp_seq=4 ttl=64 time=1.021 ms

    --- 192.168.1.16 ping statistics ---
    5 packets transmitted, 5 packets received, 0.0% packet loss
    round-trip min/avg/max/stddev = 0.829/1.014/1.202/0.127 ms

The output above validates that the EOS node is reachable from the Ansible
control host.  

If the configured playbook or task is not using `connection: local`, then we
can use SSH to validate that the SSH keyless login is working properly::

    $ ssh ansible@192.168.1.16
    Last login: Sun May  3 17:49:07 2015 from 192.168.1.130

    Arista Networks EOS shell

    [ansible@Arista ~]$

If the user (ansible in the above example) is unable to login to the node,
please review the quickstart guide.

Lastly, check to make sure the dependency eAPI has been enabled on the target
Arista EOS node.  To verify that eAPI is enabled and running, use the `show
management apt http-commands` command in EOS::

    Arista#show management api http-commands
    Enabled:        Yes
    HTTPS server:   shutdown, set to use port 443
    HTTP server:    running, set to use port 80
    VRF:            default
    Hits:           4358
    Last hit:       59729 seconds ago
    Bytes in:       680505
    Bytes out:      64473935
    Requests:       4278
    Commands:       10918
    Duration:       833.907 seconds
    User       Hits       Bytes in       Bytes out    Last hit
    ---------- ---------- -------------- --------------- -----------------
    eapi       4278       680505         64473935     59729 seconds ago

    URLs
    ------------------------------------
    Management1 : http://192.168.1.16:80

In the example command output above, check to be sure that `Enabled:` is `Yes`
and either `HTTP server:` or `HTTPS server` is in a running state.


.. _debug: http://docs.ansible.com/debug_module.html 
