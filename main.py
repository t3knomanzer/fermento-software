import hardware_setup
from lib.gui.core.ugui import Screen
from app.screens.splash import SplashScreen


def main():
    Screen.change(SplashScreen)


main()
