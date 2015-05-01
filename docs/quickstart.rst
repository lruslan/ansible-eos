###########
Quick Start
###########

************
Introduction
************
This quick-start guide provides the fastest method to get up and running with
the Ansible Role for EOS.  It assumes that you already have an Ansible
environment running. If not, see :ref:`install-ansible-label` before following
this guide.

************
Requirements
************
* Arista EOS 4.12 or later
* EOS Command API enabled (see :ref:`enable-eapi-label`)
* Linux shell account (see :ref:`prepare-eos-for-ansible-label`)


***************
Getting Started
***************

.. _enable-eapi-label:

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
created in the Preparing EOS for Ansible section.  Please see the section
Understanding the Security Model for more details.

.. code-block:: console

  switch(config)# username eapi secret icanttellyou


The username (eapi) and password (icanttellyou) can be anything you like.
This user is used to authenticate to eAPI and should be used for the
eapi_username and eapi_password variables in your playbooks.


.. _prepare-eos-for-ansible-label:

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

.. tip:: Wait for your node to come back before going to the next section


Running Adhoc Commands
======================
If you are new to Ansible then it's easier to dip your toes in using `Adhoc <http://docs.ansible.com/intro_adhoc.html>`_
commands versus writing a full `playbook <http://docs.ansible.com/playbooks.html>`_.
The section below will help guide you through running some Adhoc commands
to configure basic settings on your node.


**1. Create an Ansible Inventory File**

Let's add the details of our test node to an Ansible Inventory file.

.. hint:: Learn more about `Ansible Inventory <http://docs.ansible.com/intro_inventory.html>`_.

.. code-block:: console

  [ansible@ansible-control-host ~]$ sudo vi /etc/ansible/hosts

and add the connection info for your host substituting the IP or FQDN of your node:

.. code-block:: console




**2. Configure the Hostname**

.. code-block:: console

  [ansible@ansible-control-host ~]$
