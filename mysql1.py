import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = sqlalchemy.create_engine(
    "mysql+mysqlconnector://pythonuser:s3cr37@localhost:3307/PythonDB"
)

Base = declarative_base()
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


class Person(Base):
    __tablename__ = 'persons'

    persons_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    cars = relationship('Car', back_populates='owner')

    def __repr__(self):
        return f'{self.persons_id}, {self.first_name}, {self.last_name} - {self.cars}'


class Car(Base):
    __tablename__ = 'cars'

    cars_id = Column(Integer, primary_key=True, autoincrement=True)
    reg_no = Column(String(7), nullable=False)
    car_model = Column(String(50))
    owner_id = Column(Integer, ForeignKey('persons.persons_id'))
    owner = relationship('Person', back_populates='cars')

    def __repr__(self):
        return f'{self.reg_no} - {self.car_model}'


def print_all():
    persons = session.query(Person).all()
    for person in persons:
        print(person)


def main():
    print_all()
    print('*' * 34)
    p1 = session.query(Person).filter(Person.persons_id == 1).first()
    p2 = session.query(Person).filter(Person.persons_id == 5).first()
    car = p1.cars[0]
    p1.cars.remove(car)
    p2.cars.append(car)
    session.add(p1)
    session.add(p2)
    session.commit()
    print_all()
    # Create a new person
    # person = Person(first_name='Eric', last_name='Erson')
    # session.add(person)
    # session.commit()
    # print_all()


if __name__ == '__main__':
    main()
