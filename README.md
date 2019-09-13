# ansible-dynamic-inventory

A dynamic inventory for ansible based on the [LibreNMS API](https://docs.librenms.org/API/Devices/).

The script can be used directly by ansible as a dynamically generated inventory.

It creates the basic [ansible inventory structure](http://docs.ansible.com/ansible/devel/dev_guide/developing_inventory.html) based on the LibreNMS device information.

## Using the script with ansible

The inventory is used by ansible with `-i ./ansible-dynamic-inventory.py`:

```shell
$ ansible -i ./ansible-dynamic-inventory.py dsw* --list
  hosts (4):
    dsw1-site1.corp.example
    dsw2-site1.corp.example
    dsw1-site2.corp.example
    dsw2-site2.corp.example
```

## Calling the script directly

As per ansible requirements, the script takes either `--list` or `--host <hostname>` as options and returns either a full ansible inventory or only details for a specific host.

Get the details for a single host with `--host <hostname>`:

```shell
$ ./ansible-dynamic-inventory.py --host dsw1-site1.corp.example|json_pp
{
   "sysname" : "dsw1-site1",
   "location" : "site1",
   "type" : "network",
   "hardware" : "J8697A Switch 5406zl",
   "ansible_network_os" : "procurve"
}
```

Get the full ansible inventory with `--list`:

```shell
$ ./ansible-dynamic-inventory.py --list|json_pp
{
   "_meta" : {
      "hostvars" : {
         "dsw1-site1" : {
            "location" : "site1",
            "sysname" : "dsw1-site1",
            "type" : "network",
            "hardware" : "J8697A Switch 5406zl",
            "ansible_network_os" : "procurve"
         },
         "dsw2-site1" : {
            "location" : "site1",
            "sysname" : "dsw2-site1",
            "type" : "network",
            "hardware" : "J8697A Switch 5406zl",
            "ansible_network_os" : "procurve"
         },
         "asw1-site1" : {
            "ansible_network_os" : "procurve",
            "hardware" : "J9574A 3800-48G-PoE+-4SFP+ Switch",
            "type" : "network",
            "location" : "site1",
            "sysname" : "asw1-site1"
         },

[..]
```
