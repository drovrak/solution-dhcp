import os
import yaml

def load_config(filename, create):
    if os.path.exists(filename):
            with open(filename, 'r') as file:
                config = yaml.safe_load(file)
                return config
    elif create:
        config={'dhcp_hosts_cfg': '/etc/dnsmasq.d/hosts.conf', 
                'user': 'sae203'}
        return config
    else:
         print('fichier,' ,filename,'introuvable, verifier la syntaxe')
