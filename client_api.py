import requests

# FONTOS: IDE A SAJÁT RENDER.COM CÍMEDET ÍRD! (Ne legyen a végén /)
SERVER_URL = "https://bme-forum-backend.onrender.com"

class ClientAPI:
    def __init__(self):
        print(f"[Rendszer] Csatlakozás a felhőhöz: {SERVER_URL}")

    def _call(self, method_name, *args):
        try:
            res = requests.post(f"{SERVER_URL}/api/call", json={"method": method_name, "args": args})
            data = res.json()
            if data.get("status") == "success":
                return data.get("result")
            else:
                print(f"[Szerverhiba - {method_name}]: {data.get('message')}")
                return None
        except Exception as e:
            print(f"[Hálózati hiba - {method_name}]: {e}")
            return None

    # --- Hitelésítés ---
    def login_user(self, username, password):
        res = self._call("login_user", username, password)
        return res if res else (False, "Szerver elérésési hiba", None)

    def register_user(self, username, fullname, email, phone, neptun, faculty, major, degree, pass1, pass2):
        res = self._call("register_user", username, fullname, email, phone, neptun, faculty, major, degree, pass1, pass2)
        return res if res else (False, "Szerver elérésési hiba")

    def send_password_reset_email(self, email):
        res = self._call("send_password_reset_email", email)
        return res if res else (False, "Szerverhiba")

    # --- Felhasználók & Profil ---
    def get_all_users(self): return self._call("get_all_users") or []
    def get_user(self, username): return self._call("get_user", username)
    def update_profile_data(self, *args): return self._call("update_profile_data", *args)
    def update_user_role(self, *args): return self._call("update_user_role", *args)
    def delete_user(self, *args): return self._call("delete_user", *args)
    def change_password_in_profile(self, *args): 
        res = self._call("change_password_in_profile", *args)
        return res if res else (False, "Szerverhiba")

    # --- Online Státusz (Heartbeat) ---
    def is_online(self, username): return self._call("is_online", username)
    def send_heartbeat(self, username): self._call("set_online", username)
    def set_offline(self, username): self._call("set_offline", username)

    # --- Privát Üzenetek ---
    def can_start_chat(self, *args): 
        res = self._call("can_start_chat", *args)
        return res if res else (False, "Szerverhiba")
    def get_private_messages(self, *args): return self._call("get_private_messages", *args) or []
    def send_private_message(self, *args): return self._call("send_private_message", *args)
    def has_unread_messages(self, *args): return self._call("has_unread_messages", *args)

    # --- Fórum Moderáció és Adatok ---
    def get_forum_data(self): 
        return self._call("get_forum_data") or {"categories": [], "private_chats": []}
        
    def add_topic(self, *args): return self._call("add_topic", *args)
    def add_post(self, *args): return self._call("add_post", *args)
    def toggle_topic_deletion(self, *args): return self._call("toggle_topic_deletion", *args)
    def toggle_post_deletion(self, *args): return self._call("toggle_post_deletion", *args)
    def toggle_topic_lock(self, *args): return self._call("toggle_topic_lock", *args)
    def move_topic(self, *args): return self._call("move_topic", *args)