#!/usr/bin/env python3
# VPN Domain Exceptions (VDE)

import dns.resolver, os, netifaces

store_file = '/var/cache/undo-vde.sh'


# Allows IP through firewall when the output chain denies by default.
iptables_fmt = 'iptables -A OUTPUT -d {ip} -j ACCEPT'
# Adds special route rules to prevent packets to certain IPs being directed through VPN
ip_route_fmt = 'ip route add {ip} via {gateway}'

# These two do the same things as before, but instead of adding the rules, they delete them.
undo_ip_route_fmt = 'ip route del {ip} via {gateway}'
undo_iptables_fmt = 'iptables -D OUTPUT -d {ip} -j ACCEPT'

# A place to store the list of commands we build to execute
cmdlist = set()
undo_cmdlist = set()

# Get our default gateway...
default_gateway = netifaces.gateways()['default'][2][0]

# Execute our previously built old rules
if os.path.exists(store_file):
    print('Undoing old rules...')
    os.system(open(store_file).read())

print('Now building new rules!')

# Iterate through list of domains
for domain in open('/etc/vde.conf', 'r').readlines():
    domain = domain.strip()
    print('Querying "%s"...' % domain)
    # Query for IP of each domain
    try:
        answer=dns.resolver.query(domain, "A")
    except dns.resolver.NXDOMAIN:
        print('Error for domain "%s". Ignoring!' % domain)
        continue
    # If iterate through IPs we were given for that domain
    for ip in answer:
        
        ip = str(ip)
        print('Processing IP "%s"...' % ip)
        # Add iptables and ip route exceptions for IP
        cmdlist.add(iptables_fmt.format(ip=ip))
        cmdlist.add(ip_route_fmt.format(ip=ip, gateway=default_gateway))
        
        # Generate reverse-commands to convienently undo these actions when needed
        undo_cmdlist.add(undo_ip_route_fmt.format(ip=ip, gateway=default_gateway))
        undo_cmdlist.add(undo_iptables_fmt.format(ip=ip))

# Format our command list as one string and dump it all into a shell at once
cmdstring = '\n'.join(cmdlist)
print('Now executing:\n' + cmdstring)
os.system(cmdstring)

# Save the undo commands in our store file for later!
with open(store_file, 'w') as f:
    for line in undo_cmdlist:
        f.write(line + '\n')
    
