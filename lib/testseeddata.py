import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Branch, Customer, Feedback

class TestSeedData(unittest.TestCase):
    def setUp(self):
        # Connect to the test database
        self.engine = create_engine('sqlite:///branches.db')
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        # Create tables
        Base.metadata.create_all(self.engine)

        # Seed data
        self.seed_data()

    def tearDown(self):
        # Clean up: rollback any changes and close the session
        self.session.rollback()
        self.session.close()
        # Drop all tables
        Base.metadata.drop_all(self.engine)

    def seed_data(self):
        # Your seed data creation code here
        nairobibranch = Branch(name='Nairobi Branch', service='Account opening')
        kisumubranch = Branch(name='Kisumu Branch', service='Cash withdrawal')
        mombasabranch = Branch(name='Mombasa Branch', service='Cash deposit')
        self.session.add_all([nairobibranch, kisumubranch, mombasabranch])

        customer1 = Customer(first_name='Ali', last_name='Hassan')
        customer2 = Customer(first_name='Jane', last_name='Wairimu')
        customer3 = Customer(first_name='Alice', last_name='Njeri')
        self.session.add_all([customer1, customer2, customer3])

        feedback1 = Feedback(star_rating=4, branch=nairobibranch, customer=customer1)
        feedback2 = Feedback(star_rating=5, branch=kisumubranch, customer=customer2)
        feedback3 = Feedback(star_rating=3, branch=mombasabranch, customer=customer3)
        self.session.add_all([feedback1, feedback2, feedback3])

        self.session.commit()

    def test_branches(self):
        # Test the seeded branches
        branches = self.session.query(Branch).all()
        self.assertEqual(len(branches), 3)  # Check if all branches are seeded

    def test_customers(self):
        # Test the seeded customers
        customers = self.session.query(Customer).all()
        self.assertEqual(len(customers), 3)  # Check if all customers are seeded

    def test_feedback(self):
        # Test the seeded feedback
        feedback = self.session.query(Feedback).all()
        self.assertEqual(len(feedback), 3)  # Check if all feedback entries are seeded

        # Additional assertions based on your data structure and expectations

if __name__ == '__main__':
    unittest.main()
