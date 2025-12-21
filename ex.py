import pandas as pd

# -----------------------------
# 1. VERİLER
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
    "Mikro İktisat", "Makro İktisat", "Finansal Yönetim", "Pazarlama Yönetimi",
    "İnsan Kaynakları Yönetimi", "Stratejik Yönetim", "Uluslararası İşletme",
    "Üretim Yönetimi", "Örgütsel Davranış", "İş Hukuku", "Girişimcilik",
    "Araştırma Yöntemleri", "E-Ticaret", "Proje Yönetimi", "Lojistik Yönetimi",
    "Kalite Yönetimi", "Yönetim Muhasebesi", "Satınalma Yönetimi",
    "Davranışsal Finans", "Küresel Pazarlama", "İş Etiği", "Risk Yönetimi",
    "Karar Analizi", "Perakende Yönetimi", "Müşteri İlişkileri Yönetimi",
    "İnovasyon Yönetimi", "İşletme Matematiği", "Organizasyon Teorisi",
    "Kültürel Yönetim", "Stratejik Pazarlama", "Yönetim Bilişim Sistemleri",
    "Sosyal Medya Pazarlama", "Ücretlendirme Yönetimi", "Kurumlar Hukuku",
    "Pazar Araştırması", "Kalite Kontrol Teknikleri"
]

derslikler = [f"Derslik {i}" for i in range(1, 25)]

sabit_ders_atamasi = {
    "Prof. Dr. Ahmet Yılmaz": ["İktisada Giriş", "Pazarlama Yönetimi"],
    "Prof. Dr. Ayşe Demir": ["Mikro İktisat", "Makro İktisat", "İşletme Matematiği"],
    "Doç. Dr. Mehmet Kaya": ["Muhasebe I", "Muhasebe II", "Finansal Yönetim"],
    "Doç. Dr. Zeynep Arslan": ["Stratejik Yönetim", "Uluslararası İşletme"],
    "Dr. Ahmet Şahin": ["Üretim Yönetimi", "Kalite Yönetimi"],
    "Dr. Cem Yıldız": ["Davranışsal Finans", "Finansal Yönetim"],
    "Dr. Deniz Koç": ["Pazarlama Yönetimi", "İnovasyon Yönetimi"],
    "Öğr. Gör. Hasan Tunç": ["Örgütsel Davranış", "İş Hukuku"],
    "Öğr. Gör. Elif Öz": ["Girişimcilik", "Araştırma Yöntemleri"],
    "Dr. Sibel Uslu": ["E-Ticaret", "Proje Yönetimi"],
    "Dr. Bora Koç": ["Lojistik Yönetimi", "Satınalma Yönetimi"],
    "Doç. Dr. Levent Ersoy": ["Stratejik Pazarlama", "Küresel Pazarlama"],
    "Prof. Dr. Zeynep Çelik": ["Yönetim Muhasebesi", "Kalite Kontrol Teknikleri"],
    "Dr. Ömer Kaplan": ["Karar Analizi", "Perakende Yönetimi"],
    "Öğr. Gör. Berna Aydın": ["Müşteri İlişkileri Yönetimi", "Sosyal Medya Pazarlama"],
    "Doç. Dr. Cem Aksoy": ["İş Etiği", "Risk Yönetimi"],
    "Dr. Ayça Öz": ["Organizasyon Teorisi", "Kültürel Yönetim"],
    "Dr. Fırat Demir": ["Yönetim Bilişim Sistemleri", "Ücretlendirme Yönetimi"],
    "Öğr. Gör. Gülhan Işık": ["Pazar Araştırması", "Lojistik Yönetimi"],
    "Dr. Murat Polat": ["E-Ticaret", "İnovasyon Yönetimi"]
}

# -----------------------------
# 2. DERSLERİN SINIF BİLGİSİ
# -----------------------------
sinif_bilgisi = {
    "1. Sınıf": ["İktisada Giriş", "Genel İşletme", "Muhasebe I", "İnsan Kaynakları Yönetimi", "Örgütsel Davranış", "İşletme Matematiği"],
    "2. Sınıf": ["Muhasebe II", "Mikro İktisat", "Makro İktisat", "Finansal Yönetim", "Pazarlama Yönetimi", "Üretim Yönetimi", "İş Hukuku"],
    "3. Sınıf": ["Stratejik Yönetim", "Uluslararası İşletme", "Lojistik Yönetimi", "Yönetim Muhasebesi", "Proje Yönetimi", "Araştırma Yöntemleri", "E-Ticaret", "Kalite Yönetimi", "Girişimcilik", "Karar Analizi", "İş Etiği"],
    "4. Sınıf": ["Stratejik Pazarlama", "Davranışsal Finans", "Küresel Pazarlama", "İnovasyon Yönetimi", "Müşteri İlişkileri Yönetimi", "Sosyal Medya Pazarlama", "Organizasyon Teorisi", "Kültürel Yönetim", "Risk Yönetimi", "Yönetim Bilişim Sistemleri", "Ücretlendirme Yönetimi", "Kurumlar Hukuku", "Pazar Araştırması", "Satınalma Yönetimi", "Kalite Kontrol Teknikleri", "Perakende Yönetimi"]
}

ders_sinif_dict = {}
for sinif, ders_listesi in sinif_bilgisi.items():
    for ders in ders_listesi:
        ders_sinif_dict[ders] = sinif

# -----------------------------
# 3. EXCEL SAYFALARI
# -----------------------------
# Öğretim Üyeleri
df_uyeler = pd.DataFrame({"OgretimUyesi": ogretim_uyeleri})

# Dersler + Sınıf
df_dersler = pd.DataFrame({
    "Dersler": dersler,
    "Sinif": [ders_sinif_dict[ders] for ders in dersler]
})

# Derslikler
df_derslikler = pd.DataFrame({"Derslikler": derslikler})

# OgretimUyeleriDersler
data_uyeler_dersler = []
for uye, ders_listesi in sabit_ders_atamasi.items():
    for ders in ders_listesi:
        data_uyeler_dersler.append({
            "OgretimUyesi": uye,
            "Ders": ders,
            "Sinif": ders_sinif_dict[ders]
        })

df_uyeler_dersler = pd.DataFrame(data_uyeler_dersler)

# -----------------------------
# 4. EXCEL DOSYASINA YAZ
# -----------------------------
with pd.ExcelWriter("dersler.xlsx") as writer:
    df_uyeler.to_excel(writer, sheet_name="OgretimUyeleri", index=False)
    df_dersler.to_excel(writer, sheet_name="Dersler", index=False)
    df_derslikler.to_excel(writer, sheet_name="Derslikler", index=False)
    df_uyeler_dersler.to_excel(writer, sheet_name="OgretimUyeleriDersler", index=False)

print("✅ dersler.xlsx dosyası oluşturuldu!")
