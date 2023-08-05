MonCon - Monyog Control
-----------------------

A simple wrapper for the Monyog REST API using Python3.4+ and The Requests module.

You can store paramters such as host, port, user, and password in the "[monyog]" section of:
 * ~/.my.cnf
 * /etc/my.cnf
 * (more to come)

### Install:
NOT YET AVAILABLE!

```pip install moncon```

###  Example

Disable alerts for server named db1:

``` $ moncon --action=alerts --value disable --server=db1```

Note, no password or user is supplied. Appending '--dry-run' we will see the details read from a config file:
```
$ ./scripts/moncon --action=alerts --value disable --server=db1 --dry-run
{'action': 'alerts',
 'dry_run': True,
 'host': '127.0.0.1',
 'object': 'MONyogAPI',
 'password': 'password123_from_file',
 'port': '5555',
 'target': '_server=db1',
 'url': 'http://127.0.0.1:5555/?_object=MONyogAPI&_action=alerts&_value=disable&_user=admin_user_in_file&_password=password123_from_file&_server=db1',
 'user': 'admin_user_in_file',
 'value': 'disable'}
```

However we can override some details like the password if needed:

```
$ ./scripts/moncon --action=alerts --value disable --server=db1 --password SuperSecret --dry-run
{'action': 'alerts',
 'dry_run': True,
 'host': '127.0.0.1',
 'object': 'MONyogAPI',
 'password': 'SuperSecret',
 'port': '5555',
 'target': '_server=db1',
 'url': 'http://127.0.0.1:5555/?_object=MONyogAPI&_action=alerts&_value=disable&_user=admin_user_in_file&_password=SuperSecret&_server=db1',
 'user': 'admin_user_in_file',
 'value': 'disable'}
```
