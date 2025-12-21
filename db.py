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

# Tablolar
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
    derslik_adi TEXT NOT NULL
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
# 2. VERİLERİ EXCEL'DEN OKU
# -----------------------------
def veri_ekle(excel_dosyasi="dersler.xlsx"):
    # Excel'deki sayfaları oku
    df_uyeler = pd.read_excel(excel_dosyasi, sheet_name="OgretimUyeleri")
    df_dersler = pd.read_excel(excel_dosyasi, sheet_name="Dersler")
    df_derslikler = pd.read_excel(excel_dosyasi, sheet_name="Derslikler")
    df_uyeler_dersler = pd.read_excel(excel_dosyasi, sheet_name="OgretimUyeleriDersler")

    # Öğretim üyelerini ekle
    for isim in df_uyeler["OgretimUyesi"]:
        cursor.execute("INSERT INTO OgretimUyeleri (isim) VALUES (?)", (isim,))

    # Dersleri ekle (sinif ile birlikte)
    for _, row in df_dersler.iterrows():
        cursor.execute(
            "INSERT INTO Dersler (ders_adi, sinif) VALUES (?, ?)",
            (row["Dersler"], row["Sinif"])
        )

    # Derslikleri ekle
    for dl in df_derslikler["Derslikler"]:
        cursor.execute("INSERT INTO Derslikler (derslik_adi) VALUES (?)", (dl,))

    conn.commit()

    # Öğretim üyeleri → hangi dersleri verecek
    cursor.execute("SELECT uye_id, isim FROM OgretimUyeleri")
    uye_listesi = cursor.fetchall()
    cursor.execute("SELECT ders_id, ders_adi FROM Dersler")
    ders_listesi = cursor.fetchall()
    ders_adi_to_id = {ders_adi: ders_id for ders_id, ders_adi in ders_listesi}
    uye_adi_to_id = {isim: uye_id for uye_id, isim in uye_listesi}

    for _, row in df_uyeler_dersler.iterrows():
        uye_id = uye_adi_to_id[row["OgretimUyesi"]]
        ders_id = ders_adi_to_id[row["Ders"]]
        sinif = row["Sinif"]
        cursor.execute(
            "INSERT INTO OgretimUyeleriDersler (uye_id, ders_id, sinif) VALUES (?, ?, ?)",
            (uye_id, ders_id, sinif)
        )

    conn.commit()

# Veri ekle
veri_ekle()

print("✅ okul.db oluşturuldu! Veriler dersler.xlsx dosyasından alındı.")
