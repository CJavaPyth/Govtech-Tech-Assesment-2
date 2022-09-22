from flask_sqlalchemy import SQLAlchemy
import datetime, string, random
from flask import jsonify

db = SQLAlchemy()

# database schema models

class Household(db.Model):

    # household id is primary key
    id = db.Column(db.Integer, primary_key=True)
    housing_type = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.now())
    members = db.relationship('FamilyMember', backref="household_members", lazy=True)

    def __repr__(self) -> str:
        return f'house_id: {self.house_id}, housing_type: {self.housing_type}'
    
class FamilyMember(db.Model):

    # family member id is primary key
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    gender = db.Column(db.Text, nullable=False)
    marital_status = db.Column(db.Text, nullable=False)
    spouse_name = db.Column(db.Text, nullable=False)
    occupation = db.Column(db.Text, nullable=False)
    annual_income = db.Column(db.Integer, nullable=False)

    # assume that inputted date is string of the format "DD/MM/YY"
    date_of_birth = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.now())

    # assign household id as foreign key
    household = db.Column(db.Integer(), db.ForeignKey("household.id"))

    def __repr__(self) -> str:
        return f'Family_member name: {self.name}'