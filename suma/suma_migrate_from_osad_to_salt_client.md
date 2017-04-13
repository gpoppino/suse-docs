# How to migrate a client from OSAD to a Salt minion

- Remove the system from SUMA using the web UI.
- Disable OSAD in the target system: 

```
 # insserv -r osad
 # rcosad stop
```

- Remove spacewalk repos from the target system:

```
# rm -f /usr/lib/zypp/plugins/services/spacewalk
# zypper rs X
```

- Replace X with the spacewalk service number.
- [Register](https://gpoppino.github.io/suse-docs/suma/suma_bootstrap_salt_client_with_script.html) the salt client.
