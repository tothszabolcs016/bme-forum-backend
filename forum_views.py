import customtkinter as ctk

ROLES = {
    "Admin": {"color": "#E74C3C", "label": "[ADMIN]"},
    "Oktató": {"color": "#3498DB", "label": "[OKTATÓ]"},
    "Hallgató": {"color": "#800020", "label": "[HALLGATÓ]"}
}

class ProfileAndChatWindow(ctk.CTkToplevel):
    def __init__(self, parent, db, current_user, target_username, on_update_callback):
        super().__init__(parent)
        self.title(f"Profil & Csevegés - {target_username}")
        self.geometry("750x650")
        self.db = db
        self.current_user = current_user
        self.target_username = target_username
        self.on_update_callback = on_update_callback
        self.configure(fg_color="#141517")

        self.tabview = ctk.CTkTabview(self, fg_color="#1d1e22", segmented_button_selected_color="#800020")
        self.tabview.pack(fill="both", expand=True, padx=15, pady=15)

        self.profile_tab = self.tabview.add("Profil Adatok")
        if self.current_user["username"] != self.target_username:
            self.chat_tab = self.tabview.add("Privát Csevegés")

        self.setup_profile_tab()
        if self.current_user["username"] != self.target_username:
            self.setup_chat_tab()

    def setup_profile_tab(self):
        user_data = self.db.get_user(self.target_username)
        if not user_data: return

        is_self = (self.current_user["username"] == self.target_username)

        box = ctk.CTkScrollableFrame(self.profile_tab, fg_color="#141517")
        box.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(box, text="Személyes Adatok", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)

        self.username_entry = ctk.CTkEntry(box, width=300, placeholder_text="Felhasználónév")
        self.username_entry.insert(0, user_data["username"])
        if not is_self: self.username_entry.configure(state="disabled")
        self.username_entry.pack(pady=4)

        self.fullname_entry = ctk.CTkEntry(box, width=300, placeholder_text="Teljes Név")
        self.fullname_entry.insert(0, user_data.get("fullname", ""))
        if not is_self: self.fullname_entry.configure(state="disabled")
        self.fullname_entry.pack(pady=4)

        self.email_entry = ctk.CTkEntry(box, width=300, placeholder_text="Email")
        self.email_entry.insert(0, user_data.get("email", ""))
        if not is_self: self.email_entry.configure(state="disabled")
        self.email_entry.pack(pady=4)

        self.phone_entry = ctk.CTkEntry(box, width=300, placeholder_text="Telefonszám")
        self.phone_entry.insert(0, user_data.get("phone", ""))
        if not is_self: self.phone_entry.configure(state="disabled")
        self.phone_entry.pack(pady=4)

        self.faculty_entry = ctk.CTkEntry(box, width=300, placeholder_text="Kar")
        self.faculty_entry.insert(0, user_data.get("faculty", ""))
        if not is_self: self.faculty_entry.configure(state="disabled")
        self.faculty_entry.pack(pady=4)

        self.major_entry = ctk.CTkEntry(box, width=300, placeholder_text="Szak")
        self.major_entry.insert(0, user_data.get("major", ""))
        if not is_self: self.major_entry.configure(state="disabled")
        self.major_entry.pack(pady=4)

        self.degree_entry = ctk.CTkEntry(box, width=300, placeholder_text="Képzési Szint")
        self.degree_entry.insert(0, user_data.get("degree_level", ""))
        if not is_self: self.degree_entry.configure(state="disabled")
        self.degree_entry.pack(pady=4)

        self.bio_entry = ctk.CTkEntry(box, width=300, placeholder_text="Bemutatkozás...")
        self.bio_entry.insert(0, user_data.get("bio", ""))
        if not is_self: self.bio_entry.configure(state="disabled")
        self.bio_entry.pack(pady=4)

        if is_self:
            ctk.CTkLabel(box, text="Jelszó Módosítása:", font=ctk.CTkFont(weight="bold")).pack(pady=(15, 5))

            self.curr_pass = ctk.CTkEntry(box, width=300, placeholder_text="Jelenlegi jelszó", show="*")
            self.curr_pass.pack(pady=4)

            self.new_pass1 = ctk.CTkEntry(box, width=300, placeholder_text="Új jelszó", show="*")
            self.new_pass1.pack(pady=4)

            self.new_pass2 = ctk.CTkEntry(box, width=300, placeholder_text="Új jelszó újra", show="*")
            self.new_pass2.pack(pady=4)

            self.status_lbl = ctk.CTkLabel(box, text="", font=ctk.CTkFont(size=12))
            self.status_lbl.pack(pady=4)

            save_btn = ctk.CTkButton(box, text="Profil Adatok Mentése", fg_color="#800020", command=self.save_profile)
            save_btn.pack(pady=15)

    def save_profile(self):
        new_u = self.username_entry.get().strip()
        fn = self.fullname_entry.get().strip()
        em = self.email_entry.get().strip()
        ph = self.phone_entry.get().strip()
        fac = self.faculty_entry.get().strip()
        maj = self.major_entry.get().strip()
        deg = self.degree_entry.get().strip()
        bio = self.bio_entry.get().strip()

        cp = self.curr_pass.get().strip()
        np1 = self.new_pass1.get().strip()
        np2 = self.new_pass2.get().strip()

        self.db.update_profile_data(self.current_user["username"], new_u, fn, em, ph, fac, maj, deg, bio)
        self.current_user["username"] = new_u

        if cp or np1 or np2:
            success, msg = self.db.change_password_in_profile(new_u, cp, np1, np2)
            if not success:
                self.status_lbl.configure(text=msg, text_color="#E74C3C")
                return

        # Profil ablak bezárása és a főfórum újrarajzolása
        self.on_update_callback()
        self.destroy()

    def setup_chat_tab(self):
        can_chat, reason = self.db.can_start_chat(self.current_user["username"], self.target_username)
        if not can_chat:
            ctk.CTkLabel(self.chat_tab, text=f"🔒 {reason}", text_color="#E74C3C", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=40)
            return

        self.chat_scroll = ctk.CTkScrollableFrame(self.chat_tab, fg_color="#141517")
        self.chat_scroll.pack(fill="both", expand=True, padx=5, pady=5)

        input_box = ctk.CTkFrame(self.chat_tab, fg_color="#1d1e22")
        input_box.pack(fill="x", pady=5)

        self.msg_entry = ctk.CTkEntry(input_box, placeholder_text="Üzenet írása...", fg_color="#141517")
        self.msg_entry.pack(side="left", fill="x", expand=True, padx=8, pady=8)

        send_btn = ctk.CTkButton(input_box, text="Küldés", width=80, fg_color="#800020", command=self.send_msg)
        send_btn.pack(side="right", padx=8, pady=8)

        self.render_chat()

    def render_chat(self):
        for w in self.chat_scroll.winfo_children(): w.destroy()
        msgs = self.db.get_private_messages(self.current_user["username"], self.target_username)
        for m in msgs:
            is_me = (m["sender"] == self.current_user["username"])
            bubble = ctk.CTkFrame(self.chat_scroll, fg_color="#800020" if is_me else "#212328", corner_radius=8)
            bubble.pack(anchor="e" if is_me else "w", pady=4, padx=8)

            lbl = ctk.CTkLabel(bubble, text=m["content"], text_color="#ffffff")
            lbl.pack(padx=10, pady=5)

    def send_msg(self):
        txt = self.msg_entry.get().strip()
        if txt:
            self.db.send_private_message(self.current_user["username"], self.target_username, txt)
            self.msg_entry.delete(0, "end")
            self.render_chat()


class MainForumFrame(ctk.CTkFrame):
    def __init__(self, parent, db, current_user, on_logout, open_admin_panel):
        super().__init__(parent, fg_color="#141517")
        self.db = db
        self.current_user = current_user
        self.on_logout = on_logout
        self.open_admin_panel = open_admin_panel

        self.selected_subforum_id = None
        self.selected_topic_id = None

        self.setup_ui()

    def setup_ui(self):
        # FONTOS: Előző widgetek letakarítása a többszörös újranyílás megelőzésére!
        for w in self.winfo_children():
            w.destroy()

        navbar = ctk.CTkFrame(self, height=55, fg_color="#1d1e22", corner_radius=0)
        navbar.pack(fill="x")

        logo = ctk.CTkLabel(navbar, text="BME FÓRUM PORTÁL", font=ctk.CTkFont(size=18, weight="bold"), text_color="#800020")
        logo.pack(side="left", padx=20, pady=12)

        if self.current_user.get("role") == "Admin":
            admin_btn = ctk.CTkButton(navbar, text="⚙ ADMIN PANEL", fg_color="#E74C3C", width=120, command=self.open_admin_panel)
            admin_btn.pack(side="left", padx=10)

        has_unread = self.db.has_unread_messages(self.current_user["username"])
        bell_txt = "🔔 (Új üzenet!)" if has_unread else "🔔"
        bell_btn = ctk.CTkButton(navbar, text=bell_txt, width=40, fg_color="#800020" if has_unread else "transparent")
        bell_btn.pack(side="left", padx=10)

        logout_btn = ctk.CTkButton(navbar, text="Kijelentkezés", width=100, fg_color="#2b2c30", command=self.handle_logout)
        logout_btn.pack(side="right", padx=15)

        role_info = ROLES.get(self.current_user.get("role"), ROLES["Hallgató"])
        user_btn = ctk.CTkButton(
            navbar, text=f"{self.current_user['username']} {role_info['label']}", 
            fg_color="transparent", text_color=role_info["color"], font=ctk.CTkFont(weight="bold"),
            command=lambda: self.open_profile(self.current_user['username'])
        )
        user_btn.pack(side="right", padx=10)

        content = ctk.CTkFrame(self, fg_color="#141517")
        content.pack(fill="both", expand=True, padx=15, pady=10)
        content.grid_columnconfigure(0, weight=3)
        content.grid_columnconfigure(1, weight=1)
        content.grid_rowconfigure(0, weight=1)

        self.left_box = ctk.CTkScrollableFrame(content, fg_color="#141517")
        self.left_box.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        right_panel = ctk.CTkFrame(content, fg_color="#1d1e22", corner_radius=8)
        right_panel.grid(row=0, column=1, sticky="nw")

        online_users = [u for u in self.db.get_all_users() if self.db.is_online(u["username"])]

        online_title = ctk.CTkLabel(right_panel, text=f"Online Tagok ({len(online_users)})", font=ctk.CTkFont(size=13, weight="bold"))
        online_title.pack(pady=8, padx=15)

        for u in online_users:
            r_info = ROLES.get(u.get("role", "Hallgató"), ROLES["Hallgató"])
            u_btn = ctk.CTkButton(
                right_panel, text=f"🟢 {u['username']}", fg_color="transparent", 
                text_color=r_info["color"], font=ctk.CTkFont(size=12, weight="bold"), anchor="w",
                command=lambda name=u['username']: self.open_profile(name)
            )
            u_btn.pack(fill="x", padx=10, pady=2)

        self.render_forum_list()

    def handle_logout(self):
        self.db.set_offline(self.current_user["username"])
        self.on_logout()

    def open_profile(self, target_username):
        ProfileAndChatWindow(self, self.db, self.current_user, target_username, on_update_callback=self.setup_ui)

    def render_forum_list(self):
        for w in self.left_box.winfo_children(): w.destroy()

        data = self.db.get_forum_data()
        for cat in data["categories"]:
            cat_hdr = ctk.CTkLabel(self.left_box, text=cat["category"], font=ctk.CTkFont(size=13, weight="bold"), text_color="#888888", anchor="w")
            cat_hdr.pack(fill="x", pady=(12, 4))

            for sf in cat["subforums"]:
                card = ctk.CTkFrame(self.left_box, fg_color="#1d1e22", corner_radius=8)
                card.pack(fill="x", pady=4)

                btn = ctk.CTkButton(card, text=sf["title"], font=ctk.CTkFont(size=14, weight="bold"), fg_color="transparent", anchor="w", command=lambda sf_id=sf["subforum_id"]: self.open_subforum(sf_id))
                btn.pack(fill="x", padx=12, pady=(8, 0))

                desc = ctk.CTkLabel(card, text=sf["description"], font=ctk.CTkFont(size=11), text_color="#aaaaaa", anchor="w")
                desc.pack(fill="x", padx=16, pady=(0, 8))

    def open_subforum(self, subforum_id):
        self.selected_subforum_id = subforum_id
        for w in self.left_box.winfo_children(): w.destroy()

        back_btn = ctk.CTkButton(self.left_box, text="← Vissza a kategóriákhoz", fg_color="transparent", text_color="#800020", anchor="w", command=self.render_forum_list)
        back_btn.pack(fill="x", pady=5)

        new_topic_btn = ctk.CTkButton(self.left_box, text="+ Új Téma Nyitása", fg_color="#800020", command=self.create_topic)
        new_topic_btn.pack(fill="x", pady=5)

        data = self.db.get_forum_data()
        for cat in data["categories"]:
            for sf in cat["subforums"]:
                if sf["subforum_id"] == subforum_id:
                    for top in sf["topics"]:
                        is_deleted = top.get("deleted", False)
                        is_locked = top.get("locked", False)

                        card_color = "#3a1e1e" if is_deleted else "#1d1e22"
                        card = ctk.CTkFrame(self.left_box, fg_color=card_color, corner_radius=8)
                        card.pack(fill="x", pady=4)

                        title_prefix = "🔒 [ARCHIVÁLT] " if is_locked else ""
                        if is_deleted: title_prefix = "❌ [TÖRÖLT TÉMA] "

                        t_btn = ctk.CTkButton(
                            card, text=f"{title_prefix}{top['title']}", fg_color="transparent", 
                            text_color="#888888" if is_deleted else "#ffffff", anchor="w",
                            command=lambda t_id=top["topic_id"]: self.open_topic(subforum_id, t_id)
                        )
                        t_btn.pack(side="left", fill="x", expand=True, padx=12, pady=10)

                        if self.current_user.get("role") == "Admin" or self.current_user["username"] == top["author"]:
                            if is_deleted:
                                rec_btn = ctk.CTkButton(card, text="Visszaállítás", fg_color="#27AE60", width=80, command=lambda t_id=top["topic_id"]: self.restore_topic(t_id))
                                rec_btn.pack(side="right", padx=5)
                            else:
                                del_btn = ctk.CTkButton(card, text="Törlés", fg_color="#E74C3C", width=60, command=lambda t_id=top["topic_id"]: self.delete_topic(t_id))
                                del_btn.pack(side="right", padx=5)

                                lock_btn = ctk.CTkButton(card, text="Nyit/Zár", fg_color="#E67E22", width=60, command=lambda t_id=top["topic_id"]: self.toggle_lock(t_id))
                                lock_btn.pack(side="right", padx=5)

    def open_topic(self, subforum_id, topic_id):
        for w in self.left_box.winfo_children(): w.destroy()

        back_btn = ctk.CTkButton(self.left_box, text="← Vissza a témákhoz", fg_color="transparent", text_color="#800020", anchor="w", command=lambda: self.open_subforum(subforum_id))
        back_btn.pack(fill="x", pady=5)

        data = self.db.get_forum_data()
        for cat in data["categories"]:
            for sf in cat["subforums"]:
                if sf["subforum_id"] == subforum_id:
                    for top in sf["topics"]:
                        if top["topic_id"] == topic_id:
                            if self.current_user.get("role") == "Admin" or self.current_user["username"] == top["author"]:
                                move_bar = ctk.CTkFrame(self.left_box, fg_color="#1d1e22")
                                move_bar.pack(fill="x", pady=5)
                                ctk.CTkLabel(move_bar, text="Téma Átmozgatása:").pack(side="left", padx=10)
                                move_opt = ctk.CTkOptionMenu(move_bar, values=["1 - Központi Hirdetmények", "2 - Python Nagyházi"], command=lambda target, t_id=topic_id: self.move_topic(t_id, target))
                                move_opt.pack(side="left", padx=10)

                            for idx, post in enumerate(top["posts"]):
                                is_p_deleted = post.get("deleted", False)
                                p_color = "#2a1818" if is_p_deleted else "#1d1e22"

                                card = ctk.CTkFrame(self.left_box, fg_color=p_color, corner_radius=8)
                                card.pack(fill="x", pady=4)

                                hdr = ctk.CTkFrame(card, fg_color="transparent")
                                hdr.pack(fill="x", padx=10, pady=(6, 0))

                                auth_lbl = ctk.CTkLabel(hdr, text=post['author'], font=ctk.CTkFont(weight="bold"), text_color="#3498DB")
                                auth_lbl.pack(side="left")

                                if self.current_user.get("role") == "Admin" or self.current_user["username"] == top["author"]:
                                    if is_p_deleted:
                                        rec_btn = ctk.CTkButton(hdr, text="Visszaállítás", fg_color="#27AE60", width=70, height=22, command=lambda p_idx=idx: self.restore_post(topic_id, p_idx))
                                        rec_btn.pack(side="right")
                                    else:
                                        del_btn = ctk.CTkButton(hdr, text="Törlés", fg_color="#E74C3C", width=50, height=22, command=lambda p_idx=idx: self.delete_post(topic_id, p_idx))
                                        del_btn.pack(side="right")

                                txt = f"❌ [TÖRÖLT BEJEGYZÉS]: {post['content']}" if is_p_deleted else post['content']
                                content_lbl = ctk.CTkLabel(card, text=txt, text_color="#888888" if is_p_deleted else "#ffffff", wraplength=520, justify="left", anchor="w")
                                content_lbl.pack(anchor="w", padx=12, pady=(4, 8))

                            if not top.get("locked", False):
                                input_frame = ctk.CTkFrame(self.left_box, fg_color="#1d1e22")
                                input_frame.pack(fill="x", pady=12)

                                self.reply_entry = ctk.CTkEntry(input_frame, placeholder_text="Írj hozzászólást...", fg_color="#141517", height=38)
                                self.reply_entry.pack(side="left", fill="x", expand=True, padx=8, pady=8)

                                send_btn = ctk.CTkButton(input_frame, text="Küldés", width=90, height=38, fg_color="#800020", command=lambda: self.send_reply(subforum_id, topic_id))
                                send_btn.pack(side="right", padx=8, pady=8)
                            else:
                                ctk.CTkLabel(self.left_box, text="🔒 Ez a téma le van zárva.", text_color="#E67E22").pack(pady=10)

    def move_topic(self, topic_id, target_str):
        target_id = int(target_str.split(" - ")[0])
        self.db.move_topic(topic_id, target_id)
        self.open_subforum(self.selected_subforum_id)

    def toggle_lock(self, topic_id):
        self.db.toggle_topic_lock(topic_id)
        self.open_subforum(self.selected_subforum_id)

    def delete_topic(self, topic_id):
        self.db.toggle_topic_deletion(topic_id, True)
        self.open_subforum(self.selected_subforum_id)

    def restore_topic(self, topic_id):
        self.db.toggle_topic_deletion(topic_id, False)
        self.open_subforum(self.selected_subforum_id)

    def delete_post(self, topic_id, post_index):
        self.db.toggle_post_deletion(topic_id, post_index, True)
        self.open_topic(self.selected_subforum_id, topic_id)

    def restore_post(self, topic_id, post_index):
        self.db.toggle_post_deletion(topic_id, post_index, False)
        self.open_topic(self.selected_subforum_id, topic_id)

    def send_reply(self, subforum_id, topic_id):
        text = self.reply_entry.get().strip()
        if text:
            self.db.add_post(subforum_id, topic_id, self.current_user["username"], text)
            self.open_topic(subforum_id, topic_id)

    def create_topic(self):
        dialog = ctk.CTkInputDialog(text="Új téma címe:", title="Téma Nyitása")
        t_title = dialog.get_input()
        if t_title and t_title.strip():
            self.db.add_topic(self.selected_subforum_id, t_title.strip(), self.current_user["username"])
            self.open_subforum(self.selected_subforum_id)