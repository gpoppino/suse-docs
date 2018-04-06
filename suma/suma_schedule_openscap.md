# How to schedule OpenSCAP reports on SUMA 3.1

- Requisites
  - On the client:
    - Install packages spacewalk-oscap y openscap-content
    - Upgrade to latest salt packages

There are three alternatives to schedule the reports:

1. On the Web UI

- Select the system and go to _Audit -> Schedule_
- In _Command-line Arguments_ enter _--profile Default_
- In _Path to XCCDF document_ enter `/usr/share/openscap/scap-xccdf.xml` or another template.
- Click on _Schedule_
- In the general menu, go to _Audit -> OpenSCAP -> All Scans_
- Click on the report

2. On the command line:

- Execute the script [suma_schedule_openscap.py](scripts/suma_schedule_openscap.py) to schedule a scan on all the systems.

3. On the command line on the client:

- With OVAL format file:

`# oscap oval eval --report myreport.html --results myresults.xml /usr/share/openscap/scap-oval.xml`

- With XCCDF format file:

`# oscap xccdf eval --profile Default /usr/share/openscap/scap-xccdf.xml`

