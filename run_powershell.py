import json
from subprocess import run

#Todo: Use PSJobs or runspaces
def update_tcp():
    cmd = run(["powershell.exe", ".\\powershell_scripts\\get_tcp.ps1"],shell=False,
              capture_output=True, text=True).stdout.strip("\n")
    cmd = json.loads(cmd)
    return cmd

def update_udp():
    pass

def update_ad():
    pass

def update_ad_report():
    pass

if __name__ == '__main__':
    update_tcp()


