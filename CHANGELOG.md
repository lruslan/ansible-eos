Arista EOS role for Ansible
===========================

## v0.2.1 (under development)

- added eapi attribute to all modules
- fixes an issue with switchport trunks being set to none (issue #7)
- support added for using enable_password over eAPI (thanks rsolomo)

Updated Modules:

* eos_vlan
* eos_vxlan
* eos_switchport
* eos_portchannel
* eos_ipv4interface

New Modules:

* eos_ethernet
* eos_stp_interface


## v0.1.2

- fixes a minor issue with eos_vlan trying to set a nonexistent vni
- fixes an issue where the wrong state was being set for configured resources
- documentation updates

Updated Modules:

* eos_eapi


## v0.1.1

- fixes a major bug with eos_command using an old variable name
- added additional details and new examples to README


## v0.1.0

- first release of role to Ansible Galaxy
- all modules initially released

New Modules:

* eos_command
* eos_interface
* eos_ipv4interface
* eos_portchannel
* eos_switchport
* eos_vlan
* eos_vxlan
* eos_purge (beta)
* eos_eapi (alpha)
* eos_facts (on-box connections only)
