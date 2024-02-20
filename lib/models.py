import os
import sys
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import declarative_base

Base = declarative_base()
engine = create_engine('sqlite:////home/janewmwaura/phase3Bankproject/Bank-Customer-Experience-Feedback-System/lib/branches.db', echo=True)

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

    def __repr__(self):
        return f'Feedback: {self.star_rating}'

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer(), primary_key=True)
    first_name = Column(String())
    last_name = Column(String())     

    feedback = relationship('Feedback', backref=backref('customer'))
    branches = relationship('Branch', secondary=branch_user, back_populates='customers')
    
    def __repr__(self):
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

    def __repr__(self):
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
