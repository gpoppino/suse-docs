# How to register a salt client with a bootstrap script

- Create a bootstrap script for salt:

`# mgr-bootstrap --salt`

- List available repos for bootstrapping systems:

`# mgr-create-bootstrap-repo -l`

- Create the necessary bootstrap repos. For example:

```
# mgr-create-bootstrap-repo -c SLE-11-SP3-x86_64
# mgr-create-bootstrap-repo -c SLE-12-SP2-x86_64
# mgr-create-bootstrap-repo -c SLE-11-SP4-x86_64
```

- Edit the needed bootstrap script to add the activation key:

```
# cd /srv/www/htdocs/pub/bootstrap
# cp bootstrap.sh bootstrap-salt-sles11sp3.sh
# vi bootstrap-salt-sles11sp3.sh
```

- Edit the line _ACTIVATION_KEYS_ and add the key, for example:

`ACTIVATION_KEYS=1-SLES11SP3-x86_64` 

or

```
# MY_ACTIVATION_KEY=1-SLES11SP3-x86_64
# sed -i.old 's/\(ACTIVATION_KEYS=\)/\1${MY_ACTIVATION_KEY}/g' bootstrap-salt-sles11sp3.sh
```

- Register the system executing the following command from the SUMA3 server:

`# cat bootstrap-salt-sles11sp3.sh | ssh root@sles11sp3.suse.ar /bin/bash`

Where sles11sp3.suse.ar is the target system.

- On Board the client from _SUMA -> Salt -> Onboarding_ in SUMA's web UI.
