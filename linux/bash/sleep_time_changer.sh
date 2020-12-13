#!/bin/bash
SleepTimeChanger(){
    suspend=`dconf read /org/gnome/settings-daemon/plugins/power/sleep-inactive-ac-timeout`
    echo "現在のサスペンドまでの時間は$((suspend/60))分です．"
    echo -n "サスペンドまでの時間を入力してください："
    while true
    do
        #入力した時間を読み取る
        read suspend
        #数値を入力した場合
        if expr "$suspend" : "[0-9]*$" > /dev/null;then
            `dconf write /org/gnome/settings-daemon/plugins/power/sleep-inactive-ac-timeout $((suspend*60))`
            echo "サスペンドまでの時間は${suspend}分に設定されました．"
            sleep 5
            break
        else
            echo "入力が正しくありません．数字を入力してください．"
        fi
    done
}
SleepTimeChanger

