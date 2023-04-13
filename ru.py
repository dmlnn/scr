import os

with open('/etc/locale.gen', 'r') as f:
  old = f.read()
with open('/etc/locale.gen', 'w') as f:
  new = old.replace('# ru_RU.UTF-8 UTF-8', 'ru_RU.UTF-8 UTF-8')
  f.write(new)

  os.system('apt install console-setup -y')
  
