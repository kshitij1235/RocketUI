@echo off
setlocal ENABLEEXTENSIONS

REM Root package directory
set ROOT=rocket

REM =========================
REM Core framework
REM =========================
mkdir %ROOT%\core
mkdir %ROOT%\core 2>nul
type nul > %ROOT%\core\__init__.py

REM =========================
REM Rendering internals
REM =========================
mkdir %ROOT%\render 2>nul
type nul > %ROOT%\render\__init__.py

REM =========================
REM Layout primitives
REM =========================
mkdir %ROOT%\layout 2>nul
type nul > %ROOT%\layout\__init__.py

REM =========================
REM UI elements
REM =========================
mkdir %ROOT%\elements 2>nul
type nul > %ROOT%\elements\__init__.py

REM =========================
REM Pages & navigation
REM =========================
mkdir %ROOT%\pages 2>nul
type nul > %ROOT%\pages\__init__.py

REM =========================
REM Runtime / window management
REM =========================
mkdir %ROOT%\runtime 2>nul
type nul > %ROOT%\runtime\__init__.py

REM =========================
REM Theme system
REM =========================
mkdir %ROOT%\theme 2>nul
type nul > %ROOT%\theme\__init__.py

REM =========================
REM CLI
REM =========================
mkdir %ROOT%\cli 2>nul
mkdir %ROOT%\cli\commands 2>nul
type nul > %ROOT%\cli\__init__.py
type nul > %ROOT%\cli\commands\__init__.py

REM =========================
REM Utilities
REM =========================
mkdir %ROOT%\utils 2>nul
type nul > %ROOT%\utils\__init__.py

echo.
echo RocketUI directory structure created successfully.
echo NOTE: No files were moved. Do that manually.
echo.

endlocal
pause
