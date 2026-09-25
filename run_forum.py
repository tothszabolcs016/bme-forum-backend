import sys
import subprocess

print("🚀 Keresem a legújabb frissítéseket a GitHubról...")

try:
    # Git pull parancs futtatása
    result = subprocess.run(["git", "pull", "origin", "main"], check=True)
    print("\n✅ Frissítés sikeres! Fórum indítása...\n")
except Exception as e:
    print("\n⚠️ Nem sikerült a frissítés (nincs internet vagy Git a gépen). Indítás a meglévő verzióval...\n")

# A main.py elindítása azzal a Pythonnal, amivel ezt a szkriptet futtatják
subprocess.run([sys.executable, "main.py"])