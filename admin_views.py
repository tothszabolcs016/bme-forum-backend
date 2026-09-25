import customtkinter as ctk

class AdminWindow(ctk.CTkToplevel):
    def __init__(self, parent, db, on_refresh_callback):
        super().__init__(parent)
        self.title("BME Fórum - Rendszergazda Adminisztráció")
        self.geometry("700x480")
        self.db = db
        self.on_refresh_callback = on_refresh_callback
        self.configure(fg_color="#141517")

        # Felső sáv a címnek és a frissítés gombnak
        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.pack(fill="x", padx=15, pady=15)

        title = ctk.CTkLabel(top_bar, text="FELHASZNÁLÓI RANGOK ÉS FIÓKKEZELÉS", font=ctk.CTkFont(size=16, weight="bold"), text_color="#E74C3C")
        title.pack(side="left")

        # UNIVERZÁLIS FRISSÍTÉS GOMB (Admin Panelhez)
        refresh_btn = ctk.CTkButton(top_bar, text="🔄 Frissítés", width=90, fg_color="#3498DB", hover_color="#2980B9", command=self.force_refresh)
        refresh_btn.pack(side="right")

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="#1d1e22")
        self.scroll.pack(fill="both", expand=True, padx=15, pady=10)

        self.setup_users()

    def force_refresh(self):
        """Újratölti a felhasználói listát az adatbázisból, és frissíti a mögötte lévő főablakot is."""
        self.setup_users()
        self.on_refresh_callback()

    def setup_users(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        for u in self.db.get_all_users():
            row = ctk.CTkFrame(self.scroll, fg_color="#141517", corner_radius=6)
            row.pack(fill="x", pady=4, padx=5)

            # Felhasználói adatok megjelenítése (Neptun kód, Név, Felhasználónév)
            txt = f"{u['username']} ({u.get('fullname', '')}) | Neptun: {u.get('neptun', 'N/A')}"
            lbl = ctk.CTkLabel(row, text=txt, font=ctk.CTkFont(size=12, weight="bold"))
            lbl.pack(side="left", padx=10, pady=8)

            # Fő adminisztrátort (admin) ne lehessen véletlenül sem törölni
            if u['username'] != "admin":
                del_btn = ctk.CTkButton(
                    row, text="Törlés", fg_color="#C0392B", hover_color="#922B21", width=70,
                    command=lambda username=u['username']: self.delete_user_action(username)
                )
                del_btn.pack(side="right", padx=10)

            # Rang módosítása legördülő menüből (Élőben frissül a szerveren)
            role_opt = ctk.CTkOptionMenu(
                row, values=["Hallgató", "Oktató", "Admin"], width=100,
                button_color="#800020", button_hover_color="#5B0017", dropdown_hover_color="#800020",
                command=lambda new_role, username=u['username']: self.change_role(username, new_role)
            )
            role_opt.set(u.get("role", "Hallgató"))
            
            # Kisebb igazítás, ha nincs törlés gomb (az admin felhasználónál)
            role_opt.pack(side="right", padx=5 if u['username'] != "admin" else 15)

    def change_role(self, username, new_role):
        self.db.update_user_role(username, new_role)
        self.force_refresh()

    def delete_user_action(self, username):
        if username == "admin": 
            return
        self.db.delete_user(username)
        self.force_refresh()