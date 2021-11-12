import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

engine = sqlalchemy.create_engine(
    "mysql+mysqlconnector://carmodelpython:s3cr37@localhost:3307/classicmodels"
)

Base = automap_base()
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

Base.prepare(engine, reflect=True)

# _sa_instance_state
def repr(self):
    return '\n'.join(k + '=' + str(v) for k, v in self.__dict__.items() if k != '_sa_instance_state')

for cls in Base.classes:
    cls.__repr__ = repr

Customer = Base.classes.customers
Employee = Base.classes.employees
Office = Base.classes.offices
OrderDetail = Base.classes.orderdetails
Order = Base.classes.orders
Payment = Base.classes.payments
ProductLine = Base.classes.productlines
Product = Base.classes.products


def customer_repr(self):
    return f'{self.customerName}, {self.contactFirstName} {self.contactLastName}. {self.country}'


# Customer.__repr__ = customer_repr


def main():
    # GiftsForHim.com
    customer = session.query(Customer).filter(Customer.customerName == 'GiftsForHim.com').first()
    print(customer)
    for order in customer.orders_collection:
        print('*' * 10)
        print(order)
        print(order.orderNumber)
        for order_row in order.orderdetails_collection:
            print(f'\t{order_row.products.productName}')
            print(f'\t\tPrice Each: ${order_row.priceEach}, Quantity: {order_row.quantityOrdered}.')
            print(f'\t\t\tTotal: ${order_row.priceEach * order_row.quantityOrdered:,}')

if __name__ == '__main__':
    main()
