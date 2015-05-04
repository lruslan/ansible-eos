###########
Quick Start
###########

.. contents::
  :depth: 3

************
Introduction
************
This quick-start guide provides the fastest method to get up and running with
the Ansible EOS role.  It assumes that you already have an Ansible
environment running. If not, see :ref:`install-ansible-label` before following
this guide.


***************
Getting Started
***************
Before jumping in head first, it's important to understand how
:ref:`ansible-eos-role-label` is deployed. At the preceding link,
you'll see two deployment options which correlate to two separate quick start
paths below. Have a quick read of :ref:`ansible-eos-role-label` and then come
follow your preferred path.


*****************************************
Option A: Connect to Arista Node over SSH
*****************************************

**Tasklist**

1. :ref:`A-enable-eapi-label`
2. :ref:`A-eos-user-label`
3. :ref:`A-install-pyeapi-label`
4. :ref:`A-run-adhoc-label`



.. _A-enable-eapi-label:

Enabling EOS Command API
========================
The modules provided in the Arista EOS role require command API (aka eAPI)
to be enabled on the switch. The modules use eAPI to communicate with EOS.
Since eAPI is not enabled by default, it must be initially enabled before the
EOS modules can be used.

.. Note:: The EOS role provides a module for enabling and configuring command
          API using a task; however, the local user still needs to be created


The steps below provide the basic steps to enable eAPI.  For more advanced
configurations, please consult the EOS User Guide.

**Step 1.** Login to the destination node and enter configuration mode

.. code-block:: console

  switch> enable
  switch# configure
  switch(config)#


**Step 2.** Enable eAPI

.. code-block:: console

  switch(config)# management api http-commands
  switch(config-mgmt-api-http-cmds)# no shutdown


The configuration above enables eAPI with the default settings.  This enables
eAPI to listen for connections on HTTPS port 443 by default.  If different
values are used, the eapi_protocol and eapi_port variables need to be updated
in your playbook.

**Step 3.** Create a local user
The user created in this step is different than the shell account to be
created in the Preparing EOS for Ansible section.  TODO Please see the section
Understanding the Security Model for more details.

.. code-block:: console

  switch(config)# username eapi secret icanttellyou


The username (eapi) and password (icanttellyou) can be anything you like.
This user is used to authenticate to eAPI and should be used for the
eapi_username and eapi_password variables in your playbooks.


.. _A-eos-user-label:

Preparing EOS for Ansible
=========================
In order to successfully execute playbook tasks the EOS node must be
configured to allow the Ansible control node to directly attach to the
Linux shell.  The following steps provide a walk through for setting up
password-less access to EOS nodes for use with Ansible.

.. Note:: These steps will create a user that has root privileges to your EOS
          node, so please handle credentials accordingly

**Step 1.** Login to the destination node and enter the Linux shell

.. code-block:: console

  veos> enable
  veos# bash

  Arista Networks EOS shell


**Step 2.** Create the user to use with Ansible, create the home directory
and prepare for uploading your SSH key. In the below example we will create
a user called ansible. The second command will create a temporary password
for the user but we will be switching to using SSH keys and the password
will be removed

.. code-block:: console

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


**Step 3.** Upload the SSH key to use from your Ansible control host and
verify access from remote host

.. code-block:: console

  ansible@hub:~$ scp ~/.ssh/id_rsa.pub ansible@veos01:.ssh/authorized_keys
  Password:

  ansible@hub:~$ ssh ansible@veos01

  Arista Networks EOS shell

  [ansible@veos ~]$


**Step 4.** Configure EOS to create user on reboot with no password assigned.
This will only allow the Ansible user to login with keys.

.. code-block:: console

  [ansible@veos ~]$ vi /mnt/flash/rc.eos

  #!/bin/sh
  useradd -d /persist/local/ansible -G eosadmin ansible


**Step 5.** Reboot the EOS node and start automating with Ansible

.. code-block:: console

  [ansible@veos ~]$ sudo reboot



.. _A-install-pyeapi-label:

Install pyeapi
==============
As mentioned earlier, the Ansible EOS role uses `pyeapi <https://github.com/arista-eosplus/pyeapi>`_
on the Arista node that will be configured. Let's install it.

If the Arista node has internet access:

.. code-block:: console

  [ansible@veos ~]$ sudo pip install pyeapi

If there's no internet access:

**Step 1:** Download Pypi Package

`Download <https://pypi.python.org/pypi/pyeapi>`_ the latest version of pyeapi on your local machine.

**Step 2:** SCP the file to the Arista node and install

.. code-block:: console

  ansible@hub:~$ scp path/to/pyeapi-<VERSION>.tar.gz ansible@veos01:/tmp

Then SSH into your node and install it:

.. code-block:: console

  [ansible@veos ~]$ sudo pip install /tmp/pyeapi-<VERSION>.tar.gz

**Step 3:** Create local pyeapi.conf file

.. code-block:: console

  [ansible@veos ~]$ vi /mnt/flash/eapi.conf

with credentials you created earlier:

.. code-block:: console

  [connection:localhost]
  transport: https
  username: eapi
  password: icanttellyou
  port: <port-if-non-default>


.. _A-run-adhoc-label:

Running Adhoc Commands
======================
If you are new to Ansible then it's easier to dip your toes in using
`Adhoc <http://docs.ansible.com/intro_adhoc.html>`_ commands versus writing a
full `Playbook <http://docs.ansible.com/playbooks.html>`_. The section below
will help guide you through running some Adhoc commands to configure basic
settings on your node.


**Step 1.** Create an Ansible Inventory File

Let's add the details of our test node to an Ansible Inventory file.

.. hint:: Learn more about `Ansible Inventory <http://docs.ansible.com/intro_inventory.html>`_.

.. code-block:: console

  ansible@hub:~$ sudo vi /etc/ansible/hosts

and add the connection info for your node substituting the IP or FQDN of your
node as well as the name of the user created in Step 2 above:

.. code-block:: console

  <node> ansible_ssh_user=<user>


**Step 2. Run Commands**

Let's set the IP address on Ethernet2 using the :ref:`eos_ipinterface` module:

.. code-block:: console

  ansible@hub:~$ ansible <node-from-inventory> -M path/to/ansible-eos/library/ -m eos_ipinterface.py -a "name=Ethernet2 address=192.0.2.150/24 debug=yes"

**Result** (debug output):
So what really happened?

1. We execute the command and Ansible goes to our inventory to find the specified node. As you can see from the output we're connecting to host ``172.16.130.20``
2. Ansible is told to connect via SSH with user ``ansible`` from ``ansible_ssh_user=ansible``.
3. Ansible creates a temp directory in the ``ansible`` user's home directory
4. Ansible copies eos_interface.py to the temp directory created above.
5. Ansible executes eos_interface.py with the specified arguments (-a)
6. eos.interface.py uses pyeapi to configure Ethernet2.
7. Ansible cleans up the temp folder and returns output to the control host.

.. code-block:: console

  172.16.130.20 | success >> {
      "changed": true,
      "changes": {
          "address": "192.0.2.150/24"
      },
      "debug": {
          "current_state": {
              "address": "192.0.2.50/24",
              "mtu": "1500",
              "name": "Ethernet2",
              "state": "present"
          },
          "desired_state": {
              "address": "192.0.2.150/24",
              "mtu": null,
              "name": "Ethernet2",
              "state": "present"
          },
          "node": "Node(connection=EapiConnection(transport=http://localhost:80//command-api))",
          "params": {
              "address": "192.0.2.150/24",
              "config": null,
              "connection": "localhost",
              "debug": true,
              "host": null,
              "logging": true,
              "mtu": null,
              "name": "Ethernet2",
              "password": null,
              "port": null,
              "state": "present",
              "transport": null,
              "username": null
          },
          "pyeapi_version": "0.2.4",
          "stateful": true
      },
      "instance": {
          "address": "192.0.2.150/24",
          "mtu": "1500",
          "name": "Ethernet2",
          "state": "present"
      }
  }


Next, let's create Vlan 1000 using the :ref:`eos_vlan` module:

.. code-block:: console

  ansible@hub:~$ ansible <node-from-inventory> -M path/to/ansible-eos/library/ -m eos_vlan.py -a "vlanid=1000 state=present debug=yes"

**Result** (debug output):

.. code-block:: console

  172.16.130.20 | success >> {
    "changed": true,
    "changes": {},
    "debug": {
        "current_state": {
            "enable": true,
            "name": "VLAN1000",
            "state": "present",
            "trunk_groups": "",
            "vlanid": "1000"
        },
        "desired_state": {
            "enable": true,
            "name": null,
            "state": "present",
            "trunk_groups": null,
            "vlanid": "1000"
        },
        "node": "Node(connection=EapiConnection(transport=http://localhost:80//command-api))",
        "params": {
            "config": null,
            "connection": "localhost",
            "debug": true,
            "enable": true,
            "host": null,
            "logging": true,
            "name": null,
            "password": null,
            "port": null,
            "state": "present",
            "transport": null,
            "trunk_groups": null,
            "username": null,
            "vlanid": "1000"
        },
        "pyeapi_version": "0.2.4",
        "stateful": true
    },
    "instance": {
        "enable": true,
        "name": "VLAN1000",
        "state": "present",
        "trunk_groups": "",
        "vlanid": "1000"
    }
  }






******************************************
Option B: Connect to Arista Node over eAPI
******************************************

**Tasklist**

1. :ref:`B-enable-eapi-label`
2. :ref:`B-install-pyeapi-label`
3. :ref:`B-run-adhoc-label`




.. _B-enable-eapi-label:

Enabling EOS Command API
========================
The modules provided in the Arista EOS role require command API (aka eAPI)
to be enabled on the switch. The modules use eAPI to communicate with EOS.
Since eAPI is not enabled by default, it must be initially enabled before the
EOS modules can be used.

.. Note:: The EOS role provides a module for enabling and configuring command
          API using a task; however, the local user still needs to be created


The steps below provide the basic steps to enable eAPI.  For more advanced
configurations, please consult the EOS User Guide.

**Step 1.** Login to the destination node and enter configuration mode

.. code-block:: console

  switch> enable
  switch# configure
  switch(config)#


**Step 2.** Enable eAPI

.. code-block:: console

  switch(config)# management api http-commands
  switch(config-mgmt-api-http-cmds)# no shutdown


The configuration above enables eAPI with the default settings.  This enables
eAPI to listen for connections on HTTPS port 443 by default.  If different
values are used, the eapi_protocol and eapi_port variables need to be updated
in your playbook.

**Step 3.** Create a local user
The user created in this step is different than the shell account to be
created in the Preparing EOS for Ansible section.  TODO Please see the section
Understanding the Security Model for more details.

.. code-block:: console

  switch(config)# username eapi secret icanttellyou


The username (eapi) and password (icanttellyou) can be anything you like.
This user is used to authenticate to eAPI and should be used for the
eapi_username and eapi_password variables in your playbooks.





.. _B-install-pyeapi-label:

Install pyeapi
==============
As mentioned earlier, the Ansible EOS role uses `pyeapi <https://github.com/arista-eosplus/pyeapi>`_
to make configuration changes to your Arista node. This requires you to have
pyeapi installed on your Ansible Contol Host (where you execute commands from).

.. hint: See the `pyeapi <https://github.com/arista-eosplus/pyeapi>`_ docs for more information.

**Step 1:** Pip install pyeapi

.. code-block:: console

  [ansible@veos ~]$ sudo pip install pyeapi

**Step 2:** Create local pyeapi.conf file

.. code-block:: console

  [ansible@veos ~]$ vi ~/.eapi.conf

with credentials you created earlier:

.. code-block:: console

  [connection:veos01]
  host: <ip-or-fqdn>
  transport: https
  username: eapi
  password: icanttellyou
  port: <port-if-non-default>





.. _B-run-adhoc-label:

Running Adhoc Commands
======================
If you are new to Ansible then it's easier to dip your toes in using
`Adhoc <http://docs.ansible.com/intro_adhoc.html>`_ commands versus writing a
full `Playbook <http://docs.ansible.com/playbooks.html>`_. The section below
will help guide you through running some Adhoc commands to configure basic
settings on your node.


**Step 1.** Create an Ansible Inventory File

Let's add the details of our test node to an Ansible Inventory file.

.. hint:: Learn more about `Ansible Inventory <http://docs.ansible.com/intro_inventory.html>`_.

.. code-block:: console

  ansible@hub:~$ sudo vi /etc/ansible/hosts

and add the connection info for your node substituting the IP or FQDN of your
node. This should match the ``host`` parameter in your ``.eapi.conf``:

.. code-block:: console

  <node> ansible_connection=local

**Step 2. Run Commands**

Let's set the IP address on Ethernet2 using the :ref:`eos_ipinterface` module.
Now that we are using a local connection we need to add an extra argument to
our command. Notice ``connection=veos01`` in our argument list. This must match
an entry in your ``~/.eapi.conf``:

.. code-block:: console

  ansible@hub:~$ ansible <node-from-inventory> -M path/to/ansible-eos/library/ -m eos_ipinterface.py -a "connection=veos01 name=Ethernet2 address=192.0.2.50/24 debug=yes"

**Result** (debug output):
So what really happened?

1. We execute the command and Ansible goes to our inventory to find the specified node. Since we added ``ansible_connection=local`` to our inventory, Ansible will execute the module locally.
2. Ansible is told to connect via SSH with user ``ansible`` from ``ansible_ssh_user=ansible``.
3. Ansible creates a temp directory in the user's home directory, eg ``$HOME/.ansible/tmp/``.
4. Ansible copies eos_interface.py to the temp directory created above.
5. Ansible executes eos_interface.py with the specified arguments (-a)
6. eos.interface.py uses pyeapi to configure Ethernet2.
7. pyeapi consults ``~/.eapi.conf`` to find connection named ``veos01``
7. Ansible cleans up the temp folder and returns output to the control host.

.. code-block:: console

  172.16.130.20 | success >> {
    "changed": true,
    "changes": {
        "address": "192.0.2.50/24"
    },
    "debug": {
        "current_state": {
            "address": "192.0.2.150/24",
            "mtu": "1500",
            "name": "Ethernet2",
            "state": "present"
        },
        "desired_state": {
            "address": "192.0.2.50/24",
            "mtu": null,
            "name": "Ethernet2",
            "state": "present"
        },
        "node": "Node(connetion=EapiConnection(transport=http://172.16.130.20:80//command-api))",
        "params": {
            "address": "192.0.2.50/24",
            "config": null,
            "connection": "veos01",
            "debug": true,
            "host": null,
            "logging": true,
            "mtu": null,
            "name": "Ethernet2",
            "password": null,
            "port": null,
            "state": "present",
            "transport": null,
            "username": null
        },
        "pyeapi_version": "0.1.0",
        "stateful": true
    },
    "instance": {
        "address": "192.0.2.50/24",
        "mtu": "1500",
        "name": "Ethernet2",
        "state": "present"
    }
  }


Next, let's create Vlan 100 using the :ref:`eos_vlan` module:

.. code-block:: console

  ansible@hub:~$ ansible <node-from-inventory> -M path/to/ansible-eos/library/ -m eos_vlan.py -a "connection=veos01 vlanid=100 state=present debug=yes"

**Result** (debug output):

.. code-block:: console

  172.16.130.20 | success >> {
    "changed": true,
    "changes": {},
    "debug": {
        "current_state": {
            "enable": true,
            "name": "VLAN0100",
            "state": "present",
            "trunk_groups": "",
            "vlanid": "100"
        },
        "desired_state": {
            "enable": true,
            "name": null,
            "state": "present",
            "trunk_groups": null,
            "vlanid": "100"
        },
        "node": "Node(connetion=EapiConnection(transport=http://172.16.130.20:80//command-api))",
        "params": {
            "config": null,
            "connection": "veos01",
            "debug": true,
            "enable": true,
            "host": null,
            "logging": true,
            "name": null,
            "password": null,
            "port": null,
            "state": "present",
            "transport": null,
            "trunk_groups": null,
            "username": null,
            "vlanid": "100"
        },
        "pyeapi_version": "0.1.0",
        "stateful": true
    },
    "instance": {
        "enable": true,
        "name": "VLAN0100",
        "state": "present",
        "trunk_groups": "",
        "vlanid": "100"
    }
  }

*********
Now what?
*********
This guide should have helped you install and configure all necessary
dependencies and given you a basic idea of how to use the Ansible EOS role.
Next, you can create some Ansible playbooks using a combination of modules.
You can also check out the list of modules provided to see how best to
configure your nodes.

.. tip:: Please send us some `feedback <eosplus-dev@arista.com>`_ on ways to improve this guide.
