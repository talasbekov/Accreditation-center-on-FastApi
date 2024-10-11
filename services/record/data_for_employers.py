from collections import defaultdict
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from models import Department, Management, Division, Position, Rank, Status, Employer, State
from schemas import DepartmentCreate, ManagementCreate, DivisionCreate, PositionCreate, RankCreate, StatusCreate, \
    EmployerRandomCreate, StateRandomCreate
from faker import Faker
import random


fake = Faker()


class DataForService:

    def create_department(self, db: Session, department_data: DepartmentCreate):
        # Попытка найти департамент с таким именем
        department = db.query(Department).filter_by(name=department_data.name).first()

        if department:
            print(f"Департамент '{department_data.name}' уже существует. Используется существующий.")
            return department

        # Если департамент не найден, создаем новый
        department = Department(name=department_data.name)
        db.add(department)
        db.commit()
        db.refresh(department)
        print(f"Департамент '{department_data.name}' успешно создан.")
        return department

    def create_management(self, db: Session, management_data: ManagementCreate):
        try:
            # Проверка на существование управления с указанным именем и департаментом
            management = db.query(Management).filter_by(
                name=management_data.name,
                department_id=management_data.department_id
            ).first()

            if management:
                print(
                    f"Управление '{management_data.name}' уже существует в департаменте с ID {management_data.department_id}. Используется существующее управление.")
                return management

            # Создание нового управления, если оно не найдено
            management = Management(
                name=management_data.name,
                department_id=management_data.department_id
            )
            db.add(management)
            db.commit()
            db.refresh(management)
            print(
                f"Управление '{management_data.name}' успешно создано в департаменте с ID {management_data.department_id}.")
            return management
        except Exception as e:
            db.rollback()
            print(f"Ошибка при создании управления: {e}")
            return None

    def create_division(self, db: Session, division_data: DivisionCreate):
        try:
            # Проверка на существование отдела с указанным именем и управлением
            division = db.query(Division).filter_by(
                name=division_data.name,
                management_id=division_data.management_id
            ).first()

            if division:
                print(
                    f"Отдел '{division_data.name}' уже существует в управлении с ID {division_data.management_id}. Используется существующий отдел.")
                return division

            # Создание нового отдела, если он не найден
            division = Division(
                name=division_data.name,
                management_id=division_data.management_id
            )
            db.add(division)
            db.commit()
            db.refresh(division)
            print(f"Отдел '{division_data.name}' успешно создан в управлении с ID {division_data.management_id}.")
            return division
        except Exception as e:
            db.rollback()
            print(f"Ошибка при создании отдела: {e}")
            return None

    def create_position(self, db: Session, position_data: PositionCreate):
        try:
            # Проверка на существование позиции с таким же именем
            position = db.query(Position).filter_by(name=position_data.name).first()

            if position:
                print(f"Позиция '{position_data.name}' уже существует. Используется существующая позиция.")
                return position

            # Создание новой позиции, если не найдена
            position = Position(name=position_data.name)
            db.add(position)
            db.commit()
            db.refresh(position)
            print(f"Позиция '{position_data.name}' успешно создана.")
            return position
        except Exception as e:
            db.rollback()
            print(f"Ошибка при создании позиции: {e}")
            return None

    def create_rank(self, db: Session, rank_data: RankCreate):
        try:
            # Проверка на существование звания с таким же именем
            rank = db.query(Rank).filter_by(name=rank_data.name).first()

            if rank:
                print(f"Звание '{rank_data.name}' уже существует. Используется существующее звание.")
                return rank

            # Создание нового звания, если не найдено
            rank = Rank(name=rank_data.name)
            db.add(rank)
            db.commit()
            db.refresh(rank)
            print(f"Звание '{rank_data.name}' успешно создано.")
            return rank
        except Exception as e:
            db.rollback()
            print(f"Ошибка при создании звания: {e}")
            return None

    def create_status(self, db: Session, status_data: StatusCreate):
        try:
            # Проверка на существование статуса с такими же параметрами
            status = db.query(Status).filter_by(
                name=status_data.name,
                start_date=status_data.start_date,
                end_date=status_data.end_date
            ).first()

            if status:
                print(
                    f"Статус '{status_data.name}' уже существует с указанными датами. Используется существующий статус.")
                return status

            # Создание нового статуса, если не найден
            status = Status(
                name=status_data.name,
                start_date=status_data.start_date,
                end_date=status_data.end_date
            )
            db.add(status)
            db.commit()
            db.refresh(status)
            print(f"Статус '{status_data.name}' успешно создан.")
            return status
        except Exception as e:
            db.rollback()
            print(f"Ошибка при создании статуса: {e}")
            return None

    def create_employer(self, db: Session, employer_data: EmployerRandomCreate):
        try:
            # Проверка на существование сотрудника с такими же данными
            employer = db.query(Employer).filter_by(
                surname=employer_data.surname,
                firstname=employer_data.firstname,
                patronymic=employer_data.patronymic,
                sort=employer_data.sort,
                rank_id=employer_data.rank_id,
                division_id=employer_data.division_id,
                status_id=employer_data.status_id
            ).first()

            if employer:
                print(
                    f"Сотрудник '{employer_data.firstname} {employer_data.surname}' уже существует. Используется существующий сотрудник.")
                return employer

            # Создание нового сотрудника, если не найден
            employer = Employer(
                surname=employer_data.surname,
                firstname=employer_data.firstname,
                patronymic=employer_data.patronymic,
                sort=employer_data.sort,
                rank_id=employer_data.rank_id,
                division_id=employer_data.division_id,
                status_id=employer_data.status_id
            )
            db.add(employer)
            db.commit()
            db.refresh(employer)
            print(f"Сотрудник '{employer_data.firstname} {employer_data.surname}' успешно создан.")
            return employer
        except Exception as e:
            db.rollback()
            print(f"Ошибка при создании сотрудника: {e}")
            return None

    def create_state(self, db: Session, state_data: StateRandomCreate):
        try:
            # Проверка на существование состояния с указанными параметрами
            state = db.query(State).filter_by(
                department_id=state_data.department_id,
                management_id=state_data.management_id,
                division_id=state_data.division_id,
                position_id=state_data.position_id,
                employer_id=state_data.employer_id
            ).first()

            if state:
                print(
                    f"Состояние для сотрудника с ID {state_data.employer_id} уже существует. Поиск другого employer_id.")

                # Найти другого сотрудника, который еще не связан с данным состоянием
                new_employer = db.query(Employer).filter(
                    Employer.id != state_data.employer_id
                ).first()

                if new_employer:
                    print(f"Используется новый сотрудник с ID {new_employer.id} вместо {state_data.employer_id}.")
                    state_data.employer_id = new_employer.id
                else:
                    print("Другой сотрудник не найден, используется исходный сотрудник.")
                    return state  # Возвращаем найденное состояние, если нет других сотрудников

            # Создание нового состояния, если не найдено
            state = State(
                department_id=state_data.department_id,
                management_id=state_data.management_id,
                division_id=state_data.division_id,
                position_id=state_data.position_id,
                employer_id=state_data.employer_id
            )
            db.add(state)
            db.commit()
            db.refresh(state)
            print(f"Состояние для сотрудника с ID {state_data.employer_id} успешно создано.")
            return state
        except Exception as e:
            db.rollback()
            print(f"Ошибка при создании состояния: {e}")
            return None

    def populate_all_tables(self, db: Session):
        # Создание департамента
        department_data = DepartmentCreate(name="Седьмой департамент")
        department = self.create_department(db, department_data)

        # Создание всех управлений и отделов
        management_names = ["1-управление", "2-управление", "3-управление", "4-управление", "5-управление",
                            "6-управление"]
        division_names = ["1-отдел", "2-отдел"]

        # Цикл для создания управлений
        for management_name in management_names:
            management_data = ManagementCreate(
                name=management_name,
                department_id=department.id
            )
            management = self.create_management(db, management_data)
            if not management:
                continue

            # Цикл для создания отделов внутри каждого управления
            for division_name in division_names:
                division_data = DivisionCreate(
                    name=division_name,
                    management_id=management.id
                )
                division = self.create_division(db, division_data)
                if not division:
                    continue

        for _ in range(15):
            # Создание должности
            position_data = PositionCreate(name=random.choice(["офицер охраны", "старший офицер охраны", "старший офицер", "инспектор", "старший инспектор", "начальник отдела"]))
            position = self.create_position(db, position_data)
            if not position:
                continue

        for _ in range(10):
            # Создание звания
            rank_data = RankCreate(name=random.choice(["лейтенант", "старший лейтенант", "капитан", "майор", "подполковник", "полковник"]))
            rank = self.create_rank(db, rank_data)
            if not rank:
                continue

        for _ in range(10):
            # Создание статуса с произвольной датой окончания
            start_date = fake.date_this_year()

            # Всегда генерируем end_date как случайную дату в следующем месяце
            today = datetime.today()
            next_month = today.replace(day=1) + timedelta(days=31)
            next_month_start = next_month.replace(day=1)
            next_month_end = (next_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)

            # Выбираем случайную дату в диапазоне следующего месяца
            end_date = fake.date_between_dates(date_start=next_month_start, date_end=next_month_end)

            status_data = StatusCreate(
                name=random.choice(["в строю", "болен", "отпуск"]),
                start_date=start_date,
                end_date=end_date
            )
            status = self.create_status(db, status_data)
            if not status:
                continue


    def create_employers_for_state(self, db: Session):
        last_names = [
            "Жуманов", "Нурланов", "Ахметов", "Султанов", "Оспанов", "Есенгельдинов",
            "Ибраев", "Касымов", "Байжанов", "Тлеубаев", "Ержанов", "Арыстанов",
            "Сеитов", "Мамыров", "Асанов", "Карабаев", "Саурбеков", "Калмырзаев",
            "Токешов", "Кенесов", "Даулетов", "Темирбаев", "Кенжебеков", "Жарылкасынов",
            "Назарбаев", "Омаров", "Сариев", "Айдаров", "Бекжанов", "Куанышев",
            "Абдикаримов", "Серикбаев", "Кабдешов", "Касенов", "Шаймерденов", "Турсынов",
            "Алиев", "Ергалиев", "Алдабергенов", "Рамазанов", "Мусин", "Абилов",
            "Бектуров", "Кусайнов", "Сапаров", "Курбанов", "Турсунбаев", "Шардарбеков",
            "Сулейменов", "Болат", "Кулмурзаев", "Мусабаев", "Кабиев", "Мынбаев",
            "Дюсекеев", "Кенес", "Нургалиев", "Еркенов", "Айымбетов", "Кудайбергенов",
            "Кусаинов", "Муталиев", "Жаксылыков", "Амиров", "Орынбасаров", "Туймебаев",
            "Абдилдаев", "Туленов", "Байбосынов", "Махамбетов", "Асанбаев", "Бегалиев",
            "Маматов", "Кожахметов", "Абдигалимов", "Муканов", "Томпиев", "Ахметжанов",
            "Жунусов", "Турмагамбетов", "Тулегенов", "Тажибаев", "Ескендиров", "Майлыбаев",
            "Асаинов", "Сарсенбаев", "Канатбаев", "Ержан", "Мамедов", "Абдрахманов",
            "Шынтасов", "Маратов", "Шарипов", "Мусатаев", "Темирбаев", "Токтаров",
            "Рахметов", "Дуйсенов", "Омарбаев", "Елемесов", "Кожабеков", "Темирбаев",
            "Садуов", "Оразов", "Асан", "Уразбаев", "Еркибаев", "Омирбеков",
            "Турапов", "Набиев", "Сакенов", "Бекенов", "Оралбаев", "Темирбаев",
            "Елеусизов", "Байбеков", "Куанышбаев", "Байсалов", "Жанузаков", "Токтарбаев",
            "Танатаров", "Онгарбаев", "Шагиров", "Бекен", "Бектемир", "Кульбаев",
            "Умбетбаев", "Сулейменов", "Маратбеков", "Абдикалиев", "Баймагамбетов",
            "Шарипов", "Турганбаев", "Калабаев", "Досмаилов", "Турлыбеков", "Сулейменов",
            "Бекенов", "Елдосов", "Таженов", "Еркебуланов", "Тургумбаев", "Турсункулов",
            "Ергалиев", "Оразов", "Жунусов", "Айтмухамбетов", "Жакупов", "Туякбаев"
        ]

        first_names = [
            "Кайрат", "Нуржан", "Асхат", "Бекжан", "Санжар", "Али",
            "Жасулан", "Ерлан", "Нурбол", "Бекзат", "Тимур", "Ерболат",
            "Ербол", "Абылай", "Серик", "Асылхан", "Арыстан", "Ернар",
            "Куаныш", "Батыр", "Азамат", "Даулет", "Мадияр", "Жанат",
            "Ербол", "Арман", "Талгат", "Еркебулан", "Асан", "Мурат",
            "Ермек", "Айдос", "Айдар", "Ораз", "Куат", "Сырым",
            "Сейтжан", "Мейрхан", "Жомарт", "Куанышбек", "Жанибек", "Нурлан",
            "Арман", "Абзал", "Берик", "Мурат", "Ербол", "Алмас",
            "Марат", "Олжас", "Нуржан", "Бекжан", "Аман", "Есен",
            "Асыл", "Мади", "Елдос", "Нурбол", "Тулеген", "Арыстан",
            "Берикбол", "Жанибек", "Мадияр", "Кайрат", "Азамат", "Алдияр",
            "Кайсар", "Жаксылык", "Серикжан", "Жанболат", "Еркебулан", "Алихан",
            "Амангельды", "Ержан", "Мурат", "Тимур", "Берик", "Нурмухаммед",
            "Ардак", "Еркебулан", "Даулет", "Азамат", "Ермек", "Аман",
            "Жанат", "Аблай", "Асан", "Берик", "Елдос", "Арман",
            "Санжар", "Ернар", "Тимур", "Алихан", "Жандос", "Даулет",
            "Елдос", "Санжар", "Жанибек", "Абылай", "Жанат", "Айдар",
            "Арман", "Ербол", "Даулет", "Тулеген", "Абзал", "Жанибек",
            "Серикжан", "Берик", "Нуржан", "Алмас", "Аман", "Жандос",
            "Нурбол", "Санжар", "Ербол", "Алихан", "Ерлан", "Елдос",
            "Ардак", "Аман", "Азамат", "Жомарт", "Нурбол", "Ермек",
            "Али", "Жанибек", "Даулет", "Асыл", "Аблай", "Берик",
            "Нурлан", "Арман", "Ерлан", "Алихан", "Асыл", "Тимур",
            "Асылбек", "Нуржан", "Кайрат", "Жаксылык", "Ернар", "Мади"
        ]

        middle_names = [
            "Кайратулы", "Нурланулы", "Асхатович", "Бекжанович", "Санжарович", "Алиевич",
            "Жасуланович", "Ерланулы", "Нурболович", "Бекзатович", "Тимурович", "Ерболатович",
            "Ерболович", "Абылаевич", "Серикович", "Асылханович", "Арыстанович", "Ернарович",
            "Куанышулы", "Батырович", "Азаматович", "Даулетович", "Мадиярович", "Жанатович",
            "Ерболович", "Арманулы", "Талгатович", "Еркебуланович", "Асанович", "Муратович",
            "Ермекович", "Айдосович", "Айдарович", "Оразович", "Куатович", "Сырымович",
            "Сейтжанович", "Мейрханович", "Жомартович", "Куанышбекович", "Жанибекович", "Нурланович",
            "Арманович", "Абзалович", "Берикович", "Муратович", "Ерболович", "Алмасович",
            "Маратович", "Олжасович", "Нуржанович", "Бекжанович", "Аманович", "Есенович",
            "Асылович", "Мадиович", "Елдосович", "Нурболович", "Тулегенович", "Арыстанович",
            "Берикболович", "Жанибекович", "Мадиярович", "Кайратович", "Азаматович", "Алдиярович",
            "Кайсарович", "Жаксылыкович", "Серикжанович", "Жанболатович", "Еркебуланович", "Алиханович",
            "Амангельдыевич", "Ержанович", "Муратович", "Тимурович", "Берикович", "Нурмухаммедович",
            "Ардакович", "Еркебуланович", "Даулетович", "Азаматович", "Ермекович", "Аманович",
            "Жанатович", "Аблаевич", "Асанович", "Берикович", "Елдосович", "Арманович",
            "Санжарович", "Ернарович", "Тимурович", "Алиханович", "Жандосович", "Даулетович",
            "Елдосович", "Санжарович", "Жанибекович", "Абылаевич", "Жанатович", "Айдарович",
            "Арманович", "Ерболович", "Даулетович", "Тулегенович", "Абзалович", "Жанибекович",
            "Серикжанович", "Берикович", "Нуржанович", "Алмасович", "Аманович", "Жандосович",
            "Нурболович", "Санжарович", "Ерболович", "Алиханович", "Ерланович", "Елдосович",
            "Ардакович", "Аманович", "Азаматович", "Жомартович", "Нурболович", "Ермекович",
            "Алиевич", "Жанибекович", "Даулетович", "Асылович", "Аблаевич", "Берикович",
            "Нурланович", "Арманович", "Ерланович", "Алиханович", "Асылович", "Тимурович",
            "Асылбекович", "Нуржанович", "Кайратович", "Жаксылыкович", "Ернарович", "Мадиович"
        ]
        self.populate_all_tables(db)

        # Получаем существующие идентификаторы
        rank_ids = [rank.id for rank in db.query(Rank.id).all()]
        division_ids = [division.id for division in db.query(Division.id).all()]
        status_ids = [status.id for status in db.query(Status.id).all()]
        # Убедимся, что получаем позиции отдельно, без привязки к state
        position_ids = [position.id for position in db.query(Position.id).all()]

        # Проверяем данные в таблицах Rank, Division и Status
        if not (rank_ids and division_ids and status_ids):
            raise ValueError("Необходимо, чтобы таблицы Rank, Division и Status имели данные.")

        # Генерация данных для сотрудников
        for _ in range(150):
            employer_data = EmployerRandomCreate(
                surname=random.choice(last_names),
                firstname=random.choice(first_names),
                patronymic=random.choice(middle_names),
                sort=fake.random_int(min=1, max=100),
                rank_id=random.choice(rank_ids),
                division_id=random.choice(division_ids),
                status_id=random.choice(status_ids)
            )
            employer = self.create_employer(db, employer_data)
            if not employer:
                continue

        # Проверяем department
        department = db.query(Department).first()

        # Получаем все employer_ids из базы данных после создания записей
        employer_ids = [employer.id for employer in db.query(Employer.id).all()]

        # Создаем словарь для соответствия management_id и division_id
        management_divisions = defaultdict(list)
        for management in db.query(Management).all():
            divisions = db.query(Division.id).filter(Division.management_id == management.id).all()
            management_divisions[management.id] = [division.id for division in divisions]

        # Создаем записи state, выбирая случайные значения для каждого поля
        for _ in range(130):  # Цикл точно на 130 итераций
            management_id = random.choice(list(management_divisions.keys()))
            division_id = random.choice(management_divisions[management_id])
            position_id = random.choice(position_ids)
            employer_id = random.choice(employer_ids)

            # Создаем данные для state
            state_data = StateRandomCreate(
                department_id=department.id,
                management_id=management_id,
                division_id=division_id,
                position_id=position_id,
                employer_id=employer_id
            )

            # Создаем запись state
            created_state = self.create_state(db, state_data)
            if created_state is None:
                print("Ошибка при создании state, пропуск итерации.")


data_service = DataForService()
