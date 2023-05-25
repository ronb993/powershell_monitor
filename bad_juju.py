import re, requests, json, csv, os, winsound

fields = ['LocalAddress',
          'LocalPort',
          'RemoteAddress',
          'RemotePort',
          'Time',
          'Process']

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
    with open('C:\\temp\\results\\json_data\\tcp_conn.json', 'r') as myfile:
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
                    key["Time"], key["process"]))
    else:
        print("No IPs found")
    return ip_list

# use offline check if you do not have internet
def offline_check():
    ip_list = []
    bad, obj = powershell_list_tcp()
    bad_ips = get_ips_locally() & bad
    if not len(bad_ips) == 0:
        duration = 1000
        freq = 440
        winsound.Beep(freq, duration)
        for ip in bad_ips:
            for key in obj:
                if key['RemoteAddress'] == ip:
                    ip_list.append((
                    key["LocalAddress"], key["LocalPort"],
                    key["RemoteAddress"], key["RemotePort"],
                    key["Time"], key["process"]))
        return ip_list

def process_data(get_type):
    if get_type == 'offline':
        data = offline_check()
    elif get_type == 'online':
        data = online_check()
    else:
        data = offline_check()
    if data is not None:
        write_to_csv(data)
    return data

def check_row(row_one, row_two):
    one = (row_one[0], row_one[1],
    row_one[2], row_one[3],
    row_one[4], row_one[5])

    two = (row_two[0], str(row_two[1]),
           row_two[2], str(row_two[3]),
           row_two[4], row_two[5])

    if one == two:
        return True
    else:
        return False


def write_to_csv(data):
    try:
        if not os.path.exists('C:\\temp\\results\\bad_tcp\\bad_tcp.csv'):
            with open('C:\\temp\\results\\bad_tcp\\bad_tcp.csv','x', newline='') as f:
                csv_out = csv.writer(f)
                csv_out.writerow(fields)
                for row in data:
                    csv_out.writerow(row)
            return
        else:
            with open('C:\\temp\\results\\bad_tcp\\bad_tcp.csv', 'r+', newline='') as f:
                read = csv.reader(f, delimiter=',')
                fix_row = list(read)
                last_row_csv = fix_row[-1]
                get_data_row = data[-1]
                csv_writer = csv.writer(f)
                if(not check_row(last_row_csv, get_data_row)):
                    for row in data:
                        csv_writer.writerow(row)

            return
    except IOError:
        print("bad_tcp.csv is already open")

    
if __name__ == '__main__':
    process_data('offline')


