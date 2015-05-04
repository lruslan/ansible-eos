##############
Meta Arguments
##############

Most EOS modules suport additional arguments (meta arguments) in additionl to
the arguments available for configuring the resource.  The meta arguments
provide additional connection and troubleshooting arguments for executing tasks
in Ansible.  

Not all modules support all meta arguments.  Please review the individual
module documentation for applicability.

*************************
Troubleshooting Arguments
*************************

This section provies an overview of the arguments available for trobleshooting
tasks with EOS modules.

    * debug (booleans) - Enables additional output from the module 
    * logging (booleans) - Enables or disables logging details to syslog


********************
Connection Arguments
********************

The connection arguments provide a set of arguments that override the values
from eapi.conf or eliminate the need for eapi.conf all together.

    * config (string) - overrides the default path to the eapi.conf file
    * username (string) - specifies the eAPI username used to authenticate
    * password (string) - specifies the eAPI password used to authenticate
    * host (string) - specifies the host address or FQDN for the connection
    * port (string or integer) - specifies the port to use when connecting
    * connection (string) - specifies the name of the connection profile to use
    * transport (string) - configures the transport to use.  Valid transport
      options inlucde "http", "https", "socket", "http_local".


***************
State Arguments
***************

The state arguments provide state configuration for modules that are identified
as stateful.

    * state (string) - configures the resource state.  Valid values include
      "present", "absent".  Note that some modules can additional states



