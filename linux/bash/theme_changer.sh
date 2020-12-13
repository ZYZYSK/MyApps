#!/bin/bash
#参考資料
### https://askubuntu.com/questions/742870/background-not-changing-using-gsettings-from-cron
### https://askubuntu.com/questions/1079361/change-gtk-theme-on-schedule-with-cron-ubuntu-18-04
#ダークテーマ
system_dark="Yaru-dark"
wps_dark="2019dark"
vscode_dark="Default Dark+"
android_studio_dark="Darcula"
#ライトテーマ
system_light="Yaru-light"
wps_light="2019white"
vscode_light="Default Light+"
android_studio_light="IntelliJ Light"
#ダークテーマにする時刻
dark_time=1800
#ライトテーマにする時刻
light_time=0600
#現在時刻を取得
current_time=`date +%H%M`

#システムテーマ変更
function ChangeSystemTheme(){
    echo $1
    `dconf write /org/gnome/desktop/interface/gtk-theme \'$1\'`
}
#WPS Officeテーマ変更
function ChangeWPSTheme(){
    `sed -i.bak "s/lastSkin.*$/lastSkin=$1"/ "$HOME/.local/share/Kingsoft/office6/skins/default/histroy.ini"`
}
#VSCodeテーマ変更
function ChangeVSCodeTheme(){
    echo $1
    `sed -i.bak "s/\"workbench.colorTheme\".*$/\"workbench.colorTheme\":\"$1\",/" "$HOME/.config/Code/User/settings.json"`
}
#Inkscapeテーマ変更
function ChangeInkscapeTheme(){
    `sed -i.bak "s/defaultTheme=\".*\"/defaultTheme=\"$1\"/" "$HOME/.config/inkscape/preferences.xml"`
}
#Android Studioテーマ変更
function ChangeAndroidStudioTheme(){
    `sed -i.bak "s/global_color_scheme.*\"/global_color_scheme name=\"$1\"/" "$HOME/.config/Google/AndroidStudio4.1/options/colors.scheme.xml"`
}

#cron実行用
echo $HOME
export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus
#時刻を比較
if [ ${current_time} -ge ${light_time} ] && [ ${current_time} -lt ${dark_time} ]
#ライトモード
then
    ChangeSystemTheme "${system_light}"
    ChangeWPSTheme "${wps_light}"
    ChangeVSCodeTheme "${vscode_light}"
    ChangeInkscapeTheme "${system_light}"
    ChangeAndroidStudioTheme "${android_studio_light}"
#ダークモード
else
    ChangeSystemTheme "${system_dark}"
    ChangeWPSTheme "${wps_dark}"
    ChangeVSCodeTheme "${vscode_dark}"
    ChangeInkscapeTheme "${system_dark}"
    ChangeAndroidStudioTheme "${android_studio_dark}"
fi
