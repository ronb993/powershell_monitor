import json
# Runs every 0.02 seconds from the background thread in main.py
def update():
    with open(".\\test.json", 'r', errors='ignore') as json_file:
        try:
            data = json.load(json_file, strict=False)
        except Exception as e:
            print(e)
    return data


