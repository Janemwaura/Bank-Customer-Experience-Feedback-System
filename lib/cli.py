import cmd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Branch, Customer, Feedback

class BankCLI(cmd.Cmd):
    prompt = 'bank> '

    def __init__(self):
        super().__init__()
        self.engine = create_engine('sqlite:////home/janewmwaura/phase3Bankproject/Bank-Customer-Experience-Feedback-System/lib/branches.db')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def do_exit(self, arg):
        """Exit the CLI"""
        print("Exiting CLI...")
        return True

    def do_list_branches(self, arg):
        """List all branches"""
        branches = self.session.query(Branch).all()
        for branch in branches:
            print(branch)

    def do_list_customers(self, arg):
        """List all customers"""
        customers = self.session.query(Customer).all()
        for customer in customers:
            print(customer)

    def do_add_customer(self, arg):
        """Add a new customer"""
        first_name, last_name = arg.split()
        customer = Customer(first_name=first_name, last_name=last_name)
        self.session.add(customer)
        self.session.commit()
        print("Customer added successfully.")

    def do_add_feedback(self, arg):
        """Add feedback for a customer"""
        customer_id, branch_id, star_rating, comment = arg.split()
        feedback = Feedback(customer_id=int(customer_id), branch_id=int(branch_id), star_rating=int(star_rating), comment=comment)
        self.session.add(feedback)
        self.session.commit()
        print("Feedback added successfully.")

if __name__ == '__main__':
    BankCLI().cmdloop()
