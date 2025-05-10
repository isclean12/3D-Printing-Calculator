import sys
import json
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QGroupBox, QFormLayout,
                             QDoubleSpinBox, QSpinBox, QTabWidget, QStyleFactory)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPalette, QColor, QDesktopServices
from PyQt5 import QtGui

class CostCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Калькулятор стоимости 3D-печати")
        self.setGeometry(100, 100, 300, 600)
        ico = QtGui.QIcon("Calculator.ico")
        self.setWindowIcon(ico)  # Значок для окна
        self.setWindowIcon(ico)  # Значок приложения

        # Имя файла для сохранения настроек
        self.settings_file = "calculator_settings.json"

        # Применяем темную тему при создании окна
        self.set_dark_theme()

        self.initUI()
        self.load_settings()  # Загружаем сохраненные настройки

    def initUI(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        # Кнопка переключения темы
        self.theme_btn = QPushButton("Переключить тему")
        self.theme_btn.clicked.connect(self.toggle_theme)
        layout.addWidget(self.theme_btn, alignment=Qt.AlignRight)

        # Создаем вкладки
        tabs = QTabWidget()
        layout.addWidget(tabs)

        # Вкладка калькулятора
        calculator_tab = QWidget()
        tabs.addTab(calculator_tab, "Калькулятор")

        # Вкладка информации
        info_tab = QWidget()
        tabs.addTab(info_tab, "Информация")

        # Настройка вкладки калькулятора
        self.setup_calculator_tab(calculator_tab)
        self.setup_info_tab(info_tab)

    def setup_calculator_tab(self, tab):
        layout = QVBoxLayout()
        tab.setLayout(layout)

        # Группа цен
        prices_group = QGroupBox("Цены")
        prices_layout = QFormLayout()

        self.delivery_edit = QDoubleSpinBox()
        self.delivery_edit.setRange(0, 100000)
        self.delivery_edit.setDecimals(2)
        self.delivery_edit.setSuffix(" руб")

        self.spool_weight_edit = QDoubleSpinBox()
        self.spool_weight_edit.setRange(0, 100)
        self.spool_weight_edit.setDecimals(3)
        self.spool_weight_edit.setSuffix(" кг")

        self.spool_price_edit = QDoubleSpinBox()
        self.spool_price_edit.setRange(0, 100000)
        self.spool_price_edit.setDecimals(2)
        self.spool_price_edit.setSuffix(" руб")

        self.electricity_price_edit = QDoubleSpinBox()
        self.electricity_price_edit.setRange(0, 100)
        self.electricity_price_edit.setDecimals(2)
        self.electricity_price_edit.setSuffix(" руб/кВт")

        self.modeling_price_edit = QDoubleSpinBox()
        self.modeling_price_edit.setRange(0, 10000)
        self.modeling_price_edit.setDecimals(2)
        self.modeling_price_edit.setSuffix(" руб/ч")

        self.printing_price_edit = QDoubleSpinBox()
        self.printing_price_edit.setRange(0, 10000)
        self.printing_price_edit.setDecimals(2)
        self.printing_price_edit.setSuffix(" руб/ч")

        self.postprocessing_price_edit = QDoubleSpinBox()
        self.postprocessing_price_edit.setRange(0, 10000)
        self.postprocessing_price_edit.setDecimals(2)
        self.postprocessing_price_edit.setSuffix(" руб/ч")

        self.depreciation_price_edit = QDoubleSpinBox()
        self.depreciation_price_edit.setRange(0, 10000)
        self.depreciation_price_edit.setDecimals(2)
        self.depreciation_price_edit.setSuffix(" руб/ч")

        prices_layout.addRow("Доставка:", self.delivery_edit)
        prices_layout.addRow("Вес катушки:", self.spool_weight_edit)
        prices_layout.addRow("Цена катушки:", self.spool_price_edit)
        prices_layout.addRow("Цена 1 кВт:", self.electricity_price_edit)
        prices_layout.addRow("Моделирование:", self.modeling_price_edit)
        prices_layout.addRow("Печать:", self.printing_price_edit)
        prices_layout.addRow("Постобработка:", self.postprocessing_price_edit)
        prices_layout.addRow("Амортизация:", self.depreciation_price_edit)

        prices_group.setLayout(prices_layout)
        layout.addWidget(prices_group)

        # Группа затрат
        costs_group = QGroupBox("Затраты")
        costs_layout = QFormLayout()

        self.material_used_edit = QDoubleSpinBox()
        self.material_used_edit.setRange(0, 100000)
        self.material_used_edit.setDecimals(1)
        self.material_used_edit.setSuffix(" г")

        self.printer_power_edit = QDoubleSpinBox()
        self.printer_power_edit.setRange(0, 10)
        self.printer_power_edit.setDecimals(2)
        self.printer_power_edit.setSuffix(" кВт")

        self.modeling_hours = QSpinBox()
        self.modeling_hours.setRange(0, 1000)
        self.modeling_minutes = QSpinBox()
        self.modeling_minutes.setRange(0, 59)

        modeling_time_layout = QHBoxLayout()
        modeling_time_layout.addWidget(self.modeling_hours)
        modeling_time_layout.addWidget(QLabel("ч"))
        modeling_time_layout.addWidget(self.modeling_minutes)
        modeling_time_layout.addWidget(QLabel("мин"))

        self.printing_hours = QSpinBox()
        self.printing_hours.setRange(0, 1000)
        self.printing_minutes = QSpinBox()
        self.printing_minutes.setRange(0, 59)

        printing_time_layout = QHBoxLayout()
        printing_time_layout.addWidget(self.printing_hours)
        printing_time_layout.addWidget(QLabel("ч"))
        printing_time_layout.addWidget(self.printing_minutes)
        printing_time_layout.addWidget(QLabel("мин"))

        self.postprocessing_hours = QSpinBox()
        self.postprocessing_hours.setRange(0, 1000)
        self.postprocessing_minutes = QSpinBox()
        self.postprocessing_minutes.setRange(0, 59)

        postprocessing_time_layout = QHBoxLayout()
        postprocessing_time_layout.addWidget(self.postprocessing_hours)
        postprocessing_time_layout.addWidget(QLabel("ч"))
        postprocessing_time_layout.addWidget(self.postprocessing_minutes)
        postprocessing_time_layout.addWidget(QLabel("мин"))

        self.quantity_edit = QSpinBox()
        self.quantity_edit.setRange(1, 10000)

        costs_layout.addRow("Потрачено материала:", self.material_used_edit)
        costs_layout.addRow("Мощность принтера:", self.printer_power_edit)
        costs_layout.addRow("Моделирование:", modeling_time_layout)
        costs_layout.addRow("Печать:", printing_time_layout)
        costs_layout.addRow("Постобработка:", postprocessing_time_layout)
        costs_layout.addRow("Количество:", self.quantity_edit)

        costs_group.setLayout(costs_layout)
        layout.addWidget(costs_group)

        # Кнопка расчета
        self.calculate_btn = QPushButton("Рассчитать стоимость")
        self.calculate_btn.clicked.connect(self.calculate)
        layout.addWidget(self.calculate_btn)

        # Группа результатов
        results_group = QGroupBox("Результаты")
        results_layout = QFormLayout()

        self.material_cost_label = QLabel("0.00 руб")
        self.electricity_cost_label = QLabel("0.00 руб")
        self.modeling_cost_label = QLabel("0.00 руб")
        self.printing_cost_label = QLabel("0.00 руб")
        self.postprocessing_cost_label = QLabel("0.00 руб")
        self.depreciation_cost_label = QLabel("0.00 руб")
        self.first_item_cost_label = QLabel("0.00 руб")
        self.additional_items_cost_label = QLabel("0.00 руб")
        self.total_cost_label = QLabel("0.00 руб")  # Добавлено новое поле для итоговой стоимости

        results_layout.addRow("Материал:", self.material_cost_label)
        results_layout.addRow("Электроэнергия:", self.electricity_cost_label)
        results_layout.addRow("Моделирование:", self.modeling_cost_label)
        results_layout.addRow("Печать:", self.printing_cost_label)
        results_layout.addRow("Постобработка:", self.postprocessing_cost_label)
        results_layout.addRow("Амортизация:", self.depreciation_cost_label)
        results_layout.addRow("Цена первой детали:", self.first_item_cost_label)
        results_layout.addRow("Цена последующих:", self.additional_items_cost_label)
        results_layout.addRow("Итого за все детали:", self.total_cost_label)  # Добавлена строка с итоговой стоимостью

        results_group.setLayout(results_layout)
        layout.addWidget(results_group)

    def setup_info_tab(self, tab):
        layout = QVBoxLayout()
        tab.setLayout(layout)

        info_text = (
            "Calculator by isclean\n\n"
            "Ссылка на пожертвование:\n"
            "https://yoomoney.ru/to/4100119137217807\n\n"
            "Страница проекта:\n"
            "https://github.com/isclean12/3D-Printing-Calculator/"
        )
        info_label = QLabel(info_text)
        info_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        # Создаем QLabel с кликабельной ссылкой
        self.link_label = QLabel(
            '<a href="https://yoomoney.ru/to/4100119137217807">'
            'Ссылка на пожертвование'
            '</a><br>' 
            '</a><br>'
            '<a href="https://github.com/isclean12/3D-Printing-Calculator/">'
            'Страница проекта'
            '</a>'
        )
        self.link_label.setAlignment(Qt.AlignLeft)
        self.link_label.setOpenExternalLinks(True)  # Позволяет открывать ссылки во внешнем браузере
        self.link_label.setTextInteractionFlags(Qt.TextBrowserInteraction)  # Делает ссылку кликабельной
        self.link_label.linkActivated.connect(self.open_link)  # Обработчик клика по ссылке

        layout.addWidget(self.link_label)

    def open_link(self, url):
        # Открываем ссылку в браузере по умолчанию
        QDesktopServices.openUrl(QUrl(url))

    def set_default_values(self):
        # Установка значений по умолчанию
        self.delivery_edit.setValue(0.0)
        self.spool_weight_edit.setValue(1.0)
        self.spool_price_edit.setValue(1500.0)
        self.electricity_price_edit.setValue(1.5)
        self.modeling_price_edit.setValue(300.0)
        self.printing_price_edit.setValue(200.0)
        self.postprocessing_price_edit.setValue(300.0)
        self.depreciation_price_edit.setValue(50.0)

        self.material_used_edit.setValue(200.0)
        self.printer_power_edit.setValue(0.3)
        self.modeling_hours.setValue(3)
        self.modeling_minutes.setValue(30)
        self.printing_hours.setValue(2)
        self.printing_minutes.setValue(5)
        self.postprocessing_hours.setValue(1)
        self.postprocessing_minutes.setValue(5)
        self.quantity_edit.setValue(1)

    def calculate(self):
        try:
            # Получаем значения из полей ввода
            delivery = self.delivery_edit.value()
            spool_weight = self.spool_weight_edit.value()
            spool_price = self.spool_price_edit.value()
            electricity_price = self.electricity_price_edit.value()
            modeling_price = self.modeling_price_edit.value()
            printing_price = self.printing_price_edit.value()
            postprocessing_price = self.postprocessing_price_edit.value()
            depreciation_price = self.depreciation_price_edit.value()

            material_used = self.material_used_edit.value()
            printer_power = self.printer_power_edit.value()
            modeling_time = self.modeling_hours.value() + self.modeling_minutes.value() / 60
            printing_time = self.printing_hours.value() + self.printing_minutes.value() / 60
            postprocessing_time = self.postprocessing_hours.value() + self.postprocessing_minutes.value() / 60
            quantity = self.quantity_edit.value()

            # Расчет стоимости материалов
            material_cost = ((delivery + spool_price) / spool_weight) / 1000 * material_used

            # Расчет стоимости электроэнергии
            electricity_cost = printer_power * electricity_price * printing_time

            # Расчет стоимости моделирования
            modeling_cost = modeling_time * modeling_price

            # Расчет стоимости печати
            printing_cost = printing_time * printing_price

            # Расчет стоимости постобработки
            postprocessing_cost = postprocessing_time * postprocessing_price

            # Расчет стоимости амортизации
            depreciation_cost = printing_time * depreciation_price

            # Расчет общей стоимости для одной детали
            total_cost_per_item = material_cost + electricity_cost + modeling_cost + printing_cost + postprocessing_cost + depreciation_cost

            # Расчет цены первой и последующих деталей
            first_item_cost = total_cost_per_item
            additional_items_cost = total_cost_per_item - modeling_cost

            # Расчет итоговой стоимости для всех деталей
            if quantity == 1:
                total_cost = first_item_cost
            else:
                total_cost = first_item_cost + additional_items_cost * (quantity - 1)

            # Обновление меток с результатами
            self.material_cost_label.setText(f"{material_cost:.2f} руб")
            self.electricity_cost_label.setText(f"{electricity_cost:.2f} руб")
            self.modeling_cost_label.setText(f"{modeling_cost:.2f} руб")
            self.printing_cost_label.setText(f"{printing_cost:.2f} руб")
            self.postprocessing_cost_label.setText(f"{postprocessing_cost:.2f} руб")
            self.depreciation_cost_label.setText(f"{depreciation_cost:.2f} руб")
            self.first_item_cost_label.setText(f"{first_item_cost:.2f} руб")
            self.additional_items_cost_label.setText(f"{additional_items_cost:.2f} руб")
            self.total_cost_label.setText(f"{total_cost:.2f} руб")  # Обновляем итоговую стоимость

        except Exception as e:
            print(f"Ошибка при расчете: {e}")

    def set_dark_theme(self):
        # Устанавливаем темную палитру
        dark_palette = QPalette()

        # Базовые цвета
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.Disabled, QPalette.Text, QColor(150, 150, 150))
        dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(150, 150, 150))

        # Устанавливаем палитру
        QApplication.setPalette(dark_palette)

        # Дополнительные стили для лучшего отображения
        self.setStyleSheet("""
                    QGroupBox {
                        border: 1px solid gray;
                        border-radius: 3px;
                        margin-top: 0.5em;
                    }
                    QGroupBox::title {
                        subcontrol-origin: margin;
                        left: 10px;
                        padding: 0 3px;
                        color: white;
                    }
                    QTabWidget::pane {
                        border: 1px solid #444;
                    }
                    QTabBar::tab {
                        background: #444;
                        color: white;
                        padding: 5px;
                        border: 1px solid #666;
                    }
                    QTabBar::tab:selected {
                        background: #555;
                        border-bottom-color: #42a2da;
                    }
                    QPushButton {
                        background: #555;
                        color: white;
                        border: 1px solid #666;
                        padding: 5px;
                    }
                    QPushButton:hover {
                        background: #666;
                        border: 1px solid #777;
                    }
                    QPushButton:pressed {
                        background: #777;
                    }
                    QSpinBox, QDoubleSpinBox {
                        color: white;
                        background-color: #353535;
                        selection-background-color: #42a2da;
                        selection-color: white;
                    }
                    QSpinBox::up-button, QDoubleSpinBox::up-button {
                        subcontrol-origin: border;
                        subcontrol-position: top right;
                        width: 16px;
                        border-left: 1px solid #666;
                        border-bottom: 1px solid #666;
                        background: #555;
                    }
                    QSpinBox::down-button, QDoubleSpinBox::down-button {
                        subcontrol-origin: border;
                        subcontrol-position: bottom right;
                        width: 16px;
                        border-left: 1px solid #666;
                        background: #555;
                    }
                    QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {
                        image: url(:/icons/up_arrow_white.png);
                        width: 7px;
                        height: 7px;
                    }
                    QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {
                        image: url(:/icons/down_arrow_white.png);
                        width: 7px;
                        height: 7px;
                    }
                """)

        # Сохраняем состояние темы
        self.dark_theme = True

    def set_light_theme(self):
        # Возвращаем стандартную палитру
        QApplication.setPalette(QApplication.style().standardPalette())
        self.setStyleSheet("")  # Сбрасываем кастомные стили

        # Сохраняем состояние темы
        self.dark_theme = False

    def toggle_theme(self):
        if self.dark_theme:
            self.set_light_theme()
        else:
            self.set_dark_theme()

    def save_settings(self):
        """Сохраняет все настройки в файл"""
        settings = {
            "prices": {
                "delivery": self.delivery_edit.value(),
                "spool_weight": self.spool_weight_edit.value(),
                "spool_price": self.spool_price_edit.value(),
                "electricity_price": self.electricity_price_edit.value(),
                "modeling_price": self.modeling_price_edit.value(),
                "printing_price": self.printing_price_edit.value(),
                "postprocessing_price": self.postprocessing_price_edit.value(),
                "depreciation_price": self.depreciation_price_edit.value()
            },
            "costs": {
                "material_used": self.material_used_edit.value(),
                "printer_power": self.printer_power_edit.value(),
                "modeling_hours": self.modeling_hours.value(),
                "modeling_minutes": self.modeling_minutes.value(),
                "printing_hours": self.printing_hours.value(),
                "printing_minutes": self.printing_minutes.value(),
                "postprocessing_hours": self.postprocessing_hours.value(),
                "postprocessing_minutes": self.postprocessing_minutes.value(),
                "quantity": self.quantity_edit.value()
            },
            "theme": "dark" if self.dark_theme else "light"
        }

        try:
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=4)
        except Exception as e:
            print(f"Ошибка при сохранении настроек: {e}")

    def load_settings(self):
        """Загружает настройки из файла, если он существует"""
        if not os.path.exists(self.settings_file):
            self.set_default_values()
            return

        try:
            with open(self.settings_file, 'r') as f:
                settings = json.load(f)

                # Загружаем цены
                prices = settings.get("prices", {})
                self.delivery_edit.setValue(prices.get("delivery", 0.0))
                self.spool_weight_edit.setValue(prices.get("spool_weight", 1.0))
                self.spool_price_edit.setValue(prices.get("spool_price", 1500.0))
                self.electricity_price_edit.setValue(prices.get("electricity_price", 1.5))
                self.modeling_price_edit.setValue(prices.get("modeling_price", 300.0))
                self.printing_price_edit.setValue(prices.get("printing_price", 200.0))
                self.postprocessing_price_edit.setValue(prices.get("postprocessing_price", 300.0))
                self.depreciation_price_edit.setValue(prices.get("depreciation_price", 50.0))

                # Загружаем затраты
                costs = settings.get("costs", {})
                self.material_used_edit.setValue(costs.get("material_used", 200.0))
                self.printer_power_edit.setValue(costs.get("printer_power", 0.3))
                self.modeling_hours.setValue(costs.get("modeling_hours", 3))
                self.modeling_minutes.setValue(costs.get("modeling_minutes", 30))
                self.printing_hours.setValue(costs.get("printing_hours", 2))
                self.printing_minutes.setValue(costs.get("printing_minutes", 5))
                self.postprocessing_hours.setValue(costs.get("postprocessing_hours", 1))
                self.postprocessing_minutes.setValue(costs.get("postprocessing_minutes", 5))
                self.quantity_edit.setValue(costs.get("quantity", 1))

                # Загружаем тему
                if settings.get("theme", "dark") == "light":
                    self.set_light_theme()
                else:
                    self.set_dark_theme()

        except Exception as e:
            print(f"Ошибка при загрузке настроек: {e}")
            self.set_default_values()

    def closeEvent(self, event):
        """Сохраняет настройки при закрытии окна"""
        self.save_settings()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = CostCalculator()
    calculator.show()
    sys.exit(app.exec_())