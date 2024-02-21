import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Branch, Customer, Feedback

# Connect to the database
engine = create_engine('sqlite:///db/branches.db')
Base.metadata.bind = engine

# Create a session to interact with the database
DBSession = sessionmaker(bind=engine)

@click.group()
def cli():
    pass

@cli.command()
@click.option('--name', prompt='Branch name', help='Name of the branch')
@click.option('--service', prompt='Service offered', help='Service offered by the branch')
def add_branch(name, service):
    session = DBSession()
    new_branch = Branch(name=name, service=service)
    session.add(new_branch)
    session.commit()
    click.echo('Branch added successfully.')

@cli.command()
def list_branches():
    session = DBSession()
    branches = session.query(Branch).all()
    for branch in branches:
        click.echo(f'Branch ID: {branch.id}, Name: {branch.name}, Service: {branch.service}')

@cli.command()
@click.argument('branch_id', type=int)
def delete_branch(branch_id):
    session = DBSession()
    branch = session.query(Branch).filter_by(id=branch_id).first()
    if branch:
        session.delete(branch)
        session.commit()
        click.echo('Branch deleted successfully.')
    else:
        click.echo('Branch not found.')

@cli.command()
@click.option('--comment', prompt='Feedback comment', help='Comment for the feedback')
@click.option('--rating', type=int, prompt='Star rating', help='Star rating for the feedback (1-5)')
@click.argument('branch_id', type=int)
@click.argument('customer_id', type=int)
def add_feedback(comment, rating, branch_id, customer_id):
    session = DBSession()
    branch = session.query(Branch).filter_by(id=branch_id).first()
    customer = session.query(Customer).filter_by(id=customer_id).first()
    if branch and customer:
        new_feedback = Feedback(comment=comment, star_rating=rating, branch=branch, customer=customer)
        session.add(new_feedback)
        session.commit()
        click.echo('Feedback added successfully.')
    else:
        click.echo('Branch or customer not found.')

if __name__ == '__main__':
    cli()
