import json
import os
import hashlib
import smtplib
import uuid
from email.mime.text import MIMEText

USERS_FILE = "users.json"
FORUM_FILE = "forum_data.json"

ROLES = {
    "Admin": {"color": "#E74C3C", "label": "[ADMIN]"},
    "Oktató": {"color": "#3498DB", "label": "[OKTATÓ]"},
    "Hallgató": {"color": "#800020", "label": "[HALLGATÓ]"}
}

FACULTIES = {
    "VIK (Villamosmérnöki és Informatikai Kar)": {
        "Mérnökinformatikus": ["BSc", "MSc", "PhD"],
        "Üzemmérnökinformatikus": ["BProf"],
        "Villamosmérnök": ["BSc", "MSc", "PhD"]
    },
    "ÉPK (Építészmérnöki Kar)": {
        "Építészmérnök": ["BSc", "MSc"]
    },
    "GTK (Gazdaság- és Társadalomtudományi Kar)": {
        "Műszaki Menedzser": ["BSc", "MSc"]
    }
}

class JsonDataManager:
    def __init__(self):
        self.active_sessions = set()
        self.init_files()

    def _hash_password(self, password):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def init_files(self):
        if not os.path.exists(USERS_FILE):
            default_users = [
                {
                    "username": "admin",
                    "fullname": "Rendszergazda Admin",
                    "email": "admin@bme.hu",
                    "phone": "+36301234567",
                    "neptun": "BMEADM",
                    "password_hash": self._hash_password("admin123"),
                    "role": "Admin",
                    "faculty": "VIK (Villamosmérnöki és Informatikai Kar)",
                    "major": "Mérnökinformatikus",
                    "degree_level": "MSc",
                    "bio": "A BME Fórum hivatalos adminisztrátora.",
                    "friends": ["dr_kovacs"],
                    "friend_requests": []
                },
                {
                    "username": "dr_kovacs",
                    "fullname": "Dr. Kovács Péter",
                    "email": "kovacs@vik.bme.hu",
                    "phone": "+36309876543",
                    "neptun": "KOV001",
                    "password_hash": self._hash_password("oktato123"),
                    "role": "Oktató",
                    "faculty": "VIK (Villamosmérnöki és Informatikai Kar)",
                    "major": "Mérnökinformatikus",
                    "degree_level": "MSc",
                    "bio": "Szoftverfejlesztés oktató.",
                    "friends": ["admin"],
                    "friend_requests": []
                },
                {
                    "username": "hallgato_peti",
                    "fullname": "Nagy Péter",
                    "email": "peti@hvt.bme.hu",
                    "phone": "+36201112233",
                    "neptun": "PET002",
                    "password_hash": self._hash_password("diak123"),
                    "role": "Hallgató",
                    "faculty": "VIK (Villamosmérnöki és Informatikai Kar)",
                    "major": "Mérnökinformatikus",
                    "degree_level": "BSc",
                    "bio": "Mérnökinformatikus BSc hallgató.",
                    "friends": [],
                    "friend_requests": []
                }
            ]
            with open(USERS_FILE, "w", encoding="utf-8") as f:
                json.dump(default_users, f, ensure_ascii=False, indent=4)

        if not os.path.exists(FORUM_FILE):
            default_data = {
                "categories": [
                    {
                        "category": "BME - HÍREK ÉS TÁJÉKOZTATÓK",
                        "subforums": [
                            {
                                "subforum_id": 1,
                                "title": "Központi Hirdetmények",
                                "description": "Rektori és Dékáni utasítások, tanévrendi információk",
                                "topics": [
                                    {
                                        "topic_id": 101,
                                        "title": "2026/27 I. Félév Regisztrációs Hét",
                                        "author": "admin",
                                        "created_at": "2026-09-01",
                                        "deleted": False,
                                        "locked": False,
                                        "posts": [
                                            {"author": "admin", "content": "Fontos információk a Neptun tárgyfelvétellel kapcsolatban...", "deleted": False},
                                            {"author": "hallgato_peti", "content": "Köszönjük a tájékoztatást!", "deleted": False}
                                        ]
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "category": "VILLAMOSMÉRNÖKI ÉS INFORMATIKAI KAR (VIK)",
                        "subforums": [
                            {
                                "subforum_id": 2,
                                "title": "Szoftverfejlesztés / Python Nagyházi",
                                "description": "Nagyházi feladatok, architektúrák, GUI fejlesztés",
                                "topics": []
                            }
                        ]
                    }
                ],
                "private_chats": []
            }
            with open(FORUM_FILE, "w", encoding="utf-8") as f:
                json.dump(default_data, f, ensure_ascii=False, indent=4)

    # --- ONLINE STATUS ---
    def set_online(self, username): self.active_sessions.add(username)
    def set_offline(self, username): self.active_sessions.discard(username)
    def is_online(self, username): return username in self.active_sessions

    # --- USER & PROFILE ---
    def get_all_users(self):
        with open(USERS_FILE, "r", encoding="utf-8") as f: return json.load(f)

    def save_all_users(self, users):
        with open(USERS_FILE, "w", encoding="utf-8") as f: json.dump(users, f, ensure_ascii=False, indent=4)

    def get_user(self, username):
        for u in self.get_all_users():
            if u["username"] == username: return u
        return None

    def update_profile_data(self, old_username, new_username, fullname, email, phone, faculty, major, degree, bio):
        users = self.get_all_users()
        for u in users:
            if u["username"] == old_username:
                u["username"] = new_username
                u["fullname"] = fullname
                u["email"] = email
                u["phone"] = phone
                u["faculty"] = faculty
                u["major"] = major
                u["degree_level"] = degree
                u["bio"] = bio
                break
        self.save_all_users(users)

    def change_password_in_profile(self, username, current_pass, new_pass1, new_pass2):
        if new_pass1 != new_pass2: return False, "A két új jelszó nem egyezik meg!"
        users = self.get_all_users()
        user = next((u for u in users if u["username"] == username), None)
        if user and user["password_hash"] == self._hash_password(current_pass):
            user["password_hash"] = self._hash_password(new_pass1)
            self.save_all_users(users)
            return True, "Jelszó megváltoztatva!"
        return False, "A jelenlegi jelszó helytelen!"

    def register_user(self, username, fullname, email, phone, neptun, faculty, major, degree, pass1, pass2):
        if not all([username, fullname, email, phone, neptun, pass1, pass2]):
            return False, "Minden mező kitöltése kötelező!"
        if pass1 != pass2:
            return False, "A megadott jelszavak nem egyeznek!"
        users = self.get_all_users()
        for u in users:
            if u["username"].lower() == username.lower(): return False, "Ez a felhasználónév foglalt!"
        users.append({
            "username": username, "fullname": fullname, "email": email, "phone": phone,
            "neptun": neptun.upper(), "faculty": faculty, "major": major, "degree_level": degree,
            "password_hash": self._hash_password(pass1), "role": "Hallgató", "bio": f"{faculty} hallgató.",
            "friends": [], "friend_requests": []
        })
        self.save_all_users(users)
        return True, "Sikeres regisztráció!"

    def login_user(self, username, password):
        users = self.get_all_users()
        p_hash = self._hash_password(password)
        for u in users:
            if u["username"].lower() == username.lower() and u["password_hash"] == p_hash:
                self.set_online(u["username"])
                return True, "Sikeres bejelentkezés!", u
        return False, "Hibás felhasználónév vagy jelszó!", None

    def send_password_reset_email(self, email):
        users = self.get_all_users()
        user = next((u for u in users if u["email"].lower() == email.lower()), None)
        if not user: return False, "Nem található felhasználó ezzel az e-mail címmel!"
        reset_code = "BME-" + str(os.urandom(2).hex().upper())
        return True, f"A visszaállító kódot elküldtük az e-mail címedre! (Kód: {reset_code})"

    # --- CHAT & FRIENDS ---
    def can_start_chat(self, sender_username, receiver_username):
        sender = self.get_user(sender_username)
        receiver = self.get_user(receiver_username)
        if not sender or not receiver: return False, "Felhasználó nem található."
        if sender["role"] in ["Admin", "Oktató"]:
            if sender["role"] == "Oktató" and sender["faculty"] != receiver["faculty"]:
                return False, "Oktatóként csak a saját karodhoz tartozó hallgatóknak írhatsz!"
            return True, "Engedélyezve"
        if receiver_username in sender.get("friends", []): return True, "Engedélyezve"
        return False, "Privát üzenetet csak visszaigazolt barátoknak küldhetsz!"

    def send_private_message(self, sender, receiver, content):
        data = self._load_forum()
        
        # JAVÍTÁS: Biztosítjuk, hogy a private_chats szótár (dict) legyen, még ha a JSON-ben listaként is maradt meg
        if "private_chats" not in data or isinstance(data.get("private_chats"), list):
            data["private_chats"] = {}
            
        chat_id = tuple(sorted([sender, receiver]))
        chat_key = f"{chat_id[0]}_{chat_id[1]}"
        
        if chat_key not in data["private_chats"]:
            data["private_chats"][chat_key] = []
        
        data["private_chats"][chat_key].append({"sender": sender, "content": content})
        self._save_forum(data)
        
        # Értesítés küldése a fogadónak
        self.add_notification(receiver, "Új privát üzenet", f"{sender} üzenetet küldött neked.", "pm", sender)

    def get_private_messages(self, user1, user2):
        data = self._load_forum()
        
        # JAVÍTÁS ITT IS: Ha véletlenül lista, akkor üresként kezeljük, hogy ne omoljon össze az olvasás
        if "private_chats" not in data or isinstance(data.get("private_chats"), list):
            return []
            
        chat_id = tuple(sorted([user1, user2]))
        chat_key = f"{chat_id[0]}_{chat_id[1]}"
        return data["private_chats"].get(chat_key, [])

    def add_post(self, subforum_id, topic_id, author, content):
        data = self._load_forum()
        for cat in data["categories"]:
            for sf in cat["subforums"]:
                if sf["subforum_id"] == subforum_id:
                    for top in sf["topics"]:
                        if top["topic_id"] == topic_id:
                            top["posts"].append({"author": author, "content": content, "deleted": False})
                            self._save_forum(data)
                            
                            # 🚀 ÚJ: Értesítés a téma írójának (ha nem saját magának válaszolt)
                            if top["author"] != author:
                                self.add_notification(
                                    top["author"], "Új hozzászólás", 
                                    f"{author} válaszolt a témádra: {top['title']}", 
                                    "topic", {"subforum_id": subforum_id, "topic_id": topic_id}
                                )
                            return

    def has_unread_messages(self, username):
        data = self.get_forum_data()
        for msg in data.get("private_chats", []):
            if msg["receiver"] == username and not msg.get("read", False): return True
        return False

    # --- FORUM OPERATIONS (FULL MODERATION) ---
    def get_forum_data(self):
        with open(FORUM_FILE, "r", encoding="utf-8") as f: return json.load(f)

    def save_forum_data(self, data):
        with open(FORUM_FILE, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=4)

    def add_topic(self, subforum_id, title, author):
        data = self.get_forum_data()
        for cat in data["categories"]:
            for sf in cat["subforums"]:
                if sf["subforum_id"] == subforum_id:
                    sf["topics"].append({
                        "topic_id": len(sf["topics"]) + 201,
                        "title": title,
                        "author": author,
                        "created_at": "2026-09-25",
                        "deleted": False,
                        "locked": False,
                        "posts": []
                    })
                    break
        self.save_forum_data(data)

    def toggle_topic_deletion(self, topic_id, delete_state=True):
        data = self.get_forum_data()
        for cat in data["categories"]:
            for sf in cat["subforums"]:
                for top in sf["topics"]:
                    if top["topic_id"] == topic_id:
                        top["deleted"] = delete_state
                        break
        self.save_forum_data(data)

    def toggle_post_deletion(self, topic_id, post_index, delete_state=True):
        data = self.get_forum_data()
        for cat in data["categories"]:
            for sf in cat["subforums"]:
                for top in sf["topics"]:
                    if top["topic_id"] == topic_id:
                        if 0 <= post_index < len(top["posts"]):
                            top["posts"][post_index]["deleted"] = delete_state
                        break
        self.save_forum_data(data)

    def toggle_topic_lock(self, topic_id):
        data = self.get_forum_data()
        for cat in data["categories"]:
            for sf in cat["subforums"]:
                for top in sf["topics"]:
                    if top["topic_id"] == topic_id:
                        top["locked"] = not top.get("locked", False)
                        break
        self.save_forum_data(data)

    def move_topic(self, topic_id, target_subforum_id):
        data = self.get_forum_data()
        moved_topic = None
        for cat in data["categories"]:
            for sf in cat["subforums"]:
                for top in sf["topics"]:
                    if top["topic_id"] == topic_id:
                        moved_topic = top
                        sf["topics"].remove(top)
                        break
        if moved_topic:
            for cat in data["categories"]:
                for sf in cat["subforums"]:
                    if sf["subforum_id"] == target_subforum_id:
                        sf["topics"].append(moved_topic)
                        break
        self.save_forum_data(data)

    def update_user_role(self, username, new_role):
        users = self.get_all_users()
        for u in users:
            if u["username"] == username:
                u["role"] = new_role
                break
        self.save_all_users(users)

    def delete_user(self, username):
        users = [u for u in self.get_all_users() if u["username"] != username]
        self.save_all_users(users)
        self.set_offline(username)

    def add_notification(self, username, title, message, target_type, target_data):
        users = self._load_users()
        for u in users:
            if u["username"] == username:
                if "notifications" not in u:
                    u["notifications"] = []
                # Új értesítés beszúrása a lista elejére
                u["notifications"].insert(0, {
                    "id": str(uuid.uuid4()),
                    "title": title,
                    "message": message,
                    "target_type": target_type,
                    "target_data": target_data,
                    "is_read": False
                })
                self._save_users(users)
                break

    def get_notifications(self, username):
        for u in self._load_users():
            if u["username"] == username:
                return u.get("notifications", [])
        return []

    def mark_notification_read(self, username, notif_id):
        users = self._load_users()
        for u in users:
            if u["username"] == username:
                for n in u.get("notifications", []):
                    if n["id"] == notif_id:
                        n["is_read"] = True
                self._save_users(users)
                break

    def _load_users(self):
        import json
        try:
            with open("users.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def _save_users(self, data):
        import json
        with open("users.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def _load_forum(self):
        import json
        try:
            with open("forum_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"categories": [], "private_chats": {}}

    def _save_forum(self, data):
        import json
        with open("forum_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)