v1.2.0
-----

2015-11-05

New Modules
^^^^^^^^^^^

* Add eos_vrrp (`78 <https://github.com/arista-eosplus/ansible-eos/pull/78>`_) [`grybak <https://github.com/grybak>`_]
    Add the eos_vrrp module. This module controls interface VRRP configuration.
    (Requires pyeapi update)
* Feature staticroute (`68 <https://github.com/arista-eosplus/ansible-eos/pull/68>`_) [`grybak <https://github.com/grybak>`_]
    Adds the eos_staticroute module to perform configuration management of static ip routes.
    (Requires pyeapi update)
* Add eos_varp and eos_varp_interface modules (`67 <https://github.com/arista-eosplus/ansible-eos/pull/67>`_) [`phil-arista <https://github.com/phil-arista>`_]
    Adds the eos_varp and eos_varp_interface modules. The eos_varp module provides management of the system's virtual mac address.  The eos_varp_interface manages virtual-router ip addresses within Vlans.
    (Requires pyeapi update)
* Add eos_routemap module (`66 <https://github.com/arista-eosplus/ansible-eos/pull/66>`_) [`phil-arista <https://github.com/phil-arista>`_]
    The eos_routemap module provides configuration management of system route-maps.
    (Requires pyeapi update)
* Add eos_user module (`51 <https://github.com/arista-eosplus/ansible-eos/pull/51>`_) [`phil-arista <https://github.com/phil-arista>`_]
    The eos_user module adds the ability to manage CLI users. All user attributes are configurable including SSH Key support.
    (Requires pyeapi update)

Enhancements
^^^^^^^^^^^^

* Added encoding option to command module. (`65 <https://github.com/arista-eosplus/ansible-eos/pull/65>`_) [`chepazzo <https://github.com/chepazzo>`_]
    The eos_command module now only supports enable commands. This enhancement allows you to pass an encoding option. The choices are json and text. The encoding option determines the format of the returned output.
* Add support for maximum-paths (`64 <https://github.com/arista-eosplus/ansible-eos/pull/64>`_) [`phil-arista <https://github.com/phil-arista>`_]
    This enhancement adds the ability to define BGP maximum paths and maximum ecmp paths.
    (Requires pyeapi update)
* Add ip routing (`61 <https://github.com/arista-eosplus/ansible-eos/pull/61>`_) [`phil-arista <https://github.com/phil-arista>`_]
    This enhancement augments the eos_system module. It now provides the ability to enable ``ip routing``.
    (Requires pyeapi update)

Fixed
^^^^^

* eos_ping should analyze loss instead of errors (`53 <https://github.com/arista-eosplus/ansible-eos/issues/53>`_)
    Due to variations in EOS ping output, it became necessary to analyze loss instead of errors.
* eos_ping fails when network is unreachable (`52 <https://github.com/arista-eosplus/ansible-eos/issues/52>`_)
    The eos_ping module will now successfully exit even when the ping result is ``network unreachable``
* eos_ping resuses 'host' argument (`47 <https://github.com/arista-eosplus/ansible-eos/issues/47>`_)
    The eos_ping module used the attribute ``host`` which caused a conflict with the meta argument ``host``. The updated attribute is called ``dst``.
* port-channel set to mode "on" not "active" on initial pass (`36 <https://github.com/arista-eosplus/ansible-eos/issues/36>`_)
    The eos_portchannel module runs set_lacp_mode before set_members. This means that when set_members is run, you end up with the default lacp mode instead of the mode you defined. Now, the set_members method includes a mode keyword.
    (Required pyeapi update)
