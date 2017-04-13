# Suggested partitioning for SUMA 3.0

mount point | size | file system | description
----------- | ---- | ----------- | -----------
/var/spacewalk | 100GB | XFS | Channels - LVM
/var/lib/pgsql | 50GB | XFS | Postgresql database - LVM
/srv/www/htdocs/pub | 10GB | XFS | OPTIONAL - LVM
/ | 30GB | Btrfs | On top of LVM

[Reference](https://www.suse.com/documentation/suse-manager-3/book_suma3_quickstart_3/data/sect1_3_chapter_book_suma3_quickstart_3.html)
