README
======
The Arista eos role provides the foundation for working with Arista EOS nodes and Ansible.  The eos role includes the necessary libraries to bootstrap an Arista EOS node and prepare it for use.  In addition, the eos role provides low level functionality for use by all other eos_* roles.

The Arista EOS roles for Ansible provide the ability to manage configuration resources in EOS.  The architecture of the roles makes inherent use of the Arista EOS command API.  This provides a secure two phase authentication that allows for clean separate between automation frameworks and node configuration.  The EOS roles allow an Ansible control host to connect to an Arista EOS node and perform tasks that traverse eAPI with a set of API credentials.

This role provides the following modules available for using in playbooks and tasks:

* eos_vlan
* eos_switchport
* eos_interface
* eos_portchannel
* eos_vxlan
* eos_ipv4interfaces

All modules are fully documented, please see the module documententation for all available parameters.  See the CHANGELOG.md file for the most update to date changes.

Requirements
------------
* Arista EOS 4.12 or later
* EOS Command API enabled (see Enabling EOS Command API)
* Linux shell account (see Preparing EOS for Ansible)

Enabling EOS Command API
------------------------
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
The configuration above enables eAPI with the default settings.  This enables eAPI to listen for connections on HTTPS port 443 by default.  If different values are used, the eapi_protocol and eapi_port variables need to be updated in your playbook.

__Step 3.__ Create a local user
The user created in this step is different than the shell account to be created in the Preparing EOS for Ansible section.  Please see the section Understanding the Security Model for more details.

```
switch(config)# username eapi secret icanttellyou
```

The username (eapi) and password (icanttellyou) can be anything you like.  This user is used to authenticate to eAPI and should be used for the eapi_username and eapi_password variables in your playbooks.


Preparing EOS for Ansible
-------------------------
In order to successfully execute playbook tasks the EOS node must be configured to allow the Ansible control node to directly attach to the Linux shell.  The following steps provide a walk through for setting up password-less access to EOS nodes for use with Ansible

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

Understanding the Security Model
--------------------------------
The Arista EOS role for Ansible provides a two stage authentication model to maximize the security and flexibility available for providing programatic access to EOS nodes.   The steps above walk through how to enable both eAPI and create a shell account for use with Ansible.   This section provides some additional details about how the two stage authentication model works.

_Note:_ The two stage authentication model only applies to tasks that are not using connection: local.  If your playbooks are using local connections, the all of the authentication is based on eAPI.

Implementing a two stage security model allows operators to secure the Ansible shell accout and prevent it from configuring EOS.  Conversely, having a separate eAPI authentication mechanism allows operators to separately control the users that can run EOS modules without giving them root access to EOS.

When Ansible connects to an EOS node, it must first authenticate to Linux as it would for any other Linux platform.  In order to create the shell account, the steps in Preparing EOS for Ansible should be followed.  The steps above will create a user called 'ansible'.  You are free to choose any username you like with the following exception. You cannot create a username the same as a local account in EOS (more on that in a moment).

By default, the EOS role assumes the user account is called 'ansible'.  If the shell account is different, then the eos_username variable must be set in your playbook to the name of the shell account you intend to use.  The ensures that the EOS node is bootstrapped properly for use with Ansible.

The second stage authentication model uses eAPI.  eAPI provides its own authentication mechanism for securing what users can perform which actions in EOS.   The eAPI user can be one that is authenticated by AAA; however, that is outside the scope of this discussion.  The section Enabling EOS Command API provides an example of how to create a local user to use when authenticating with eAPI.

The username and password chosen when configuring the local user must be updated in the playbooks variables setting the values for eapi_username and eapi_password.

_Note:_ The shell account and eAPI user must be different.


Role Variables
--------------
The eos role is highly configurable for connecting to the EOS configuration.

_defaults/main.yml_

```
# sets the default for eAPI connectivity.  More specific values should be
# overwritten in the implmenting playbook
eapi_hostname: localhost
eapi_username: admin
eapi_password:
eapi_protocol: https
eapi_port:

# enables debug output from the eos_* roles
eos_debug: []

# enables purge of resources in eos_* roles
eos_purge: []

# configures the playbook to use the role supplied libraries instead
# of downloading them from PyPi.  Using this eliminates the need to
# allow the EOS switch to access the https://pypi.python.org/pypi
eos_required_libs:
    - eapilib-0.1.0.tar.gz

# configures the save configuration handler to run on every configuration
# change.  if this setting is false, then the running config is never
# saved to non-volatile memory
eos_save_on_change: true

# configures the backup configuration handler to run on every configuration
# change.  with this setting enable, the eos role will download the
# startup-config to the Ansible control host and store it
eos_backup_on_change: true
eos_backup_dir: {{ ansible_hostname }}
```

_vars/eos.yml_
```
# configures the username to use with ansible.  this variable is used
# to configure the working environment on the EOS node
eos_username: ansible

# overrides the default working directory and configures for working with
# an EOS node
eos_working_dir: "/persist/local/{{ eos_username }}"
eos_source_dir: "{{ working_dir }}/src"

# configures the PIP extension name for use with EOS.  this is required
# for EOS nodes prior to 4.14 and should not be changed
eos_python_pip: python-pip-1.4.1.swix
```

Dependencies
------------
* eapilib


Example Playbook
----------------
The example playbook demostrates how to send a list of commands to the EOS node.  Note the commands send using eos_command are *not* idempotent.

```
- name: eos nodes
  hosts: eos_switches
  gather_facts: yes
  sudo: true

  vars:
    eapi_username: eapi
    eapi_password: password
    commands:
      - show version
      - show lldp neighbors

  roles:
    - role: arista.eos

  tasks:
    - name: run an arbitrary EOS command
      eos_command: eapi_username={{ eapi_username }}
                   eapi_password={{ eapi_password }}
      args: { commands: "{{ commands }}" }
      register: eos_command_output

    - debug: var=eos_command_output

```

The next example demonstrates how to use playbooks with a local connection to configure VLANs in EOS.

```
- name: eos nodes
  hosts: eos_switches
  gather_facts: yes
  sudo: true
  connection: local

  roles:
    - role: arista.eos

  tasks:
    - name: create a vlan
      eos_vlan: name=myvlan vlanid=100
                eapi_username=eapi
                eapi_password=itsasecret
                eapi_hostname={{ inventory_hostname }}
```

License
-------
BSD-3 (see LICENSE)

Author Information
------------------
Arista EOS+ (eosplus-dev@arista.com)
