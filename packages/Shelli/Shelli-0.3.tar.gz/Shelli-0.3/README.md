# Shelli
## Store remote execution batches in a human-readable YAML file.

Have you ever had to ssh into many machines and run the same command, and wait for it to finish before moving to the
next machine?  If this is something you find yourself doing often, you have probably found yourself using a custom
script or something like fab to get the job done. This can be error-prone and difficult to generalize for different
server groups.

Shelli attempts to create a human-readable way to intelligently define groups of machines to execute shell commands
with, while allowing simple configuration for authentication, file/script transport, and more. The only configuration
you need it a simple YAML file.

Example yaml:

``` yaml 
hosts:
  - ns1.mydomain.org
  - ns2.mydomain.org
  - fiat.mydomain.org:
      auth_method: key
      key: /root/.ssh/id_rsa-fiat 
hostgroups:
  - dns:
      hosts:
        - ns1.mydomain.org
        - ns2.mydomain.org 
      options: 
        auth_method: key
        username: bind 
        key: /root/.ssh/id_rsa_dns
  - fiat: 
      hosts:
        - fiat
targets:
  - temp_fix: 
      hostgroups:
        - fiat 
      commands:
        - systemctl restart openvpn
  - run_scripts:
      hostgroups:
        - dns 
      transports:
        - /home/kindlehl/my_script1:/tmp/my_script1
        - /home/kindlehl/my_script2:/tmp/my_script2 
      commands:
        - /tmp/my_script1
        - /tmp/my_script2 
```
### Scenario

Say you've got two nameservers named `ns1.mydomain.org` and `ns2.mydomain.org`, and vpn server named `fiat`. These
names have to be resolvable by your OS's stub resolver, so you don't need to use the FQDN of the server. You have to
login to your nameservers and run some scripts to update your zones. You should probably automate the updates, but you
decide to use Shelli instead.  You also frequently have issues with openvpn tunnels connecting to your cloud infra, and
you think the best solution is to just restart openvpn each time an issue comes up. You could define the above YAML
file. 

This creates three hosts: ns1.mydomain.org, ns2.mydomain.org, and fiat. Fiat uses password auth and needs to log in with root.

It also creates two hostgroups, one for fiat by itself, and one for your DNS servers. Even if you only want to run your
commands on one host, you still need to define the hostgroup.

This YAML also creates two targets, temp\_fix and run\_scripts. run\_scripts will transport two scripts to /tmp before running.
them. It will only prompt you once for credentials since the hostgroup shares authentication parameters. If one of the
nameservers required login as a different user, then you'd be prompted twice.

When commander is run on the temp\_fix target, it will login to fiat as root (while prompting you for your password),
and it will restart the openvpn service.

When commander runs the my\_scripts target, it will login to the DNS servers, copy `/home/kindlehl/my\_script{1,2}` to
`ns1.mydomain.org:/tmp/my_script{1,2}` and `ns2.mydomain.org:/tmp/my\_script{1,2}`. It will then run `/tmp/my_script1` and `/tmp/my_script2`,
on each host, then delete the scripts.

Say you create a new nameserver, ns3, and you want to run the same commands as the others. Just go right on and add 
`ns3` to your hosts and your dns hostgroup.

Currently, commands are run on hosts in serial. Options for parallelism are in the future.

### Configuration

All configuration for Shelli is done with a single YAML file. The path for the default YAML file is ~/.shelli.yml.  You
can tell Shelli to use a custom config with the -c flag.

There are three top-level hashes in the YAML file:

- hosts
- hostgroups
- targets

### Terminology

- host: A server along with the parameters needed to login.
- hostgroup: A group of hosts, with optional defaults for authentication.
- command: A command that gets ran by the shell on a host.
- transport: A file that is transported to the host before command execution. It is removed after all commands finish
  running.
- target: A list of commands, transports, and hostgroups to apply them to.

#### Hosts

A YAML hash containing a YAML list. The values in here can be a string or a hash. If a string is used, it will create a
host with default authentication parameters. If a hash is given, the name of key is the hostname, and the contents of
the hash define authentication options.  

Default authentication is root login with a password over port 22.

Possible authentication options:

- auth\_method: < key | password >
- username: < login name >
- key: < path/to/ssh/key > # Required if `auth_method` is 'key'.
- password: < user password | keypair password > # Very insecure for obvious reasons. You will be prompted for
  credentials without this option.
- port: < ssh port number >

#### Hostgroups

A YAML hash containing a YAML list. The values in here are hashes. The key of each hash defines the name of the
hostgroup and can contain two hashes inside.

##### Options

- hosts: A YAML list of hosts, as defined in the hosts section.
- options: A hash of authentication options identical to those set for individual hosts. This sets the default
  authentication for the entire group of hosts. Any hosts in the hostgroups that define their own authentication will
  override this group-wide default.

#### Targets

A YAML hash containing a YAML list. The values in here are hashes. The key of each hash defines the name of the target
and can contains a list of commands and hostgroups. Optionally, transports can be defined.

##### Options

- hostgroups: The hostgroups to apply the transports and commands on.
- commands: List of shell commands to run in order on the hosts in the hostgroups hash that is supplied.
- transport: Optional list of files in the form <localpath>:<remotepath> that get copied to each host before commands
  are run.  They are removed afterwards.

Issues
------

Feel free to submit issues and enhancement requests.

Contributing
------------

 1. **Fork** the repo on GitHub
 2. **Clone** the project to your own machine
 3. **Environment** Create virtualenv and install the packages in requirements.txt
 3. **Lint** Run `pylint shelli` from the base of the project. Make sure the score is 10/10.
 3. **Test** Run `python -m unittest discover -s test -v` from the base of the project. Add your own tests and
		make sure your changes don't break other tests.
 3. **Commit** changes to your own branch
 4. **Push** your work back up to your fork
 5. Submit a **Pull request** so that we can review your changes

NOTE: Be sure to merge the latest from "upstream" before making a pull request!
