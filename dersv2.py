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
ders_ogretmen = {}
tum_ders_gorevleri = []

for ogretmen, ders, sinif in cursor.fetchall():
    benzersiz_id = f"{ders} ({ogretmen})"
    ders_ogretmen[benzersiz_id] = ogretmen
    ders_info[benzersiz_id] = {
        "ders_adi_saf": ders,
        "siniflar": [s.strip() for s in str(sinif).split(",")],
        "gun_yasaklari": []
    }
    tum_ders_gorevleri.append(benzersiz_id)

cursor.execute("SELECT derslik_adi FROM Derslikler")
derslikler = [r[0] for r in cursor.fetchall()]
conn.close()

# ==============================
# 2. KISITLAR
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
    d_adi = r["Ders"]
    ilgili_idler = [kid for kid in tum_ders_gorevleri if ders_info[kid]["ders_adi_saf"] == d_adi]
    for d_id in ilgili_idler:
        ders_info[d_id]["gun_yasaklari"] = [g for g in gunler if r.get(f"{g}_Olamaz (1=Evet, 0=Hayır)", 0) == 1]

# ==============================
# 3. PROGRAM YAPILARI
# ==============================
program = {g: {s: {} for s in range(gunluk_saat)} for g in gunler}
ogretmen_prog = {g: {s: set() for s in range(gunluk_saat)} for g in gunler}
sinif_prog = {g: {s: [] for s in range(gunluk_saat)} for g in gunler}

gun_yuku = {g: 0 for g in gunler}
saat_yuku = {g: {s: 0 for s in range(gunluk_saat)} for g in gunler}

# ==============================
# 4. TERCİHLERİ SABİT YERLEŞTİR
# ==============================
tercih_df = pd.read_excel("tercih.xlsx")
yerlesen_dersler = set()

for _, row in tercih_df.iterrows():
    gun = row["Gün"]
    if gun not in gunler: continue
    for col in tercih_df.columns[1:]:
        if pd.isna(row[col]): continue
        bas = int(col.split("-")[0].split(":")[0])
        bit = int(col.split("-")[1].split(":")[0])
        saat_idx = [i for i, s in enumerate(saatler) if bas <= int(s.split(":")[0]) < bit]

        dersler_in_cell = [d.strip() for d in str(row[col]).split(",")]
        for d_id in dersler_in_cell:
            if d_id not in ders_ogretmen: continue
            ogretmen = ders_ogretmen[d_id]
            siniflar = ders_info[d_id]["siniflar"]

            placed = False
            for dl in derslikler:
                if all(dl not in program[gun][s] and ogretmen not in ogretmen_prog[gun][s] and
                       uygunluk.get((ogretmen, gun, saatler[s]), 1) != 0 and
                       not any(sf in sinif_prog[gun][s] for sf in siniflar) for s in saat_idx):
                    for s in saat_idx:
                        program[gun][s][dl] = d_id
                        ogretmen_prog[gun][s].add(ogretmen)
                        sinif_prog[gun][s].extend(siniflar)
                        saat_yuku[gun][s] += 1
                    gun_yuku[gun] += 1
                    yerlesen_dersler.add(d_id)
                    placed = True
                    break

# ==============================
# 5. KALAN DERSLER
# ==============================
kalan_dersler = list(set(tum_ders_gorevleri) - yerlesen_dersler)
kalan_dersler.sort(key=lambda d: len(ders_info[d]["gun_yasaklari"]), reverse=True)

# ==============================
# 6. BACKTRACKING (KADEMELİ SOFT MOD & RAPORLU)
# ==============================
deneme = 0
MAX_DENEME = 1000000
soft_kullanim = []


def yerlestir(i):
    global deneme
    deneme += 1

    if i == len(kalan_dersler): return True
    if deneme > MAX_DENEME: return False

    # Tolerans her 10.000 denemede 1 artar
    guncel_max_soft = deneme // 10000

    if deneme % 10000 == 0:
        print(f"🔄 Deneme: {deneme} | Kalan: {len(kalan_dersler) - i} | Tolerans: {guncel_max_soft} Çakışma İzni")

    ders_id = kalan_dersler[i]
    ogretmen = ders_ogretmen[ders_id]
    siniflar = ders_info[ders_id]["siniflar"]

    adaylar = []
    for g in gunler:
        if g in ders_info[ders_id]["gun_yasaklari"]: continue
        for s in range(gunluk_saat):
            for dl in derslikler:
                adaylar.append((g, s, dl))
    adaylar.sort(key=lambda x: (gun_yuku[x[0]], saat_yuku[x[0]][x[1]]))

    for g, s, dl in adaylar:
        if dl in program[g][s]: continue
        if ogretmen in ogretmen_prog[g][s]: continue
        if uygunluk.get((ogretmen, g, saatler[s]), 1) == 0: continue

        # Çakışan sınıfları tespit et
        cakisanlar = [sf for sf in siniflar if sf in sinif_prog[g][s]]

        if cakisanlar:
            # Tolerans limitini aşıyorsa bu yerleşimi yapma
            if len(soft_kullanim) >= guncel_max_soft:
                continue

        # YERLEŞTİR
        program[g][s][dl] = ders_id
        ogretmen_prog[g][s].add(ogretmen)
        sinif_prog[g][s].extend(siniflar)
        saat_yuku[g][s] += 1
        gun_yuku[g] += 1

        # Çakışma bilgisini rapora ekle
        if cakisanlar:
            soft_kullanim.append({
                "ders": ders_id,
                "gun": g,
                "saat": saatler[s],
                "cakisan_siniflar": cakisanlar
            })

        if yerlestir(i + 1): return True

        # GERİ AL
        if cakisanlar:
            soft_kullanim.pop()
        del program[g][s][dl]
        ogretmen_prog[g][s].remove(ogretmen)
        for sf in siniflar:
            sinif_prog[g][s].remove(sf)
        saat_yuku[g][s] -= 1
        gun_yuku[g] -= 1

    return False


# ==============================
# 7. ÇALIŞTIR VE SONUÇLARI YAZDIR
# ==============================
print(f"🚀 {len(kalan_dersler)} ders için kademeli toleransla yer aranıyor...")

if yerlestir(0):
    # Çakışma Raporunu Terminale Yazdır
    if soft_kullanim:
        print("\n⚠️ YUMUŞAK KISIT (SOFT CONSTRAINT) KULLANILAN DERSLER:")
        for rapor in soft_kullanim:
            print(
                f"- {rapor['ders']} | {rapor['gun']} {rapor['saat']} | Çakışan Sınıf Grupları: {rapor['cakisan_siniflar']}")
    else:
        print("\n✅ Harika! Hiçbir sınıf çakışması olmadan çözüm bulundu.")

    # Excel Tablosunu Oluştur
    tablo = []
    for g in gunler:
        satir = []
        for s in range(gunluk_saat):
            hucre_verileri = []
            for dl in sorted(program[g][s].keys()):
                d_id = program[g][s][dl]
                d_adi = ders_info[d_id]["ders_adi_saf"]
                d_hoca = ders_ogretmen[d_id]
                d_siniflar = ", ".join(ders_info[d_id]["siniflar"])
                hucre_verileri.append(f"{dl}: {d_adi} ({d_siniflar}, {d_hoca})")
            satir.append("\n".join(hucre_verileri))
        tablo.append(satir)

    pd.DataFrame(tablo, index=gunler, columns=saatler).to_excel("isletme_ders_programi.xlsx")
    print(f"\n✅ Program 'isletme_ders_programi.xlsx' dosyasına kaydedildi.")
else:
    print(f"\n❌ {deneme} deneme yapıldı ancak uygun bir yerleşim bulunamadı.")