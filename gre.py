import os
import ipaddress

local_ip = input("IP etoi mashini: ")
endpoint_ip = input("IP kone4noi mashini: ")
gre_ip = input("IP dlya GRE: ")
gre_ip2 = str(ipaddress.IPv4Address(gre_ip) + 1)

with open("/etc/network/interfaces", 'a') as f:
    f.write(f'''
\n\nauto gre30
iface gre30 inet tunnel
address {gre_ip}
netmask 255.255.255.252
mode gre
local {local_ip}
endpoint {endpoint_ip}
ttl 255
''')

os.system("apt install libreswan sshpass -y")

with open("/etc/ipsec.conf", "a") as f:
    f.write(f'''
\n\nconn "vpn"
auto=start
type=tunnel
authby=secret
ike=3des-sha1;dh14
esp=aes-sha2
left={local_ip}
right={endpoint_ip}
leftprotoport=gre
rightprotoport=gre
''')

with open("/etc/ipsec.secrets", "a") as f:
    f.write(f'{local_ip} {endpoint_ip} : PSK "SLOVOPAROL"')

#СОЗДАНИЕ ФАЙЛА ДЛЯ ВТОРОЙ МАШИНЫ    
   
with open('scr-main/agent_gre', 'w+') as f:
    f.write(f"""
import os

with open("/etc/network/interfaces", 'a') as f:
    f.write(f'''


auto gre30
iface gre30 inet tunnel
address {gre_ip2}
netmask 255.255.255.252
mode gre
local {endpoint_ip}
endpoint {local_ip}
ttl 255
''')

os.system("apt install libreswan sshpass -y")

with open("/etc/ipsec.conf", "a") as f:
    f.write(f'''

            
conn "vpn"
auto=start
type=tunnel
authby=secret
ike=3des-sha1;dh14
esp=aes-sha2
left={endpoint_ip}
right={local_ip}
leftprotoport=gre
rightprotoport=gre
''')

with open("/etc/ipsec.secrets", "a") as f:
    f.write(f'{endpoint_ip} {local_ip} : PSK "SLOVOPAROL"')""")
    
os.system(f'sshpass -proot scp scr-main/agent_gre root@{endpoint_ip}:/etc')
os.system(f'sshpass -proot ssh root@{endpoint_ip} python3 /etc/agent_gre')
