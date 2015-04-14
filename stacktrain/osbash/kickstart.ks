# Kickstat file manually created by dguitarbite.
# version

# Installation
install
#graphical
text

# Keyboard layouts
keyboard 'us'
# Reboot after installation
reboot

# Root password
rootpw osbash
# System timezone
timezone Europe/Berlin
# Use network installation
url --url http://ftp.astral.ro/distros/centos/7/os/x86_64/
repo --name=updates --baseurl=http://ftp.astral.ro/distros/centos/7/updates/x86_64/

# System language
lang en_US

# Firewall configuration
firewall --disabled

# SELinux configuration
selinux --disabled

# Network information
network  --bootproto=dhcp --device=eth0

# System authorization information
auth  --useshadow  --passalgo=sha512

# Do not configure the X Window System
skipx

# System bootloader configuration
bootloader --location=mbr
# Clear the Master Boot Record
zerombr
# Partition clearing information
clearpart --all
# Disk partitioning information
part / --fstype="ext4" --grow --size=8000

bootloader --location=mbr --append="rhgb quiet"

# Configure the user
user --name=osbash --password=osbash

#
# Packages TODO
#
%packages --ignoremissing
openssh-clients
openssh-server
yum
acpid
which
wget
make
gcc
screen

%end

%post --log=/root/post_install.log
exec < /dev/tty3 > /dev/tty3
chvt 3
echo
echo "################################"
echo "# Running Post Configuration   #"
echo "################################"
cd /tmp
/usr/bin/yum -y update  >> /root/post_update.log
/usr/bin/yum -y upgrade >> /root/post_upgrade.log
touch /home/osbash/test1
echo "dguitarbite: Rock n' Roll!" > /home/osbash/test

%end
