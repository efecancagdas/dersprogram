import sqlite3
import random
import pandas as pd

# =============================
# 1. VERİTABANI BAĞLANTISI
# =============================
conn = sqlite3.connect("okul.db")
cursor = conn.cursor()

# Öğretim üyesi - ders ilişkisi ve sınıf bilgisi
cursor.execute("""
SELECT OgretimUyeleri.isim, Dersler.ders_adi, Dersler.sinif
FROM OgretimUyeleri
JOIN OgretimUyeleriDersler ON OgretimUyeleri.uye_id = OgretimUyeleriDersler.uye_id
JOIN Dersler ON Dersler.ders_id = OgretimUyeleriDersler.ders_id
""")

ogretmen_dersler = {}
ders_info = {}

for ogretmen, ders, sinif in cursor.fetchall():
    ogretmen_dersler.setdefault(ogretmen, []).append(ders)
    ders_info[ders] = {"sinif": sinif, "blok": False, "gun_yasaklari": []}

# Derslikler
cursor.execute("SELECT derslik_adi FROM Derslikler")
derslikler = [r[0] for r in cursor.fetchall()]

conn.close()

# Ders listesi
dersler_listesi = list({d for dl in ogretmen_dersler.values() for d in dl})

# =============================
# 2. EXCEL KISIT FORMUNU OKU
# =============================
kisitler = pd.read_excel("ders_programi_kisit_formu.xlsx", sheet_name=None)
df_uygunluk = kisitler["Ogretmen_Uygunluk"]
df_ders_bilgileri = kisitler["Ders_Bilgileri"]

# Öğretmen uygunluk sözlüğü: (ogretmen, gun, saat) -> 0/1
uygunluk = {}
for _, r in df_uygunluk.iterrows():
    uygunluk[(r["Ogretim_Uyesi"], r["Gun"], r["Saat"])] = r["Uygun_mu (1=Evet, 0=Hayır)"]

# Saat ve günleri al
saatler = sorted(df_uygunluk["Saat"].unique(), key=lambda x: int(x.split(":")[0]))
gunler = sorted(df_uygunluk["Gun"].unique(), key=lambda x: ["Pazartesi","Salı","Çarşamba","Perşembe","Cuma"].index(x))
gunluk_saat = len(saatler)

# Ders bilgileri sözlüğüne blok ve yasaklı gün bilgisi ekle
for _, r in df_ders_bilgileri.iterrows():
    if r["Ders"] in ders_info:
        ders_info[r["Ders"]]["blok"] = r["Blok_Ders (1=Evet, 0=Hayır)"] == 1
        gun_yasaklari = []
        for gun in ["Pazartesi","Salı","Çarşamba","Perşembe","Cuma"]:
            if r.get(f"{gun}_Olamaz (1=Evet, 0=Hayır)", 0) == 1:
                gun_yasaklari.append(gun)
        ders_info[r["Ders"]]["gun_yasaklari"] = gun_yasaklari

# =============================
# 3. PROGRAM MATRİSİ
# =============================
program = {gun: {saat: {} for saat in range(gunluk_saat)} for gun in gunler}
ogretmen_program = {gun: {saat: set() for saat in range(gunluk_saat)} for gun in gunler}

# =============================
# 4. DERS YERLEŞTİRME (BOŞLUK MINİMİZE)
# =============================
for ders in dersler_listesi:

    adaylar = []

    for gun in gunler:
        if gun in ders_info.get(ders, {}).get("gun_yasaklari", []):
            continue

        for saat_idx, saat in enumerate(saatler):
            for derslik in derslikler:

                if derslik in program[gun][saat_idx]:
                    continue

                for ogretmen, verdigi_dersler in ogretmen_dersler.items():
                    if ders not in verdigi_dersler:
                        continue

                    # Öğretmen uygun mu?
                    if uygunluk.get((ogretmen, gun, saat), 1) == 0:
                        continue

                    # Aynı anda başka derste mi?
                    if ogretmen in ogretmen_program[gun][saat_idx]:
                        continue

                    # Aynı sınıftan başka ders var mı? (sınıf çakışma kısıtı)
                    ders_sinif = ders_info[ders]["sinif"]
                    if any(
                        ders_info.get(program[gun][saat_idx][dl].split(" (")[0], {}).get("sinif") == ders_sinif
                        for dl in program[gun][saat_idx]
                    ):
                        continue

                    # Blok ders kontrolü
                    if ders_info.get(ders, {}).get("blok"):
                        if saat_idx + 1 >= gunluk_saat:
                            continue
                        if derslik in program[gun][saat_idx + 1]:
                            continue
                        if ogretmen in ogretmen_program[gun][saat_idx + 1]:
                            continue
                        if uygunluk.get((ogretmen, gun, saatler[saat_idx + 1]), 1) == 0:
                            continue
                        # Blok ders ikinci saatinde aynı sınıf dersi kontrolü
                        if any(
                            ders_info.get(program[gun][saat_idx + 1][dl].split(" (")[0], {}).get("sinif") == ders_sinif
                            for dl in program[gun][saat_idx + 1]
                        ):
                            continue

                    adaylar.append((gun, saat_idx, derslik, ogretmen))

    if not adaylar:
        raise ValueError(f"❌ Yerleştirilemeyen ders: {ders}")

    # -----------------------------
    # BOŞLUK MINİMİZE SEÇİM
    # -----------------------------
    adaylar.sort(key=lambda x: len(program[x[0]][x[1]]))  # az dolu olan saat/derslikleri öncelikli
    min_dolu = len(program[adaylar[0][0]][adaylar[0][1]])
    en_az_dolu = [a for a in adaylar if len(program[a[0]][a[1]]) == min_dolu]

    gun, saat_idx, derslik, ogretmen = random.choice(en_az_dolu)

    # Dersin sınıf bilgisini al
    ders_sinif = ders_info[ders]["sinif"]

    # Yerleştir
    program[gun][saat_idx][derslik] = f"{ders} ({ders_sinif}, {ogretmen})"
    ogretmen_program[gun][saat_idx].add(ogretmen)

    # Blok dersse ikinci saat
    if ders_info.get(ders, {}).get("blok"):
        program[gun][saat_idx + 1][derslik] = f"{ders} ({ders_sinif}, {ogretmen})"
        ogretmen_program[gun][saat_idx + 1].add(ogretmen)

# =============================
# 5. EXCEL ÇIKTISI
# =============================
satirlar = []
for gun in gunler:
    satir = []
    for saat_idx in range(gunluk_saat):
        hucre = "\n".join(
            f"{dl}: {program[gun][saat_idx][dl]}" for dl in program[gun][saat_idx]
        )
        satir.append(hucre)
    satirlar.append(satir)

df = pd.DataFrame(
    satirlar,
    index=gunler,
    columns=[f"Saat {s}" for s in saatler]
)

df.to_excel("isletme_ders_programi.xlsx")
print("✅ Ders programı oluşturuldu: isletme_ders_programi.xlsx")
