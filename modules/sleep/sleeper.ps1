#初期処理
$x = $host.UI.RawUI
[void][Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms") 
$KeyMap = [Windows.Forms.Keys]
#スリープを実行する
#https://ch.nicovideo.jp/lunaorbit/blomaga/ar1918660
function StartSleep {
    Add-Type -Assembly System.Windows.Forms
    [System.Windows.Forms.Application]::SetSuspendState('Suspend', $false, $false)
}
$IsSleep = $true
Write-Output "10秒後にスリープします。`n[y] 今すぐスリープ   [n] スリープしない"
#待ち終了時刻
$limit = (Get-Date).AddSeconds(10)
#待ち終了時刻になるまでキー入力を待つ
While ((Get-Date) -le $limit) {
    Start-Sleep -Milliseconds 1
    if ($x.KeyAvailable -eq $true) {
        $KeyInfo = $x.ReadKey("IncludeKeyDown,IncludeKeyUp,AllowCtrlC,NoEcho")
        if ($keyInfo.VirtualKeyCode -eq $KeyMap::Y) {
            break
        }
        elseif ($keyInfo.VirtualKeyCode -eq $KeyMap::N) {
            $IsSleep = $false
            break
        }
        else {
            continue
        }
    }
}
if ($IsSleep -eq $true) {
    Write-Output "スリープします！"
    StartSleep
}