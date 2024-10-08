from sqlalchemy.orm import Session
from models import Department, Management, Division, Position, Rank, Status, Employer, State
from schemas import DepartmentCreate, ManagementCreate, DivisionCreate, PositionCreate, RankCreate, StatusCreate, \
    EmployerRandomCreate, StateRandomCreate
from faker import Faker
import random

fake = Faker()


class DataForService:

    def create_department(self, db: Session, department_data: DepartmentCreate):
        try:
            department = Department(name=department_data.name)
            db.add(department)
            db.commit()
            db.refresh(department)
            return department
        except Exception as e:
            db.rollback()
            print(f"Ошибка при создании департамента: {e}")
            return None

    def create_management(self, db: Session, management_data: ManagementCreate):
        try:
            management = Management(
                name=management_data.name,
                department_id=management_data.department_id
            )
            db.add(management)
            db.commit()
            db.refresh(management)
            return management
        except Exception as e:
            db.rollback()
            print(f"Ошибка при создании управления: {e}")
            return None

    def create_division(self, db: Session, division_data: DivisionCreate):
        try:
            division = Division(
                name=division_data.name,
                management_id=division_data.management_id
            )
            db.add(division)
            db.commit()
            db.refresh(division)
            return division
        except Exception as e:
            db.rollback()
            print(f"Ошибка при создании отдела: {e}")
            return None

    def create_position(self, db: Session, position_data: PositionCreate):
        try:
            position = Position(name=position_data.name)
            db.add(position)
            db.commit()
            db.refresh(position)
            return position
        except Exception as e:
            db.rollback()
            print(f"Ошибка при создании должности: {e}")
            return None

    def create_rank(self, db: Session, rank_data: RankCreate):
        try:
            rank = Rank(name=rank_data.name)
            db.add(rank)
            db.commit()
            db.refresh(rank)
            return rank
        except Exception as e:
            db.rollback()
            print(f"Ошибка при создании звания: {e}")
            return None

    def create_status(self, db: Session, status_data: StatusCreate):
        try:
            status = Status(
                name=status_data.name,
                start_date=status_data.start_date,
                end_date=status_data.end_date
            )
            db.add(status)
            db.commit()
            db.refresh(status)
            return status
        except Exception as e:
            db.rollback()
            print(f"Ошибка при создании статуса: {e}")
            return None

    def create_employer(self, db: Session, employer_data: EmployerRandomCreate):
        try:
            employer = Employer(
                surname=employer_data.surname,
                firstname=employer_data.firstname,
                patronymic=employer_data.patronymic,
                sort=employer_data.sort,
                rank_id=employer_data.rank_id,
                position_id=employer_data.position_id,
                division_id=employer_data.division_id,
                status_id=employer_data.status_id
            )
            db.add(employer)
            db.commit()
            db.refresh(employer)
            return employer
        except Exception as e:
            db.rollback()
            print(f"Ошибка при создании сотрудника: {e}")
            return None

    def create_state(self, db: Session, state_data: StateRandomCreate):
        try:
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
            return state
        except Exception as e:
            db.rollback()
            print(f"Ошибка при создании состояния: {e}")
            return None

    def populate_all_tables(self, db: Session, num_records: int):
        # Создание департамента
        department_data = DepartmentCreate(name="Седьмой департамент")
        department = self.create_department(db, department_data)

        for _ in range(6):
            # Создание управления в департаменте
            management_data = ManagementCreate(
                name=random.choice(["1-управление", "2-управление", "3-управление", "4-управление", "5-управление", "6-управление"]),
                department_id=department.id
            )
            management = self.create_management(db, management_data)
            if not management:
                continue

        for _ in range(2):
            # Создание отдела в управлении
            division_data = DivisionCreate(
                name=random.choice(["1-отдел", "2-отдел"]),
                management_id=fake.random_int(min=1, max=6)
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
            end_date = start_date if random.choice([True, False]) else None
            status_data = StatusCreate(
                name=random.choice(["в строю", "болен", "отпуск"]),
                start_date=start_date,
                end_date=end_date
            )
            status = self.create_status(db, status_data)
            if not status:
                continue

        for _ in range(num_records):
            # Создание сотрудника
            employer_data = EmployerRandomCreate(
                surname=fake.last_name(),
                firstname=fake.first_name(),
                patronymic=fake.first_name(),
                sort=fake.random_int(min=1, max=100),
                rank_id=fake.random_int(min=1, max=10),
                position_id=fake.random_int(min=1, max=15),
                division_id=fake.random_int(min=1, max=2),
                status_id=fake.random_int(min=1, max=10)
            )
            employer = self.create_employer(db, employer_data)
            if not employer:
                continue

        for _ in range(129):
            # Создание состояния
            state_data = StateRandomCreate(
                department_id=department.id,
                management_id=fake.random_int(min=1, max=6),
                division_id=fake.random_int(min=1, max=5),
                position_id=fake.random_int(min=1, max=15),
                employer_id=fake.random_int(min=1, max=num_records)
            )
            self.create_state(db, state_data)

data_service = DataForService()
