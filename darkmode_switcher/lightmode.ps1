#ダークテーマかどうか確認
#変更しない場合は終了
$islight = Get-ItemProperty "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize" | select -ExpandProperty "AppsUseLightTheme"
if ($islight -eq 0) {
  Write-Output "change to light mode"
  #system
  Set-ItemProperty -Path HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize -Name AppsUseLightTheme -Value 1

  #office
  #https://www.cloudappie.nl/change-theme-officeproplus-powershell/
  $proPlusThemeValue = 0;
  $OfficeThemeRegKey = 'HKCU:\Software\Microsoft\Office\16.0\Common'
  Set-ItemProperty -Path $OfficeThemeRegKey -Name 'UI Theme' -Value $proPlusThemeValue -Type DWORD
  # Set your identity
  Get-ChildItem -Path ($OfficeThemeRegKey + "\Roaming\Identities\") | ForEach-Object {
    $identityPath = ($_.Name.Replace('HKEY_CURRENT_USER', 'HKCU:') + "\Settings\1186\{00000000-0000-0000-0000-000000000000}");
    if (Get-ItemProperty -Path $identityPath -Name 'Data' -ErrorAction Ignore) {
      Write-Verbose $identityPath
      Set-ItemProperty -Path $identityPath -Name 'Data' -Value ([byte[]]($proPlusThemeValue, 0, 0, 0)) -Type Binary
    }
  }

  #vscode
  $vscode_path = "C:\Users\huang\AppData\Roaming\Code\User\settings.json"
  $vscode_settings = Get-Content $vscode_path | ConvertFrom-Json
  $vscode_settings."workbench.colorTheme" = "Default Light+"
  $vscode_settings | ConvertTo-Json  | Set-Content $vscode_path
}