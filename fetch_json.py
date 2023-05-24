import json

# Calls from main to push out tcp connections for monitoring
def update_conn():
    with open('C:\\temp\\results\\monitor\\tcp_conn.json', 'r', errors='ignore') as json_file:
        try:
            data = json.load(json_file, strict=False)
        except Exception as e:
            print(e)
    return data


if __name__ == '__main__':
    update_conn()


