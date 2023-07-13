import sys

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import Qt

from module.setting import ConfigFile


class SettingWindow(QWidget):

    def __init__(self):
        super(SettingWindow, self).__init__()
        self.config = ConfigFile()
        self.initUi()

    def initUi(self) -> None:
        self.initUi_components()
        self.setWindowTitle('Настройка исключений')
        self.resize(800, 400)

    def initUi_components(self) -> None:
        self.main_layout = QVBoxLayout()
        self.users_layout = QVBoxLayout()
        self.gb_layout = QGroupBox('Студенты для исключений')
        btn_add_user = QPushButton('+')
        btn_add_user.clicked.connect(self.add_new_user)
        # Adding users
        for user in self.config.data:
            user: dict
            # Create new layout and components
            user_layout = QHBoxLayout()
            components = [
                self.new_user_line_edit(
                    name='user_id',
                    value=user.get('user_id', ''),
                    placeholder='ID студента',
                    max_width=50,
                ),
                self.new_user_line_edit(
                    name='user_name',
                    value=user.get('user_name', ''),
                    placeholder='ФИО студента (опционально)',
                ),
                self.new_user_line_edit(
                    name='comment',
                    value=user.get('comment', ''),
                    placeholder='Комментарий (опционально)',
                ),
                self.new_status_combobox(
                    status=user.get('status', 'remove'),
                ),
            ]
            # Add created components to layout
            for item in components:
                user_layout.addWidget(item)
            self.users_layout.addLayout(user_layout)
        # Add all to main_layout
        self.gb_layout.setLayout(self.users_layout)
        self.main_layout.addWidget(self.gb_layout)
        self.main_layout.addWidget(btn_add_user, alignment=Qt.AlignRight)
        btn_save_configure = QPushButton('Сохранить')
        btn_save_configure.clicked.connect(self.save_configure)
        # Configure window
        self.main_layout.addStretch()
        self.main_layout.addWidget(btn_save_configure, alignment=Qt.AlignLeft)
        self.setLayout(self.main_layout)

    def new_user_line_edit(self, name: str = '', value: str = '',
                           placeholder: str = '', max_width: int = 0,
                           ) -> QLineEdit:
        line_edit = QLineEdit(str(value))
        line_edit.name = name
        line_edit.setPlaceholderText(str(placeholder))
        # line_edit.value = str(placeholder)
        if max_width:
            line_edit.setMaximumWidth(max_width)
        return line_edit

    def new_status_combobox(self, status: str = 'remove') -> QComboBox:
        allow_status = dict(
            green='Зеленый',
            blue='Синий',
            red='Красный',
            other='Белый',
            remove='Не считать',
        )
        combobox = QComboBox()
        combobox.name = 'status'
        [combobox.addItem(status_name, status_key)
         for status_key, status_name in allow_status.items()]
        if status in allow_status:
            combobox.setCurrentText(allow_status[status])
        return combobox

    def add_new_user(self):
        layout = QHBoxLayout()
        layout.addWidget(self.new_user_line_edit(
            name='user_id', placeholder='ID студента', max_width=50))
        layout.addWidget(self.new_user_line_edit(
            name='user_name', placeholder='ФИО студента (опционально)'))
        layout.addWidget(self.new_user_line_edit(
            name='comment', placeholder='Комментарий (опционально)'))
        layout.addWidget(self.new_status_combobox())
        self.users_layout.addLayout(layout)

    def save_configure(self):

        def extract_values(user_layout):
            result = dict()
            for data_id in range(user_layout.count()):
                data_widget = user_layout.itemAt(data_id).widget()
                if isinstance(data_widget, QLineEdit):
                    result[data_widget.name] = data_widget.text()
                elif isinstance(data_widget, QComboBox):
                    result[data_widget.name] = data_widget.itemData(
                        data_widget.currentIndex())
            return result

        # Extract Widgets in main_layout
        new_config_data = list()
        # for widget_id in range(self.main_layout.count()):
        # Search QGroupBox widgets
        # gb_widget = self.main_layout.itemAt(widget_id).widget()
        # if isinstance(gb_widget, QGroupBox):
        #     # Extract main_users_layout from GroupBox widget
        #     category_name = gb_widget.value
        #     new_config_data[category_name] = list()
        gb_in_layout = self.gb_layout.children()[0]
        # Extraxt user_data from user_layouts
        for user_layout_id in range(gb_in_layout.count()):
            user_layout = gb_in_layout.itemAt(user_layout_id)
            user_data = extract_values(user_layout)
            if 'user_id' in user_data and user_data['user_id'].strip():
                new_config_data.append(user_data)
        # Saving
        self.config.data = new_config_data
        self.config.save_file()


if __name__ == '__main__':
    app = QApplication([])
    window = SettingWindow()
    window.show()
    sys.exit(app.exec_())
