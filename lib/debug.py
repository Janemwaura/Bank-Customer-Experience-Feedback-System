import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Branch, Customer, Feedback
import ipdb;


if __name__ == '__main__':
    engine = create_engine('sqlite:////home/janewmwaura/phase3Bankproject/Bank-Customer-Experience-Feedback-System/lib/branches.db', echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    ipdb.set_trace()
