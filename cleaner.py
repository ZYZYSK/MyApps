import subprocess
# ディスククリーンアップ
subprocess.Popen('C:\\WINDOWS\\system32\\cleanmgr.exe')
# 復元ポイントの削除
subprocess.Popen(
    'C:\\WINDOWS\\system32\\SystemPropertiesProtection.exe', shell=True)
