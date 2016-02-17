v1.3.0
------

2016-02-17

New Modules
^^^^^^^^^^^
* None

Enhancements
^^^^^^^^^^^^

* Enhance autorefresh (`88 <https://github.com/arista-eosplus/ansible-eos/pull/88>`_) [`phil-arista <https://github.com/phil-arista>`_]
    This knob is accessible in the module and is turned off by default. This reduces the number of 'show run all' that are executed during a module run.
* Workaround for Ansible 2.0 changes in AnsibleModule._log_invocation(). (`85 <https://github.com/arista-eosplus/ansible-eos/pull/85>`_) [`chepazzo <https://github.com/chepazzo>`_]
    Modify module logging to accommodate Ansible 2.0 core changes.
* Add disable key to existing modules for negation of properties (`84 <https://github.com/arista-eosplus/ansible-eos/pull/84>`_) [`grybak-arista <https://github.com/grybak-arista>`_]
    Implements a disable key in modules for negation of properties, when appropriate.

Fixed
^^^^^

* Enable/Disable logic incorrect in modules with command_builder (`86 <https://github.com/arista-eosplus/ansible-eos/issues/86>`_)
    The command builder in pyeapi was updated to make logic more uniform across all APIs. This required an update to the Ansible modules.  This bug addresses some modules that did not get updated on the first go.
* [eos_vlan] Set_trunks doesn't pass correct value to API (`82 <https://github.com/arista-eosplus/ansible-eos/issues/82>`_)
    The eos_vlan module did not properly separate the trunk groups when calling the set_trunks API method. This fixes that issue within the module. No change to pyeapi.
* eos_interface defaulting an interface (`73 <https://github.com/arista-eosplus/ansible-eos/issues/73>`_)
    The common/eos.py code was fixed to allow flexible support of state methods within the module.  This issue was resolved with that addition to the common code along with an added 'default' method within the module to call the interfaces API default method.  Note that state=default is not an idempotent operation.  It will run every time since the resulting state will be state=present.
* eos_bgp_* modules take a long time to complete (`59 <https://github.com/arista-eosplus/ansible-eos/issues/59>`_)
    This has been improved. It's still not lightning fast since 'show run all' is used to parse the config. In PR #88 we add a knob to control pyeapi's autorefresh, so the running config will only get pulled down 1x (max 2x if router bgp is created) and then all other commands will get run to configure the attributes of the bgp config.
* Using "params['connection']" in the modules means that the [DEFAULT] section configuration in pyeapi (eapi.conf) will not work (`26 <https://github.com/arista-eosplus/ansible-eos/issues/26>`_)
    This issue has been retested with the latest code and is no longer present.  Note: It is unclear at what point this was resolved.

Known Caveats
^^^^^^^^^^^^^

* domain_id parameter of eos_mlag_config module doesn't support '-' and dot (`90 <https://github.com/arista-eosplus/ansible-eos/issues/90>`_)


Notes
^^^^^

* This ansible-eos release should be partnered with min pyeapi version 0.5.0
* Ansible is releasing new networking modules into the core ansible code. These
  new modules will allow you to easily work with Jinja templates to implement
  your running-config.  They are also releasing eos_facts and eos_commands modules
  which will make it easier to get up and running. Please contact us at ansible-dev@arista.com
  for more information.
