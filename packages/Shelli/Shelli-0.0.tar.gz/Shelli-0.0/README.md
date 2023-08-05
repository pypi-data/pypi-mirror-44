# Shelli
## Store remote execution batches in a human-readable YAML file.

Have you ever had to ssh into many machines and run the same command, and wait for it to finish before moving to the next machine? 
If this is something you find yourself doing often, you have probably found yourself using a custom script or something like fab to 
get the job done. This can be error-prone and difficult to generalize for different server groups.

Shelli attempts to create a human-readable way to intelligently define groups of machines to execute shell commands with, while 
allowing simple configuration for authentication, file/script transport, and more. The only configuration you need it a simple YAML file.

### Terminology

- Host: A server along with the parameters needed to login.
- HostGroup: A group of hosts, with optional defaults for authentication.
- Command: A command that gets ran by the shell on a Host.
- Transport: A file that is transported to the Host before command execution. It is removed after all commands finish running.
- Target: A list of Commands, Transports, and HostGroups to apply them to.

### Configuration

All configuration for Shelli is done with a single YAML file. The path for this YAML file is ~/.commander.yml.

There are three top-level hashes in the .commander.yml file:

- hosts
- hostgroups
- targets

#### Hosts

A YAML hash containing a YAML list. The values in here can be a string or a hash. If a string is used, it will create a host with default authentication parameters. If 
a hash is given, the name of key is the hostname, and the contents of the hash define authentication.

Default authentication is root login with a password.

Possible authentication options:

- auth\_method: < rsa-keypair | password >
- username: < login name >
- key: < path/to/ssh/key > # Only works with auth\_method is `rsa-keypair`
- password: < user password | keypair password > # Very insecure for obvious reasons. You will be prompted for credentials without this option.
- port: < ssh port number >

#### HostGroups

A YAML hash containing a YAML list. The values in here are hashes. The key of each hash defines the name of the HostGroup and can contain two hashes inside.

##### Options

- hosts: A YAML list of Hosts, as defined in the Hosts section.
- options: A hash of authentication options identical to those set for individual Hosts. This sets authentication for the entire group of hosts. The authentication options
from the Hosts section are merged into the authentication options for the HostGroup section, with the Hosts section taking priority.

#### Targets

A YAML hash containing a YAML list. The values in here are hashes. The key of each hash defines the name of the target and can contain three hashes inside.

##### Options

- commands: List of shell commands to run in order on the Hosts in the HostGroups hash that is supplied.
- transport: Optional list of files in the form <localpath>:<remotepath> that get copied to each Host before commands are run. They are removed afterwards.
- hostgroups: The HostGroups to apply the transports and commands on.

### Scenario

Say you've got two name servers named `ns1` and `ns2`, and vpn server named fiat. These names have to be resolvable by your OS's stub resolver.
Your DNS infrastructure is 30 years outdated and you have to login to your nameservers and run some scripts to update your zones. You also frequently have issues
with openvpn tunnels connecting to your cloud infra, and you think the best solution is to just restart openvpn each time an issue comes up. You could define the
following YAML file:

``` yaml
hosts:
  - ns1:
  - ns2:
  - fiat:
      auth_method: password
      username: root
hostgroups:
  - DNS:
      hosts:
        - ns1
        - ns2
      options:
        auth_method: rsa-keypair
        username: root
  - fiat:
      hosts:
        - fiat
targets:
  - temp_fix:
      hostgroups:
        - fiat
      commands:
        - systemctl restart openvpn
  - my_scripts:
      hostgroups:
        - DNS
      transport:
        - /home/kindlehl/my_script1:/tmp/my_script1
        - /home/kindlehl/my_script2:/tmp/my_script2
      commands:
        - ls
        - /tmp/my_script1
        - /tmp/my_script2
```

This creates three hosts: ns1, ns2, and fiat. Fiat uses password auth and needs to log in with root.

It also creates two HostGroups, one for fiat by itself, and one for your DNS servers.

It creates two targets, temp\_fix and my\_scripts. my\_scripts will transport two scripts to /tmp before running.

When commander is run on the temp\_fix target, it will login to fiat as root (while prompting you for your password),
and it will restart the openvpn service.

When commander runs the my\_scripts target, it will login to the DNS servers, copy /home/kindlehl/my\_script{1,2} to 
ns1:/tmp/my\_script{1,2} and ns2:/tmp/my\_script{1,2}. It will then run `ls`, `/tmp/my\_script1` and `/tmp/my\_script2`, then delete the scripts.

Say you create a new nameserver, ns3, and you want to add it to your script. Just go right on and add `ns3` to your Hosts and your DNS HostGroup.
