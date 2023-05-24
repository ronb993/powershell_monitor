
# Checks if results folder is setup and creates if not
if (-Not (Test-Path "C:\temp\results")) {
    write-host "results folder not found, creating directories" -f Magenta
    write-host "Pushing monitor data to C:\temp\results\monitor" -f Magenta
    New-Item -Path "C:\temp\results\monitor" -ItemType Directory
}
else {
    Write-host "monitor results will go to C:\temp\results\monitor" -f Green
}

# While loop to push TCP connections
# Todo - Add more data to be pushed out such as AD-OBJECTS
write-host "Starting loop to monitor TCP Connections" -f Green
write-host "Malicious connections can be found in C:\temp\results\monitor" -f Green
Start-Sleep(5)
while($true){
    $date = (get-date).AddSeconds(-15) # Minutes to check for newest processes in the last 3 mins
    Get-NetTCPConnection | where-object {$_.LocalAddress -eq "192.168.10.10"} | 
    Select-Object LocalAddress,LocalPort,RemoteAddress,RemotePort,CreationTime,
    @{name="NewConnection";Expression={if(($_.CreationTime) -gt $date){$true}else{$false}}},
    @{name="process";Expression={(get-process -id $_.OwningProcess).ProcessName}},
    @{name="cmdline";Expression={(Get-WmiObject Win32_Process -filter "ProcessId = $($_.OwningProcess)").commandline}} |
    Sort-Object RemoteAddress -Descending -Unique | ConvertTo-Json |
    set-content "C:\temp\results\monitor\tcp_conn.json"


    Start-Sleep(1)
}
