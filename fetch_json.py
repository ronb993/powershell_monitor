import json

# Calls from main to push out tcp connections for monitoring
def update_conn():
    try:
        with open('C:\\temp\\results\\json_data\\tcp_conn.json', 'r') as json_file:
            data = json.load(json_file, strict=False)
        return data
    except IOError:
        print("File tcp_conn.json is already open")


if __name__ == '__main__':
    update_conn()


