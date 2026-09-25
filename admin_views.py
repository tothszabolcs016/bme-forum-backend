import customtkinter as ctk

class AdminWindow(ctk.CTkToplevel):
    def __init__(self, parent, db, on_refresh_callback):
        super().__init__(parent)
        self.title("BME Fórum - Rendszergazda Adminisztáció")
        self.geometry("800x550")
        self.db = db
        self.on_refresh_callback = on_refresh_callback
        self.configure(fg_color="#141517")

        # TabView a különböző admin feladatoknak
        self.tabview = ctk.CTkTabview(self, fg_color="#1d1e22", segmented_button_selected_color="#800020", segmented_button_selected_hover_color="#5B0017")
        self.tabview.pack(fill="both", expand=True, padx=15, pady=15)

        self.users_tab = self.tabview.add("Felhasználók Kezelése")
        self.deleted_tab = self.tabview.add("Törölt Tartalmak Kuka / Visszaállítás")

        self.setup_users_tab()
        self.setup_deleted_tab()

    # 1. TAB: Felhasználók törlése és rangok módosítása
    def setup_users_tab(self):
        scroll = ctk.CTkScrollableFrame(self.users_tab, fg_color="#141517")
        scroll.pack(fill="both", expand=True, padx=5, pady=5)

        for u in self.db.get_all_users():
            row = ctk.CTkFrame(scroll, fg_color="#212328", corner_radius=6)
            row.pack(fill="x", pady=4, padx=5)

            txt = f"{u['username']} ({u['fullname']}) | Neptun: {u.get('neptun', 'N/A')}"
            lbl = ctk.CTkLabel(row, text=txt, font=ctk.CTkFont(size=12, weight="bold"))
            lbl.pack(side="left", padx=10, pady=8)

            # Törlés gomb
            del_btn = ctk.CTkButton(
                row, text="Törlés", fg_color="#C0392B", hover_color="#922B21", width=70,
                command=lambda username=u['username']: self.delete_user_action(username)
            )
            del_btn.pack(side="right", padx=10)

            # Rang váltó
            role_opt = ctk.CTkOptionMenu(
                row, values=["Hallgató", "Oktató", "Admin"], width=100,
                button_color="#800020", button_hover_color="#5B0017", dropdown_hover_color="#800020",
                command=lambda new_role, username=u['username']: self.change_role(username, new_role)
            )
            role_opt.set(u.get("role", "Hallgató"))
            role_opt.pack(side="right", padx=5)

    def change_role(self, username, new_role):
        self.db.update_user_role(username, new_role)
        self.on_refresh_callback()

    def delete_user_action(self, username):
        if username == "admin":
            return
        self.db.delete_user(username)
        self.setup_users_tab()
        self.on_refresh_callback()

    # 2. TAB: Soft-deleted témák és hozzászólások helyreállítása
    def setup_deleted_tab(self):
        for w in self.deleted_tab.winfo_children():
            w.destroy()

        scroll = ctk.CTkScrollableFrame(self.deleted_tab, fg_color="#141517")
        scroll.pack(fill="both", expand=True, padx=5, pady=5)

        data = self.db.get_forum_data()
        found_deleted = False

        for cat in data:
            for sf in cat["subforums"]:
                for top in sf["topics"]:
                    # Törölt témák visszaállítása
                    if top.get("deleted", False):
                        found_deleted = True
                        row = ctk.CTkFrame(scroll, fg_color="#212328")
                        row.pack(fill="x", pady=4, padx=5)

                        lbl = ctk.CTkLabel(row, text=f"[TÖRÖLT TÉMA] {top['title']} (Szerző: {top['author']})", text_color="#E74C3C")
                        lbl.pack(side="left", padx=10, pady=8)

                        rec_btn = ctk.CTkButton(row, text="Visszaállítás", fg_color="#27AE60", hover_color="#1E8449", width=100, command=lambda t_id=top["topic_id"]: self.restore_topic(t_id))
                        rec_btn.pack(side="right", padx=10)

                    # Törölt posztok visszaállítása
                    for idx, post in enumerate(top["posts"]):
                        if post.get("deleted", False):
                            found_deleted = True
                            row = ctk.CTkFrame(scroll, fg_color="#212328")
                            row.pack(fill="x", pady=4, padx=5)

                            lbl = ctk.CTkLabel(row, text=f"[TÖRÖLT HOZZÁSZÓLÁS] {post['author']}: {post['content'][:30]}...", text_color="#E67E22")
                            lbl.pack(side="left", padx=10, pady=8)

                            rec_btn = ctk.CTkButton(row, text="Visszaállítás", fg_color="#27AE60", hover_color="#1E8449", width=100, command=lambda t_id=top["topic_id"], p_idx=idx: self.restore_post(t_id, p_idx))
                            rec_btn.pack(side="right", padx=10)

        if not found_deleted:
            empty_lbl = ctk.CTkLabel(scroll, text="Nincs törölt tartalom a rendszerben.", text_color="#888888")
            empty_lbl.pack(pady=20)

    def restore_topic(self, topic_id):
        self.db.toggle_topic_deletion(topic_id, False)
        self.setup_deleted_tab()
        self.on_refresh_callback()

    def restore_post(self, topic_id, post_index):
        self.db.toggle_post_deletion(topic_id, post_index, False)
        self.setup_deleted_tab()
        self.on_refresh_callback()