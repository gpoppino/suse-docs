# Procedure to extend a filesystem on LVM when a disk is expanded

## Scenario

A disk that is already in use by LVM is expanded in size and we want to use this new space for our existing LVM volumes that reside inside this disk (physical volume).

In this example, there is a XFS filesystem mounted on */data* that has a Logical Volume *mylv* that belongs to a Volume Group *myvg* that contains a Physical Volume */dev/sdb1*.

## Procedure

In SLES11 SP4 I have found that it is necessary to deactive the Volume Group (VG) before continuing with a *pvresize*. Taking this into account, the procedure is the following:

1. Stop processes that might be using the volumes mounted.
2. Umount the filesystem with: `umount /data`.
3. Deactivate the Volume Group: `vgchange -a n myvg`
4. Delete the partition: `parted /dev/sdb rm 1`
5. Create a new, larger partition: `parted /dev/sdb mkpart primary ext2 0% 100%`
6. Re-read partition table: `partprobe /dev/sdb`
7. Resize physical volume: `pvresize -v /dev/sdb1`
8. Check the new size of the physical volume: `pvs`
9. Re-activate the volume group: `vgchange -a y myvg`
10. Extend the logical volume: `lvextend -l 100%FREE /dev/myvg/mylv`
11. Mount the filesystem: `mount /data`
12. Resize the filesystem online: `xfs_growfs /dev/myvg/mylv`

## Alternative procedure

Another option is to create a new additional partition along the existing one. For example:

1. After expanding the disk, reboot or rescan disks with: `rescan-scsi-bus.sh`
2. Create a new partition: `parted /dev/sdb mkpart primary ext2 0% 100%`
3. Create a new physical volume: `pvcreate /dev/sdb2`
4. Extend the volume group: `vgextend myvg /dev/sdb2`
5. Extend the logical volume: `lvextend -l 100%FREE /dev/myvg/mylv`
6. Resize filesystem: `xfs_growfs /dev/myvg/mylv`

## Final notes

The filesystem used in this examples is XFS and its resizing utility is called *xfs_growfs*. This will be different for other filesystems. For instance, *ext2*, *ext3* and *ext4* use a command named *resize2fs*.
