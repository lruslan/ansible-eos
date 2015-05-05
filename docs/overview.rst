########
Overview
########

************
Introduction
************
Ansible is a configuration management framework that provides an automated
infrastructure for managing systems devices and applications. Ansible provides
this functionality using an agent-less approach that focuses on management of
the destination device and/or application over SSH. Ansible achieves it vision
through the implementation of playbooks and modules. Playbooks, which are in
turn comprised of a series of tasks to be executed on a host or group of
hosts, provide the fundamental workflow in Ansible. Modules are host and/or
application specific that perform the operations based on the directives of
the tasks and playbooks. Complete details about Ansible can be found at
their `website <http://docs.ansible.com/index.html>`_.

****************
Connection Types
****************
Ansible provides three distinctly different connection types each providing
a different method for connecting the Ansible runtime components
(playbooks, modules) with the destination device. A summary of the connection
types are below.

SSH Connection
==============
When operating in this mode, Ansible will connect to the destination host
using an encrypted SSH session. The SSH connection is established using
either the hosts native SSH binary or using the
`Paramiko <http://docs.ansible.com/intro_getting_started.html#remote-connection-information>`_
library. Since it uses SSH as the transport, the Ansible connection needs to
be able to authenticate to the remote system and expects to operate in a
Linux shell environment

Local connections
=================
When a host or task is operating with a local connection, tasks are executed
from the Ansible host where the job was initiated. Local connections allow
Ansible to make use of API transports and remove the need for establishing an
SSH connection to the target device.

Accelerated mode
================
Ansible supported (since v0.8) a mode of operation known as Fireball mode.
Fireball mode has since been depreciated in favor of accelerated mode (as of v1.3).
Accelerated mode connects to the destination node and starts a daemon that is
used for the remainder of the transaction. More details about accelerated
mode can be found at this link.

In addition to the connection types discussed above, Ansible also supports
a pull model. The pull model works in conjunction with SCM systems to perform
its duties locally on the node. The pull model executes a local utility that
retrieves the configuration data and proceeds to execute all of the activity
locally on the node.


.. _ansible-eos-role-label:

********************
The Ansible EOS Role
********************

Integration with the Python Client for eAPI
===========================================
The Ansible Role for EOS builds on the `Python Client for eAPI <https://github.com/arista-eosplus/pyeapi>`_ to provide
automation of the management plane.  Using eAPI as the underlying tranport,
Ansible can be configured to interface with Arista EOS using either SSH based
connections or HTTP based connections.


Topologies
==========
Above, we discussed how Ansible is typically used to control a node. These
principles remain true for Arista EOS nodes, however, there are some nuances
that are important to understand. Next, we will discuss the two main
methods used to control an Arista EOS node using Ansible.

.. image:: _img/ansible-deploy.jpg
        :width: 85%
        :align: center

The illustration above demonstrates a typical scenario. You, as the user, want
to execute an Ansible Playbook on one (or many) of your Arista nodes. From the
user's perspective the interaction with the Ansible Control Host is the same,
from your shell you would type

.. code-block:: console

  ansible-playbook eos.yaml

but the way in which the playbook is executed will differ between Option A and
Option B. Let's discuss those differences below.

Option A
========
This method follows the traditional Ansible control procedure, namely:

1. Execute ``ansible-playbook eos.yaml`` from the Ansible Control Host
2. Collect Fact information from the node
3. Download the module to the node
4. Execute the module on the node
5. Read stdout and parse it into JSON
6. Return the result to the Ansible Control Host

**Assumption 1**
You'll notice that this method uses SSH to communicate with the node. This
implies that you have already included the Ansible Control Host's public SSH
key in the nodes ``authorized_keys`` file, or you are providing a password
when the playbook executes.

**Assumption 2**
Pyeapi is being used by the module to make configuration changes on the
node. This implies that ``pyeapi`` is already installed on the node. The pyeapi
module is NOT installed on Arista EOS nodes by default, so installation would
be required by the user.


Option B
========
This method uses the ``connection: local`` feature within the ``eos.yaml``
playbook. This changes how the playbook gets executed in the following way:

1. Include ``connection: local`` in ``eos.yaml``
2. Execute ``ansible-playbook eos.yaml`` from the Ansible Control Host
3. pyeapi consults the local eapi.conf file which provide node connection information
4. Collect Fact information from the node
5. Execute the module on the Ansible Control Host
6. Read stdout and parse it into JSON
7. Return the result to the Ansible Control Host

**Assumption 1**
Here, the connection between the Ansible Control Host and the Arista node is
an eAPI connection. This implies that you have an ``eapi.conf`` file on your
Ansible Control Host that contains the connection parameters for this node, or
you pass the connection parameters as arguments.
The caveat when using ``eapi.conf`` is that the password for the eAPI
connection is stored as plaintext.

**Example** Include connection parameters in playbook

.. code-block:: yaml

  - name: eos nodes
    hosts: eos_switches

  (truncated)

  tasks:
  - name: Configure EOS VLAN resources
    eos_vlan: vlanid=100
              username=eapi
              password=password
              transport=https

**Example** Consult ``eapi.conf`` for connection information

.. code-block:: yaml

  tasks:
  - name: Configure EOS VLAN resources
    eos_vlan: vlanid=100
              connection=veos02

Sample ``eapi.conf``

.. code-block:: ini

  [connection:veos02]
  host: 192.0.2.2
  username: eapi
  password: password
  enablepwd: itsasecret
  port: 1234
  transport: https

.. _security-model-label:

********************************
Understanding the Security Model
********************************
The Ansible EOS role provides a two stage authentication model to
maximize the security and flexibility available for providing programatic
access to EOS nodes.   The steps above walk through how to enable both eAPI
and create a shell account for use with Ansible.   This section provides some
additional details about how the two stage authentication model works.

.. Note:: The two stage authentication model only applies to Option A.

Implementing a two stage security model allows operators to secure the
Ansible shell account and prevent it from configuring EOS.  Conversely, having
a separate eAPI authentication mechanism allows operators to separately
control the users that can run EOS modules without giving them root
access to EOS.

When Ansible connects to an EOS node, it must first authenticate to Linux
as it would for any other Linux platform.  In order to create the shell
account, the steps in :ref:`A-eos-user-label` should be followed.  The
steps above will create a user called 'ansible'.  You are free to choose
any username you like with the following exception: you cannot create a
username the same as a local account in EOS (more on that in a moment).

By default, the EOS role assumes the user account is called 'ansible'.  If
the shell account is different, then the eos_username variable must be set
in your playbook to the name of the shell account you intend to use.  This
ensures that the EOS node is bootstrapped properly for use with Ansible.

The second stage authentication model uses eAPI.  eAPI provides its own
authentication mechanism for securing what users can perform which actions
in EOS. The eAPI user can be one that is authenticated by AAA; however,
that is outside the scope of this discussion.  The section :ref:`A-enable-eapi-label`
provides an example of how to create a local user to use when
authenticating with eAPI.

.. Note:: The shell account and eAPI user must be different.

*************
Ansible Tower
*************
Ansible provides a product that implements a web based interface and REST API
known as `Tower <http://www.ansible.com/tower>`_. The web interface provides
some additional capabilities to the base Ansible framework around role based
access and programmatic interface to the Ansible environment.
