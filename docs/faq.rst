###
FAQ
###

************
Introduction
************

The below list provides some answers to commonly asked questions about the
Ansible EOS role.


What are the basic requirements for using the EOS role for Ansible?
===================================================================

This varies a little bit based upon how you communicate with your node.
The two options are explained in :ref:`deployment-topologies-label`.

Regardless of connection method you need the following:

* Arista EOS 4.13.7M or later running on your node
* EOS Command API enabled (see :ref:`A-enable-eapi-label` for more information)

In addition to the above, there are other connection-specific requirements:

If you connect to your node via SSH:

* You need the `Python Client for eAPI <https://github.com/arista-eosplus/pyeapi>`_ 0.3.0 or later **installed on your EOS node** (see :ref:`A-install-pyeapi-label` for more information)
* Linux shell account on your EOS node (see :ref:`A-eos-user-label` for more information)

If you connect to your node via eAPI:

* You need the `Python Client for eAPI <https://github.com/arista-eosplus/pyeapi>`_ 0.3.0 or later **installed on your Ansible server** (see :ref:`B-install-pyeapi-label` for more information)


.. _faq-security-label:

Is there any intention to encrypt passwords we put into eapi.conf?
==================================================================

No, we are working on support for certificates but we cannot encrypt the
password in eapi.conf.  The best alternative is to use Ansible vault or prompt
for password at runtime of the playbook.


Is pyeapi required on both the Ansible control host and the EOS node?
=====================================================================

It depends on if using (or want to use) connection local.  The Python client
for eAPI (pyeapi) must be installed where ever the Ansible module is executed
from.  The pyeapi client is a dependency of the common module code for all of
the modules.

Do I have to use the pyeapi eapi.conf file?
===========================================

No, it is not a absolutel requirement.  All EOS modules will accept connection
parameters for configuring the eAPI transport properties.  Using eapi.conf is
convienent but not necessary.

Does the EOS role work with Ansible Tower?
==========================================

Yes, the Ansible EOS role works fine with implementations that utilize Ansible
Tower for management.

Does the Ansible EOS role work with all version of Arista EOS?
==============================================================

The Ansible EOS role is tested to work with EOS 4.13.7M or later releases.  Any
EOS release prior to 4.13.7M is not guaranteed to work with the EOS role.

Is there any requirement to put changes into ansible.cfg?
=========================================================

No, it works with all the Ansible defaults.

Is there something like a rollback function available in ansible?
=================================================================

Yes, its all in the implementation.  When working with a tool like Ansible,
the node configuration should be kept under version control.  As such, rolling
back a nodes configuration is a matter of reverting the config.  It's an
implementation detail, not necessarily a module or feature.   We have
successfully demonstrated rollback many times using Ansible.
