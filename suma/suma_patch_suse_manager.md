# How to patch SUMA 3.x

- Stop the Spacewalk service:
`# spacewalk-service stop`

- Start the postgresql database (if on the same server):

`# rcpostgresql start`

- Apply the patches:

`# zypper patch`

- Upgrade the database schema:

`# spacewalk-schema-upgrade`

- Start the Spacewalk service:

`# spacewalk-service start`

Reference material: [Updating SUSE Manager](https://www.suse.com/documentation/suse-manager-3/book_suma_best_practices/data/update_suse_manager.html)
