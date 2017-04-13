# How to register a SUMA 3.x server with the SCC

- Register SLES12:

`# SUSEConnect -r [YourActivationCode] -e <YourEmailAddress>`

- Register SUMA3:

`# SUSEConnect -p SUSE-Manager-Server/3.0/x86_64 -r [SUSE_MANAGER_CODE]`

- Check registration status:

`# SUSEConnect -s`

- Install SUMA3:

`# zypper in -t pattern suma_server`

