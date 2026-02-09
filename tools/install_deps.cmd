@echo off
set TEMPDIR=.tmp
set TARGETDIR=lib\fermento_embedded_schemas
set REPO=git+https://github.com/t3knomanzer/fermento-schemas.git@main#subdirectory=fermento-embedded-schemas

echo ----- Installing dependencies -----
echo Removing temporary directory if it exists...
rmdir /s /q %TEMPDIR% 2>nul
mkdir %TEMPDIR% 2>nul

echo Installing %REPO% to temporary directory...
pip install %REPO% --no-cache-dir --target %TEMPDIR%

echo Removing target directory if it exists...
rmdir /s /q %TARGETDIR% 2>nul
mkdir %TARGETDIR% 2>nul

echo Copying installed files to target directory...
copy %TEMPDIR%\fermento_embedded_schemas\ %TARGETDIR%\