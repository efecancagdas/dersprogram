import pandas as pd

# -----------------------------
# 1. VERİLER
# -----------------------------
ogretim_uyeleri = [
    "Öğretmen 1",
    "Öğretmen 2",
    "Öğretmen 3",
    "Öğretmen 4",
    "Öğretmen 5",
    "Dr. Öğr. Üyesi Miray BAYBARS",
    "Doç. Dr. Burcu ŞENTÜRK YILDIZ",
    "Araş. Gör. Dr. Özgür BABACAN",
    "Prof. Dr. G. Nazan GÜNAY",
    "Prof. Dr. Burcu ARACIOĞLU",
    "Doç. Dr. İnanç KABASAKAL",
    "Prof. Dr. A. Nazlı AYYILDIZ ÜNNÜ",
    "Dr. Öğr. Üyesi Hakan ERKAL",
    "Dr. Öğr. Üyesi A. Erhan ZALLUHOĞLU",
    "Prof. Dr. Dilek DEMİRHAN",
    "Dr. Öğr. Üyesi Esin GÜRBÜZ",
    "Prof. Dr. Ayla Özhan DEDEOĞLU",
    "Doç. Dr. Elif ÜSTÜNDAĞLI ERTEN",
    "Prof. Dr. Murat KOCAMAZ",
    "Doç. Dr. Haydar YALÇIN",
    "Prof. Dr. İpek KAZANÇOĞLU",
    "Dr. Öğr. Üyesi Ş. Sertaç ÇAKI",
    "Doç. Dr. Aydın KOÇAK",
    "Prof. Dr. Haluk SOYUER",
    "Prof. Dr. Türker SUSMUŞ",
    "Prof. Dr. Derya İLİC",
    "Doç. Dr. U. Gökay ÇİÇEKLİ",
    "Prof. Dr. Burak ÇAPRAZ",
    "Prof. Dr. Aykan CANDEMİR",
    "Prof. Dr. Keti VENTURA",
    "Araş. Gör. Dr. Begüm KANAT TİRYAKİ",
    "Dr. Öğr. Üyesi Sema AYDIN"
]


dersler = [
    "Matematik-I (Tek)",
    "Matematik-I (Çift)",
    "Business",
    "Sosyoloji",
    "Introduction to Microeconomics",
    "Kariyer Planlama",
    "Türk Dili I",
    "Atatürk İlkeleri ve İnkılap Tarihi I",
    "Muhasebe I",
    "Marketing Management I",
    "Operations Management I",
    "İstatistik I",
    "Organizational Behavior (Tek)",
    "Organizational Behavior (Çift)",
    "Araştırma Yöntemleri (Çift)",
    "Araştırma Yöntemleri (Tek)",
    "Financial Management I",
    "İşletme Hukuku",
    "Consumer Behavior (Tek)",
    "Consumer Behavior (Çift)",
    "Operations Research I",
    "Girişimcilik ve KOBİ Yönetimi",
    "Enformetri",
    "Sürdürülebilir Pazarlama",
    "Yönetim Muhasebesi",
    "Reklamcılık Yönetimi",
    "E-İş ve Kurumsal Kaynak Planlama",
    "Teknoloji ve Sanayi Dinamikleri",
    "Uygulamalı Finansal Piyasa İşlemleri",
    "Küresel Tedarik Zinciri ve Lojistik",
    "Bilgi Yönetimi",
    "Yatırım Yönetimi",
    "Management Consultancy",
    "Yönetim Geliştirme",
    "Borçlar Hukuku",
    "System Analysis and Design",
    "Human Resources Management",
    "Global Marketing (Tek)",
    "Global Marketing (Çift)",
    "Mali Tablolar Analizi",
    "Vestel İşletmecilik Seminerleri I",
    "Retailing I",
    "Muhasebe I (Örgün + İ.Ö.)",
    "Muhasebe II (Tasfiye)",
    "Uygulamalı Finansal Piyasa İşlemleri (Örgün)",
    "Business I (Tasfiye)",
    "Introduction to Business (Örgün + İ.Ö)",
    "Hukukun Temel Kavramları (Örgün + İ.Ö.)",
    "Ticaret Hukuku (Tasfiye)",
    "İşletmeye Giriş"
]


derslikler = [
    "Derslik 101",
    "Derslik 102",
    "Derslik 103",
    "Derslik 104",
    "Derslik 105",
    "Derslik 108",
    "Derslik 109",
    "Derslik 110",
    "Derslik 111",
    "Derslik 201",
    "Derslik 202",
    "Derslik 203",
    "Derslik 204",
    "Derslik 205",
    "Derslik 208",
    "Derslik 209",
    "Derslik 210",
    "Derslik 211",
    "Derslik 301",
    "Derslik 302",
    "Derslik 303"
]


kontenjan_bilgisi = {
    "Derslik 101": 32,
    "Derslik 102": 49,
    "Derslik 103": 20,
    "Derslik 104": 48,
    "Derslik 105": 49,
    "Derslik 108": 49,
    "Derslik 109": 20,
    "Derslik 110": 20,
    "Derslik 111": 20,
    "Derslik 201": 30,
    "Derslik 202": 49,
    "Derslik 203": 20,
    "Derslik 204": 48,
    "Derslik 205": 49,
    "Derslik 208": 49,
    "Derslik 209": 20,
    "Derslik 210": 20,
    "Derslik 211": 20,
    "Derslik 301": 41,
    "Derslik 302": 36,
    "Derslik 303": 64
}


# Derslerin sınıf bilgisi
sinif_bilgisi = {
    "1. Sınıf": [
        "Matematik-I (Tek)",
        "Matematik-I (Çift)",
        "Business",
        "Sosyoloji",
        "Introduction to Microeconomics",
        "Kariyer Planlama",
        "Türk Dili I",
        "Atatürk İlkeleri ve İnkılap Tarihi I"
    ],
    "2. Sınıf": [
        "Muhasebe I",
        "Marketing Management I",
        "Operations Management I",
        "İstatistik I",
        "Organizational Behavior (Tek)",
        "Organizational Behavior (Çift)"
    ],
    "3. Sınıf": [
        "Araştırma Yöntemleri (Çift)",
        "Araştırma Yöntemleri (Tek)",
        "Financial Management I",
        "İşletme Hukuku",
        "Consumer Behavior (Tek)",
        "Consumer Behavior (Çift)",
        "Operations Research I",
        "Girişimcilik ve KOBİ Yönetimi",
        "Enformetri",
        "Sürdürülebilir Pazarlama",
        "Yönetim Muhasebesi",
        "Reklamcılık Yönetimi",
        "E-İş ve Kurumsal Kaynak Planlama",
        "Teknoloji ve Sanayi Dinamikleri",
        "Uygulamalı Finansal Piyasa İşlemleri",
        "Küresel Tedarik Zinciri ve Lojistik",
        "Bilgi Yönetimi",
        "Yatırım Yönetimi",
        "Management Consultancy",
        "Yönetim Geliştirme",
        "Borçlar Hukuku"
    ],
    "4. Sınıf": [
        "System Analysis and Design",
        "Human Resources Management",
        "Global Marketing (Tek)",
        "Global Marketing (Çift)",
        "Mali Tablolar Analizi",
        "Vestel İşletmecilik Seminerleri I",
        "Retailing I"
    ],
    "0. Sınıf": [
        "Muhasebe I (Örgün + İ.Ö.)",
        "Muhasebe II (Tasfiye)",
        "Uygulamalı Finansal Piyasa İşlemleri (Örgün)",
        "Business I (Tasfiye)",
        "Introduction to Business (Örgün + İ.Ö)",
        "Hukukun Temel Kavramları (Örgün + İ.Ö.)",
        "Ticaret Hukuku (Tasfiye)",
        "İşletmeye Giriş"
    ]
}


# Sabit ders atamaları
sabit_ders_atamasi = {
    "ÖĞRETMEN 1": [
        "Matematik-I (Tek)"
    ],
    "ÖĞRETMEN 2": [
        "Matematik-I (Çift)"
    ],
    "Dr. Öğr. Üyesi Miray BAYBARS": [
        "Business",
        "Kariyer Planlama",
        "Retailing I"
    ],
    "Doç. Dr. Burcu ŞENTÜRK YILDIZ": [
        "Sosyoloji"
    ],
    "ÖĞRETMEN 3": [
        "Introduction to Microeconomics"
    ],
    "ÖĞRETMEN 4": [
        "Türk Dili I"
    ],
    "ÖĞRETMEN 5": [
        "Atatürk İlkeleri ve İnkılap Tarihi I"
    ],
    "Araş. Gör. Dr. Özgür BABACAN": [
        "Muhasebe I",
        "Yatırım Yönetimi",
        "İşletmeye Giriş"
    ],
    "Prof. Dr. G. Nazan GÜNAY": [
        "Marketing Management I",
        "Vestel İşletmecilik Seminerleri I"
    ],
    "Prof. Dr. Burcu ARACIOĞLU": [
        "Operations Management I",
        "Küresel Tedarik Zinciri ve Lojistik"
    ],
    "Doç. Dr. İnanç KABASAKAL": [
        "İstatistik I",
        "Bilgi Yönetimi"
    ],
    "Prof. Dr. A. Nazlı AYYILDIZ ÜNNÜ": [
        "Organizational Behavior (Tek)"
    ],
    "Dr. Öğr. Üyesi Hakan ERKAL": [
        "Organizational Behavior (Çift)"
    ],
    "Dr. Öğr. Üyesi A. Erhan ZALLUHOĞLU": [
        "Araştırma Yöntemleri (Çift)",
        "Araştırma Yöntemleri (Tek)",
        "Girişimcilik ve KOBİ Yönetimi"
    ],
    "Prof. Dr. Dilek DEMİRHAN": [
        "Financial Management I"
    ],
    "Dr. Öğr. Üyesi Esin GÜRBÜZ": [
        "İşletme Hukuku",
        "Borçlar Hukuku"
    ],
    "Prof. Dr. Ayla Özhan DEDEOĞLU": [
        "Consumer Behavior (Tek)"
    ],
    "Doç. Dr. Elif ÜSTÜNDAĞLI ERTEN": [
        "Consumer Behavior (Çift)",
        "Reklamcılık Yönetimi"
    ],
    "Prof. Dr. Murat KOCAMAZ": [
        "Operations Research I"
    ],
    "Doç. Dr. Haydar YALÇIN": [
        "Enformetri"
    ],
    "Prof. Dr. İpek KAZANÇOĞLU": [
        "Sürdürülebilir Pazarlama"
    ],
    "Dr. Öğr. Üyesi Ş. Sertaç ÇAKI": [
        "Yönetim Muhasebesi",
        "Mali Tablolar Analizi"
    ],
    "Doç. Dr. Aydın KOÇAK": [
        "E-İş ve Kurumsal Kaynak Planlama"
    ],
    "Prof. Dr. Haluk SOYUER": [
        "Teknoloji ve Sanayi Dinamikleri"
    ],
    "Prof. Dr. Türker SUSMUŞ": [
        "Uygulamalı Finansal Piyasa İşlemleri",
        "Muhasebe I (Örgün + İ.Ö.)",
        "Muhasebe II (Tasfiye)",
        "Uygulamalı Finansal Piyasa İşlemleri (Örgün)"
    ],
    "Prof. Dr. Derya İLİC": [
        "Management Consultancy",
        "Yönetim Geliştirme"
    ],
    "Doç. Dr. U. Gökay ÇİÇEKLİ": [
        "System Analysis and Design"
    ],
    "Prof. Dr. Burak ÇAPRAZ": [
        "Human Resources Management"
    ],
    "Prof. Dr. Aykan CANDEMİR": [
        "Global Marketing (Tek)"
    ],
    "Prof. Dr. Keti VENTURA": [
        "Global Marketing (Çift)"
    ],
    "Araş. Gör. Dr. Begüm KANAT TİRYAKİ": [
        "Business I (Tasfiye)",
        "Introduction to Business (Örgün + İ.Ö)"
    ],
    "Dr. Öğr. Üyesi Sema AYDIN": [
        "Hukukun Temel Kavramları (Örgün + İ.Ö.)",
        "Ticaret Hukuku (Tasfiye)"
    ]
}

gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma"]
saatler = [
    "09:00-12:00", "13:00-16:00", "16:00-19:00",
    "19:00-21:00"
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
