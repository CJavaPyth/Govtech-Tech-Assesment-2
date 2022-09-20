from audioop import add
from flask import Blueprint, request, jsonify
import json, datetime
from src.constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from src.database import FamilyMember, Household, db

household = Blueprint("household", __name__, url_prefix="/api/v1/household")

@household.route('/create_household', methods=['POST'])
def create_household():
    housing_type = request.json['housing_type']
    address = request.json['address']
    house_types = ['landed', 'condominium', 'hdb']

    if housing_type not in house_types:
        return jsonify({'error': "House type must be either: 'landed', 'condominium' or 'hdb' only"}), HTTP_400_BAD_REQUEST
    household = Household(housing_type=housing_type, address=address)

    db.session.add(household)
    db.session.commit()

    return jsonify({
        'message': "Household created",
        'house': {
            'housing_type': housing_type,
            'address': address,
            'household_created_on': datetime.datetime.now(),
        }
    }), HTTP_201_CREATED

@household.route('/add_member', methods=['POST'])
def add_member():
    name = request.json['name']
    gender = request.json['gender']
    marital_status = request.json['marital_status']
    spouse = request.json['spouse']
    occupation = request.json['occupation']
    annual_income = request.json['annual_income']
    date_of_birth = request.json['date_of_birth']
    household_id = request.json['household']
    s = ["male", "female"]
    if gender not in s:
        return jsonify({'error': "gender must be either: 'male' or 'female' only"}), HTTP_400_BAD_REQUEST
    if int(annual_income) < 0:
        return jsonify({'error': "annual_income must be more than 0"}), HTTP_400_BAD_REQUEST
    o = ['unemployed', 'student', 'employed']
    if occupation not in o:
        return jsonify({'error': "occupation must be either: 'unemployed', 'student' or 'employed' only"}), HTTP_400_BAD_REQUEST

    member = FamilyMember(name=name, gender=gender, marital_status=marital_status, spouse_name=spouse, occupation=occupation, annual_income=annual_income, date_of_birth=date_of_birth, household=household_id)
    db.session.add(member)
    db.session.commit()

    return jsonify({
        'message': "Family member created",
        'particulars': {
            'name': name,
            'gender': gender,
            'marital_status': marital_status,
            'spouse': spouse,
            'occupation': occupation,
            'annual_income': annual_income,
            'dob': date_of_birth,
            'household_id': household_id
        }
    }), HTTP_201_CREATED