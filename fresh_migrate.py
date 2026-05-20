import os
import shutil

print("===================================================")
print("     Memulai Proses Django Fresh Migrate...        ")
print("===================================================")

if os.path.exists("db.sqlite3"):
    print("\n[1/4] Menghapus db.sqlite3...")
    os.remove("db.sqlite3")
    print("      Berhasil.")
else:
    print("\n[1/4] db.sqlite3 tidak ditemukan, lanjut...")

print("\n[2/4] Membersihkan file migrasi di app lokal...")
for root, dirs, files in os.walk("."):
    if "venv" in root or "env" in root or ".venv" in root or ".git" in root:
        continue
        
    if os.path.basename(root) == "migrations":
        print(f"      Membersihkan: {root}")
        for file in files:
            if file != "__init__.py" and (file.endswith(".py") or file.endswith(".pyc")):
                os.remove(os.path.join(root, file))
        
        init_path = os.path.join(root, "__init__.py")
        if not os.path.exists(init_path):
            with open(init_path, "w") as f:
                pass
print("      Selesai membersihkan migrations.")

print("\n[3/4] Menjalankan makemigrations...")
os.system("python manage.py makemigrations")

print("\n[4/4] Menjalankan migrate...")
os.system("python manage.py migrate")

print("\n===================================================")
print("      Fresh Migrate Selesai! Database bersih.")
print("===================================================")