import re, ipaddress, requests, json

def get_ips_from_ipsum() -> set:
    # Thank you stamparm
    url = 'https://raw.githubusercontent.com/stamparm/ipsum/master/ipsum.txt'
    content = requests.get(url).content
    return set(re.findall(r'[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}', str(content)))

# Get IP from local machine
def get_ips_locally():
    with open('.\\Data\ipsum.txt') as f:
        lines = f.readlines()
    return set(re.findall(r'[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}', str(lines)))

# Get IPs from tcp_conn.json (monitoring tool)
def powershell_list_tcp() -> set:
    result = set()
    with open('C:\\temp\\results\\monitor\\tcp_conn.json', 'r') as myfile:
        data=myfile.read()
    obj = json.loads(data)
    conns = re.findall(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', str(obj))
    for conn in conns:
        #If you are looking for non-private from malware ip list
        #if not ipaddress.IPv4Address(conn).is_private:
        result.add(conn)
    return result, obj

# Choose online check if you wanna use the local ip list
def online_check():
    ip_list = []
    bad, obj = powershell_list_tcp()
    bad_ips = get_ips_from_ipsum() & bad
    if not len(bad_ips) == 0:
        for ip in bad_ips:
            for key in obj:
                if key['RemoteAddress'] == ip:
                    ip_list.append((
                    key["LocalAddress"], key["LocalPort"],
                    key["RemoteAddress"], key["RemotePort"],
                    key["process"], key["cmdline"]))
    else:
        print("No IPs found")
    return ip_list

# use offline check if you do not have internet
def offline_check():
    ip_list = []
    bad, obj = powershell_list_tcp()
    bad_ips = get_ips_locally() & bad
    if not len(bad_ips) == 0:
        for ip in bad_ips:
            for key in obj:
                if key['RemoteAddress'] == ip:
                    ip_list.append((
                    key["LocalAddress"], key["LocalPort"],
                    key["RemoteAddress"], key["RemotePort"],
                    key["process"], key["cmdline"]))
    else:
        print("No IPs found")
    return ip_list

if __name__ == '__main__':
    x = offline_check()
    print(x)

