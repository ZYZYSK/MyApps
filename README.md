# 事前設定
* システム環境変数
   - 変数：MYAPPS
   - 値：このディレクトリのパス
* Sleeperをスタートに登録する
* SleeptimeChangerをスタートに登録する

# module
## weather
* 気象関係のプログラム
* jma_downloader: JMA画像をダウンロード
* gpv_downloader: GPV画像をダウンロード
* jma_maker: JMA画像から動画を作成
* viewer(未完成): JMA画像，GPV画像を見る
* temperature_loader: 気温計からデータをロード
* temperature_viewer(未完成): 気温計からロードしたデータを見る


## PCManager
* PCのクリーンアップと診断，アップデートなどを行います 
* タスクスケジューラで30日に1回自動起動

## Weather_DL
* 気象衛星画像，天気図，レーダー，高層天気図をダウンロードします 
* タスクスケジューラでログオン時に自動起動
* GPV_dlが動作しない場合，環境変数"GRIB_DEFINITION_PATH"の設定に問題があると思われる

## Temperature Loader
* 気温計からデータをロードします

## Weather
* 気象関係のプログラム

## Sleeper
* ショートカットからスリープします 

## SleeptimeChanger
* スリープまでの時間を変更します

## ThemeChanger
* 指定された時間にダークモードとライトモードを切り替えます 
* タスクスケジューラでログオン時，指定された時間に自動起動