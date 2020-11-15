DISM.exe /Online /Cleanup-image /Restorehealth
sfc /scannow
wsl sudo apt update
wsl sudo apt upgrade
wsl sudo apt dist-upgrade
wsl sudo apt autoremove
conda update --all
cmd /k