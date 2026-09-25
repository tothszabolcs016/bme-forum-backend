import customtkinter as ctk

class AuthFrame(ctk.CTkFrame):
    def __init__(self, parent, db, on_login_success):
        super().__init__(parent, fg_color="#141517")
        self.db = db
        self.on_login_success = on_login_success

        self.box = ctk.CTkFrame(self, width=440, height=640, corner_radius=12, fg_color="#1d1e22", border_color="#800020", border_width=1)
        self.box.pack_propagate(False)
        self.box.place(relx=0.5, rely=0.5, anchor="center")

        self.show_login_mode()

    def clear_box(self):
        for widget in self.box.winfo_children():
            widget.destroy()

    def show_login_mode(self):
        self.clear_box()

        title = ctk.CTkLabel(self.box, text="BME DIÁKFÓRUM", font=ctk.CTkFont(size=24, weight="bold"), text_color="#800020")
        title.pack(padx=20, pady=(40, 5))

        subtitle = ctk.CTkLabel(self.box, text="Központi Hallgatói és Oktatói Portál", font=ctk.CTkFont(size=12), text_color="#aaaaaa")
        subtitle.pack(pady=(0, 25))

        self.user_entry = ctk.CTkEntry(self.box, placeholder_text="Felhasználónév", width=260, height=40, fg_color="#141517")
        self.user_entry._entry.configure(justify="center")
        self.user_entry.pack(pady=8)

        self.pass_entry = ctk.CTkEntry(self.box, placeholder_text="Jelszó", show="*", width=260, height=40, fg_color="#141517")
        self.pass_entry._entry.configure(justify="center")
        self.pass_entry.pack(pady=8)

        self.status_lbl = ctk.CTkLabel(self.box, text="", font=ctk.CTkFont(size=12))
        self.status_lbl.pack(pady=4)

        btn_login = ctk.CTkButton(
            self.box, text="BEJELENTKEZÉS", width=260, height=42, corner_radius=8,
            fg_color="#800020", hover_color="#5B0017", font=ctk.CTkFont(weight="bold"),
            command=self.handle_login
        )
        btn_login.pack(pady=10)

        forgot_btn = ctk.CTkButton(self.box, text="Elfelejtett jelszó?", fg_color="transparent", text_color="#aaaaaa", hover_color="#1d1e22", command=self.show_forgot_password_dialog)
        forgot_btn.pack(pady=2)

        btn_switch = ctk.CTkButton(self.box, text="Még nincs fiókod? Regisztráció", fg_color="transparent", text_color="#800020", hover_color="#1d1e22", command=self.show_register_mode)
        btn_switch.pack(pady=8)

    def show_register_mode(self):
        self.clear_box()

        title = ctk.CTkLabel(self.box, text="BME REGISZTRÁCIÓ", font=ctk.CTkFont(size=20, weight="bold"), text_color="#800020")
        title.pack(padx=20, pady=(15, 5))

        self.reg_user = ctk.CTkEntry(self.box, placeholder_text="Felhasználónév", width=260, height=34, fg_color="#141517")
        self.reg_user._entry.configure(justify="center")
        self.reg_user.pack(pady=4)

        self.reg_fullname = ctk.CTkEntry(self.box, placeholder_text="Teljes Név", width=260, height=34, fg_color="#141517")
        self.reg_fullname._entry.configure(justify="center")
        self.reg_fullname.pack(pady=4)

        self.reg_email = ctk.CTkEntry(self.box, placeholder_text="Egyetemi Email (.bme.hu)", width=260, height=34, fg_color="#141517")
        self.reg_email._entry.configure(justify="center")
        self.reg_email.pack(pady=4)

        self.reg_phone = ctk.CTkEntry(self.box, placeholder_text="Telefonszám (+36...)", width=260, height=34, fg_color="#141517")
        self.reg_phone._entry.configure(justify="center")
        self.reg_phone.pack(pady=4)

        self.reg_neptun = ctk.CTkEntry(self.box, placeholder_text="Neptun Kód", width=260, height=34, fg_color="#141517")
        self.reg_neptun._entry.configure(justify="center")
        self.reg_neptun.pack(pady=4)

        # Kar és Szak Választó
        self.faculty_opt = ctk.CTkOptionMenu(self.box, values=["VIK (Villamosmérnöki és Informatikai Kar)", "ÉPK (Építészmérnöki Kar)", "GTK (Gazdaság- és Társadalomtudományi Kar)"], width=260)
        self.faculty_opt.pack(pady=4)

        self.major_opt = ctk.CTkOptionMenu(self.box, values=["Mérnökinformatikus", "Üzemmérnökinformatikus", "Villamosmérnök"], width=260)
        self.major_opt.pack(pady=4)

        self.degree_opt = ctk.CTkOptionMenu(self.box, values=["BSc", "BProf", "MSc", "PhD"], width=260)
        self.degree_opt.pack(pady=4)

        self.reg_pass1 = ctk.CTkEntry(self.box, placeholder_text="Jelszó", show="*", width=260, height=34, fg_color="#141517")
        self.reg_pass1._entry.configure(justify="center")
        self.reg_pass1.pack(pady=4)

        self.reg_pass2 = ctk.CTkEntry(self.box, placeholder_text="Jelszó újra", show="*", width=260, height=34, fg_color="#141517")
        self.reg_pass2._entry.configure(justify="center")
        self.reg_pass2.pack(pady=4)

        self.status_lbl = ctk.CTkLabel(self.box, text="", font=ctk.CTkFont(size=12))
        self.status_lbl.pack(pady=2)

        btn_reg = ctk.CTkButton(
            self.box, text="REGISZTRÁCIÓ", width=260, height=38, corner_radius=8,
            fg_color="#800020", hover_color="#5B0017", font=ctk.CTkFont(weight="bold"),
            command=self.handle_register
        )
        btn_reg.pack(pady=6)

        btn_switch = ctk.CTkButton(self.box, text="Vissza a bejelentkezéshez", fg_color="transparent", text_color="#aaaaaa", command=self.show_login_mode)
        btn_switch.pack(pady=2)

    def handle_login(self):
        u = self.user_entry.get().strip()
        p = self.pass_entry.get().strip()
        success, msg, user_data = self.db.login_user(u, p)
        if success:
            self.on_login_success(user_data)
        else:
            self.status_lbl.configure(text=msg, text_color="#E74C3C")

    def handle_register(self):
        u = self.reg_user.get().strip()
        fn = self.reg_fullname.get().strip()
        em = self.reg_email.get().strip()
        ph = self.reg_phone.get().strip()
        nep = self.reg_neptun.get().strip()
        fac = self.faculty_opt.get()
        maj = self.major_opt.get()
        deg = self.degree_opt.get()
        p1 = self.reg_pass1.get().strip()
        p2 = self.reg_pass2.get().strip()

        success, msg = self.db.register_user(u, fn, em, ph, nep, fac, maj, deg, p1, p2)
        if success:
            self.show_login_mode()
            self.status_lbl.configure(text=msg, text_color="#2ECC71")
        else:
            self.status_lbl.configure(text=msg, text_color="#E74C3C")

    def show_forgot_password_dialog(self):
        dialog = ctk.CTkInputDialog(text="Adj meg az egyetemi e-mail címed:", title="Elfelejtett Jelszó")
        email = dialog.get_input()
        if email and email.strip():
            success, msg = self.db.send_password_reset_email(email.strip())
            self.status_lbl.configure(text=msg, text_color="#2ECC71" if success else "#E74C3C")