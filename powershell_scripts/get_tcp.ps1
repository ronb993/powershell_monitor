try{
    $date = (get-date).AddSeconds(-15) # Minutes to check for newest processes in the last 3 mins
    Get-NetTCPConnection | where-object {$_.LocalAddress -eq "192.168.10.10" -and $_.State -like "Established*"} | 
    Select-Object LocalAddress,LocalPort,RemoteAddress,RemotePort,
    @{name="Time";Expression={$_.CreationTime.ToString()}},
    @{name="NewConnection";Expression={if(($_.CreationTime) -gt $date){$true}else{$false}}},
    @{name="process";Expression={(get-process -id $_.OwningProcess | where-object {$_.ProcessName -ne 'Idle'}).ProcessName}} |
    Sort-Object RemoteAddress -Descending -Unique | ConvertTo-Json
    }
    
catch { "Error occured, most likely due to tcp_conn.json being used by another process" }
