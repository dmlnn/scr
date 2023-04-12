import os
import ipaddress

hostname = input("Vvedi hostname: ")

file2 = open('/etc/hostname','w')
file2.write(hostname)
file2.close()
print("hostname ystanovlen")

x = input("Vvedi ip pervoi seti (x.x.x.0): ")
x2 = input("Vvedi ip seti mejdy routerami (x.x.x.0): ")
x3 = input("Vvedi ip tretei seti (x.x.x.0): ")
nomer = input("Vvedi nomer etogo routera(1 or 2): ")


network1 = ipaddress.IPv4Address(x)
network2 = ipaddress.IPv4Address(x2)
network3 = ipaddress.IPv4Address(x3)
netmask = "255.255.255.0"
netmask_pr = "/24"

network1_pr = str(network1) + netmask_pr
network2_pr = str(network2) + netmask_pr
network3_pr = str(network3) + netmask_pr

if nomer == "1":
	s8 = str(network1 + 1)
	s9 = str(network2 + 1)
	settings = ("\nauto enp0s8\n" + "iface enp0s8 inet static\n" + "address " + s8 + "\nnetmask " + netmask +
	"\n\nauto enp0s9\n" + "iface enp0s9 inet static\n" + "address " + s9 + "\nnetmask " + netmask + "\n\nup ip route add " +
	network3_pr + " via " + s9)
	file1 = open('/etc/network/interfaces','a')
	file1.write(settings)
	file1.close()
	print("gotovo \ngateway clienta:", s8)
elif nomer == "2":
	s8 = str(network3 + 1)
	s9 = str(network2 + 2)
	settings = ("\nauto enp0s8\n" + "iface enp0s8 inet static\n" + "address " + s8 + "\nnetmask " + netmask +
	"\n\nauto enp0s9\n" + "iface enp0s9 inet static\n" + "address " + s9 + "\nnetmask " + netmask + "\n\nup ip route add " +
	network1_pr + " via " + s9)
	file1 = open('/etc/network/interfaces','a')
	file1.write(settings)
	file1.close()
	print("gotovo \ngateway clienta:", s8)
else: print("Fail")

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
else: print(":((")
