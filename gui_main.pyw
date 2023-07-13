import os
import sys

from PyQt5.QtCore import QObject
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from dotenv import load_dotenv
from dotenv import find_dotenv

from module.priemka_site import PriemkaSite
from module.setting import ConfigFile
from gui_setting import SettingWindow


class MainWindow(QMainWindow):
    thread = QThread()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUi()

    def initUi(self):
        self.initUi_components()
        self.resize(350, 250)
        self.setMinimumSize(350, 200)
        self.setMaximumSize(350, 250)
        self.setWindowTitle('Отчеты приемка')

    def initUi_components(self):
        main_layout = QVBoxLayout()
        site_layout = QHBoxLayout()
        site_layout_spo = QVBoxLayout()
        site_layout_spo_title = QHBoxLayout()
        site_layout_spo_title.setAlignment(Qt.AlignCenter)
        site_layout_spo_green = QHBoxLayout()
        site_layout_spo_blue = QHBoxLayout()
        site_layout_spo_red = QHBoxLayout()
        site_layout_spo_other = QHBoxLayout()
        site_layout_spo_all = QHBoxLayout()
        site_layout_vpo = QVBoxLayout()
        site_layout_vpo_title = QHBoxLayout()
        site_layout_vpo_title.setAlignment(Qt.AlignCenter)
        site_layout_vpo_green = QHBoxLayout()
        site_layout_vpo_blue = QHBoxLayout()
        site_layout_vpo_red = QHBoxLayout()
        site_layout_vpo_other = QHBoxLayout()
        site_layout_vpo_all = QHBoxLayout()
        site_layout_system = QVBoxLayout()

        # Site head layout
        l_spo_title = QLabel('СПО', self)
        site_layout_spo_title.addWidget(l_spo_title)
        l_vpo_title = QLabel('ВПО', self)
        site_layout_vpo_title.addWidget(l_vpo_title)

        # Green SPO
        l_spo_green_name = QLabel('Зеленые: ', self)
        self.l_spo_green_result = QLabel('', self)
        site_layout_spo_green.addWidget(l_spo_green_name)
        site_layout_spo_green.addWidget(self.l_spo_green_result)
        # Green VPO
        l_vpo_green_name = QLabel('Зеленые: ', self)
        self.l_vpo_green_result = QLabel('', self)
        site_layout_vpo_green.addWidget(l_vpo_green_name)
        site_layout_vpo_green.addWidget(self.l_vpo_green_result)
        # Blue SPO
        l_spo_blue_name = QLabel('Синие: ', self)
        self.l_spo_blue_result = QLabel('', self)
        site_layout_spo_blue.addWidget(l_spo_blue_name)
        site_layout_spo_blue.addWidget(self.l_spo_blue_result)
        # Blue VPO
        l_vpo_blue_name = QLabel('Синие: ', self)
        self.l_vpo_blue_result = QLabel('', self)
        site_layout_vpo_blue.addWidget(l_vpo_blue_name)
        site_layout_vpo_blue.addWidget(self.l_vpo_blue_result)
        # Red SPO
        l_spo_red_name = QLabel('Красные: ', self)
        self.l_spo_red_result = QLabel('', self)
        site_layout_spo_red.addWidget(l_spo_red_name)
        site_layout_spo_red.addWidget(self.l_spo_red_result)
        # Red VPO
        l_vpo_red_name = QLabel('Красные: ', self)
        self.l_vpo_red_result = QLabel('', self)
        site_layout_vpo_red.addWidget(l_vpo_red_name)
        site_layout_vpo_red.addWidget(self.l_vpo_red_result)
        # Other SPO
        l_spo_other_name = QLabel('Остальные: ', self)
        self.l_spo_other_result = QLabel('', self)
        site_layout_spo_other.addWidget(l_spo_other_name)
        site_layout_spo_other.addWidget(self.l_spo_other_result)
        # Other VPO
        l_vpo_other_name = QLabel('Остальные: ', self)
        self.l_vpo_other_result = QLabel('', self)
        site_layout_vpo_other.addWidget(l_vpo_other_name)
        site_layout_vpo_other.addWidget(self.l_vpo_other_result)
        # All SPO
        l_spo_all_name = QLabel('Всего: ', self)
        self.l_spo_all_result = QLabel('', self)
        site_layout_spo_all.addWidget(l_spo_all_name)
        site_layout_spo_all.addWidget(self.l_spo_all_result)
        # All VPO
        l_vpo_all_name = QLabel('Всего: ', self)
        self.l_vpo_all_result = QLabel('', self)
        site_layout_vpo_all.addWidget(l_vpo_all_name)
        site_layout_vpo_all.addWidget(self.l_vpo_all_result)
        # Update button
        self.btn_update = QPushButton('Обновить')
        self.btn_update.clicked.connect(self._update_scan_result)
        site_layout_system.addWidget(self.btn_update)
        # System info
        # UpDate date
        self.l_update_date = QLabel('', self)
        site_layout_system.addWidget(self.l_update_date)
        # Settings button
        btn_setting_window = QPushButton('Исключения')
        btn_setting_window.clicked.connect(self.open_setting_window)
        site_layout_system.addWidget(
            btn_setting_window,
            alignment=Qt.AlignRight,
        )

        # Add to main_layout
        # SPO layout
        site_layout_spo.addLayout(site_layout_spo_title)
        site_layout_spo.addLayout(site_layout_spo_green)
        site_layout_spo.addLayout(site_layout_spo_blue)
        site_layout_spo.addLayout(site_layout_spo_red)
        site_layout_spo.addLayout(site_layout_spo_other)
        site_layout_spo.addLayout(site_layout_spo_all)
        # VPO
        site_layout_vpo.addLayout(site_layout_vpo_title)
        site_layout_vpo.addLayout(site_layout_vpo_green)
        site_layout_vpo.addLayout(site_layout_vpo_blue)
        site_layout_vpo.addLayout(site_layout_vpo_red)
        site_layout_vpo.addLayout(site_layout_vpo_other)
        site_layout_vpo.addLayout(site_layout_vpo_all)
        # Other
        # Main layout
        site_layout.addLayout(site_layout_spo)
        site_layout.addLayout(site_layout_vpo)
        main_layout.addLayout(site_layout)
        main_layout.addLayout(site_layout_system)
        # Show main window
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def set_spo_scan_result(self, result: dict = dict()):
        self.l_spo_green_result.setText(str(len(result.get('green', []))))
        self.l_spo_blue_result.setText(str(len(result.get('blue', []))))
        self.l_spo_red_result.setText(str(len(result.get('red', []))))
        self.l_spo_other_result.setText(str(len(result.get('other', []))))
        self.l_spo_all_result.setText(str(len(result.get('all', []))))

    def set_vpo_scan_result(self, result: dict = dict()):
        self.l_vpo_green_result.setText(str(len(result.get('green', []))))
        self.l_vpo_blue_result.setText(str(len(result.get('blue', []))))
        self.l_vpo_red_result.setText(str(len(result.get('red', []))))
        self.l_vpo_other_result.setText(str(len(result.get('other', []))))
        self.l_vpo_all_result.setText(str(len(result.get('all', []))))

    def _update_scan_result(self):
        if not os.getenv('LOGIN') \
            or not os.getenv('PASSWORD') \
                or not os.getenv('DOMAIN'):
            self.l_update_date.setText('Необходимо указать переменные '
                                       'среды:\nLOGIN, PASSWORD, DOMAIN')
            return
        self.set_spo_scan_result()
        self.set_vpo_scan_result()
        self.btn_update.setEnabled(False)
        self.worker = ThreadUpdate()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.start()

        self.worker.progress.connect(
            lambda: self.l_update_date.setText(
                str(self.worker.progress_string)))
        self.worker.spo_finished.connect(
            lambda: self.set_spo_scan_result(self.worker.spo_result))
        self.worker.vpo_finished.connect(
            lambda: self.set_vpo_scan_result(self.worker.vpo_result))
        self.worker.finished.connect(
            lambda: self.btn_update.setEnabled(True))
        self.worker.finished.connect(
            lambda: self.thread.terminate())

    def open_setting_window(self):
        self.setting_window = SettingWindow()
        self.setting_window.show()


class ThreadUpdate(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal()
    progress_string = str()
    spo_finished = pyqtSignal()
    spo_result = dict()
    vpo_finished = pyqtSignal()
    vpo_result = dict()

    def run(self):
        config = ConfigFile()
        site = PriemkaSite(
            login=os.getenv('LOGIN'),
            password=os.getenv('PASSWORD'),
            domain=os.getenv('DOMAIN'),
        )
        self.progress_string = 'Авторизация...'
        self.progress.emit()
        try:
            site.authentication()
            self.progress_string = ''
            self.progress.emit()
        except Exception:
            self.progress_string = 'Ошибка авторизации'
            self.progress.emit()
            self.finished.emit()
            return False
        # SPO
        self.progress_string = 'Получение результатов СПО'
        self.progress.emit()
        self.spo_result = config.repair_data(
            site.search_users(faculty=9),
        )
        self.spo_finished.emit()
        # VPO
        self.progress_string = 'Получение результатов ВПО'
        self.progress.emit()
        self.vpo_result = config.repair_data(
            site.search_users(faculty=21),
        )
        self.vpo_finished.emit()
        # Finished
        self.progress_string = 'Успешно'
        self.progress.emit()
        self.finished.emit()


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
