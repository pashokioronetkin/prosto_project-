import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QTextEdit, QListWidget, QMessageBox, QComboBox,
    QTabWidget, QGroupBox, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt
from datetime import datetime


# Класс для представления топлива
class Fuel:
    def __init__(self, name, price_per_liter):
        self.name = name
        self.price_per_liter = price_per_liter

    def __str__(self):
        return f"{self.name} ({self.price_per_liter} руб./литр)"


# Класс для представления клиента
class Client:
    def __init__(self, name, car_number):
        self.name = name
        self.car_number = car_number

    def __str__(self):
        return f"{self.name}, {self.car_number}"


# Класс для представления заказа
class Order:
    def __init__(self, client, fuel, liters):
        self.client = client
        self.fuel = fuel
        self.liters = liters
        self.date = datetime.now()
        self.status = "Активен"  # Добавляем статус заказа

    def calculate_total(self):
        return self.fuel.price_per_liter * self.liters

    def __str__(self):
        return f"[{self.date.strftime('%d.%m.%Y %H:%M')}] {self.status} | Клиент: {self.client}, Топливо: {self.fuel}, Литров: {self.liters}, Итого: {self.calculate_total():.2f} руб."


# Класс для управления заправочной станцией
class GasStation:
    def __init__(self):
        self.fuels = []  # Список доступных топлив
        self.clients = []  # Список клиентов
        self.orders = []  # Список заказов
        self.total_sales = 0  # Общие продажи
        self.loyal_customers = set()  # Постоянные клиенты

    def add_fuel(self, fuel):
        self.fuels.append(fuel)

    def add_client(self, client):
        self.clients.append(client)

    def add_order(self, order):
        self.orders.append(order)

    def get_fuels(self):
        return "\n".join([str(fuel) for fuel in self.fuels])

    def get_clients(self):
        return "\n".join([str(client) for client in self.clients])

    def get_orders(self):
        return "\n".join([str(order) for order in self.orders])

    def get_total_revenue(self):
        return sum(order.calculate_total() for order in self.orders)
    
    def get_fuel_statistics(self):
        stats = {}
        for order in self.orders:
            if order.fuel.name not in stats:
                stats[order.fuel.name] = 0
            stats[order.fuel.name] += order.liters
        return stats

    def get_client_statistics(self):
        stats = {}
        for order in self.orders:
            if order.client.name not in stats:
                stats[order.client.name] = 0
            stats[order.client.name] += order.calculate_total()
        return stats

    def get_loyal_customers(self):
        # Клиенты с более чем 3 заказами считаются постоянными
        customer_orders = {}
        for order in self.orders:
            customer_orders[order.client.name] = customer_orders.get(order.client.name, 0) + 1
        return {name for name, count in customer_orders.items() if count >= 3}


# Основное приложение на PyQt5
class GasStationApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.gas_station = GasStation()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Система управления АЗС")
        self.setGeometry(100, 100, 1000, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QGroupBox {
                background-color: white;
                border-radius: 5px;
                margin-top: 10px;
                padding: 10px;
                border: 1px solid #ddd;
            }
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton#danger {
                background-color: #f44336;
            }
            QPushButton#danger:hover {
                background-color: #d32f2f;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: #ffffff;
            }
            QTextEdit, QTableWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: #ffffff;
            }
            QLabel {
                color: #333333;
                font-weight: bold;
            }
            QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: #ffffff;
            }
            QTableWidget {
                gridline-color: #ddd;
            }
            QHeaderView::section {
                background-color: #2196F3;
                color: white;
                padding: 8px;
                border: none;
            }
        """)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # Создаем вкладки
        tabs = QTabWidget()
        main_layout.addWidget(tabs)

        # Вкладка операций
        operations_tab = QWidget()
        operations_layout = QVBoxLayout()
        operations_tab.setLayout(operations_layout)

        # Группа для топлива
        fuel_group = QGroupBox("Добавление топлива")
        fuel_layout = QHBoxLayout()
        fuel_group.setLayout(fuel_layout)

        fuel_layout.addWidget(QLabel("Название:"))
        self.fuel_name_input = QLineEdit()
        fuel_layout.addWidget(self.fuel_name_input)

        fuel_layout.addWidget(QLabel("Цена за литр:"))
        self.fuel_price_input = QLineEdit()
        fuel_layout.addWidget(self.fuel_price_input)

        add_fuel_button = QPushButton("Добавить топливо")
        add_fuel_button.clicked.connect(self.add_fuel)
        fuel_layout.addWidget(add_fuel_button)

        operations_layout.addWidget(fuel_group)

        # Группа для клиентов
        client_group = QGroupBox("Добавление клиента")
        client_layout = QHBoxLayout()
        client_group.setLayout(client_layout)

        client_layout.addWidget(QLabel("Имя:"))
        self.client_name_input = QLineEdit()
        client_layout.addWidget(self.client_name_input)

        client_layout.addWidget(QLabel("Номер машины:"))
        self.car_number_input = QLineEdit()
        client_layout.addWidget(self.car_number_input)

        add_client_button = QPushButton("Добавить клиента")
        add_client_button.clicked.connect(self.add_client)
        client_layout.addWidget(add_client_button)

        operations_layout.addWidget(client_group)

        # Группа для заказов
        order_group = QGroupBox("Новый заказ")
        order_layout = QHBoxLayout()
        order_group.setLayout(order_layout)

        order_layout.addWidget(QLabel("Клиент:"))
        self.client_choice_input = QComboBox()
        order_layout.addWidget(self.client_choice_input)

        order_layout.addWidget(QLabel("Топливо:"))
        self.fuel_choice_input = QComboBox()
        order_layout.addWidget(self.fuel_choice_input)

        order_layout.addWidget(QLabel("Литров:"))
        self.liters_input = QLineEdit()
        order_layout.addWidget(self.liters_input)

        add_order_button = QPushButton("Оформить заказ")
        add_order_button.clicked.connect(self.add_order)
        order_layout.addWidget(add_order_button)

        operations_layout.addWidget(order_group)

        # Информационное поле
        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        operations_layout.addWidget(self.info_text)

        # Вкладка статистики
        stats_tab = QWidget()
        stats_layout = QVBoxLayout()
        stats_tab.setLayout(stats_layout)

        # Таблица заказов
        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(6)
        self.orders_table.setHorizontalHeaderLabels(["Дата", "Клиент", "Топливо", "Литров", "Сумма", "Статус"])
        self.orders_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        stats_layout.addWidget(self.orders_table)

        # Кнопки управления заказами
        orders_buttons_layout = QHBoxLayout()
        complete_order_button = QPushButton("Завершить заказ")
        complete_order_button.clicked.connect(self.complete_order)
        cancel_order_button = QPushButton("Отменить заказ")
        cancel_order_button.setObjectName("danger")
        cancel_order_button.clicked.connect(self.cancel_order)
        
        orders_buttons_layout.addWidget(complete_order_button)
        orders_buttons_layout.addWidget(cancel_order_button)
        stats_layout.addLayout(orders_buttons_layout)

        # Статистика
        stats_group = QGroupBox("Общая статистика")
        stats_info_layout = QVBoxLayout()
        self.stats_text = QTextEdit()
        self.stats_text.setReadOnly(True)
        stats_info_layout.addWidget(self.stats_text)
        stats_group.setLayout(stats_info_layout)
        stats_layout.addWidget(stats_group)

        # Добавляем вкладки
        tabs.addTab(operations_tab, "Операции")
        tabs.addTab(stats_tab, "Статистика")

    def add_fuel(self):
        name = self.fuel_name_input.text()
        price = self.fuel_price_input.text()

        if name and price:
            try:
                price = float(price)
                fuel = Fuel(name, price)
                self.gas_station.add_fuel(fuel)
                self.update_info()
                self.update_comboboxes()
                self.fuel_name_input.clear()
                self.fuel_price_input.clear()
            except ValueError:
                QMessageBox.warning(self, "Ошибка", "Цена должна быть числом!")
        else:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")

    def add_client(self):
        name = self.client_name_input.text()
        car_number = self.car_number_input.text()

        if name and car_number:
            client = Client(name, car_number)
            self.gas_station.add_client(client)
            self.update_info()
            self.update_comboboxes()
            self.client_name_input.clear()
            self.car_number_input.clear()
        else:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")

    def update_comboboxes(self):
        # Обновляем список клиентов
        self.client_choice_input.clear()
        for client in self.gas_station.clients:
            self.client_choice_input.addItem(client.name)

        # Обновляем список топлива
        self.fuel_choice_input.clear()
        for fuel in self.gas_station.fuels:
            self.fuel_choice_input.addItem(fuel.name)

    def add_order(self):
        client_name = self.client_choice_input.currentText()
        fuel_name = self.fuel_choice_input.currentText()
        liters = self.liters_input.text()

        if client_name and fuel_name and liters:
            try:
                liters = float(liters)
                client = next((c for c in self.gas_station.clients if c.name == client_name), None)
                fuel = next((f for f in self.gas_station.fuels if f.name == fuel_name), None)

                if client and fuel:
                    order = Order(client, fuel, liters)
                    self.gas_station.add_order(order)
                    self.update_info()
                    self.liters_input.clear()
                else:
                    QMessageBox.warning(self, "Ошибка", "Клиент или топливо не найдены!")
            except ValueError:
                QMessageBox.warning(self, "Ошибка", "Количество литров должно быть числом!")
        else:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")

    def complete_order(self):
        current_row = self.orders_table.currentRow()
        if current_row >= 0:
            order = self.gas_station.orders[current_row]
            order.status = "Завершен"
            self.update_statistics()

    def cancel_order(self):
        current_row = self.orders_table.currentRow()
        if current_row >= 0:
            order = self.gas_station.orders[current_row]
            order.status = "Отменен"
            self.update_statistics()

    def update_statistics(self):
        self.stats_text.clear()
        self.orders_table.setRowCount(0)
        
        # Обновляем таблицу заказов
        for i, order in enumerate(self.gas_station.orders):
            self.orders_table.insertRow(i)
            self.orders_table.setItem(i, 0, QTableWidgetItem(order.date.strftime('%d.%m.%Y %H:%M')))
            self.orders_table.setItem(i, 1, QTableWidgetItem(order.client.name))
            self.orders_table.setItem(i, 2, QTableWidgetItem(order.fuel.name))
            self.orders_table.setItem(i, 3, QTableWidgetItem(f"{order.liters:.1f}"))
            self.orders_table.setItem(i, 4, QTableWidgetItem(f"{order.calculate_total():.2f}"))
            self.orders_table.setItem(i, 5, QTableWidgetItem(order.status))

        # Обновляем статистику
        total_revenue = self.gas_station.get_total_revenue()
        active_orders = sum(1 for order in self.gas_station.orders if order.status == "Активен")
        completed_orders = sum(1 for order in self.gas_station.orders if order.status == "Завершен")
        loyal_customers = self.gas_station.get_loyal_customers()

        self.stats_text.append(f"💰 Общая выручка: {total_revenue:.2f} руб.")
        self.stats_text.append(f"📊 Активных заказов: {active_orders}")
        self.stats_text.append(f"✅ Завершенных заказов: {completed_orders}\n")

        self.stats_text.append("🔥 Статистика по топливу:")
        for fuel, liters in self.gas_station.get_fuel_statistics().items():
            self.stats_text.append(f"   • {fuel}: {liters:.1f} литров")
        
        self.stats_text.append("\n👥 Постоянные клиенты:")
        for client in loyal_customers:
            self.stats_text.append(f"   • {client}")

        self.stats_text.append("\n💳 Статистика по клиентам:")
        for client, spent in self.gas_station.get_client_statistics().items():
            self.stats_text.append(f"   • {client}: {spent:.2f} руб.")

    def update_info(self):
        self.info_text.clear()
        self.info_text.append("Доступные топлива:")
        self.info_text.append(self.gas_station.get_fuels())
        self.info_text.append("\nКлиенты:")
        self.info_text.append(self.gas_station.get_clients())
        self.info_text.append("\nЗаказы:")
        self.info_text.append(self.gas_station.get_orders())
        self.update_statistics()  # Обновляем статистику


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GasStationApp()
    window.show()
    sys.exit(app.exec_())


