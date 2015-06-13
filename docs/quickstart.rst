.. _quickstart:

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
environment running with the Ansible EOS role. If not, see :ref:`install-ansible-label`
and :ref:`install-role-label` before following this guide.
This guide assumes very little experience with Ansible, therefore,
if the steps seem to leave you with questions and uncertainties please let us know
so that we can improve it.


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

- :ref:`A-enable-eapi-label`
- :ref:`A-eos-user-label`
- :ref:`A-install-pyeapi-label`
- :ref:`A-run-adhoc-label`



.. _A-enable-eapi-label:

1. Enabling EOS Command API
===========================
The modules provided in the Arista EOS role require command API (aka eAPI)
to be enabled on the switch. The modules use eAPI to communicate with EOS.
Since eAPI is not enabled by default, it must be initially enabled before the
EOS modules can be used.

.. Note:: The EOS role provides a module for enabling and configuring command
          API using a task; however, the local user still needs to be created


The steps below provide the basic steps to enable eAPI.  For more advanced
configurations, please consult the EOS User Guide.

**Step 1.1.** Login to the destination node and enter configuration mode

.. code-block:: console

  switch> enable
  switch# configure
  switch(config)#


**Step 1.2.** Enable eAPI

.. code-block:: console

  switch(config)# management api http-commands
  switch(config-mgmt-api-http-cmds)# no shutdown


The configuration above enables eAPI with the default settings.  This enables
eAPI to listen for connections on HTTPS port 443 by default.

**Step 1.3.** Create a local user
The user created in this step is different than the shell account to be
created in the Preparing EOS for Ansible section. Please see the section
:ref:`security-model-label` for more details.

.. code-block:: console

  switch(config)# username eapi secret icanttellyou


The username (eapi) and password (icanttellyou) can be any valid string
value.


.. _A-eos-user-label:

2. Preparing EOS for Ansible
============================
In order to successfully execute playbook tasks the EOS node must be
configured to allow the Ansible control node to directly attach to the
Linux shell.  The following steps provide a walk through for setting up
password-less access to EOS nodes for use with Ansible.

.. Note:: These steps will create a user that has root privileges to your EOS
          node, so please handle credentials accordingly

**Step 2.1.** Login to the destination node and enter the Linux shell

.. code-block:: console

  veos> enable
  veos# bash

  Arista Networks EOS shell


**Step 2.2.** Create the user to use with Ansible, create the home directory
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


**Step 2.3.** Upload the SSH key to use from your Ansible control host and
verify access from remote host

.. code-block:: console

  ansible@hub:~$ scp ~/.ssh/id_rsa.pub ansible@veos01:.ssh/authorized_keys
  Password:

  ansible@hub:~$ ssh ansible@veos01

  Arista Networks EOS shell

  [ansible@veos ~]$


**Step 2.4.** Configure EOS to create user on reboot with no password assigned.
This will only allow the Ansible user to login with keys.

.. code-block:: console

  [ansible@veos ~]$ vi /mnt/flash/rc.eos

  #!/bin/sh
  useradd -d /persist/local/ansible -G eosadmin ansible


**Step 2.5.** Reboot the EOS node and start automating with Ansible

.. code-block:: console

  [ansible@veos ~]$ sudo reboot



.. _A-install-pyeapi-label:

3. Install pyeapi
=================
As mentioned earlier, the Ansible EOS role uses `pyeapi <https://github.com/arista-eosplus/pyeapi>`_
on the Arista node that will be configured. Let's install it.

If the Arista node has internet access:

.. code-block:: console

  [ansible@veos ~]$ sudo pip install pyeapi

If there's no internet access:

**Step 3.1:** Download Pypi Package

`Download <https://pypi.python.org/pypi/pyeapi>`_ the latest version of pyeapi on your local machine.

**Step 3.2:** SCP the file to the Arista node and install

.. code-block:: console

  ansible@hub:~$ scp path/to/pyeapi-<VERSION>.tar.gz ansible@veos01:/tmp

Then SSH into your node and install it:

.. code-block:: console

  [ansible@veos ~]$ sudo pip install /tmp/pyeapi-<VERSION>.tar.gz

**Step 3.3:** Create local pyeapi.conf file

.. code-block:: console

  [ansible@veos ~]$ vi /mnt/flash/eapi.conf

with credentials and settings you configured in steps 1.2 and 1.3:

.. code-block:: console

  [connection:localhost]
  transport: https
  username: eapi
  password: icanttellyou
  port: <port-if-non-default>


.. _A-run-adhoc-label:

4. A Simple Playbook
====================
If you are new to Ansible it might seem like a lot is going on, but this step will
show you how easy it is to manage your Arista device. The power of Ansible lies in
the `Playbook <http://docs.ansible.com/playbooks.html>`_. We will just skim the
surface of what's possible in a playbook, but this should serve as a good launching
point.


**Step 4.1.** Create an Ansible Inventory File

Each Ansible play references one or more nodes. You define these nodes in an
Ansible ``hosts`` file.

.. hint:: Learn more about `Ansible Inventory <http://docs.ansible.com/intro_inventory.html>`_.

.. code-block:: console

  ansible@hub:~$ sudo vi /etc/ansible/hosts

and add the connection info for your node substituting the IP or FQDN of your
node as well as the name of the user created in Step 2.2 above:

.. code-block:: console

  [eos_switches]
  <node>
  # Add more entries here for additional devices you want to
  # keep in the eos_switches group

  [eos_switches:vars]
  ansible_ssh_user=<user>

Example

.. code-block:: console

  [eos_switches]
  veos01
  veos02
  veos03
  veos04

  [eos_switches:vars]
  ansible_ssh_user=ansible


**Step 4.2. Create playbook**

Let's create Vlan150 using the :ref:`eos_vlan` module:

.. code-block:: console

  ansible@hub:~$ vi my-test-eos-playbook.yml

Then paste in the following

.. code-block:: yaml

  ---
  - hosts: eos_switches
    gather_facts: no

    roles:
      - arista.eos

    tasks:
      - name: Add Vlan 150 to my switches
        eos_vlan:
          vlanid=150
          name=newVlan150

**Result**:

So what really happened?

1. We execute the command and Ansible goes to our inventory to find the specified nodes in group ``eos_switches``.
2. Ansible is told to connect via SSH with user ``ansible`` from ``ansible_ssh_user=ansible``.
3. Ansible creates a temp directory in the ``ansible`` user's home directory
4. Ansible copies eos_vlan.py to the temp directory created above.
5. Ansible executes eos_vlan.py with the specified arguments
6. eos.interface.py uses pyeapi to configure the new Vlan.
7. Ansible cleans up the temp folder and returns output to the control host.




******************************************
Option B: Connect to Arista Node over eAPI
******************************************

**Tasklist**

- :ref:`B-enable-eapi-label`
- :ref:`B-install-pyeapi-label`
- :ref:`B-run-adhoc-label`




.. _B-enable-eapi-label:

1. Enabling EOS Command API
===========================
The modules provided in the Arista EOS role require command API (aka eAPI)
to be enabled on the switch. The modules use eAPI to communicate with EOS.
Since eAPI is not enabled by default, it must be initially enabled before the
EOS modules can be used.

The steps below provide the basic steps to enable eAPI.  For more advanced
configurations, please consult the EOS User Guide.

**Step 1.1.** Login to the destination node and enter configuration mode

.. code-block:: console

  switch> enable
  switch# configure
  switch(config)#


**Step 1.2.** Enable eAPI

.. code-block:: console

  switch(config)# management api http-commands
  switch(config-mgmt-api-http-cmds)# no shutdown


The configuration above enables eAPI with the default settings.  This enables
eAPI to listen for connections on HTTPS port 443 by default.

**Step 1.3.** Create a local user
The user created in this step is used by pyeapi to run configuration commands.

.. code-block:: console

  switch(config)# username eapi secret icanttellyou


The username (eapi) and password (icanttellyou) can be any string value.  The
values are then used in either eapi.conf or passed in through the module
meta arguments to authenticate to eAPI.



.. _B-install-pyeapi-label:

2. Install pyeapi
=================
As mentioned earlier, the Ansible EOS role uses `pyeapi <https://github.com/arista-eosplus/pyeapi>`_
to make configuration changes to your Arista node. This requires you to have
pyeapi installed on your Ansible Contol Host (where you execute commands from).

.. hint: See the `pyeapi <https://github.com/arista-eosplus/pyeapi>`_ docs for more information.

**Step 2.1:** Pip install pyeapi

.. code-block:: console

  [ansible@hub ~]$ sudo pip install pyeapi

**Step 2.2:** Create local pyeapi.conf file

.. code-block:: console

  [ansible@hub ~]$ vi ~/.eapi.conf

with credentials you created in Step 1.3. The ``connection:<NAME>`` should match
the entry in ``/etc/ansible/hosts``, Step 3.1 below:

.. code-block:: console

  [connection:veos01]
  host: <ip-or-fqdn>
  transport: https
  username: eapi
  password: icanttellyou
  port: <port-if-non-default>


.. _B-run-adhoc-label:

3. A Simple Playbook
====================
If you are new to Ansible it might seem like a lot is going on, but this step will
show you how easy it is to manage your Arista device. The power of Ansible lies in
the `Playbook <http://docs.ansible.com/playbooks.html>`_. We will just skim the
surface of what's possible in a playbook, but this should serve as a good launching
point.


**Step 3.1.** Create an Ansible Inventory File

Let's add the details of our test node to an Ansible Inventory file.

.. hint:: Learn more about `Ansible Inventory <http://docs.ansible.com/intro_inventory.html>`_.

.. code-block:: console

  ansible@hub:~$ sudo vi /etc/ansible/hosts

and add the connection info for your node substituting the IP or FQDN of your
node under our ``eos_switches`` group.
This should match the ``connection`` parameter in your ``~/.eapi.conf``:

.. code-block:: console

  [eos_switches]
  <node>

Example

.. code-block:: console

  [eos_switches]
  veos01


**Step 4.2. Create playbook**

Let's create Vlan150 using the :ref:`eos_vlan` module:

.. code-block:: console

  ansible@hub:~$ vi my-test-eos-playbook.yml

Then paste in the following

.. code-block:: yaml

  ---
  - hosts: eos_switches
    gather_facts: no
    connection: local

    roles:
      - arista.eos

    tasks:
      - name: Add Vlan 150 to my switches
        eos_vlan:
          vlanid=150
          name=newVlan150
          connection={{ inventory_hostname }}

**Result**:

So what really happened?

1. We execute the command and Ansible goes to our inventory to find the specified nodes that match group ``eos_switches``.
2. Ansible is told to use ``connection:local`` so no SSH connection will be established to the node.
3. Ansible substitutes the host name from ``/etc/ansible/hosts`` into the ``{{ inventory_hostname }}`` parameter. This creates the link to the ``[connection:veos01]`` in ``~/.eapi.conf``.
4. Ansible creates a temp directory in the user's home directory, eg ``$HOME/.ansible/tmp/``.
5. Ansible copies eos_vlan.py to the temp directory created above.
6. Ansible executes eos_vlan.py with the specified arguments
7. eos_vlan.py uses pyeapi to configure the Vlan.
8. pyeapi consults ``~/.eapi.conf`` to find connection named ``veos01``
9. Ansible cleans up the temp folder and returns output to the control host.


*********
Now what?
*********
This guide should have helped you install and configure all necessary
dependencies and given you a basic idea of how to use the Ansible EOS role.
Next, you can add to your Ansible playbooks using a combination of modules.
You can also check out the list of modules provided within the Ansible EOS Role
to see all of the ways to make configuration changes.

.. tip:: Please send us some `feedback <eosplus-dev@arista.com>`_ on ways to improve this guide.
