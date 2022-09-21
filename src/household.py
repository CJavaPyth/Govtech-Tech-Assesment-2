from audioop import add
from flask import Blueprint, request, jsonify
import json, datetime
from src.constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
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


@household.route('/get_households_info', methods=['GET'])
def get_households_info():
    all_households = Household.query.filter_by()
    house_ids = []
    for household in all_households:
        house_ids.append(household.id)

    all_household_info = []
    for id in house_ids:
        house = Household.query.filter_by(id=id).first()
        all_household_info.append({
                "house_id": id,
                "household_type": house.housing_type,
                "address": house.address
            })
            
        all_family_members = FamilyMember.query.filter_by(household=id)
        family_members = []
        for member in all_family_members:
            family_members.append({
                "name": member.name,
                "gender": member.gender,
                "marital_status": member.marital_status,
                "spouse": member.spouse_name,
                "occupation": member.occupation,
                "annual_income": member.annual_income,
                "date_of_birth": member.date_of_birth,      
            })
        all_household_info.append({"family_members": family_members})

    return jsonify({
        "households": all_household_info
    }), HTTP_200_OK


    
@household.route('/search_household', methods=['GET'])
def search_household():
    
    # takes in household_id as parameter
    household_id = request.json['household_id']
    house = Household.query.filter_by(id=household_id).first()
    household_type = house.housing_type
    household_address = house.address

    all_members = FamilyMember.query.filter_by(household=household_id)
    members_info = []
    for member in all_members:
        h = Household.query.filter_by(id=household_id).first()
        print(h.housing_type, h.address)
        members_info.append({
             "name": member.name,
             "gender": member.gender,
             "marital_status": member.marital_status,
             "spouse": member.spouse_name,
             "occupation": member.occupation,
             "annual_income": member.annual_income,
             "date_of_birth": member.date_of_birth,
        })

    return jsonify({
        'household_id': household_id,
        'household_type': household_type,
        'household_address': household_address,
        'family_members': members_info
    }), HTTP_200_OK
