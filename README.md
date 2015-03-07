Stacktrain
----------

<a href='https://travis-ci.org/dguitarbite/stacktrain'><img
src='https://secure.travis-ci.org/dguitarbite/stacktrain.png?branch=master'></a>

Stack train is the python implementation for osbash. Stack train will only
replace the host side scripts from bash to python.


About
-----

OpenStack training labs are the tools useful for trainers and trainees. These
scripts will automate deployment of OpenStack on VirtualBox and KVM/Qemu.

Refer this etherpad https://etherpad.openstack.org/p/stacktrain


What this script does
-----------------------
Deploys OpenStack multi-node cluster on KVM hypervisor.


Pre-requisite:
---------------
* Install KVM/Qemu
* Install python libvirt modules
        pip2 install libvirt-python
* Install Fabric (required for ssh)
          pip2 install fabric



How to run the cluster
-----------------------

          ./stacktrain.py


Note
----

This repository is `Proof of Concept` and should not be used for serious
buisness. Once the POC's are finalized, they will be pushed to the training
guides official repository. Please look out for that repository for more stable
and working copy of osbash/stacktrain.

Scope
-----

I am creating POC on KVM/Qemu with Libvirt for automating openstack training
labs tools. This repository should eventually do the following:

1. Automate creating of KVM/Qemu machines.
2. Take step by step snapshots of the guest VM
3. Use libvirt libraries and also oslo if possible.
4. Keep the dependencies as less as possible.
5. Manage the lifecycle of the VMs.

This may look like scripts for managing the KVM hypervisor, well it may end up
being something like that but the goal is not to do that, if you want something
like that you may look at OpenStack compute!

This is also not intended to be the replacement of Vagrant. The reason for
implementing these scripts is very simple:

1. Keep as much code in python as possible to stick to OpenStack's ways of
   things.
2. Keep the dependencies as less as possible! This is for making it very simple
   and convinent for the end-users to use these tools.

Vagrant is really good for what it does but comes with a bit of dependences and
is not as cross-platform as we require it to be for what we want to do. If you
are looking for something similar to this, then I would suggest using Vagrant,
it has amazing community around it and supports multiple hypervisors.
