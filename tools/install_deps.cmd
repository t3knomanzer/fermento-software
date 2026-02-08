@echo off
pip install git+https://github.com/t3knomanzer/fermento-schemas.git@main#subdirectory=fermento-embedded-schemas --target .tmp
mkdir lib\fermento_embedded_schemas
copy .tmp\fermento_embedded_schemas\ lib\fermento_embedded_schemas\