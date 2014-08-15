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

All modules are fully documented, please see the module documententation for all available parameters.

Requirements
------------
* Arista EOS 4.12 or later
* EOS Command API enabled
* Linux shell account (see Preparing EOS for Ansible)

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

Role Variables
--------------
The eos role is highly configurable for connecting to the EOS configuration.

_defaults/main.yml_

```
# should not be modified, use for bug reporting
eos_version: 0.1.0

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
eos_use_local_libs: true
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

# configures the username to use with ansible.  this variable is used
# to configure the working environment on the EOS node
eos_username: ansible

# configures the working directory to use with Ansible for temporary
# storage.  it defaults to /tmp and is overridden in vars/eos.yml
eos_working_dir: /tmp
eos_source_dir: /tmp
```

_vars/eos.yml_
```
# overrides the default working directory and configures for working with
# an EOS node
eos_working_dir: "/persist/local/{{ eos_username }}"
eos_source_dir: "{{ working_dir }}/src"

# configures the PIP extension name for use with EOS.  this is required
# for EOS nodes prior to 4.14
eos_python_pip: python-pip-1.4.1.swix
```

Dependencies
------------
* eapilib


Example Playbook
----------------
```
- name: eos nodes
  hosts: veos01
  gather_facts: yes
  sudo: true

  vars:
    eapi_username: eapi
    eapi_password: password
    commands:
      - show version

  roles:
    - role: eos

  tasks:
    - name: run an arbitrary EOS command
      eos_command: eapi_username={{ eapi_username }}
                   eapi_password={{ eapi_password }}
                   eapi_hostname={{ ansible_hostname }}
      args: { commands: "{{ commands }}" }

```

License
-------
BSD-3 (see LICENSE)

Author Information
------------------
Arista EOS+ (eosplus-dev@arista.com)
