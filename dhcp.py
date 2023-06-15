from fabric import Connection



def dhcp_list(server, cfg):
    '''Retourne une liste de configurations DHCP des hôtes lues dans la configuration dnsmasq sur le serveur'''

    # Établir une connexion SSH vers le serveur avec les informations de connexion fournies dans la configuration
    with Connection(server, user=cfg['user']) as conn:

        # Exécuter la commande pour lire la configuration dnsmasq
        result = conn.run(f"cat /etc/dnsmasq.conf", hide=True)
        lines = result.stdout.splitlines()

    hosts = []
    for line in lines:
        line = line.strip()

        # Vérifier si la ligne commence par "dhcp-host"
        if line.startswith("dhcp-host"):
            parts = line.split(",")
            mac = parts[0].split("=")[1].strip()
            ip = parts[1].split("=")[1].strip()

            # Créer un dictionnaire représentant l'association de l'adresse MAC et de l'adresse IP
            host = {"mac": mac, "ip": ip}
            hosts.append(host)

    return hosts    

def ip_other_mac_exists(cnx, ip, mac, cfg):
    # Exécuter la commande pour lire les configurations DHCP sur l'hôte connecté avec cnx
    result = cnx.run(f"cat /etc/dnsmasq.conf'", hide=True)
    lines = result.stdout.splitlines()

    for line in lines:
        line = line.strip()

        # Vérifier si la ligne contient une entrée dhcp-host
        if line.startswith("dhcp-host"):
            parts = line.split(",")
            host_mac = parts[0].split("=")[1].strip()
            host_ip = parts[1].split("=")[1].strip()

            # Vérifier si l'adresse IP est la même mais l'adresse MAC est différente
            if host_ip == ip and host_mac != mac:
                return True

    return False