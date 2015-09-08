# Ansible EOS Role

[![Documentation Status](https://readthedocs.org/projects/ansible-eos/badge/?version=master)](https://readthedocs.org/projects/ansible-eos/?badge=master)
[![Build Status](https://travis-ci.org/arista-eosplus/ansible-eos.svg)](https://travis-ci.org/arista-eosplus/ansible-eos)

## Overview

The Arista EOS role provides the foundation for working with Arista EOS nodes and Ansible.  The Arista EOS role for Ansible provides the ability to manage configuration resources in EOS.  The architecture of the roles makes inherent use of the Arista EOS command API using either a traditional Ansible SSH connection or by specifying connection: local and using eAPI to send and receive commands.  

The Ansible EOS role is freely provided to the open source community for automating Arista EOS node configurations using Ansible.  Support for the modules is provided on a best effort basis by the Arista EOS+ community.  Please file any bugs, questions or enhancement requests using [Github Issues](http://github.com/arista-eosplus/ansible-eos/issues)

[Read More about support] [support]

### Requirements

* Arista EOS 4.13.7M or later
* EOS Command API enabled (see [Enabling EOS Command API] [eapi])
* [Python Client for eAPI 0.3.0 or later] [pyeapi]
* Linux shell account (optional) (see [Preparing EOS for Ansible] [sshaccess])

## Documentation

All documentation for the
[Arista EOS](http://ansible-eos.readthedocs.org/en/master/index.html) role is
hosted using readthedocs.org. Here are some helpful links within those docs:

* [Quickstart] [quickstart]
* [Installation] [install]
* [Modules] [modules]


## License

Copyright (c) 2015, Arista Networks, Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

  Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.

  Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution.

  Neither the name of Arista Networks nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL ARISTA NETWORKS
BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

[pyeapi]: https://github.com/arista-eosplus/pyeapi
[eapi]: http://ansible-eos.readthedocs.org/en/master/quickstart.html#enabling-eos-command-api
[sshaccess]: http://ansible-eos.readthedocs.org/en/master/quickstart.html#option-a-connect-to-arista-node-over-ssh
[quickstart]: http://ansible-eos.readthedocs.org/en/master/quickstart.html
[install]: http://ansible-eos.readthedocs.org/en/master/install.html
[modules]: http://ansible-eos.readthedocs.org/en/master/_modules/list_of_All_modules.html
[support]: http://ansible-eos.readthedocs.org/en/master/support.html
