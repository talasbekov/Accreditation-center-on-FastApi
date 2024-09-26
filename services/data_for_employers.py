import random
import requests

# Управления и количество мест в каждом управлении
departments = [
    {"name": "2-управление", "count_state": 16, "id": 2, "employers": []},
    {"name": "1-управление", "count_state": 34, "id": 1, "employers": []},
    {"name": "3-управление", "count_state": 24, "id": 3, "employers": []},
    {"name": "4-управление", "count_state": 20, "id": 4, "employers": []},
    {"name": "5-управление", "count_state": 15, "id": 5, "employers": []},
    {"name": "6-управление", "count_state": 17, "id": 6, "employers": []},
]

# Фиктивные данные для создания сотрудников
surnames = ["Құралбеков", "Алдыназаров", "Жумабаев", "Кокузов", "Данабеков"]
firstnames = ["Абылай", "Диас", "Алмас", "Данияр", "Ерлан"]
patronymics = ["Абайұлы", "Дәуренұлы", "Максатұлы", "Сәрсенбекұлы", "Дәулетұлы"]

# Статусы сотрудников
# statuses = ["IN_SERVICE", "ON_LEAVE", "ON_SICK_LEAVE", "BUSINESS_TRIP", "SECONDED_IN", "SECONDED_OUT", "ON_DUTY", "AFTER_ON_DUTY", "AT_THE_COMPETITION"]
statuses = [
    "в строю",
    "в отпуске",
    "на больничном",
    "в командировке",
    "прикомандирован",
    "откомандирован",
    "на дежурстве",
    "после дежурства",
    "на соревновании",
]

# URL для API запроса
api_url = "https://accr.new.sgork.kz:64778/api/v2/employers"  # Ваш реальный URL
# api_url = "http://127.0.0.1:8000/api/v2/employers"


# Функция для создания работника
def create_employee(surname, firstname, patronymic, status, record_id):
    return {
        "surname": surname,
        "firstname": firstname,
        "patronymic": patronymic,
        "start_date": "2024-09-26",
        "end_date": "2024-09-27",
        "status": status,
        "record_id": record_id,
    }


# Функция для выбора статуса, 70% IN_SERVICE
def choose_status():
    if random.random() < 0.7:
        return "в строю"  # 70% случаев будет "IN_SERVICE"
    else:
        return random.choice(
            statuses[1:]
        )  # Остальные 30% случайно среди других статусов


# Переменная для подсчета общего количества созданных сотрудников
total_employees = 0

# Итерация по департаментам и добавление сотрудников
for department in departments:
    for _ in range(department["count_state"]):
        if total_employees >= 129:
            break  # Если достигли 129 сотрудников, прекращаем добавление

        # Создаем данные для сотрудника
        surname = random.choice(surnames)
        firstname = random.choice(firstnames)
        patronymic = random.choice(patronymics)
        status = choose_status()  # Используем функцию для выбора статуса
        record_id = str(department["id"])

        employee_data = create_employee(
            surname, firstname, patronymic, status, record_id
        )

        # Выполняем запрос к API для создания сотрудника
        headers = {"accept": "application/json", "Content-Type": "application/json"}

        response = requests.post(
            api_url, headers=headers, json=employee_data, verify=False
        )

        if response.status_code == 201:  # Проверяем, успешно ли создан сотрудник
            print(
                f"Сотрудник {surname} {firstname} {patronymic} добавлен в {department['name']} со статусом {status}"
            )
        else:
            print(
                f"Ошибка при добавлении сотрудника: {response.status_code}, {response.text}"
            )

        total_employees += 1

print(f"Всего создано сотрудников: {total_employees}")
