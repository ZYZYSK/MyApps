# 事前設定(Windows)
1. システム環境変数
   - 変数：MYAPPS_PATH
   - 値：このディレクトリのパス
2. 「shortcuts」内のファイルをスタートフォルダに入れる
3. 最初は，ショートカットファイルに設定したキーボードショートカットが動作しないことが多いので，確認する
4. 「task_scheduler」内のファイルをタスクスケジューラに登録する
___
# module
## weather
### 気象関係のプログラム
- [x] jma_downloader: JMA画像をダウンロード
- [x] gpv_downloader: GPV画像をダウンロード
   * 動作しない場合，環境変数"GRIB_DEFINITION_PATH"の設定に問題があると思われる
- [x] jma_maker: JMA画像から動画を作成
- [ ] viewer(未完成): JMA画像，GPV画像を見る
- [x] temperature_loader: 気温計からデータをロード
- [ ] temperature_viewer(未完成): 気温計からロードしたデータを見る
## pcmanager
- [x] PCの管理などを行う
## sleep
- [x] sleeper: ワンスリープ
- [x] sleep_time_changer: スリープまでの時間を変更
## others
- [x] usv: USVに接続
- [x] theme_changer: 6:00と18:00にライトテーマとダークテーマを切り替え