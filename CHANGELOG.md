Arista EOS Role for Ansible
===========================

## IN PROGRESS

- adds trunk_groups argument to eos_switchport
- changes trunk_allowed_vlans to allow a range of vlans
- changes arguments used by eos_config (see documentation)
- fixes an issue with out of order vlans in eos_switchport

### New Modules

* eos_acl_entry
* eos_bgp_config
* eos_bgp_neighbor
* eos_bgp_network

## 1.0.1, 6/13/2015

- adds additional parameters to eos_config
- adds vlan argument to eos_vxlan_vtep
- fixes issue with honoring enablepwd if specified
- fixes #37

## 1.0.0, 5/4/2015

- adds support for pyeapi
- adds system test harness for testing modules against eos nodes
- adds stateful common module

### New Modules

* eos_command.py
* eos_config.py
* eos_ethernet.py
* eos_facts.py
* eos_interface.py
* eos_ipinterface.py
* eos_mlag_config.py
* eos_mlag_interface.py
* eos_portchannel.py
* eos_purge.py
* eos_stp_interface.py
* eos_switchport.py
* eos_system.py
* eos_vlan.py
* eos_vxlan.py
* eos_vxlan_vlan.py
* eos_vxlan_vtep.py

