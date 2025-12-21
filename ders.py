import sqlite3
import random
import pandas as pd

# -----------------------------
# 1. VERİTABANI BAĞLANTISI
# -----------------------------
conn = sqlite3.connect("okul.db")
cursor = conn.cursor()

# Öğretim üyesi - ders ilişkisini çek
cursor.execute("""
SELECT OgretimUyeleri.isim, Dersler.ders_adi
FROM OgretimUyeleri
JOIN OgretimUyeleriDersler ON OgretimUyeleri.uye_id = OgretimUyeleriDersler.uye_id
JOIN Dersler ON Dersler.ders_id = OgretimUyeleriDersler.ders_id
""")

ogretmen_dersler = {}
for ogretmen, ders in cursor.fetchall():
    if ogretmen not in ogretmen_dersler:
        ogretmen_dersler[ogretmen] = []
    ogretmen_dersler[ogretmen].append(ders)

# -----------------------------
# 2. PROGRAM AYARLARI
# -----------------------------
gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma"]
gunluk_saat = 3

# Derslikleri veritabanından al
cursor.execute("SELECT derslik_adi FROM Derslikler")
derslikler = [row[0] for row in cursor.fetchall()]

# Ders listesi (her ders yalnızca 1 kez verilecek)
dersler_listesi = list({d for dersler in ogretmen_dersler.values() for d in dersler})

# Ders-Öğretmen ataması (sabit atamaya göre rastgele)
ders_ogretmen = {}
for ders in dersler_listesi:
    uygun_ogretmenler = [o for o, dl in ogretmen_dersler.items() if ders in dl]
    ders_ogretmen[ders] = random.choice(uygun_ogretmenler)

# -----------------------------
# 3. PROGRAM MATRİSİ OLUŞTUR
# -----------------------------
program = {gun: {saat: {} for saat in range(gunluk_saat)} for gun in gunler}

# -----------------------------
# 4. DERSLERİ YERLEŞTİRME (BOŞLUKLARI AZALT)
# -----------------------------
for ders in dersler_listesi:
    # Tüm kombinasyonları oluştur
    tum_kombinasyonlar = [
        (gun, saat, dl)
        for gun in gunler
        for saat in range(gunluk_saat)
        for dl in derslikler
        if dl not in program[gun][saat]
    ]

    if not tum_kombinasyonlar:
        raise ValueError(f"❌ Bu dersi yerleştiremedim! Ders: {ders}")

    # Kombinasyonları öncelikle en az dolu olan saat/derslik sırasına göre sırala
    tum_kombinasyonlar.sort(key=lambda x: len(program[x[0]][x[1]]))

    # En az dolu olanlardan rastgele birini seç
    min_dolu = len(program[tum_kombinasyonlar[0][0]][tum_kombinasyonlar[0][1]])
    en_az_dolu = [k for k in tum_kombinasyonlar if len(program[k[0]][k[1]]) == min_dolu]
    gun, saat, derslik = random.choice(en_az_dolu)

    program[gun][saat][derslik] = f"{ders} ({ders_ogretmen[ders]})"

# -----------------------------
# 5. EXCEL ÇIKTISI
# -----------------------------
satirlar = []
for gun in gunler:
    satir = []
    for saat in range(gunluk_saat):
        dersler_saat = [f"{dl}: {program[gun][saat][dl]}" for dl in program[gun][saat]]
        satir.append("\n".join(dersler_saat))
    satirlar.append(satir)

df = pd.DataFrame(satirlar, index=gunler, columns=[f"Saat {i+1}" for i in range(gunluk_saat)])
df.to_excel("isletme_ders_programi.xlsx")
print("✅ Ders programı oluşturuldu! Dosya: isletme_ders_programi.xlsx")
