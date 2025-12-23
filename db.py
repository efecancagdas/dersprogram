import sqlite3
import pandas as pd
import os

# -----------------------------
# 0. ESKİ VERİTABANINI SİL
# -----------------------------
if os.path.exists("okul.db"):
    os.remove("okul.db")
    print("⚠️ Mevcut okul.db dosyası silindi.")

# -----------------------------
# 1. VERİTABANI BAĞLANTISI
# -----------------------------
conn = sqlite3.connect("okul.db")
cursor = conn.cursor()

# -----------------------------
# 2. TABLOLAR
# -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS OgretimUyeleri (
    uye_id INTEGER PRIMARY KEY AUTOINCREMENT,
    isim TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Dersler (
    ders_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ders_adi TEXT NOT NULL,
    sinif TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Derslikler (
    derslik_id INTEGER PRIMARY KEY AUTOINCREMENT,
    derslik_adi TEXT NOT NULL,
    kontenjan INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS OgretimUyeleriDersler (
    uye_id INTEGER,
    ders_id INTEGER,
    sinif TEXT NOT NULL,
    FOREIGN KEY (uye_id) REFERENCES OgretimUyeleri(uye_id),
    FOREIGN KEY (ders_id) REFERENCES Dersler(ders_id)
)
""")

conn.commit()

# -----------------------------
# 3. EXCEL'DEN VERİLERİ OKU
# -----------------------------
def veri_ekle(excel_dosyasi="dersler.xlsx"):
    # Excel sayfalarını oku
    df_uyeler = pd.read_excel(excel_dosyasi, sheet_name="OgretimUyeleri")
    df_dersler = pd.read_excel(excel_dosyasi, sheet_name="Dersler")
    df_derslikler = pd.read_excel(excel_dosyasi, sheet_name="Derslikler")
    df_uyeler_dersler = pd.read_excel(excel_dosyasi, sheet_name="OgretimUyeleriDersler")

    # Öğretim üyelerini ekle
    for isim in df_uyeler["OgretimUyesi"]:
        cursor.execute("INSERT INTO OgretimUyeleri (isim) VALUES (?)", (isim.strip(),))

    # Dersleri ekle
    for _, row in df_dersler.iterrows():
        cursor.execute(
            "INSERT INTO Dersler (ders_adi, sinif) VALUES (?, ?)",
            (row["Dersler"].strip(), row["Sinif"].strip())
        )

    # Derslikleri ve kontenjanlarını ekle
    if "Kontenjan" in df_derslikler.columns:
        for _, row in df_derslikler.iterrows():
            cursor.execute(
                "INSERT INTO Derslikler (derslik_adi, kontenjan) VALUES (?, ?)",
                (row["Derslikler"].strip(), int(row["Kontenjan"]))
            )
    else:
        for dl in df_derslikler["Derslikler"]:
            cursor.execute(
                "INSERT INTO Derslikler (derslik_adi) VALUES (?)",
                (dl.strip(),)
            )

    conn.commit()

    # Öğretim üyeleri → hangi dersleri verecek
    cursor.execute("SELECT uye_id, isim FROM OgretimUyeleri")
    uye_listesi = cursor.fetchall()
    cursor.execute("SELECT ders_id, ders_adi FROM Dersler")
    ders_listesi = cursor.fetchall()

    # Büyük harfe çevirerek eşleştirme (KeyError önlemi)
    uye_adi_to_id = {isim.strip().upper(): uye_id for uye_id, isim in uye_listesi}
    ders_adi_to_id = {ders_adi.strip().upper(): ders_id for ders_id, ders_adi in ders_listesi}

    for _, row in df_uyeler_dersler.iterrows():
        uye_id = uye_adi_to_id[row["OgretimUyesi"].strip().upper()]
        ders_id = ders_adi_to_id[row["Ders"].strip().upper()]
        sinif = row["Sinif"].strip()
        cursor.execute(
            "INSERT INTO OgretimUyeleriDersler (uye_id, ders_id, sinif) VALUES (?, ?, ?)",
            (uye_id, ders_id, sinif)
        )

    conn.commit()

# -----------------------------
# 4. VERİ EKLE VE DB OLUŞTUR
# -----------------------------
veri_ekle()
print("✅ okul.db oluşturuldu! Veriler dersler.xlsx dosyasından alındı.")
