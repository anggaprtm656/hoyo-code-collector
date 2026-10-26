@echo off
title HoYo Codes Collector Test
chcp 65001 >nul
cd /d "%~dp0"
echo ========================================================
echo        HoYo Codes Collector (GI, HSR, ZZZ, HI3)
echo ========================================================
echo.
python collector.py
echo.
pause
