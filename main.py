import customtkinter as ctk
from data_manager import JsonDataManager
from auth_views import AuthFrame
from forum_views import MainForumFrame
from admin_views import AdminWindow

ctk.set_appearance_mode("Dark")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BME Egyetemi Fórum Portál")
        self.geometry("1100x700")

        self.db = JsonDataManager()
        self.current_user = None

        self.container = ctk.CTkFrame(self, fg_color="#141517")
        self.container.pack(fill="both", expand=True)

        self.show_auth()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_auth(self):
        self.clear_container()
        auth_frame = AuthFrame(self.container, self.db, self.on_login_success)
        auth_frame.pack(fill="both", expand=True)

    def on_login_success(self, user_data):
        self.current_user = user_data
        self.show_forum()

    def show_forum(self):
        self.clear_container()
        forum_frame = MainForumFrame(
            self.container, self.db, self.current_user, 
            on_logout=self.show_auth, open_admin_panel=self.open_admin_panel
        )
        forum_frame.pack(fill="both", expand=True)

    def open_admin_panel(self):
        AdminWindow(self, self.db, on_refresh_callback=self.show_forum)

if __name__ == "__main__":
    app = App()
    app.mainloop()