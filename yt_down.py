import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                             QLineEdit, QLabel, QRadioButton, QButtonGroup, 
                             QMessageBox, QFileDialog)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import yt_dlp

class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.download_directory = os.getcwd()  
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("YouTube Downloader")
        self.setGeometry(100, 100, 400, 350)

        layout = QVBoxLayout()

        self.ascii_label = QLabel("""\
▄▄▄              ▪
▀▄ █·▪     ▪    ▄██
▐▀▀▄  ▄█▀▄  ▄█▀▄ ▐█·
▐█•█▌▐█▌.▐▌▐█▌.▐▌▐█▌
.▀  ▀ ▀█▄▀▪ ▀█▄▀▪▀▀▀""", self)

        font = QFont("Courier New", 10)  
        self.ascii_label.setFont(font)
        self.ascii_label.setAlignment(Qt.AlignCenter)  
        layout.addWidget(self.ascii_label)

        
        self.url_label = QLabel("Insira a URL do vídeo:", self)
        layout.addWidget(self.url_label)

        self.url_input = QLineEdit(self)
        layout.addWidget(self.url_input)

        
        self.radio_group = QButtonGroup(self)

        self.radio_music = QRadioButton("Música (MP3)", self)
        self.radio_video = QRadioButton("Vídeo (MP4)", self)
        layout.addWidget(self.radio_music)
        layout.addWidget(self.radio_video)

        self.radio_group.addButton(self.radio_music)
        self.radio_group.addButton(self.radio_video)

        
        self.choose_directory_button = QPushButton("Escolher diretório de download", self)
        self.choose_directory_button.clicked.connect(self.choose_directory)
        layout.addWidget(self.choose_directory_button)

        
        self.download_button = QPushButton("Baixar", self)
        self.download_button.clicked.connect(self.download_media)
        layout.addWidget(self.download_button)

        
        self.setLayout(layout)

    def choose_directory(self):
        
        directory = QFileDialog.getExistingDirectory(self, "Escolha o diretório")
        if directory:
            self.download_directory = directory
            QMessageBox.information(self, "Diretório selecionado", f"O download será salvo em: {self.download_directory}")

    def download_media(self):
        url = self.url_input.text()
        if not url:
            QMessageBox.warning(self, "Erro", "Por favor, insira uma URL.")
            return

        if not self.radio_music.isChecked() and not self.radio_video.isChecked():
            QMessageBox.warning(self, "Erro", "Por favor, selecione se deseja baixar música ou vídeo.")
            return

        ydl_opts = {}

        
        output_template = os.path.join(self.download_directory, '%(title)s.%(ext)s')

        if self.radio_music.isChecked():
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': output_template,  
            }
        elif self.radio_video.isChecked():
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
                'outtmpl': output_template,
            }

        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            QMessageBox.information(self, "Sucesso", "Download concluído!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro: {str(e)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = YouTubeDownloader()
    window.show()
    sys.exit(app.exec_())
