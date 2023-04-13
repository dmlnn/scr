import os

input("!!! Etot script prednazna4en tolko dlya debiana, centos srazy podderjivaet russkiy yazik !!!")
with open('/etc/locale.gen', 'r') as f:
  old = f.read()
with open('/etc/locale.gen', 'w') as f:
  new = old.replace('# ru_RU.UTF-8 UTF-8', 'ru_RU.UTF-8 UTF-8')
  f.write(new)

os.system('DEBIAN_FRONTEND=noninteractive apt install console-setup -y')

with open('/etc/default/console-setup', 'r') as f:
  old = f.read()
with open('/etc/default/console-setup', 'w') as f:
  new = old.replace('CODESET="Lat15"', 'CODESET="CyrSlav"')
  f.write(new)

os.system('reboot')
