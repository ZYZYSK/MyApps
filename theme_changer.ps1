#システムテーマの値の保存場所
$SystemTheme_Path = "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize"
#Officeテーマの値の保存場所
$OfficeTheme_Path = "HKCU:\Software\Microsoft\Office\16.0\Common"
#ユーザのホームフォルダーのパス
$UserPath = $env:USERPROFILE
#VSCodeの設定ファイルの保存場所
$VSCode_Path = "$UserPath\AppData\Roaming\Code\User\settings.json"
#変更後のテーマ(1でライト、0でダーク)
$Theme = $args[0]

#現在のテーマを取得
function GetCurrentTheme {
  $islight = Get-ItemProperty -Path $SystemTheme_Path | Select-Object -ExpandProperty "AppsUseLightTheme"
  return $islight
}
#システムテーマの変更
function ChangeSystemTheme([int]$x) {
  Set-ItemProperty -Path $SystemTheme_Path -Name AppsUseLightTheme -Value $x
}

#Officeテーマの変更
#https://www.cloudappie.nl/change-theme-officeproplus-powershell/
function ChangeOfficeTheme([int]$x) {
  if ($x -eq 1) {
    $proPlusThemeValue = 0
  }
  elseif ($x -eq 0) {
    $proPlusThemeValue = 4
  }
  Set-ItemProperty -Path $OfficeTheme_Path -Name "UI Theme" -Value $proPlusThemeValue -Type DWORD
  # Set your identity
  Get-ChildItem -Path ($OfficeTheme_Path + "\Roaming\Identities\") | ForEach-Object {
    $identityPath = ($_.Name.Replace("HKEY_CURRENT_USER", "HKCU:") + "\Settings\1186\{00000000-0000-0000-0000-000000000000}");
    if (Get-ItemProperty -Path $identityPath -Name "Data" -ErrorAction Ignore) {
      Write-Verbose $identityPath
      Set-ItemProperty -Path $identityPath -Name "Data" -Value ([byte[]]($proPlusThemeValue, 0, 0, 0)) -Type Binary
    }
  }
}

#VSCodeテーマの変更
function ChangeVSCodeTheme([int] $x) {
  if ($x -eq 1) {
    $VSCode_Theme = "Default Light+"
  }
  elseif ($x -eq 0) {
    $VSCode_Theme = "Default Dark+"
  }
  $VSCode_Settings = Get-Content $VSCode_Path | ConvertFrom-Json
  $VSCode_Settings."workbench.colorTheme" = $VSCode_Theme
  $VSCode_Settings | ConvertTo-Json  | Set-Content $VSCode_Path

}
$islight = GetCurrentTheme
#現在のテーマと変更後のテーマが同じではない
if ($islight -ne $Theme) {
  Write-Output "Changing Theme!"
  ChangeSystemTheme $Theme
  ChangeOfficeTheme $Theme
  ChangeVSCodeTheme $Theme
}