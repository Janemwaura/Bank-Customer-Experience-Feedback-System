import os
import sys
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
from tabulate import tabulate
from colorama import Fore, Style

Base = declarative_base()
engine = create_engine('sqlite:///db/branches.db', echo=False)

branch_user = Table(
    'branch_user', Base.metadata,
    Column('branch_id', ForeignKey('branches.id'), primary_key=True),
    Column('customer_id', ForeignKey('customers.id'), primary_key=True),
    extend_existing=True
)

class Feedback(Base):
    __tablename__ = 'feedback'
    
    id = Column(Integer(), primary_key=True)
    comment = Column(String())
    star_rating = Column(Integer())

    branch_id = Column(Integer(), ForeignKey('branches.id'))
    customer_id = Column(Integer(), ForeignKey('customers.id'))

    def _repr_(self):
        return f'Feedback: {self.star_rating}'

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer(), primary_key=True)
    first_name = Column(String())
    last_name = Column(String())     

    feedback = relationship('Feedback', backref=backref('customer'))
    branches = relationship('Branch', secondary=branch_user, back_populates='customers')
    
    def _repr_(self):
        return f'Customer: {self.first_name} {self.last_name}'

    def get_feedback(self):
        """
        Returns the Feedback instances associated with this customer.
        """
        return self.feedback 

    def get_branches(self):
        """
        Returns the Branch instances associated with this customer.
        """
        return self.branches

class Branch(Base):
    __tablename__ = 'branches'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    service = Column(String())

    feedback = relationship('Feedback', backref=backref('branch'))
    customers = relationship('Customer', secondary=branch_user, back_populates='branches')

    def _repr_(self):
        return f'Branch: {self.name}'

    def get_feedback(self):
        """
        Returns the Feedback instances associated with this branch.
        """
        return self.feedback

    def get_customers(self):
        """
        Returns the Customer instances associated with this branch.
        """
        return self.customers

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# CLI functionality
def view_branches(session):
    branches = session.query(Branch).all()
    branch_data = [[branch.id, branch.name, branch.service] for branch in branches]
    print(tabulate(branch_data, headers=["ID", "Name", "Service"], tablefmt="fancy_grid"))

def view_customers(session):
    customers = session.query(Customer).all()
    customer_data = [[customer.id, customer.first_name, customer.last_name] for customer in customers]
    print(tabulate(customer_data, headers=["ID", "First Name", "Last Name"], tablefmt="fancy_grid"))

def view_feedback(session):
    feedback_entries = session.query(Feedback).all()
    feedback_data = [[entry.id, entry.comment, entry.star_rating, entry.branch.name, entry.customer.first_name] for entry in feedback_entries]
    print(tabulate(feedback_data, headers=["ID", "Comment", "Star Rating", "Branch", "Customer"], tablefmt="fancy_grid"))

def main():
    while True:
        print("\n" + "-"*50)
        print(f"{Fore.CYAN}Welcome to Bank Feedback System{Style.RESET_ALL}")
        print("-"*50)
        print("1. View Branches")
        print("2. View Customers")
        print("3. View Feedback")
        print("4. Exit")
        choice = input(f"{Fore.YELLOW}Enter your choice: {Style.RESET_ALL}")

        if choice == '1':
            view_branches(session)
        elif choice == '2':
            view_customers(session)
        elif choice == '3':
            view_feedback(session)
        elif choice == '4':
            print(f"{Fore.CYAN}Goodbye!{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()