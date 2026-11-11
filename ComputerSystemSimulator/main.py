from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, FadeTransition

from config import APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT, BG_COLOR
from screens.dashboard import DashboardScreen
from screens.system_screen import SystemScreen
from screens.files_screen import FilesScreen
from screens.process_screen import ProcessScreen


class ComputerSimulator(App):
    def build(self):
        self.title = APP_NAME
        Window.size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        Window.minimum_width = 900
        Window.minimum_height = 600
        Window.clearcolor = BG_COLOR

        self.screen_manager = ScreenManager(
            transition=FadeTransition(duration=0.15)
        )

        screens = [
            DashboardScreen(name="dashboard", navigate_callback=self.navigate),
            SystemScreen(name="system", navigate_callback=self.navigate),
            FilesScreen(name="files", navigate_callback=self.navigate),
            ProcessScreen(name="process", navigate_callback=self.navigate),
        ]

        for screen in screens:
            self.screen_manager.add_widget(screen)

        self.screen_manager.current = "dashboard"
        return self.screen_manager

    def navigate(self, screen_name):
        if screen_name in self.screen_manager.screen_names:
            self.screen_manager.current = screen_name


if __name__ == "__main__":
    ComputerSimulator().run()
