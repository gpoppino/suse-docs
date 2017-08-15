# How to do basic queries with the tool 'psql'

- Connect to the SUMA DB
 ```
  # su - postgres
  # psql -d susemanager
 ```

- List the tables:

`susemanager=# \dt`

- List servers: 

`susemanager=# select * from rhnserver ;`

- Quit:

`susemanager=# \q`

