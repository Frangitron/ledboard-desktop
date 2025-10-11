from logging import basicConfig
basicConfig(level="INFO")


if __name__ == "__main__":
    from ledboarddesktop.launcher import Launcher
    launcher = Launcher()
    launcher.run()
