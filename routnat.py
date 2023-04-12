import os
import ipaddress

hostname = input("Vvedi hostname: ")
networks = input('Vvedi 4 podseti sleva napravo 4erez probel(x.x.x.0 x.x.x.0...)')
l_or_r = input("Eto leviy ili praviy router?(1 or 2): ")

ip1 = networks.split()[0]
ip2 = networks.split()[1]
ip3 = networks.split()[2]
ip4 = networks.split()[3]

def left():
	ip_rt = str(ipaddress.IPv4Address(ip2) + 1)
	with open('/etc/network/interfaces', 'a') as f:
		f.write(f'''
up ip route add {ip3 + '/24'} via {ip_rt}
up ip route add {ip4 + '/24'} via {ip_rt}
''')

def right():
	ip_rt = str(ipaddress.IPv4Address(ip3) + 1)
	with open('/etc/network/interfaces', 'a') as f:
		f.write(f'''
up ip route add {ip2 + '/24'} via {ip_rt}
up ip route add {ip1 + '/24'} via {ip_rt}
''')

if l_or_r == "1": left(); ostalnoe()
elif l_or_r == "2": right(); ostalnoe()
else: print('Davai zanovo, nepravilno vibran router')

def ostalnoe():
	file2 = open('/etc/hostname','w')
	file2.write(hostname)
	file2.close()
	print("hostname ystanovlen")

	nat = input("nastroit nat?(y or n)")

	if nat == "y":
		os.system("apt install iptables -y")
		os.system("iptables -t nat -A POSTROUTING -o enp0s3 -j MASQUERADE")
		os.system("DEBIAN_FRONTEND=noninteractive apt install iptables-persistent")
		os.system("systemctl restart netfilter-persistent")
		print("nat nastoren")
	else: print("ny lan")

	file3 = open('/etc/sysctl.conf','a')
	file3.write("net.ipv4.ip_forward=1")
	file3.close()
	os.system("sysctl -p")

	reb = input("reboot?(y)")
	if reb =="y": os.system("reboot")
	else: print("Ne zabyd rebootnyt")
