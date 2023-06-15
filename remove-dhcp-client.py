import fabric, os, sys, yaml, subprocess

def main():
    for i in range(1, len(sys.argv)):
        MAC = sys.argv[1]
        IP = sys.argv[2]
    check_MAC(MAC,IP)
def check_DHCP(IP):
    '''Recherche du DHCP correspondant à l'ip fournit dans le fichier conf.yml qui contient tout les DHCP du réseau'''
    IPstr=IP.split(".")
    with open('conf.yml','r') as file: #ouverture du fichier de conf yaml
        conf = yaml.safe_load(file)
        lDHCP = conf['dhcp-servers'] #dictionaire des ip de DHCP
        IPstr=IPstr[:-1] # suppression du dernier nombre de la liste pour n'avoir que les nombres réseau

        for i in lDHCP.items():#parcour le dico
            DHCP=i[0] # prend l'ip du DHCP
            ip_DHCP = DHCP.split(".") # transforme l'ip en list
            ip_DHCP=ip_DHCP[:-1] # comme pour IPstr
            if ip_DHCP==IPstr:
                #print('serveur DHCP :', DHCP)
                return DHCP
    error='Unable to identify DHCP server'
    return error
def check_MAC(MAC,IP):
    '''verifie que l'adresse MAC de la machine n'est pas trouvée dans la configuration dnsmasq du serveur concerné'''
    dnsmasq = '/etc/dnsmasq.conf'
    with open('/etc/dnsmasq.conf','r') as file:
        ligne = file.readline()
        while ligne != '':
            ligne = ligne.split("=")
            if ligne[0] == 'dhcp-host':
                macdecoup = ligne[1].split(",")
                MACfound = macdecoup[0]
                if MACfound == MAC :
                    print('la MAC',MAC,"réserve déjà l'ip",macdecoup[1])
                    return False
            ligne = file.readline()
    with open('/etc/dnsmasq.conf','w') as file:
        nvlLigne='\ndhcp-write=' + MAC+","+ IP
        print(nvlLigne)
        file.write('nvlLigne')

if __name__=='__main__':
    main()