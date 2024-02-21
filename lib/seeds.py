from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Branch, Customer, Feedback

# Connect to the database
engine = create_engine('sqlite:///db/branches.db')

Base.metadata.bind = engine

# Create a session to interact with the database
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Seed data for branches
nairobibranch = Branch(name='Nairobi Branch', service='Account opening')
kisumubranch = Branch(name='Kisumu Branch', service='Cash withdrawal')
mombasabranch = Branch(name='Mombasa Branch', service='Cash deposit')
kikuyubranch = Branch(name='Kikuyu Branch', service='Account opening')
makongenibranch = Branch(name='Makongeni Branch', service='Cheque deposit')
jujabranch = Branch(name='Juja Branch', service='Cash withdrawal')

session.add_all([nairobibranch, kisumubranch, mombasabranch, kikuyubranch, makongenibranch, jujabranch])

# Seed data for customers
customer1 = Customer(first_name='Ali', last_name='Hassan')
customer2 = Customer(first_name='Jane', last_name='Wairimu')
customer3 = Customer(first_name='Alice', last_name='Njeri')
customer4 = Customer(first_name='John', last_name='Doe')
customer5 = Customer(first_name='Mary', last_name='Jane')
customer6 = Customer(first_name='Peter', last_name='Waithaka')
customer7 = Customer(first_name='James', last_name='Mwangi')
customer8 = Customer(first_name='Lilian', last_name='Wanjiru')

session.add_all([customer1, customer2, customer3, customer4, customer5, customer6, customer7, customer8])

# Seed data for feedback
feedback1 = Feedback(comment="no complaint so far", star_rating=4, customer=customer6, branch=nairobibranch)
feedback2 = Feedback(comment="best branch so far", star_rating=5, customer=customer7, branch=kisumubranch)
feedback3 = Feedback(comment="there was no water at the branch", star_rating=3, customer=customer8, branch=mombasabranch)
feedback4 = Feedback(comment="few staff at the tellers", star_rating=4, customer=customer1, branch=kikuyubranch)
feedback5 = Feedback(comment="good customer service", star_rating=5, customer=customer2, branch=makongenibranch)
feedback6 = Feedback(comment="excellent service", star_rating=3, customer=customer3, branch=jujabranch)

session.add_all([feedback1, feedback2, feedback3, feedback4, feedback5, feedback6])

# Additional feedback
feedback7 = Feedback(comment="no complaint so far", star_rating=5, customer=customer3, branch=nairobibranch)
feedback8 = Feedback(comment="no complaint so far", star_rating=5, customer=customer4, branch=kisumubranch)
feedback9 = Feedback(comment="best branch so far", star_rating=5, customer=customer5, branch=mombasabranch)
session.add_all([feedback7, feedback8, feedback9])

# Commit the transactions
session.commit()
