import customtkinter as ctk
from auth_views import AuthFrame
from forum_views import MainForumFrame
from admin_views import AdminWindow
from client_api import ClientAPI  # <--- EZ VÁLTOZOTT (Helyi JSON helyett Hálózati API)

class ForumApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BME Fórum Portál")
        self.geometry("1100x700")
        
        # EZ OLDJA MEG A PROBLÉMÁT: A GUI mostantól a felhőhöz kapcsolódik!
        self.db = ClientAPI()
        
        self.current_user = None

        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.show_auth()

    def clear_container(self):
        for w in self.container.winfo_children():
            w.destroy()

    def show_auth(self):
        self.clear_container()
        if self.current_user:
            self.db.set_offline(self.current_user["username"])
        self.current_user = None
        AuthFrame(self.container, self.db, self.on_login_success).pack(fill="both", expand=True)

    def on_login_success(self, user_data):
        self.current_user = user_data
        self.show_forum()

    def show_forum(self):
        self.clear_container()
        MainForumFrame(self.container, self.db, self.current_user, self.show_auth, self.open_admin_panel).pack(fill="both", expand=True)

    def open_admin_panel(self):
        AdminWindow(self, self.db, self.show_forum)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = ForumApp()
    app.mainloop()