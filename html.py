import pandas as pd

# =============================
# 1. EXCEL DOSYASINI OKU
# =============================
excel_dosya = "isletme_ders_programi.xlsx"
df = pd.read_excel(excel_dosya, index_col=0)

# =============================
# 2. \n -> <br> DÖNÜŞÜMÜ (UYARI YOK)
# =============================
df = df.astype(str).map(lambda x: x.replace("\n", "<br>"))

# =============================
# 3. HTML TABLOYA DÖNÜŞTÜR
# =============================
html_tablo = df.to_html(
    border=1,
    justify="center",
    escape=False  # <br> çalışsın
)

# =============================
# 4. HTML ŞABLONU
# =============================
html_sablon = f"""
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Ders Programı</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            padding: 20px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
        }}
        th, td {{
            border: 1px solid #333;
            padding: 8px;
            text-align: center;
            vertical-align: top;
            white-space: normal;
        }}
        th {{
            background-color: #f2f2f2;
        }}
    </style>
</head>
<body>

<h2>Ders Programı</h2>

{html_tablo}

</body>
</html>
"""

# =============================
# 5. HTML DOSYASINA YAZ
# =============================
with open("ders_programi.html", "w", encoding="utf-8") as f:
    f.write(html_sablon)

print("✅ HTML dosyası başarıyla oluşturuldu: ders_programi.html")
