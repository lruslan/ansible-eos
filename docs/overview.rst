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

*************
Ansible Tower
*************
Ansible provides a product that implements a web based interface and REST API
known as `Tower <http://www.ansible.com/tower>`_. The web interface provides
some additional capabilities to the base Ansible framework around role based
access and programmatic interface to the Ansible environment.
