@echo off

:loop
	set /p time="スリープまでの時間を入力してください(分)："

	echo;

	set N=%time%
	if defined N set N=%N:0=%
	if defined N set N=%N:1=%
	if defined N set N=%N:2=%
	if defined N set N=%N:3=%
	if defined N set N=%N:4=%
	if defined N set N=%N:5=%
	if defined N set N=%N:6=%
	if defined N set N=%N:7=%
	if defined N set N=%N:8=%
	if defined N set N=%N:9=%

if defined N (
	echo 入力がただしくありません。数字を入力してください．
	echo;
	goto loop
) else (
	powercfg /change standby-timeout-ac %time%
	echo スリープまでの時間は%time%分に設定されました．
	timeout /nobreak  5 > /nul
	goto end
)

:end
exit /b 0