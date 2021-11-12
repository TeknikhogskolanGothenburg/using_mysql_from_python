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
    __tablename__ = 'car_owners'

    persons_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100))
    cars = relationship('Car', back_populates='owner')

    def __repr__(self):
        return f'{self.persons_id}, {self.first_name}, {self.last_name} - {self.cars}'


class Car(Base):
    __tablename__ = 'autos'

    cars_id = Column(Integer, primary_key=True, autoincrement=True)
    reg_no = Column(String(7), nullable=False)
    car_model = Column(String(50))
    color = Column(String(50))
    owner_id = Column(Integer, ForeignKey('car_owners.persons_id'))
    owner = relationship('Person', back_populates='cars')

    def __repr__(self):
        return f'{self.reg_no} - {self.car_model}'


def main():
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    main()
