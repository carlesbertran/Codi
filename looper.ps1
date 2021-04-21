while (1){
    $var1 = type "./reports/report.txt"
    if ($var1 -ne "") {
        node .\web3check.js
        Start-Sleep -s 15
    } else {
        Start-Sleep -s 20
    }
}