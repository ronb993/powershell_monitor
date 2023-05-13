import json, re

# Runs every 0.02 seconds from the background thread in main.py
def update():
    e_list = []
    f_list = []
    s_list = []
    p_list = []
    i_list = []
    with open("C:\\json_data\\positions.json", 'r', errors='ignore') as json_file:
        try:
            data = json.load(json_file, strict=False)
            json_data = data['Position']
            for key in json_data:
                if key['name'] == 'local_player':
                    p_list.append((key['x'], key['y'], key['z'], key['rot']))
                elif key['name'] == 'ENEMY':
                    e_list.append((key['x'], key['y'], key['z'], key['rot'], key['id']))
                elif key['name'] == 'FRIEND':
                    f_list.append((key['x'], key['y'], key['z'], key['rot'], key['id']))
                elif key['name'] == 'SCAV':
                    s_list.append((key['x'], key['y'], key['z'], key['rot']))
                elif key['name'] == 'ITEM':
                    i_list.append((key['x'], key['y'], key['i_name']))
                else:
                    print(f"no json loaded for {key['name']}")
        except Exception as e:
            pass
            
    return i_list, e_list, f_list, s_list, p_list