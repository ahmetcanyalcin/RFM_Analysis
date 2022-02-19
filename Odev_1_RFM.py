
***** RFM ile Musteri alanizi*****



import pandas as pd

# 1) Online Retail II excelindeki 2010-2011 verisini okuyunuz. Oluşturduğunuz dataframe’in kopyasını oluşturunuz.
df_ = pd.read_excel("D:\VBO Veri Bilimi Okulu Bootcamp Eğitimi\Veri Bilimi için Pyhton Dersi çalışmaları\Veri Setleri\online_retail_II.xlsx", sheet_name="Year 2010-2011")
df = df_.copy()
df.head()
# 2) Online Retail II excelindeki 2010-2011 verisini okuyunuz. Oluşturduğunuz dataframe’in kopyasını oluşturunuz.
# 3) Veri setinde eksik gözlem var mı? Varsa hangi değişkende kaç tane eksik gözlem vardır?
df.isnull().sum()

# 4) Eksik gözlemleri veri setinden çıkartınız. Çıkarma işleminde ‘inplace=True’ parametresini kullanınız.
df.shape
df.dropna(inplace=True)
df.shape

# 5) Eşsiz ürün sayısı kaçtır?
list(df.head())
df["StockCode"].nunique()

# 6) Hangi üründen kaçar tane vardır?

list(df.head())

df.groupby("StockCode")["Quantity"].agg("count")

# 7) En çok sipariş edilen 5 ürünü çoktan aza doğru sıralayınız.

df.groupby("StockCode")["Quantity"].agg("sum").sort_values(ascending=False).head(5)

# 8) Faturalardaki ‘C’ iptal edilen işlemleri göstermektedir. İptal edilen işlemleri veri setinden çıkartınız.

df = df[~df["Invoice"].str.contains("C", na=False)]

# 9) Fatura başına elde edilen toplam kazancı ifade eden ‘TotalPrice’ adında bir değişken oluşturunuz.

df["TotalPrice"] = df["Price"] * df["Quantity"]
df.head()
# ####################################
# Görev 2: RFM metriklerinin hesaplanması
# ####################################

# Not 1: recency değeri için bugünün tarihini (2011, 12, 11) olarak kabul ediniz.
# Not 2: rfm dataframe’ini oluşturduktan sonra veri setini "monetary>0" olacak şekilde filtreleyiniz.

# Recency, Frequency ve Monetary tanımlarını yapınız.
# Müşteri özelinde Recency, Frequency ve Monetary metriklerini groupby, agg ve lambda ile hesaplayınız.
# Hesapladığınız metrikleri rfmisimli bir değişkene atayınız.
# Oluşturduğunuz metriklerin isimlerini recency, frequency ve monetary olarak değiştiriniz.

""""
# Recency   = Tarihle alakalı değerler içerir Ör: gün hafta vb.
# Frequency = bir şeyin kaç defa yapıldığının/tekrar edildiğinin sayısıdır
# Monetary  = Para para para :D 


"""


today_date = df.datetime(2011, 12, 11)

rfm = df.groupby('Customer ID').agg({'InvoiceDate': lambda date: (today_date - date.max()).days,
                                     'Invoice': lambda num: num.nunique(),
                                     'TotalPrice': lambda total: total.sum()})

rfm.columns = ["Recency", "Frequency", "Monetary"]

rfm = rfm[rfm["Monetary"] > 0]


# ####################################
# Görev 3: RFM skorlarının oluşturulması ve tek bir değişkene çevrilmesi
# ####################################

#  Recency, Frequency ve Monetary metriklerini qcut yardımı ile 1-5 arasında skorlara çeviriniz.
#  Bu skorları recency_score, frequency_score ve monetary_score olarak kaydediniz.
#  Oluşan 3 farklı değişkenin değerini tek bir değişken olarak ifade ediniz ve RFM_SCORE olarak kaydediniz.
# Örneğin;
# Ayrı ayrı değişkenlerde sırasıyla 5, 2, 1 olan recency_score, frequency_score ve monetary_score skorlarını
# RFM_SCORE değişkeni isimlendirmesi ile 521 olarak oluşturunuz.

rfm["recency_score"] = pd.qcut(rfm["Recency"], 5, labels=[5, 4, 3, 2, 1])

rfm["frequency_score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])

rfm["monetary_score"] = pd.qcut(rfm["Monetary"], 5, labels=[1, 2, 3, 4, 5])


rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) +
                    rfm['frequency_score'].astype(str) +
                    rfm['monetary_score'].astype(str))

# ####################################
# Görev 4: RFM skorlarının segment olarak tanımlanması
# ####################################
#  Oluşturulan RFM skorların daha açıklanabilir olması için segment tanımlamaları yapınız.
#  Aşağıdaki seg_map yardımı ile skorları segmentlere çeviriniz.




seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

rfm['segment'] = (rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str)).replace(seg_map, regex=True)

