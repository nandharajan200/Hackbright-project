
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from model import db, connect_to_db, User, Team, UserTeam, Board


# MAKE NEW OBJECT #######################################################

def make_user(email, password):
    """Takes in registration form strings, makes a User object, returns it."""

    new_user = User(email=email, password=password)
    return new_user


def make_team(t_name, t_desc):
    """Takes in string parameters, makes a Team object, returns it."""

    new_team = Team(name=t_name, desc=t_desc)
    return new_team


def make_userteam(u_id, t_id):
    """Takes in integer parameters, makes a UserTeam object, returns it."""

    new_userteam = UserTeam(user_id=u_id, team_id=t_id)
    return new_userteam


# UPDATE DATABASE #######################################################

def update_db(baseobject):
    """Takes in any Model object and adds it to the database,
    committing the update."""

    db.session.add(baseobject)
    db.session.commit()
    print "Added to db."


# OBJECT QUERIES #########################################################

def get_user_object(u_id):
    """Takes in an integer and queries the user_accounts table for that
    user object."""

    user = User.query.get(u_id)
    return user


# FETCH INSTANCE QUERIES (WITH FIRST) ####################################

def get_user_by_email(email):
    """Filters for user record by email, returning None if not present. """

    user = User.query.filter(User.email == email).first()
    return user
