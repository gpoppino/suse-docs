# How to configure an Admin and Branch server for SLEPOS 11 SP3

First of all, you can use my SLEPOS scripts located at
[suse-toolbox](https://github.com/gpoppino/suse-toolbox) (the ones starting with slepos) to
perform the tasks described here without typing all these commands and in a
easier way.

You should replace the parameters to the commands options with values you see
fit. In this example, I use:

- Country (c): _ar_
- Organization (o): _myorg_
- Organizational Unit (ou): _myou_
- Branch location (scLocation): _mybranch_
- Network address: 10.0.0.0

## Configure Admin server

- Init the Admin server:

```
posInitAdminserver
```

- Check the LDAP structure:

```
posAdmin --query
```

## Configure Branch server

Run `posAdmin` commands on the Admin server.

- Create Organization Unit:

```
posAdmin --base o=myorg,c=ar --add --organizationalUnit --ou myou --description 'My description'
```

- Create location container (branch server - with DHCP):
```
posAdmin \
--base ou=myou,o=myorg,c=ar --add --scLocation --cn mybranch \
--ipNetworkNumber 10.0.0.0 --ipNetmaskNumber 255.255.255.0 \
--scDhcpRange 10.0.0.2,10.0.0.152 \
--scDhcpFixedRange 10.0.0.153,10.0.0.254 \
--scDefaultGw 10.0.0.1 \
--scDynamicIp TRUE --scDhcpExtern FALSE \
--scWorkstationBaseName CR --scEnumerationMask 000 \
--userPassword suse
```

- Create location container (branch server - without DHCP - external DHCP):
If you have an external DHCP and do not use the command above (with DHCP), run this
command:
```
posAdmin \
--base ou=myou,o=myorg,c=ar --add --scLocation --cn mybranch \
--ipNetworkNumber 10.0.0.0 --ipNetmaskNumber 255.255.255.0 \
--scDefaultGw 10.0.0.1 \
--scDynamicIp TRUE --scDhcpExtern TRUE \
--scWorkstationBaseName CR --scEnumerationMask 000 \
--userPassword suse
```

- Add server container object:

```
posAdmin --base cn=mybranch,ou=myou,o=myorg,c=ar --add --scServerContainer --cn server
```

- Add branch server object:

```
posAdmin --base cn=server,cn=mybranch,ou=myou,o=myorg,c=ar --add --scBranchServer --cn bs
```

- Add network card information:

```
posAdmin --base cn=bs,cn=server,cn=mybranch,ou=myou,o=myorg,c=ar --add --scNetworkcard \
--scDevice eth0 --ipHostNumber 10.0.0.1
```

- Add DNS, DHCP (if needed), TFTP and posleases services:

Note: 10.0.0.1 is Branch Server's IP address.

```
posAdmin \
--base cn=bs,cn=server,cn=mybranch,ou=myou,o=myorg,c=ar \
--add --scService --cn dns --ipHostNumber 10.0.0.1 \
--scDnsName dns --scServiceName dns --scServiceStartScript named \
--scServiceStatus TRUE
posAdmin \
--base cn=bs,cn=server,cn=mybranch,ou=myou,o=myorg,c=ar \
--add --scService --cn dhcp --ipHostNumber 10.0.0.1 \
--scDnsName dhcp --scServiceName dhcp \
--scDhcpDynLeaseTime 300 --scDhcpFixedLeaseTime 14400 \
--scServiceStartScript dhcpd --scServiceStatus TRUE
posAdmin \
--base cn=bs,cn=server,cn=mybranch,ou=myou,o=myorg,c=ar \
--add --scService --cn tftp --ipHostNumber 10.0.0.1 \
--scDnsName tftp --scServiceName tftp \
--scServiceStartScript atftpd --scServiceStatus TRUE
posAdmin \
--base cn=bs,cn=server,cn=mybranch,ou=myou,o=myorg,c=ar \
--add --scService --cn posaswatch --ipHostNumber 10.0.0.1 \
--scDnsName posaswatch --scServiceName posASWatch \
--scServiceStartScript posASWatch --scServiceStatus TRUE
posAdmin \
--base cn=bs,cn=server,cn=mybranch,ou=myou,o=myorg,c=ar \
--add --scService --cn posleases --scDnsName posleases \
--ipHostNumber 10.0.0.1 --scServiceName posleases \
--scPosleasesTimeout 10 --scPosleasesChecktime 30 \
--scPosleasesMaxNotify 6 --scServiceStartScript posleases2ldap \
--scServiceStatus TRUE
```

### Add a cash register
You can add a cash register object to LDAP in _legacy mode_ or using _roles_.

 - Add a default cash register (in legacy mode):
```
posAdmin --base cn=global,o=myorg,c=ar --add --scCashRegister --cn cr-default \
--scCashRegisterName default \
--scPosImageDn cn=GraphicalImage,cn=default,cn=global,o=myorg,c=ar
```

 - Add ramdisk (optional - if no hard disk is available):
```
posAdmin --base cn=cr-default,cn=global,o=myorg,c=ar --add --scRamDisk --cn ram \
--scDevice /dev/ram0
```

 - Add hard disk to image:
```
posAdmin --base cn=cr-default,cn=global,o=myorg,c=ar --add --scHarddisk --cn sda \
--scDevice /dev/sda --scHdSize 16384
posAdmin --base cn=sda,cn=cr-default,cn=global,o=myorg,c=ar --add --scPartition \
--scPartNum 0 --scPartType 82 --scPartMount x --scPartSize 2048
posAdmin --base cn=sda,cn=cr-default,cn=global,o=myorg,c=ar --add --scPartition \
--scPartNum 1 --scPartType 83 --scPartMount '/' --scPartSize 14336
```

 - Add the jpos.xml configuration file for the POS
```
posAdmin \
--base cn=cr-default,cn=global,o=myorg,c=ar --add --scConfigFileSyncTemplate
--cn jpos.xml \
--scConfigFile /opt/ibm/javapos/jpos.xml --scMust TRUE --scBsize 1024 \
--scConfigFileLocalPath /srv/SLEPOS/config/jpos.xml
```

 - Add xorg.conf configuration POS
```
posAdmin \
--base cn=cr-default,cn=global,o=myorg,c=ar \
--add --scConfigFileSyncTemplate --cn xorg.conf \
--scConfigFile /etc/X11/xorg.conf --scMust TRUE  --scBsize 1024 \
    --scConfigFileLocalPath /srv/SLEPOS/config/xorg.conf.pos
```

- Add cash register using global roles (preferred method):
```
posAdmin --base cn=global,o=myorg,c=ar --add --scRole --cn myrole \
--scRoleName 'My Role 01' --scRoleDescription 'My role'
```

 - Add a cash register to role:
```
posAdmin --base cn=myrole,cn=global,o=myorg,c=ar --add --scCashRegister \
--cn cr-default --scCashRegisterName default \
--scPosImageDn cn=LatestImage,cn=default,cn=global,o=myorg,c=ar
```

 - Add harddisk to image:
```
posAdmin --base cn=cr-default,cn=myrole,cn=global,o=myorg,c=ar --add \
--scHarddisk --cn sda --scDevice /dev/sda --scHdSize 16384
posAdmin --base cn=sda,cn=cr-default,cn=myrole,cn=global,o=myorg,c=ar --add --scPartition \
--scPartNum 0 --scPartType 82 --scPartMount x --scPartSize 2048
posAdmin --base cn=sda,cn=cr-default,cn=myrole,cn=global,o=myorg,c=ar --add --scPartition \
--scPartNum 1 --scPartType 83 --scPartMount '/' --scPartSize 14336
```

 - Add the jpos.xml configuration file for the POS
```
posAdmin \
--base cn=myrole,cn=global,o=myorg,c=ar --add --scConfigFileSyncTemplate --cn jpos.xml \
--scConfigFile /opt/ibm/javapos/jpos.xml --scMust TRUE --scBsize 1024 \
--scConfigFileLocalPath /srv/SLEPOS/config/jpos.xml
```

- Enable roles for branch:
```
posAdmin --DN cn=mybranch,ou=myou,o=myorg,c=ar --modify --scLocation --scAllowRoles TRUE
posAdmin --DN cn=mybranch,ou=myou,o=myorg,c=ar --modify --scLocation --scAllowGlobalRoles TRUE
```

### Add POS Image object

 - With posAdmin
```
posAdmin \
--base cn=default,cn=global,o=myorg,c=ar --add --scPosImage --cn GraphicalImage \
--scImageName suse_pos --scPosImageVersion "1.0.0;active" \
--scDhcpOptionsRemote /boot/pxelinux.0 --scDhcpOptionsLocal LOCALBOOT \
--scImageFile suse_pos.i686 --scBsize 8192
```

 - With registerImanges (preferred method):
```
registerImages --ldap --gzip \
--kernel /var/lib/SLEPOS/system/images/GraphicalImage-3.1.5/initrd*.kernel \
--initrd /var/lib/SLEPOS/system/images/GraphicalImage-3.1.5/initrd*.splash.gz \
/var/lib/SLEPOS/system/images/GraphicalImage-3.1.5/GraphicalImage.i686-3.1.5
```

- Create delta for new image:

```
registerImages --delta GraphicalImage.i686-3.1.5 --ldap /var/lib/SLEPOS/system/images/GraphicalImage-3.1.6/GraphicalImage.i686-3.1.6
```


## Configure Branch Server - Manual installation

- Init the branch server:

```
posInitBranchServer
```

- Sync images to Branch Server:

```
possyncimages
```

- Start posASWatch service
```
insserv posASWatch
rcposASWatch start
```

- Configure openldap service to start at boot time
```
insserv ldap
rcldap start
```

## Setup branch server image for offline installation

- Generate OIF file for offline initialization:

```
posAdmin --base cn=mybranch,ou=myou,o=myorg,c=ar --generate
```

OIF file is generated under /usr/share/SLEPOS/OIF. Example:

 _/usr/share/SLEPOS/OIF/mybranch.myou.myorg.ar.tgz_

- Copy this file to branch image. Example:
```
cd /var/lib/SLEPOS/system/branchserver-4.0.0
mkdir -p root/usr/share/SLEPOS/OIF
cp /usr/share/SLEPOS/OIF/mybranch.myou.myorg.ar.tgz \
    /var/lib/SLEPOS/system/branchserver-1.0.0/root/usr/share/SLEPOS/OIF
```
- Generate the image with KIWI.
- At installation time, choose OFFLINE initialization from Wizard.

## HOWTOs

Note: Always run posAdmin commands on the admin server.

- How to remove an object:

```
posAdmin --remove --DN cn=cr-default,cn=global,o=myorg,c=ar
```

- How to modify an object:
```
posAdmin --DN cn=cr-default,cn=global,o=myorg,c=ar --modify \
--scCashRegister --scPosImageDn cn=GraphicalImage,cn=default,cn=global,o=myorg,c=ar
```

- How to clear a value (modify):
```
posAdmin --DN cn=GraphicalImage,cn=default,cn=global,o=myorg,c=ar --modify --scPosImage --scPosImageVersion ""
```

- How to change Branch Server's password:

```
posInitBranchServer --chpasswd
```

- How to create password for users in image definition (config.xml):

```
kiwi --createpassword
```

- Modify xorg.conf file (To update md5 hash)
```
posAdmin --DN cn=xorg.conf,cn=cr-default,cn=global,o=myorg,c=ar \
--modify --scConfigFileSyncTemplate --scConfigFile /etc/X11/xorg.conf \
--scMust TRUE  --scBsize 1024 --scConfigFileLocalPath /srv/SLEPOS/config/xorg.conf.pos
```

- How to create 32-bit images on a 64-bit machine
```
mkdir /var/lib/SLEPOS/system/graphical-default
cp -R /usr/share/kiwi/image/SLEPOS/graphical-3/* /var/lib/SLEPOS/system/graphical-default/
cd /var/lib/SLEPOS/system/

linux32 kiwi --prepare ./graphical-default --root ./chroot/graphical-default
linux32 kiwi --create ./chroot/graphical-default --destdir ./images/graphical-default
```
Also download the 32-bit repositories with the Subscription Management Tool (SMT) and update the _config.xml_ file to reference them.
