# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QTableWidget, QTableWidgetItem, QLabel, QLineEdit,
                             QSpinBox, QDoubleSpinBox, QMessageBox, QDialog, QFormLayout,
                             QTabWidget, QFrame, QComboBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QColor, QIcon, QPalette, QBrush, QLinearGradient
from PyQt5.QtCore import QRect
from kütüphane3 import Market, Mal

class UrunEkleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ürün Ekle")
        self.setGeometry(100, 100, 400, 300)
        self.urun_data = None
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

        self.isim_input = QLineEdit()
        self.isim_input.setPlaceholderText("Ürün Adı")
        self.isim_input.setStyleSheet("padding: 8px; border-radius: 5px; border: 2px solid #3498db;")
        
        self.marka_input = QLineEdit()
        self.marka_input.setPlaceholderText("Ürün Markası")
        self.marka_input.setStyleSheet("padding: 8px; border-radius: 5px; border: 2px solid #3498db;")
        
        self.cins_input = QLineEdit()
        self.cins_input.setPlaceholderText("Ürün Cinsi")
        self.cins_input.setStyleSheet("padding: 8px; border-radius: 5px; border: 2px solid #3498db;")
        
        self.yer_input = QLineEdit()
        self.yer_input.setPlaceholderText("Ürünün Yeri")
        self.yer_input.setStyleSheet("padding: 8px; border-radius: 5px; border: 2px solid #3498db;")
        
        self.adet_input = QSpinBox()
        self.adet_input.setMinimum(0)
        self.adet_input.setMaximum(100000)
        self.adet_input.setStyleSheet("padding: 8px; border-radius: 5px; border: 2px solid #3498db;")
        
        self.fiyat_input = QDoubleSpinBox()
        self.fiyat_input.setMinimum(0)
        self.fiyat_input.setMaximum(1000000)
        self.fiyat_input.setDecimals(2)
        self.fiyat_input.setStyleSheet("padding: 8px; border-radius: 5px; border: 2px solid #3498db;")

        layout.addRow("İsim:", self.isim_input)
        layout.addRow("Marka:", self.marka_input)
        layout.addRow("Cins:", self.cins_input)
        layout.addRow("Yer:", self.yer_input)
        layout.addRow("Adet:", self.adet_input)
        layout.addRow("Fiyat:", self.fiyat_input)

        button_layout = QHBoxLayout()
        
        kaydet_btn = QPushButton("Kaydet")
        kaydet_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """)
        kaydet_btn.clicked.connect(self.kaydet)
        
        iptal_btn = QPushButton("İptal")
        iptal_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
        """)
        iptal_btn.clicked.connect(self.reject)

        button_layout.addWidget(kaydet_btn)
        button_layout.addWidget(iptal_btn)

        layout.addRow(button_layout)

        self.setLayout(layout)

    def kaydet(self):
        if not self.isim_input.text() or not self.marka_input.text() or not self.cins_input.text() or not self.yer_input.text():
            QMessageBox.warning(self, "Uyarı", "Lütfen tüm alanları doldurun!")
            return

        self.urun_data = {
            'isim': self.isim_input.text(),
            'marka': self.marka_input.text(),
            'cins': self.cins_input.text(),
            'yer': self.yer_input.text(),
            'adet': self.adet_input.value(),
            'fiyat': self.fiyat_input.value()
        }
        self.accept()


class MarketGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.market = Market()
        self.setWindowTitle("Market Stok Yönetimi")
        self.setGeometry(100, 100, 1200, 700)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ecf0f1;
            }
            QLabel {
                color: #2c3e50;
            }
        """)
        
        self.init_ui()
        self.tabloyu_guncelle()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()

        # Sol Panel - Kontrol Button
        left_panel = QFrame()
        left_panel.setStyleSheet("""
            QFrame {
                background-color: #34495e;
                border-radius: 10px;
            }
        """)
        left_layout = QVBoxLayout()

        title_label = QLabel("Market Yönetimi")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: white; padding: 15px;")
        left_layout.addWidget(title_label)

        # Şıra paneli
        self.toplam_urun_label = QLabel("Toplam Ürün: 0")
        self.toplam_urun_label.setStyleSheet("color: #ecf0f1; font-size: 12px; padding: 10px;")
        left_layout.addWidget(self.toplam_urun_label)

        self.toplam_adet_label = QLabel("Toplam Adet: 0")
        self.toplam_adet_label.setStyleSheet("color: #ecf0f1; font-size: 12px; padding: 10px;")
        left_layout.addWidget(self.toplam_adet_label)

        left_layout.addSpacing(20)

        # Butonlar
        ekle_btn = QPushButton("➕ Ürün Ekle")
        ekle_btn.setStyleSheet(self.buton_style("#3498db", "#2980b9", "#1f618d"))
        ekle_btn.clicked.connect(self.urun_ekle)
        left_layout.addWidget(ekle_btn)

        sil_btn = QPushButton("🗑️ Ürün Sil")
        sil_btn.setStyleSheet(self.buton_style("#e74c3c", "#c0392b", "#a93226"))
        sil_btn.clicked.connect(self.urun_sil)
        left_layout.addWidget(sil_btn)

        guncelle_btn = QPushButton("✏️ Ürün Güncelle")
        guncelle_btn.setStyleSheet(self.buton_style("#f39c12", "#d68910", "#b7590f"))
        guncelle_btn.clicked.connect(self.urun_guncelle)
        left_layout.addWidget(guncelle_btn)

        ara_btn = QPushButton("🔍 Ürün Ara")
        ara_btn.setStyleSheet(self.buton_style("#9b59b6", "#7d3c98", "#6c3483"))
        ara_btn.clicked.connect(self.ara_dialog_ac)
        left_layout.addWidget(ara_btn)

        left_layout.addSpacing(20)

        yenile_btn = QPushButton("🔄 Yenile")
        yenile_btn.setStyleSheet(self.buton_style("#27ae60", "#229954", "#1e8449"))
        yenile_btn.clicked.connect(self.tabloyu_guncelle)
        left_layout.addWidget(yenile_btn)

        left_layout.addSpacing(30)

        cikis_btn = QPushButton("❌ Çıkış")
        cikis_btn.setStyleSheet(self.buton_style("#7f8c8d", "#566573", "#34495e"))
        cikis_btn.clicked.connect(self.close)
        left_layout.addWidget(cikis_btn)

        left_layout.addStretch()

        left_panel.setLayout(left_layout)
        left_panel.setMaximumWidth(200)

        # Sağ Panel - Tablo
        right_layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["İsim", "Marka", "Cins", "Yer", "Adet", "Fiyat"])
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border-radius: 5px;
                border: 1px solid #bdc3c7;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 5px;
                border: none;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 5px;
                border: 1px solid #ecf0f1;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)
        self.table.setSelectionBehavior(self.table.SelectRows)
        self.table.setSelectionMode(self.table.SingleSelection)
        right_layout.addWidget(self.table)

        main_layout.addWidget(left_panel)
        main_layout.addLayout(right_layout, 1)

        central_widget.setLayout(main_layout)

    def buton_style(self, normal_color, hover_color, pressed_color):
        return f"""
            QPushButton {{
                background-color: {normal_color};
                color: white;
                border: none;
                padding: 12px 10px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 11px;
                margin: 5px 0px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {pressed_color};
            }}
        """

    def tabloyu_guncelle(self):
        self.table.setRowCount(0)
        try:
            urunler = self.market.tum_urunleri_al()
        except Exception as e:
            print(f"Hata: {e}")
            return
        
        if not urunler:
            return
            
        for row, urun in enumerate(urunler):
            if len(urun) < 6:
                print(f"Uyarı: Ürün verisi eksik - {urun}")
                continue
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(urun[0])))
            self.table.setItem(row, 1, QTableWidgetItem(str(urun[1])))
            self.table.setItem(row, 2, QTableWidgetItem(str(urun[2])))
            self.table.setItem(row, 3, QTableWidgetItem(str(urun[3])))
            self.table.setItem(row, 4, QTableWidgetItem(str(urun[4])))
            self.table.setItem(row, 5, QTableWidgetItem(str(urun[5])))

        self.istatistikleri_guncelle()
        self.table.resizeColumnsToContents()

    def istatistikleri_guncelle(self):
        toplam_urun, toplam_adet = self.market.istatistikler()
        self.toplam_urun_label.setText(f"Toplam Ürün: {toplam_urun if toplam_urun else 0}")
        self.toplam_adet_label.setText(f"Toplam Adet: {toplam_adet if toplam_adet else 0}")

    def urun_ekle(self):
        dialog = UrunEkleDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.urun_data
            mal = Mal(data['isim'], data['marka'], data['cins'], data['yer'], data['adet'], data['fiyat'])
            try:
                self.market.ürün_ekle(mal)
                QMessageBox.information(self, "Başarı", f"'{data['isim']}' başarıyla eklendi!")
                self.tabloyu_guncelle()
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Ürün eklenirken hata oluştu: {str(e)}")

    def urun_sil(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Uyarı", "Lütfen silecek bir ürün seçin!")
            return

        isim = self.table.item(current_row, 0).text()
        reply = QMessageBox.question(self, "Onayla", f"'{isim}' silinsin mi?", 
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                self.market.ürün_sil(isim)
                QMessageBox.information(self, "Başarı", "Ürün silindi!")
                self.tabloyu_guncelle()
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Ürün silinirken hata oluştu: {str(e)}")

    def urun_guncelle(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Uyarı", "Lütfen güncellenecek bir ürün seçin!")
            return

        eski_isim = self.table.item(current_row, 0).text()
        
        dialog = UrunEkleDialog(self)
        dialog.isim_input.setText(eski_isim)
        dialog.marka_input.setText(self.table.item(current_row, 1).text())
        dialog.cins_input.setText(self.table.item(current_row, 2).text())
        dialog.yer_input.setText(self.table.item(current_row, 3).text())
        dialog.adet_input.setValue(int(self.table.item(current_row, 4).text()))
        dialog.fiyat_input.setValue(float(self.table.item(current_row, 5).text()))

        if dialog.exec_() == QDialog.Accepted:
            data = dialog.urun_data
            mal = Mal(data['isim'], data['marka'], data['cins'], data['yer'], data['adet'], data['fiyat'])
            try:
                self.market.urun_guncelle(eski_isim, mal)
                QMessageBox.information(self, "Başarı", "Ürün güncellendi!")
                self.tabloyu_guncelle()
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Ürün güncellenirken hata oluştu: {str(e)}")

    def ara_dialog_ac(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Ürün Ara")
        dialog.setGeometry(100, 100, 300, 150)
        
        layout = QVBoxLayout()
        
        ara_input = QLineEdit()
        ara_input.setPlaceholderText("İsmıne göre ara")
        ara_input.setStyleSheet("padding: 8px; border-radius: 5px; border: 2px solid #3498db; font-size: 12px;")
        layout.addWidget(ara_input)

        button_layout = QHBoxLayout()
        
        ara_btn = QPushButton("Ara")
        ara_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        
        def ara():
            isim = ara_input.text()
            if not isim:
                QMessageBox.warning(dialog, "Uyarı", "Lütfen bir Ürün adı girin!")
                return
            
            sonuc = self.market.urun_ara(isim)
            if sonuc:
                self.table.setRowCount(0)
                for row, urun in enumerate(sonuc):
                    self.table.insertRow(row)
                    self.table.setItem(row, 0, QTableWidgetItem(str(urun[0])))
                    self.table.setItem(row, 1, QTableWidgetItem(str(urun[1])))
                    self.table.setItem(row, 2, QTableWidgetItem(str(urun[2])))
                    self.table.setItem(row, 3, QTableWidgetItem(str(urun[3])))
                    self.table.setItem(row, 4, QTableWidgetItem(str(urun[4])))
                    self.table.setItem(row, 5, QTableWidgetItem(str(urun[5])))
                dialog.close()
            else:
                QMessageBox.information(dialog, "Sonuç", f"'{isim}' adı altında ürün bulunamadı!")

        ara_btn.clicked.connect(ara)
        button_layout.addWidget(ara_btn)
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        dialog.exec_()

    def closeEvent(self, event):
        self.market.baglantiyi_kes()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = MarketGUI()
    gui.show()
    sys.exit(app.exec_())
