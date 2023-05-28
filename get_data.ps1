
# Checks if results folder is setup and creates if not
if (-Not (Test-Path "C:\temp\results")) {
    write-host "results folder not found, creating directories" -f Magenta
    write-host "Pushing TCP monitoring data to C:\temp\results\bad_tcp" -f Magenta
    New-Item -Path "C:\temp\results\bad_tcp" -ItemType "Directory"
    New-Item -Path "C:\temp\results\json_data" -ItemType "Director"
}
else {
    Write-host "All results will go to C:\temp\results\" -f Green
}


# While loop to push TCP connections
# Todo - Add more data to be pushed out such as AD-OBJECTS
write-host "Starting loop to monitor TCP Connections" -f Green
write-host "Malicious connections can be found in C:\temp\results\" -f Green
Start-Sleep(5)
while($true){
    try{
        $date = (get-date).AddSeconds(-15) # Minutes to check for newest processes in the last 3 mins
        Get-NetTCPConnection | where-object {$_.LocalAddress -eq "192.168.10.10"} | 
        Select-Object LocalAddress,LocalPort,RemoteAddress,RemotePort,
        @{name="Time";Expression={$_.CreationTime.ToString()}},
        @{name="NewConnection";Expression={if(($_.CreationTime) -gt $date){$true}else{$false}}},
        @{name="process";Expression={(get-process -id $_.OwningProcess | where-object {$_.ProcessName -ne 'Idle'}).ProcessName}} |
        Sort-Object RemoteAddress -Descending -Unique | ConvertTo-Json |
        set-content "C:\temp\results\json_data\tcp_conn.json"
        Copy-Item "C:\temp\results\json_data\tcp_conn.json" -Destination "C:\temp\results\json_data\tcp_mal.json"
    }
    
    catch { "Error occured, most likely due to tcp_conn.json being used by another process" }
}

