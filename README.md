# Ansible EOS Role

#### Table of Contents

1. [Overview](#overview)
    * [Requirements](#requirements)
2. [Setup](#setup)
    * [Enabling EOS Command API](#enablingeoscommandapi)
    * [Preparing EOS for Ansible](#preparingeosforansible)
3. [Examples](#examples)
4. [Development](#development)
5. [License](#license)

## Overview

The Arista EOS role provides the foundation for working with Arista EOS nodes and Ansible.  The Arista EOS role for Ansible provides the ability to manage configuration resources in EOS.  The architecture of the roles makes inherent use of the Arista EOS command API using either a traditional Ansible SSH connection or by specifying connection: local and using eAPI to send and receive commands.  

The Ansible EOS role is freely provided to the open source community for automating Arista EOS node configurations using Ansible.  Support for the modules is provided on a best effort basis by the Arista EOS+ community.  Please file any bugs, questions or enhancement requests using [Github Issues](http://github.com/arista-eosplus/ansible-eos/issues)

### Requirements

* Arista EOS 4.13.7M or later
* EOS Command API enabled (see Enabling EOS Command API)
* [Python Client for eAPI 0.1.1 or later] [pyeapi]
* Linux shell account (optional) (see Preparing EOS for Ansible)

## Setup

The instruction below provider a walk through for preparing an Arista EOS node
to be managinged by Ansible.  

### Enabling EOS Command API

The modules provided in the Arista EOS role require command API (aka eAPI) to be enabled on the switch.   The modules use eAPI to communicate with EOS.  Since eAPI is not enabled by default, it must be initially enabled before the EOS modules can be used.

The steps below provide the basic steps to enable eAPI.  For more advanced configurations, please consult the EOS User Guide.

__Step 1.__ Login to the destination node and enter configuration mode

```
switch> enable
switch# configure
switch(config)#
```

__Step 2.__ Enable eAPI

```
switch(config)# management api http-commands
switch(config-mgmt-api-http-cmds)# no shutdown
```

The configuration above enables eAPI with the default settings.  This enables eAPI to listen for connections on HTTPS port 443 by default.  

__Step 3.__ Create user account for eAPI

The user account is used to authenticate the API calls.  See the [Python Client
for eAPI] [pyeapi] for more details.

```
switch(config)# username eapi secret icanttellyou
```

### Preparing EOS for Ansible

In order to successfully execute playbook tasks using a SSH conneciton, the EOS node must be configured to allow the Ansible control node to directly attach to the Linux shell.  The following steps provide a walk through for setting up password-less access to EOS nodes for use with Ansible

_Note: These steps will create a user that has root priviledges to your EOS node so please handle credentials accordingly_

__Step 1.__ Login to the destination node and enter the Linux shell

```
veos> enable
veos# bash

Arista Networks EOS shell

```

__Step 2.__ Create the user to use with Ansible, create the home directory and prepare for uploading your SSH key.  In the below example we will create a user called ansible.  The second command will create a temporary password for the user but we will be switching to using SSH keys and the password will be removed.

```
# create the user 'ansible' with temporary password 'password'
[admin@veos ~]$ sudo useradd -d /persist/local/ansible -G eosadmin ansible
[admin@veos ~]$ echo password | sudo passwd --stdin ansible
Changing password for user ansible.
passwd: all authentication tokens updated successfully.

# prepare the home directory so we can upload an ssh key
[admin@veos ~]$ sudo mkdir /persist/local/ansible/.ssh
[admin@veos ~]$ sudo chmod 700 /persist/local/ansible/.ssh
[admin@veos ~]$ sudo chown ansible:eosadmin /persist/local/ansible/.ssh
[admin@veos ~]$ sudo ls -lah /persist/local/ansible

# exit the Linux shell and disconnect
[admin@veos01 ~]$ logout
veos#logout
Connection to veos01 closed.

```

__Step 3.__ Upload the SSH key to use from your Ansible control host and verify access from remote host

```
ansible@hub:~$ scp ./.ssh/id_rsa.pub ansible@veos01:.ssh/authorized_keys
Password:

ansible@hub:~$ ssh ansible@veos01

Arista Networks EOS shell

[ansible@veos ~]$
```

__Step 4.__ Configure EOS to create user on reboot with no password assigned.  This will only allow the Ansible user to login with keys.

```
[ansible@veos ~]$ vi /mnt/flash/rc.eos

#!/bin/sh
useradd -d /persist/local/ansible -G eosadmin ansible

```

__Step 5.__ Reboot the EOS node and start automating with Ansible

```
[ansible@veos ~]$ sudo reboot
```

## Examples

The example playbook demostrates how to send a list of commands to the EOS node.  Note the commands send using eos_command are *not* idempotent.

```
- name: eos nodes
  hosts: eos_switches
  gather_facts: no

  vars:
    eos_vlans:
      - vlanid: 1
        name: default
      - vlanid: 103
        name: TEST_VLAN_103
      - vlanid: 104
        name: TEST_VLAN_104
      - vlanid: 105
        name: TEST_VLAN_105

    eos_interfaces:
      - name: Ethernet1
        description: connection to leaf veos03
        enable: true
      - name: Ethernet2
        description: connection to leaf veos04
        enable: true
      - name: Loopback0
        description: managed by Ansible
        enable: true

    eos_ipinterfaces:
      - name: Loopback0
        address: 1.1.1.1/32
      - name: Ethernet1
        address: 172.16.11.1/24

  roles:
    - role: arista.eos

  tasks:
    - name: Configure EOS VLAN resources
      eos_vlan: vlanid={{ item.vlanid }}
                name={{ item.name }}
                enable={{ item.enable|default('true') }}
                connection={{ inventory_hostname }}
      with_items: eos_vlans
      when: eos_vlans is defined
      register: eos_vlan_output

    - name: Configure EOS physical interfaces
      eos_interface: name={{ item.name }}
                     description="{{ item.description|default('managed by Ansible') }}"
                     enable={{ item.enable|default('false') }}
                     connection={{ inventory_hostname }}
      with_items: eos_interfaces
      when: eos_interfaces is defined
      register: eos_interface_output

    - name: Configure EOS IPv4 interfaces
      eos_ipinterface: name={{ item.name }}
                         address={{ item.address }}
                         connection={{ inventory_hostname }}
      with_items: eos_ipinterfaces
      when: eos_ipinterfaces is defined
      register: eos_ipinterfaces_output

```

## License

Copyright (c) 2015, Arista Networks, Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

  Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.

  Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution.

  Neither the name of Arista Networks nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL ARISTA NETWORKS
BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

[pyeapi]: https://github.com/arista-eosplus/pyeapi

