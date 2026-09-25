import requests

# Ha elindul a felhős szervered, csak ezt az URL-t kell átírnod!
SERVER_URL = "http://127.0.0.1:5000"  # Pl.: "https://bme-forum.onrender.com"

class ClientAPI:
    def login(self, username, password):
        try:
            res = requests.post(f"{SERVER_URL}/login", json={"username": username, "password": password})
            return res.json()["success"], res.json()["message"], res.json()["user"]
        except Exception as e:
            return False, f"Szerver elérésési hiba: {e}", None

    def register(self, username, fullname, email, phone, neptun, faculty, major, degree, pass1, pass2):
        try:
            res = requests.post(f"{SERVER_URL}/register", json={
                "username": username, "fullname": fullname, "email": email, "phone": phone,
                "neptun": neptun, "faculty": faculty, "major": major, "degree": degree,
                "pass1": pass1, "pass2": pass2
            })
            return res.json()["success"], res.json()["message"]
        except Exception as e:
            return False, f"Szerver elérésési hiba: {e}"

    def get_forum_data(self):
        return requests.get(f"{SERVER_URL}/forum_data").json()

    def add_topic(self, subforum_id, title, author):
        requests.post(f"{SERVER_URL}/add_topic", json={"subforum_id": subforum_id, "title": title, "author": author})

    def add_post(self, subforum_id, topic_id, author, content):
        requests.post(f"{SERVER_URL}/add_post", json={"subforum_id": subforum_id, "topic_id": topic_id, "author": author, "content": content})

    def get_all_users(self):
        return requests.get(f"{SERVER_URL}/users").json()

    def send_private_message(self, sender, receiver, content):
        requests.post(f"{SERVER_URL}/send_pm", json={"sender": sender, "receiver": receiver, "content": content})

    def get_private_messages(self, user1, user2):
        return requests.post(f"{SERVER_URL}/get_pms", json={"user1": user1, "user2": user2}).json()

    def send_heartbeat(self, username):
        requests.post(f"{SERVER_URL}/heartbeat", json={"username": username})