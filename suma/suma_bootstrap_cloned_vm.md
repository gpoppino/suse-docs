# How to bootstrap a cloned VM

Reference URL is [Register
clones](https://wiki.microfocus.com/index.php/SUSE_Manager/Register_Clones)

On the cloned VM, run the following:

SLES11:

```
# rm /var/lib/dbus/machine-id
# dbus-uuidgen --ensure
```

SLES12:

```
# rm /etc/machine-id
# rm /var/lib/dbus/machine-id
# dbus-uuidgen --ensure
# systemd-machine-id-setup
```

SLES12:

`# rm  -f /etc/zypp/credentials.d/{SCCcredentials,NCCcredentials}`

SLES11:

`# suse_register -E`

If the system was previously registered:

SLES11/12:

```
# zypper remove salt

# rm /etc/salt/minion_id
# mv /etc/salt /etc/salt.bkp
```

Bootstrap from the Web UI the salt client.

