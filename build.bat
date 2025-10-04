@echo off
echo ========================================
echo Hex Map Generator - Build Script (CustomTkinter Edition)
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://www.python.org/
    pause
    exit /b 1
)

echo Python detected!
echo.

REM Install CustomTkinter
echo Checking for CustomTkinter...
python -m pip show customtkinter >nul 2>&1
if %errorlevel% neq 0 (
    echo CustomTkinter not found. Installing now...
    python -m pip install customtkinter
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install CustomTkinter
        pause
        exit /b 1
    )
    echo CustomTkinter installed successfully!
    echo.
)

REM Install PyInstaller
echo Checking for PyInstaller...
python -m pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller not found. Installing now...
    python -m pip install pyinstaller
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install PyInstaller
        pause
        exit /b 1
    )
    echo PyInstaller installed successfully!
    echo.
)

echo Building executable...
echo.

REM Clean previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Build options
echo Select build type:
echo 1. Single file (slower startup, easier to share)
echo 2. Folder (faster startup, multiple files)
echo.
set /p choice="Enter choice (1 or 2): "

if "%choice%"=="1" (
    echo.
    echo Building single file executable...
    python -m PyInstaller --onefile --windowed --name "HexMapGenerator-CTK" --collect-all customtkinter hex_map_generator.py
) else if "%choice%"=="2" (
    echo.
    echo Building folder-based executable...
    python -m PyInstaller --windowed --name "HexMapGenerator-CTK" --collect-all customtkinter hex_map_generator.py
) else (
    echo Invalid choice. Building single file by default...
    python -m PyInstaller --onefile --windowed --name "HexMapGenerator-CTK" --collect-all customtkinter hex_map_generator.py
)

echo.
if %errorlevel% equ 0 (
    echo ========================================
    echo Build complete!
    echo ========================================
    echo.
    echo Your executable is in the dist folder:
    if "%choice%"=="2" (
        echo Run: dist\HexMapGenerator-CTK\HexMapGenerator-CTK.exe
    ) else (
        echo Run: dist\HexMapGenerator-CTK.exe
    )
) else (
    echo.
    echo ========================================
    echo Build FAILED!
    echo ========================================
    echo.
    echo Please check the error messages above.
)
echo.
pause
