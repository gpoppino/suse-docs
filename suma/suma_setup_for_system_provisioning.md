# How to setup SUMA 3.x for system provisioning

This examples uses SLES12 SP2 as the system to be provisioned by SUMA.

- Sync a distro from a ISO file into a destination directory

```
# mount -o loop SLES12-SP2.iso /mnt
# mkdir -p /var/distros/sles12-sp2-x86_64
# rsync -av /mnt/ /var/distros/sles12-sp2-x86_64
```
Note: create a LVM volume for mount point /var/distros

- In SUMA web UI, go to _Systems -> Autoinstallation -> Distributions_ and click
  on _Create a Distribution_.
    - Use _/var/distros/sles12-sp2-x86_64_ for _Path_ and the _SLES12-SP2-Pool_
      for _Pool_.

- Upload autoyast.xml profile.

- Setup an external DHCP with "next-server" pointing to SUMA IP address and the
  _file_ option to _pxelinux.0_ (TFTP is already setup in SUMA).

  - Optional. Libvirt DHCP setup: Add the following line to the network's config
    inside the `<dhcp>` tags (`virsh net-edit $network`):

    `<bootp file='pxelinux.0' server='192.168.100.3'/>`

    Where _192.168.100.3_ is SUMA's server IP address.

- Boot target system to test using PXE.

