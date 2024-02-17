import cv2
from pyzbar import pyzbar
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap

class QRCodeScannerThread(QThread):
    image_signal = pyqtSignal(object)
    result_signal = pyqtSignal(object)

    def run(self):
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        camera = cv2.VideoCapture(0)

        while True:
            ret, frame = camera.read()

            if not ret:
                break

            barcodes = self.decode_qr_code(frame)

            if barcodes:
                self.result_signal.emit(barcodes)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.image_signal.emit(qt_image)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        camera.release()
        cv2.destroyAllWindows()

    def decode_qr_code(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        barcodes = pyzbar.decode(gray)

        if len(barcodes) == 0:
            return None

        results = []
        for barcode in barcodes:
            barcode_data = barcode.data.decode("utf-8")
            barcode_type = barcode.type
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            results.append({"data": barcode_data, "type": barcode_type, "datetime": current_datetime})

        return results

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("QR Code Scanner")
        self.setGeometry(100, 100, 660, 620)

        self.setStyleSheet("background-color: #F0F0F0;")

        self.video_label = QtWidgets.QLabel(self)
        self.video_label.setGeometry(QtCore.QRect(10, 40, 640, 480))
        self.video_label.setScaledContents(True)

        self.result_text = QtWidgets.QTextEdit(self)
        self.result_text.setGeometry(QtCore.QRect(10, 530, 640, 80))

        self.welcome_label = QtWidgets.QLabel(self)
        self.welcome_label.setGeometry(QtCore.QRect(10, 10, 300, 30))
        self.welcome_label.setText("Welcome! Start scanning QR codes.")
        self.welcome_label.setStyleSheet("color: #336699; font-size: 18px; font-weight: bold;")

        self.goodbye_label = QtWidgets.QLabel(self)
        self.goodbye_label.setGeometry(QtCore.QRect(10, 620, 300, 30))
        self.goodbye_label.setText("Goodbye!")
        self.goodbye_label.setStyleSheet("color: #336699; font-size: 18px; font-weight: bold;")

        self.scanner_thread = QRCodeScannerThread()
        self.scanner_thread.image_signal.connect(self.update_video_label)
        self.scanner_thread.result_signal.connect(self.handle_results)
        self.scanner_thread.start()

    def update_video_label(self, image):
        pixmap = QPixmap.fromImage(image)
        self.video_label.setPixmap(pixmap)

    def handle_results(self, results):
        self.result_text.clear()

        if results is not None:
            for result in results:
                self.result_text.append(result["data"])

            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.result_text.append("سلام")
            self.result_text.append("التاريخ والوقت: " + current_datetime)
        else:
            self.result_text.append("No QR code found.")

app = QtWidgets.QApplication([])
window = MainWindow()
window.show()
app.exec()