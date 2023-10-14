from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from convert import Ui_MainWindow
import sys
import qrcode
from PIL import Image

class QR(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.clear.clicked.connect(self.clear)
        self.ui.exit.clicked.connect(self.exit)
        self.ui.generate.clicked.connect(self.generate_qr)
        self.ui.save.clicked.connect(self.save_qr_image)

    def save_qr_image(self):
        qr_text = self.ui.lineEdit.text()
        if qr_text:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_text)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            # QR kodunu PNG olarak kaydetme
            file_name , _ = QFileDialog.getSaveFileName(self, "Save QR Code", "", "Images (*.png)")
            if file_name:
                img.save(file_name)
                self.ui.statusbar.showMessage("QR Code saved successfully!", 5000)
            else:
                self.ui.statusbar.showMessage("Saving operation canceled.", 5000)
        else:
            self.ui.statusbar.showMessage("Please enter text to generate QR code.", 5000)

    def generate_qr(self):
        qr_text = self.ui.lineEdit.text()
        if qr_text:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_text)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            # QR kodunu QImage nesnesine dönüştürme
            img_qt = self.pil_image_to_qimage(img)
            pixmap = QPixmap.fromImage(img_qt)

            # QR kodu 'result' QLabel'a yerleştirme
            self.ui.result.setPixmap(pixmap.scaled(251, 221))
            self.ui.statusbar.showMessage("QR Code generated successfully!", 5000)
        else:
            self.ui.result.clear()
            self.ui.statusbar.showMessage("Please enter text to generate QR code.", 5000)

    def pil_image_to_qimage(self, img):
        data = img.convert("RGBA").tobytes("raw", "RGBA")
        qimage = QImage(data, img.size[0], img.size[1], QImage.Format_ARGB32)
        return qimage

    def clear(self):
        self.ui.lineEdit.clear()
        self.ui.result.clear()
        self.ui.statusbar.clearMessage()

    def exit(self):
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QR()
    window.show()
    sys.exit(app.exec_())
