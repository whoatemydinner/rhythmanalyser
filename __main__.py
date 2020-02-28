from gui import MainWindow

# TODO: move filepath reference elsewhere
filepath = None

# create and display a main window object
main_window = MainWindow.MainWindow(filepath)
main_window.start()