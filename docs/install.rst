############
Installation
############

The installation of Ansible is straightforward and simple. This section
provides an overview of the installation of Ansible on a host system as well
as how to configure an Arista EOS node to work with the Ansible framework.


.. _install-ansible-label:

*********************
Host (Control) System
*********************
Installing Ansible on a host (or control) system is a relatively simple
process. Ansible supports all major Linux distributions running Python 2.6 or
later as a control system. Ansible is integrated with package managers for
each system type to ease the installation. Ansible can also be run directly
from a Git checkout.

A quick reference summary of the various installation method is found below.
For authoritative details regarding the installation of Ansible on a
control system, see Ansible's `installation documentation <http://docs.ansible.com/intro_installation.html>`_.

Installing via YUM
==================
Ansible is provided via standard RPM installations from EPEL 6 and Fedora repositories.  Simply run Yum with appropriate permissions to install the latest version of Ansible.

.. code-block:: console

  $ sudo yum install ansible


Installing via Apt (Ubuntu)
===========================
In order to install directly from Apt, the Ansible PPA will need to be added
to Apt’s sources. Ansible binaries are installed from this PPA.  Once the PPA
has been added to the Apt sources list execute the following commands to
install Ansible.

.. code-block:: console

  sudo apt-get install software-properties-common
  sudo apt-add-repository ppa:ansible/ansible
  sudo apt-get update
  sudo apt-get install ansible

Installing via PIP
==================
Ansible can be installed using Python PIP. To install Ansible with PIP,
simply enter the following command from a shell prompt.

.. code-block:: console

  sudo pip install ansible


.. _install-role-label:

****************************
Install the Ansible EOS Role
****************************
There are two methods that can be used to install the ansible-eos modules on
your system; (1) Ansible Galaxy, (2) Github - from source.  The first method
is the easiest and makes using the modules a little easier, but the drawback
is that you are dependent upon releases being posted to Ansible Galaxy. The second
method is good if you plan on working with the actual module code from source
or wish to closely follow all changes in development.

Install Using Ansible Galaxy
============================
From your Ansible Control Host, type:

.. code-block:: console

  ansible-galaxy install arista.eos


Installing from GitHub (for active development)
===============================================
Arista EOS+ Consulting Services maintains a set of modules that provide
native integration with Ansible. All of the modules are available via
`Github <http://github.com/aristanetworks/ansible-eos>`_.  This section will
provide an overview of the available EOS modules.

To get started, download the latest Arista EOS modules from Github using the
clone command. From a terminal on the Ansible control system issue the
following command:

.. code-block:: console

  git clone https://github.com/aristanetworks/ansible-eos.git

The command above will create a new directory call ‘ansible-eos’ and clone the
entire repository. Currently, the ansible-eos folder contains the “develop”
branch which provides the latest code. Since the “develop” branch is still
a work in progress, it might be necessary to switch to a released version of
the EOS modules. In order to switch to a specific release version, change
directories to the ansible-eos directory and enter the following command.

.. code-block:: console

  git tag
  git checkout tags/<tag name>

The first command above “git tag” provides a list of all available tags.
Each release has a corresponding tag that denotes the released code.
To switch to a specific release simply use the name of the tag in the
second command as the <tag name>.

For instance, to use the v1.0.0 release, enter the command

.. code-block:: console

  git checkout tags/v1.0.0

At any point in time switching to a different release is as easy as changing
to the ansible-eos directory and re-issuing the “git checkout” command.

You will need to make Ansible aware of this new role if you want to use the
included modules in your plays. You have a few options:


**Option 1:** Create Symlink (preferred)

We will create a symlink in ``/etc/ansible/roles/`` to make Ansible aware of the
``ansible-eos`` role.  Notice that the symlink name is ``arista.eos``. This is
because the Ansible Galaxy role is named ``arista.eos``:

.. code-block:: console

  # create soft symlink
  cd /etc/ansible/roles
  sudo ln -s /path/to/where/your/git/clone/is/ansible-eos arista.eos

Then you can use the role in your play as:

.. code-block:: yaml

  #my-playbook.yml
  ---
  - hosts: eos_switches
    gather_facts: no

    roles:
      - arista.eos

    tasks:
      - name: configures the hostname on tor1
        eos_vlan:
          vlanid=150


**Option 2:** Edit ansible.cfg roles_path

Here, you can edit ``/etc/ansible/ansible.cfg`` to make Ansible look for the
``ansible-eos`` directory:

.. code-block:: console

  # open the config file in an editor
  sudo vi /etc/ansible/ansible.cfg

  # if roles_path exists add a colon and the new path
  # if the variable doesn't exist, create it under [defaults] section
  [defaults]
  roles_path=/path/to/where/your/git/clone/is/ansible-eos

Then you can use the role in your play as:

.. code-block:: yaml

  #my-playbook.yml
  ---
  - hosts: eos_switches
    gather_facts: no

    roles:
      - ansible-eos

    tasks:
      - name: configures the hostname on tor1
        eos_vlan:
          vlanid=150
