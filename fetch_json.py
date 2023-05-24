import json

# Calls from main to push out tcp connections for monitoring
def update_conn():
    try:
        with open('C:\\temp\\results\\json_data\\tcp_conn.json', 'r') as json_file:
            data = json.load(json_file, strict=False)
        return data
    except Exception as e:
        print(e)
        print("There is something wrong reading json from update_conn()")


if __name__ == '__main__':
    update_conn()


