@echo off

:loop
	set /p time="�X���[�v�܂ł̎��Ԃ���͂��Ă�������(��)�F"

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
	echo ���͂�������������܂���B��������͂��Ă��������D
	echo;
	goto loop
) else (
	powercfg /change standby-timeout-ac %time%
	echo �X���[�v�܂ł̎��Ԃ�%time%���ɐݒ肳��܂����D
	timeout /nobreak  5 > /nul
	goto end
)

:end
exit /b 0