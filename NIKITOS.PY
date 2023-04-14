import os

os.system('yum install epel-release -y')
os.system('yum update -y')
os.system('yum install easy-rsa openvpn -y')
os.system('cp -r /usr/share/easy-rsa /etc/openvpn/')
os.chdir('/etc/openvpn/easy-rsa/3')
with open('vars', 'w+') as f:
  f.write(f'''set_var EASYRSA                "$PWD"
set_var EASYRSA_PKI               "$EASYRSA/pki"
set_var EASYRSA_DN                "cn_only"
set_var EASYRSA_REQ_COUNTRY       "RU"
set_var EASYRSA_REQ_PROVINCE      "MSK"
set_var EASYRSA_REQ_CITY          "MSK"
set_var EASYRSA_REQ_ORG           "KMPO"
set_var EASYRSA_REQ_EMAIL         "{name_vars}"
set_var EASYRSA_REQ_OU            "IT"
set_var EASYRSA_KEY_SIZE          4096
set_var EASYRSA_ALGO              rsa
set_var EASYRSA_CA_EXPIRE         7500
set_var EASYRSA_CERT_EXPIRE       3650
set_var EASYRSA_NS_SUPPORT        "no"
set_var EASYRSA_NS_COMMENT        "CERTIFICATE AUTHORITY"
set_var EASYRSA_EXT_DIR           "$EASYRSA/x509-types"
set_var EASYRSA_SSL_CONF          "$EASYRSA/openssl-1.0.cnf"
set_var EASYRSA_DIGEST            "sha512"''')
os.system('chmod +x vars')
input("Сейчас будут генерироваться ключи, где pass phrase введи root, где попросят yes пиши yes, поля common name можешь оставить пустыми")
os.system('./easyrsa init-pki')
os.system('./easyrsa build-ca') 
os.system(f'./easyrsa gen-req {name} nopass')
os.system(f'./easyrsa sign-req server {name}')
os.chdir('/root')
