import sqlite3
import pandas as pd
import sys

sys.setrecursionlimit(10000)

# ==============================
# 1. VERİLER
# ==============================
conn = sqlite3.connect("okul.db")
cursor = conn.cursor()

cursor.execute("""
SELECT OgretimUyeleri.isim, Dersler.ders_adi, Dersler.sinif
FROM OgretimUyeleri
JOIN OgretimUyeleriDersler ON OgretimUyeleri.uye_id = OgretimUyeleriDersler.uye_id
JOIN Dersler ON Dersler.ders_id = OgretimUyeleriDersler.ders_id
""")

ders_info = {}
ders_ogretmen = {}  # ders -> list of (ogretmen, sinif list)

for ogretmen, ders, sinif in cursor.fetchall():
    if ders not in ders_ogretmen:
        ders_ogretmen[ders] = []
    ders_ogretmen[ders].append((ogretmen, [s.strip() for s in str(sinif).split(",")]))

    if ders not in ders_info:
        ders_info[ders] = {
            "gun_yasaklari": []
        }

cursor.execute("SELECT derslik_adi FROM Derslikler")
derslikler = [r[0] for r in cursor.fetchall()]
conn.close()

# ==============================
# 2. KISIT FORMU
# ==============================
kisitler = pd.read_excel("kisit_formu.xlsx", sheet_name=None)
df_uygunluk = kisitler["Ogretmen_Uygunluk"]
df_ders_bilgileri = kisitler["Ders_Bilgileri"]

uygunluk = {}
for _, r in df_uygunluk.iterrows():
    uygunluk[(r["Ogretim_Uyesi"], r["Gun"], r["Saat"])] = r["Uygun_mu (1=Evet, 0=Hayır)"]

saatler = sorted(df_uygunluk["Saat"].unique(), key=lambda x: int(x.split(":")[0]))
gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma"]
gunluk_saat = len(saatler)

for _, r in df_ders_bilgileri.iterrows():
    d = r["Ders"]
    if d in ders_info:
        ders_info[d]["gun_yasaklari"] = [
            g for g in gunler
            if r.get(f"{g}_Olamaz (1=Evet, 0=Hayır)", 0) == 1
        ]

# ==============================
# 3. PROGRAM YAPILARI
# ==============================
program = {g: {s: {} for s in range(gunluk_saat)} for g in gunler}
ogretmen_prog = {g: {s: set() for s in range(gunluk_saat)} for g in gunler}
sinif_prog = {g: {s: set() for s in range(gunluk_saat)} for g in gunler}

gun_yuku = {g: 0 for g in gunler}
saat_yuku = {g: {s: 0 for s in range(gunluk_saat)} for g in gunler}

# ==============================
# 4. TERCİHLERİ SABİT YERLEŞTİR
# ==============================
tercih_df = pd.read_excel("tercih.xlsx")
yerlesen_dersler = set()

for _, row in tercih_df.iterrows():
    gun = row["Gün"]
    if gun not in gunler:
        continue

    for col in tercih_df.columns[1:]:
        if pd.isna(row[col]):
            continue

        bas = int(col.split("-")[0].split(":")[0])
        bit = int(col.split("-")[1].split(":")[0])

        saat_idx = [
            i for i, s in enumerate(saatler)
            if bas <= int(s.split(":")[0]) < bit
        ]

        dersler = [d.strip() for d in str(row[col]).split(",")]

        for ders in dersler:
            if ders not in ders_ogretmen:
                raise RuntimeError(f"❌ Tercih ders DB'de yok: {ders}")

            # artık ders_ogretmen[ders] bir liste
            for ogretmen, siniflar in ders_ogretmen[ders]:
                placed = False
                for dl in derslikler:
                    if all(
                        dl not in program[gun][s] and
                        ogretmen not in ogretmen_prog[gun][s] and
                        uygunluk.get((ogretmen, gun, saatler[s]), 1) != 0 and
                        all(sf not in sinif_prog[gun][s] for sf in siniflar)
                        for s in saat_idx
                    ):
                        for s in saat_idx:
                            program[gun][s][dl] = f"{ders} ({', '.join(siniflar)}, {ogretmen})"
                            ogretmen_prog[gun][s].add(ogretmen)
                            sinif_prog[gun][s].update(siniflar)
                            saat_yuku[gun][s] += 1
                        gun_yuku[gun] += 1
                        yerlesen_dersler.add((ders, ogretmen))
                        placed = True
                        break

                if not placed:
                    raise RuntimeError(
                        f"❌ Tercih verisi tutarsız:\n"
                        f"Ders: {ders}\nOgretmen: {ogretmen}\nGün: {gun}\nSaat: {col}\n"
                        f"(Muhtemel neden: hoca uygunluk formu)"
                    )

# ==============================
# 5. KALAN DERSLER
# ==============================
kalan_dersler = []

for ders in ders_ogretmen:
    for ogretmen, siniflar in ders_ogretmen[ders]:
        if (ders, ogretmen) not in yerlesen_dersler:
            kalan_dersler.append((ders, ogretmen, siniflar))

# zor dersleri önce yerleştirmek için sırala
kalan_dersler.sort(
    key=lambda x: (len(ders_info[x[0]]["gun_yasaklari"]),),
    reverse=True
)

# ==============================
# 6. BACKTRACKING
# ==============================
MAX_DENEME = 5000
MAX_SOFT = 2
deneme = 0
soft_kullanim = []

def yerlestir(i):
    global deneme
    deneme += 1

    if deneme % 100 == 0:
        print(f"🔄 Çözüm {deneme} deneniyor...")

    if i == len(kalan_dersler):
        return True

    ders, ogretmen, siniflar = kalan_dersler[i]

    soft_mod = deneme > MAX_DENEME

    adaylar = []
    for g in gunler:
        if g in ders_info[ders]["gun_yasaklari"]:
            continue
        for s in range(gunluk_saat):
            for dl in derslikler:
                adaylar.append((g, s, dl))

    adaylar.sort(key=lambda x: (gun_yuku[x[0]], saat_yuku[x[0]][x[1]]))

    for g, s, dl in adaylar:
        if dl in program[g][s]:
            continue
        if ogretmen in ogretmen_prog[g][s]:
            continue
        if uygunluk.get((ogretmen, g, saatler[s]), 1) == 0:
            continue

        cakisan = [sf for sf in siniflar if sf in sinif_prog[g][s]]
        if cakisan and (not soft_mod or len(soft_kullanim) >= MAX_SOFT):
            continue

        program[g][s][dl] = f"{ders} ({', '.join(siniflar)}, {ogretmen})"
        ogretmen_prog[g][s].add(ogretmen)
        sinif_prog[g][s].update(siniflar)
        saat_yuku[g][s] += 1
        gun_yuku[g] += 1

        if cakisan:
            soft_kullanim.append((ders, g, s, cakisan))

        if yerlestir(i + 1):
            return True

        del program[g][s][dl]
        ogretmen_prog[g][s].remove(ogretmen)
        saat_yuku[g][s] -= 1
        gun_yuku[g] -= 1
        for sf in siniflar:
            sinif_prog[g][s].discard(sf)

        if cakisan:
            soft_kullanim.pop()

    return False

# ==============================
# 7. ÇALIŞTIR
# ==============================
print("🚀 Program başlatıldı...")

if yerlestir(0):
    if soft_kullanim:
        print("⚠️ Soft constraint kullanıldı:")
        for d, g, s, sf in soft_kullanim:
            print(f"- {d} | {g} {saatler[s]} | Çakışan sınıf: {sf}")

    tablo = []
    for g in gunler:
        tablo.append([
            "\n".join([f"{dl}: {program[g][s][dl]}" for dl in program[g][s]])
            for s in range(gunluk_saat)
        ])

    pd.DataFrame(tablo, index=gunler, columns=saatler)\
        .to_excel("isletme_ders_programi.xlsx")

    print("✅ Excel çıktısı oluşturuldu.")
else:
    print("❌ Çözüm bulunamadı.")
