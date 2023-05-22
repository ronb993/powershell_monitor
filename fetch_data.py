import subprocess, re, ipaddress, requests, json

# Runs every 0.02 seconds from the background thread in main.py
def update_conn():
    with open('.\\Data\\test.json', 'r', errors='ignore') as json_file:
        try:
            data = json.load(json_file, strict=False)
        except Exception as e:
            print(e)
    return data

def update_process():
    with open('.\\Data\\process.json', 'r', errors='ignore') as json_file:
        try:
            data = json.load(json_file, strict=False)
        except Exception as e:
            print(e)
    return data

def get_ips_from_ipsum() -> set:
    # Thank you stamparm
    url = 'https://raw.githubusercontent.com/stamparm/ipsum/master/ipsum.txt'
    content = requests.get(url).content
    return set(re.findall(r'[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}', str(content)))

# Get IP from local machine
def get_ips_locally():
    ip_list = []
    with open('.\\Data\ipsum.txt') as f:
        lines = f.readlines()
    return set(re.findall(r'[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}', str(lines)))

def netstat_list() -> set:
    result = set()
    net_conn = subprocess.check_output('netstat -n'.split(), universal_newlines=True).splitlines()
    nets = re.findall(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', str(net_conn))
    for net in nets:
        if not ipaddress.IPv4Address(net).is_private:
            result.add((net).rstrip('\n'))
    return result
    
def online_check():
    ip_list = []
    bad_ips = get_ips_from_ipsum() & netstat_list()
    if not len(bad_ips) == 0:
        for ip in bad_ips:
            ip_list.append(ip)
    else:
        print(f'Network is clear of malicious IPs')
    return ip_list

def offline_check():
    ip_list = []
    bad_ips = get_ips_locally() & netstat_list()
    if not len(bad_ips) == 0:
        for ip in bad_ips:
            ip_list.append(ip)
    else:
        print(f'Network is clear of malicious IPs')
    return ip_list

if __name__ == '__main__':
    online_check()


