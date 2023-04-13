import os
import ipaddress

oc = input('Настраиваем debian или centos?(1/2): ')
networks = input('Введи все 4 подсети слева направо через пробел по образцу(x.x.x.0 x.x.x.0...)')
l_or_r = input("Это левый или правый роутер?(1/2): ")

ip1 = networks.split()[0]
ip2 = networks.split()[1]
ip3 = networks.split()[2]
ip4 = networks.split()[3]

# ФУНКЦИИ ДЛЯ ДЕБИАНА

def left_deb():
	ip_rt = str(ipaddress.IPv4Address(ip2) + 1)
	with open('/etc/network/interfaces', 'a') as f:
		f.write(f'''
up ip route add {ip3 + '/24'} via {ip_rt}
up ip route add {ip4 + '/24'} via {ip_rt}
''')

def right_deb():
	ip_rt = str(ipaddress.IPv4Address(ip3) + 1)
	with open('/etc/network/interfaces', 'a') as f:
		f.write(f'''
up ip route add {ip2 + '/24'} via {ip_rt}
up ip route add {ip1 + '/24'} via {ip_rt}
''')



def ostalnoe_deb():
	nat = input("Настроить nat?(y/n)")

	if nat == "y":
		os.system("apt install iptables -y")
		os.system("iptables -t nat -A POSTROUTING -o enp0s3 -j MASQUERADE")
		os.system("DEBIAN_FRONTEND=noninteractive apt install iptables-persistent")
		os.system("systemctl restart netfilter-persistent")
		print("nat nastoren")
	else: print("Ну лан")

	file3 = open('/etc/sysctl.conf','a')
	file3.write("net.ipv4.ip_forward=1")
	file3.close()
	os.system("sysctl -p")

	reb = input("reboot?(y)")
	if reb =="y": os.system("reboot")
	else: print("Не забудь перезагрузить")

# ФУНКЦИИ ДЛЯ ЦЕНТОСА

def left_cent():
	ip_rt = str(ipaddress.IPv4Address(ip2) + 1)
	with open('/etc/rc.local', 'a') as f:
		routs = (f'''
up ip route add {ip3 + '/24'} via {ip_rt}
up ip route add {ip4 + '/24'} via {ip_rt}
''')
		f.write("\n{" + routs + "\n}" )
	os.system('chmod +x /etc/rc.d/rc.local')

def right_cent():
	ip_rt = str(ipaddress.IPv4Address(ip3) + 1)
	with open('/etc/rc.local', 'a') as f:
		routs = (f'''
up ip route add {ip2 + '/24'} via {ip_rt}
up ip route add {ip1 + '/24'} via {ip_rt}
''')
		f.write("\n{" + routs + "\n}" )
	os.system('chmod +x /etc/rc.d/rc.local')

def ostalnoe_cent():
	nat = input("Настроить nat?(y/n)")

	if nat == "y":
		os.system("apt install iptables -y")
		os.system("iptables -t nat -A POSTROUTING -o enp0s3 -j MASQUERADE")
		os.system("DEBIAN_FRONTEND=noninteractive apt install iptables-persistent")
		os.system("systemctl restart netfilter-persistent")
		print("nat nastoren")
	else: print("Ну лан")

	file3 = open('/etc/sysctl.conf','a')
	file3.write("net.ipv4.ip_forward=1")
	file3.close()
	os.system("sysctl -p")

	reb = input("reboot?(y)")
	if reb =="y": os.system("reboot")
	else: print("Не забудь перезагрузить")

if oc == "1":
	if l_or_r == "1": left_deb(); ostalnoe_deb()
	elif l_or_r == "2": right_deb(); ostalnoe_deb()
	else: print('Davai zanovo, nepravilno vibran router')
elif oc == "2":
	if l_or_r == "1": left_cent(); ostalnoe_cent()
	elif l_or_r == "2": right_cent(); ostalnoe_cent()
	else: print('Davai zanovo, nepravilno vibran router')
else: print("Nepravilno ykazal OS davai zanovo")
