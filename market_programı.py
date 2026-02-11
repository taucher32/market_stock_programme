import kütüphane3
from kütüphane3 import *

import time
print("""****************************

Market Ürün Programı

1.Ürünleri göster

2.Ürün sorgula

3.Ürün ekle

4.Ürün sil

5.Ürün Güncelle

****************************""")

kütüphane = Market()

while True:
    işlem = input("Yapmak istediğiniz işlemi girin:")

    if (işlem == "q"):
        print("Çıkıs yapılıyor.")
        time.sleep(1)
        break
    elif (işlem == "1"):
        print("Ürünler gösteriliyor.")
        time.sleep(1)
        kütüphane.ürünleri_göster()
    elif (işlem == "2"):
        isim = input("Aranan Ürün:")
        print("Ürün sorgulanıyor")
        time.sleep(1)
        kütüphane.ürün_sorgulama(isim)
    elif (işlem == "3"):
        isim = input("Eklenecek marka:")
        cins = input("Ürünün cinsi:")
        yer = input("Ürünün yeri:")
        adet = input("Ürün miktarı:")
        fiyat = input("Ürünün fiyatı:")
        yeni_ürün = Mal(isim,cins,yer,adet,fiyat)
        print("Ürün ekleniyor.")
        time.sleep(1)
        kütüphane.ürün_ekle(yeni_ürün)
        print("Ürün eklendi.")
    elif (işlem == "4"):
        isim = input("Silinecek ürün:")
        print("Ürün siliniyor.")
        time.sleep(1)
        kütüphane.ürün_sil(isim)
        print("Ürün silindi.")
    elif (işlem == "5"):
        isim = input("Güncellenecek Ürün:")
        print("Güncellenecek ürün Seçin")
        kütüphane3.Market.ürün_güncelle(isim, yeni_ürün)

