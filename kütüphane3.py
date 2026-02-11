# -*- coding: utf-8 -*-
import sqlite3

class Mal():
    def __init__(self, isim, marka, cins, yer, adet, fiyat):

        self.isim = isim
        self.marka = marka
        self.cins = cins
        self.yer = yer
        self.adet = adet
        self.fiyat = fiyat

    def __str__(self):
        return "Isim:{}\nMarka:{}\nCins:{}\nYer:{}\nAdet:{}\nFiyat:{}\n".format(self.isim, self.marka,self.cins,self.yer,self.adet,self.fiyat)

class Market():
    def __init__(self):
        self.baglanti_olustur()

    def baglanti_olustur(self):

        self.baglanti = sqlite3.connect("kütüphane3.db")

        self.cursor = self.baglanti.cursor()

        sorgu = "CREATE TABLE IF NOT EXISTS market (isim TEXT PRIMARY KEY, marka TEXT, cins TEXT, yer TEXT, adet INT, fiyat REAL)"

        self.cursor.execute(sorgu)
        self.baglanti.commit()

    def baglantiyi_kes(self):
        self.baglanti.close()

    def ürünleri_göster(self):

        sorgu = "Select * From market"

        self.cursor.execute(sorgu)

        market = self.cursor.fetchall()

        if (len(market) == 0):
            print("Herhangi bir ürün bulumamaktadır.")
        else:
            for i in market:
                ürün = Mal(i[0],i[1],i[2],i[3],i[4],i[5])
                print(ürün)

    def ürün_sorgulama(self, isim):

        sorgu = "Select * From market where isim = ?"

        self.cursor.execute(sorgu,(isim,))

        market = self.cursor.fetchall()

        if (len(market) == 0):
            print("Böyle bir ürün bulumamaktadır.")
        else:
            ürün = Mal(market[0][0],market[0][1],market[0][2],market[0][3],market[0][4],market[0][5])
            print(ürün)

    def ürün_ekle(self, mal):

        sorgu = "Insert into market Values (?,?,?,?,?,?)"

        self.cursor.execute(sorgu,(mal.isim,mal.marka,mal.cins,mal.yer,mal.adet,mal.fiyat))

        self.baglanti.commit()

    def urun_sil(self, isim):

        sorgu = "Delete From market where isim = ?"

        self.cursor.execute(sorgu,(isim,))

        self.baglanti.commit()

    def urun_guncelle(self, eski_isim, mal):
        sorgu = "UPDATE market SET isim = ?, marka = ?, cins = ?, yer = ?, adet = ?, fiyat = ? WHERE isim = ?"
        self.cursor.execute(sorgu, (mal.isim, mal.marka, mal.cins, mal.yer, mal.adet, mal.fiyat, eski_isim))
        self.baglanti.commit()

    def tum_urunleri_al(self):
        sorgu = "Select * From market"
        self.cursor.execute(sorgu)
        return self.cursor.fetchall()

    def urun_ara(self, isim):
        sorgu = "Select * From market where isim LIKE ?"
        self.cursor.execute(sorgu, ('%' + isim + '%',))
        return self.cursor.fetchall()

    def istatistikler(self):
        sorgu = "SELECT COUNT(*) as toplam_urun, SUM(adet) as toplam_adet FROM market"
        self.cursor.execute(sorgu)
        result = self.cursor.fetchone()
        return result if result else (0, 0)
