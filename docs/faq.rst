###
FAQ
###


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
