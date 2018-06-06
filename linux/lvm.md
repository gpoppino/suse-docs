# Procedure to extend a filesystem on LVM when a disk is expanded

## Scenario

A disk that is already in use by LVM is expanded in size and we want to use this new space for our existing LVM volumes that reside inside this disk (physical volume).

In this example, there is a XFS filesystem mounted on */data* that has a Logical Volume *mylv* that belongs to a Volume Group *myvg* that contains a Physical Volume */dev/sdb1*.

## Procedure

In SLES11 SP4 I have found that it is necessary to deactive the Volume Group (VG) before continuing with a *pvresize*. Taking this into account, the procedure is the following:

1. After expanding the disk, reboot or rescan disk with: `echo 1 > /sys/class/block/sdb/device/rescan`
2. Verify the disk has the correct new size: `parted /dev/sdb print`
3. Stop processes that might be using the volumes mounted.
4. Umount the filesystem with: `umount /data`.
5. Deactivate the Volume Group: `vgchange -a n myvg`
6. Delete the partition: `parted /dev/sdb rm 1`
7. Create a new, larger partition and set LVM flag on: `parted /dev/sdb mkpart primary ext2 0% 100%; parted /dev/sdb set 1 lvm on`
8. Re-read partition table: `partprobe /dev/sdb`
9. Resize physical volume: `pvresize -v /dev/sdb1`
10. Check the new size of the physical volume: `pvs`
11. Re-activate the volume group: `vgchange -a y myvg`
12. Extend the logical volume: `lvextend -l 100%FREE /dev/myvg/mylv`
13. Mount the filesystem: `mount /data`
14. Resize the filesystem online: `xfs_growfs /dev/myvg/mylv`

## Alternative procedure

Another option is to create a new additional partition along the existing one. For example:

1. After expanding the disk, reboot or rescan disk with: `echo 1 > /sys/class/block/sdb/device/rescan`
2. Verify the disk has the correct new size: `parted /dev/sdb print`
3. Create a new, larger partition and set LVM flag on: `parted /dev/sdb mkpart primary ext2 0% 100%; parted /dev/sdb set 2 lvm on`
4. Create a new physical volume: `pvcreate /dev/sdb2`
5. Extend the volume group: `vgextend myvg /dev/sdb2`
6. Extend the logical volume: `lvextend -l 100%FREE /dev/myvg/mylv`
7. Resize filesystem: `xfs_growfs /dev/myvg/mylv`

## Final notes

The filesystem used in this examples is XFS and its resizing utility is called *xfs_growfs*. This will be different for other filesystems. For instance, *ext2*, *ext3* and *ext4* use a command named *resize2fs*.
