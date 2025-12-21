import pandas as pd

# -----------------------------
# VERİLER
# -----------------------------
ogretim_uyeleri = [
    "Prof. Dr. Ahmet Yılmaz", "Prof. Dr. Ayşe Demir",
    "Doç. Dr. Mehmet Kaya", "Doç. Dr. Zeynep Arslan",
    "Dr. Ahmet Şahin", "Dr. Cem Yıldız", "Dr. Deniz Koç",
    "Öğr. Gör. Hasan Tunç", "Öğr. Gör. Elif Öz", "Dr. Sibel Uslu",
    "Dr. Bora Koç", "Doç. Dr. Levent Ersoy", "Prof. Dr. Zeynep Çelik",
    "Dr. Ömer Kaplan", "Öğr. Gör. Berna Aydın", "Doç. Dr. Cem Aksoy",
    "Dr. Ayça Öz", "Dr. Fırat Demir", "Öğr. Gör. Gülhan Işık",
    "Dr. Murat Polat"
]

dersler = [
    "İktisada Giriş", "Genel İşletme", "Muhasebe I", "Muhasebe II",
    "Mikro İktisat", "Makro İktisat", "Finansal Yönetim",
    "Pazarlama Yönetimi"
]

derslikler = [f"Derslik {i}" for i in range(1, 25)]

sabit_ders_atamasi = {
    "Prof. Dr. Ahmet Yılmaz": ["İktisada Giriş", "Pazarlama Yönetimi"],
    "Prof. Dr. Ayşe Demir": ["Mikro İktisat", "Makro İktisat"]
}

gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma"]
saatler = [
    "09:00-10:00", "10:00-11:00", "11:00-12:00",
    "13:00-14:00", "14:00-15:00", "15:00-16:00"
]

# -----------------------------
# 1. OGRETIM UYESI UYGUNLUK
# -----------------------------
rows = []
for hoca in ogretim_uyeleri:
    for gun in gunler:
        for saat in saatler:
            rows.append({
                "Ogretim_Uyesi": hoca,
                "Gun": gun,
                "Saat": saat,
                "Uygun_mu (1=Evet, 0=Hayır)": 1
            })

df_uygunluk = pd.DataFrame(rows)

# -----------------------------
# 2. DERS - OGRETIM UYESI
# -----------------------------
ders_hoca = []
for hoca, ders_list in sabit_ders_atamasi.items():
    for ders in ders_list:
        ders_hoca.append({
            "Ders": ders,
            "Ogretim_Uyesi": hoca,
            "Sabit_Atama (1=Evet)": 1
        })

df_ders_hoca = pd.DataFrame(ders_hoca)

# -----------------------------
# 3. DERS BILGILERI
# -----------------------------
df_ders = pd.DataFrame({
    "Ders": dersler,
    "Haftalik_Saat": [3] * len(dersler),
    "Blok_Ders (1=Evet, 0=Hayır)": [0] * len(dersler)
})

# -----------------------------
# 4. DERSLIKLER
# -----------------------------
df_derslik = pd.DataFrame({
    "Derslik": derslikler,
    "Kapasite": [40] * len(derslikler)
})

# -----------------------------
# 5. GENEL KISITLAR
# -----------------------------
df_kisit = pd.DataFrame({
    "Kisit": [
        "Bir öğretim üyesi aynı anda iki derse giremez",
        "Bir derslikte aynı anda iki ders yapılamaz",
        "Ders haftalık saatini aşamaz",
        "Öğretim üyesi max haftalık ders saati"
    ],
    "Deger": ["Zorunlu", "Zorunlu", "Zorunlu", 12]
})

# -----------------------------
# EXCEL'E YAZ (ENGINE YOK!)
# -----------------------------
with pd.ExcelWriter("ders_programi_kisit_formu.xlsx") as writer:
    df_uygunluk.to_excel(writer, sheet_name="Ogretmen_Uygunluk", index=False)
    df_ders_hoca.to_excel(writer, sheet_name="Ders_Ogretmen", index=False)
    df_ders.to_excel(writer, sheet_name="Ders_Bilgileri", index=False)
    df_derslik.to_excel(writer, sheet_name="Derslikler", index=False)
    df_kisit.to_excel(writer, sheet_name="Genel_Kisitlar", index=False)

print("Excel kısıt formu başarıyla oluşturuldu.")
