######################
Developer Information
######################

************
Introduction
************

This section provides information for individuals that want to get started
developing EOS modules.  Whether adding new modules, extending existing modules
or developing bug fixes, the details here explain how to get started working
with the Ansible EOS role form source.

This section assumes that an Ansible development environment has already been
created.  For specific details on developing with Ansible please see the
`Developer Information`_ found in the official Ansible documentation.

*******************
Running from Source
*******************

In order to get started running the Ansible EOS role from source, create a
clone of the `develop` branch (or any other branch that you are interested in)
on your local machine.::

    $ git clone https://github.com/arista-eosplus/ansible-eos
    Cloning into 'ansible-eos'...
    remote: Counting objects: 486, done.
    remote: Compressing objects: 100% (34/34), done.
    remote: Total 486 (delta 6), reused 0 (delta 0), pack-reused 450
    Receiving objects: 100% (486/486), 1.66 MiB | 1.51 MiB/s, done.
    Resolving deltas: 100% (303/303), done.
    Checking connectivity... done.

Once the ansible-eos Github repository is installed, using the modules is as
easy as passing the path to the ansible executable::

    $ ansible -M /workspace/ansible-eos/library -m eos_vlan -a "vlanid=100"

Simply specify the module to be run (eos_vlan in the above example) and the
arguments to pass to the module using the -a option.

****************
Write Test Cases
****************

The EOS role includes a number of modules for configuring resources on
destination EOS nodes.   All module test cases are defined in test/testcases.
Test cases are defined as a simple YAML file that describes the module to run
along with the arguments to be passed to the module.  The test suite will then
build an ansible command run it against a switch (either a hardware based model
or vEOS).

In order to configure the test suite to run against switches in a given
environment, modify the test/fixtures/eapi.conf and test/fixtures/hosts file to
reflect the nodes to be tested.

Once the eapi.conf file and hosts file have been updated, use the following
command to execute the test suite::

    $ make tests

************
Contributing
************

The modules developed as part of the Ansible EOS role are supported by the
Arista EOS+ community.  We gladly accept and encourage contributions in the form
of new modules, updated modules, test cases and documentation updates.  Simply
develop the changes and submit a pull request through Github.

For changes submitted by pull request, the Arista EOS+ community enforces some
basic rules for new contributions.

1. New modules must be fully documented per Ansible module documentation
   standards
2. New or changed modules must include test cases that test the new module or
   new arguments made available in the module.

If you have any questions regarding module development or running modules from
source, please feel free to contact Arista EOS+ at ansible-dev@arista.com


.. _Developer Information: http://docs.ansible.com/developing.html
