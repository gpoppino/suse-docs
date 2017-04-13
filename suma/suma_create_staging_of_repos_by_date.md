# How to clone a repo by date and from the Web UI

From the CLI:

- Install _spacekwalk-utils_ package:

`# zypper in spacewalk-utils`

- Create a config file like the one listed at the end of this document.

- In any case, run `spacewalk-clone-by-date --sample-config` to obtain an example.

- Adjust the file and clone by date:

`# spacewalk-clone-by-date -c clone-updates-sles11-sp4.txt`

From the web UI:

- Go to _Channels -> Manage Software Channel -> Clone Channel_ and follow the workflow.

Finally, add the new channels to an Activation Key.

The _clone-updates-sles11-sp4.txt_ example file, clones up to date 2017-02-01
(yyyy-mm-dd):

```
{
 "username":"admin",
 "password":"mypassword",
 "assumeyes":true,
 "to_date": "2017-02-01",
 "skip_depsolve":false,
 "security_only":false,
 "use_update_date":false,
 "no_errata_sync":false,
 "dry_run":false,
 "channels":[
             {
                "sles11-sp4-pool-x86_64": {
                    "label": "sles11-sp4-pool-x86_64",
                    "existing-parent-do-not-modify": true
                },
                "sles11-sp4-updates-x86_64": {
                    "label": "my-sles11-sp4-update-x86_64-clone",
                    "name": "My Clone's SLES11 SP4 Updates",
                    "summary": "This is my channel's summary",
                    "description": "This is my channel's description"
                }
            }
           ]
}
```

