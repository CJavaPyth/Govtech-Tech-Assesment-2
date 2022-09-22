from unittest import result
from sqlalchemy import desc, func
from flask import Blueprint, request, jsonify
import json, datetime
from src.constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from src.models import FamilyMember, Household, db

household = Blueprint("household", __name__, url_prefix="/api/v1/household")

# endpoint 1: to create household
@household.route('/create_household', methods=['POST'])
def create_household():
    housing_type = request.json['housing_type']
    address = request.json['address']

    # possible options for housing_type
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

# endpoint 2: to add new member to a household
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

    # possible options for gender, occupation, and marital_status
    gen = ["male", "female"]
    occ = ['unemployed', 'student', 'employed']
    mar = ['divorced', 'widowed', 'married', 'single']

    # gender must be male or female only
    if gender not in s:
        return jsonify({'error': "gender must be either: 'male' or 'female' only"}), HTTP_400_BAD_REQUEST

    # annual_income cannot be below 0
    if int(annual_income) < 0:
        return jsonify({'error': "annual_income must be more than 0"}), HTTP_400_BAD_REQUEST

    # occupation must be unemployed, student, or employed only
    if occupation not in o:
        return jsonify({'error': "occupation must be either: 'unemployed', 'student' or 'employed' only"}), HTTP_400_BAD_REQUEST

    if marital_status not in mar:
        return jsonify({'error': "martial_status must be either: 'divorced', 'widowed', 'married' or 'single' only"}), HTTP_400_BAD_REQUEST

    # assume spouse is inputted as either nil, or a legitimate name of a person of the opposite gender
    # assume DOB is inputted correctly as DD/MM/YY format, no error checking

    member = FamilyMember(name=name, gender=gender, marital_status=marital_status, spouse_name=spouse, occupation=occupation, annual_income=annual_income, date_of_birth=date_of_birth, household=household_id)
    db.session.add(member)
    db.session.commit()

    # return response
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


# endpoint 3: list all households and members info
@household.route('/get_households_info', methods=['GET'])
def get_households_info():
    
    # get all household models in database
    all_households = Household.query.filter_by()
    house_ids = []
    for household in all_households:
        # get all household ids into a list
        house_ids.append(household.id)

    all_household_info = []

    # loop through each household
    for id in house_ids:
        house = Household.query.filter_by(id=id).first()
        
        # append this for each household
        all_household_info.append({
                "house_id": id,
                "household_type": house.housing_type,
                "address": house.address
            })

        # get all members in the current household in the loop
        all_family_members = FamilyMember.query.filter_by(household=id)
        family_members = []
        for member in all_family_members:

            # append each family member for the current household in the loop
            family_members.append({
                "name": member.name,
                "gender": member.gender,
                "marital_status": member.marital_status,
                "spouse": member.spouse_name,
                "occupation": member.occupation,
                "annual_income": member.annual_income,
                "date_of_birth": member.date_of_birth,      
            })

        # append everying into a results list to return as reponse
        all_household_info.append({"family_members": family_members})

    # response
    return jsonify({
        "households": all_household_info
    }), HTTP_200_OK


# endpoint 4: search for a particular household, takes in household_id as a parameter
@household.route('/search_household', methods=['GET'])
def search_household():
    
    # takes in household_id as parameter
    household_id = request.json['household_id']

    # search for the first household with the id that is given, collect its household_address and household_type information, to return as a response
    house = Household.query.filter_by(id=household_id).first()
    household_type = house.housing_type
    household_address = house.address

    # search and get all family members in the particular id
    all_members = FamilyMember.query.filter_by(household=household_id)
    members_info = []
    for member in all_members:

        # append each family member's info into a list, to be return as part of response
        members_info.append({
             "name": member.name,
             "gender": member.gender,
             "marital_status": member.marital_status,
             "spouse": member.spouse_name,
             "occupation": member.occupation,
             "annual_income": member.annual_income,
             "date_of_birth": member.date_of_birth,
        })

    # response
    return jsonify({
        'household_id': household_id,
        'household_type': household_type,
        'household_address': household_address,
        'family_members': members_info
    }), HTTP_200_OK


# endpoint 5: check for grant_disbursement
# for Student Encouragement Bonus, takes in "SEB" as parameter
# for Multigeneration Scheme, takes in "MGS" as parameter
# for Elder Bonus, takes in "EB" as parameter
# for Baby Sunshine Grant, takes in "BSG" as parameter
# for YOLO GST Grant, takes in "YOLO_GST" as parameter
@household.route('/grant_disbursement_eligibiity', methods=['GET'])
def get_grants():

    # get the highest house_id in the database currently
    max_house_id = db.session.query(func.max(Household.id)).scalar()
    
    # append all qualifying family_members for the various schemes into this list, to be sent as a response result
    family_members = []

    # a list to append information, to be sent as a response result
    result = []
    
    # if "SEB" is sent as parameter - Student Encouragement Bonus
    if request.json['grant_disbursement'] == 'SEB':

        # loop through house IDs
        for house_id in range(1, max_house_id+1):
            age_criteria = False       
            # get family members info, for student(s) in each household
            students_in_house =  FamilyMember.query.filter_by(occupation='student', household=house_id)
            for student in students_in_house:
                
                # verify the age of each student in each household
                if 2022 - int(student.date_of_birth[len(student.date_of_birth)-4:len(student.date_of_birth)]) < 16:
                    # age_criteria variable set to True
                    age_criteria = True
                    # append each family member to be sent as part of response result
                    family_members.append({
                        "name": student.name,
                        "gender": student.gender,
                        "marital_status": student.marital_status,
                        "spouse": student.spouse_name,
                        "occupation": student.occupation,
                        "annual_income": student.annual_income,
                        "date_of_birth": student.date_of_birth,
                    })

            if age_criteria == True:
                h = Household.query.filter_by(id=student.household).first()

                # append house info as part of response result 
                result.append({
                    "house_id": h.id,
                    "household_type": h.housing_type,
                    "address": h.address,
                    'qualifying_members': family_members
                })
        
        # response
        return jsonify({
            "households_eligible_for_SEB": result
        }), HTTP_200_OK

    
    # if "MGS" is sent as parameter = Multigenerational Scheme
    elif request.json['grant_disbursement'] == 'MGS':

        # loop through house IDs
        for house_id in range(1, max_house_id+1):

            # get family members info in each household
            members_in_house = FamilyMember.query.filter_by(household=house_id)

            # set household_combined_income to 0 and age_criteria to False as default
            household_combined_income = 0
            age_criteria = False

            # for each member in the same household
            for member in members_in_house:
                # sum up annual_income
                household_combined_income += member.annual_income
                # check if any member in the current household has fulfilled age criteria
                if (2022 - int(member.date_of_birth[len(member.date_of_birth)-4:len(member.date_of_birth)]) < 18 or (2022 - int(member.date_of_birth[len(member.date_of_birth)-4:len(member.date_of_birth)]) > 55)):
                    age_criteria = True
            
            # if age_criteria and combined annual income is fulfilled
            if age_criteria == True and household_combined_income < 150000:
                h = Household.query.filter_by(id=member.household).first() 

                # append household information to be sent as part of response result
                result.append({
                    "house_id": h.id,
                    "household_type": h.housing_type,
                    "address": h.address,
                    'qualifying_members': family_members
                })
                
                members = FamilyMember.query.filter_by(household=house_id)
                
                # append each member's information to be sent as part of response result
                for member in members:
                    family_members.append({
                        "name": member.name,
                        "gender": member.gender,
                        "marital_status": member.marital_status,
                        "spouse": member.spouse_name,
                        "occupation": member.occupation,
                        "annual_income": member.annual_income,
                        "date_of_birth": member.date_of_birth,
                    })

        # response
        return jsonify({
            "households_eligible_for_MGS": result
        }), HTTP_200_OK 


    # if "EB" is sent as parameter - Elder Bonus
    elif request.json['grant_disbursement'] == 'EB':

        # search for all HDB households in database
        hdb_houses = Household.query.filter_by(housing_type='hdb')
        for hdb in hdb_houses:

            # search all family members living in same household
            hdb_fellows = FamilyMember.query.filter_by(household=hdb.id)
            age_criteria = False

            # for each family member living in same household
            for member in hdb_fellows:

                # check if any member in the current household fulfils age criteria
                if (2022 - int(member.date_of_birth[len(member.date_of_birth)-4:len(member.date_of_birth)])) >= 55: 
                    age_criteria = True

                    # append each qualifying family member info, to be sent later as part of response result
                    family_members.append({
                        "name": member.name,
                        "gender": member.gender,
                        "marital_status": member.marital_status,
                        "spouse": member.spouse_name,
                        "occupation": member.occupation,
                        "annual_income": member.annual_income,
                        "date_of_birth": member.date_of_birth,
                    })
                     

            # append house information to be sent later as part of response result       
            if age_criteria == True:
                result.append({
                    "house_id": hdb.id,
                    "household_type": hdb.housing_type,
                    "address": hdb.address,
                    'qualifying_members': family_members
                })

        # response
        return jsonify({
            "households_eligible_for_EB": result
        }), HTTP_200_OK 


    # if "BGS" is sent as parameter - Baby Sunshine Grant
    elif request.json['grant_disbursement'] == 'BSG':

        # loop through house IDs
        for house_id in range(1, max_house_id+1):

            # search and collect all members who belong to the same household
            members_in_house = FamilyMember.query.filter_by(household=house_id)
            age_criteria = False
            # for each member living in same household
            for member in members_in_house:

                # we assume DOB is in DD/MM/YY format
                # assume today's date is 21 September 2022 in this case, could also use python datetime module for more generic use
                # i.e. baby must be < 8 months, taking into account the month and date

                # check age_criteria
                year = member.date_of_birth[6:]
                if year == '2022':
                    date = int(member.date_of_birth[:2])
                    month = int(member.date_of_birth[3:5])
                    if 9-month <= 8 and date < 21:
                        age_criteria = True

                        # append member's information to be sent later as a response result
                        family_members.append({
                            "name": member.name,
                            "gender": member.gender,
                            "marital_status": member.marital_status,
                            "spouse": member.spouse_name,
                            "occupation": member.occupation,
                            "annual_income": member.annual_income,
                            "date_of_birth": member.date_of_birth,
                        })

            if age_criteria == True:
                house = Household.query.filter_by(id=house_id).first()

                # append household information, to be sent as a response result
                result.append({
                    "house_id": house.id,
                    "household_type": house.housing_type,
                    "address": house.address,
                    'qualifying_members': family_members
                })

        # response
        return jsonify({
            "households_eligible_for_BSG": result
        }), HTTP_200_OK


    # if "YOLO_GST" is sent as parameter - YOLO GST Grant
    elif request.json['grant_disbursement'] == 'YOLO_GST':

        # search and collect all HDB households in database
        hdb_houses = Household.query.filter_by(housing_type='hdb')
        
        # for each HDB household
        for hdb in hdb_houses:
            # initialise income_criteria to be False and household combined income to be 0 by default
            income_criteria = False
            household_combined_income = 0

            # search and get all family members living in the same HDB household
            hdb_fellows = FamilyMember.query.filter_by(household=hdb.id)

            # for each family member living in same hdb household
            for member in hdb_fellows:
                # sum up household income
                household_combined_income += member.annual_income
            if household_combined_income < 100000:
                # set income_criteria to be True
                income_criteria = True
                
                # for each family member living in same hdb household
                for member in hdb_fellows:

                    # append member's info, to be sent as part of response result
                    family_members.append({
                        "name": member.name,
                        "gender": member.gender,
                        "marital_status": member.marital_status,
                        "spouse": member.spouse_name,
                        "occupation": member.occupation,
                        "annual_income": member.annual_income,
                        "date_of_birth": member.date_of_birth,
                    })  
        
        if income_criteria == True:

            # append house information, to be sent as part of response result
            result.append({
                "house_id": hdb.id,
                "household_type": hdb.housing_type,
                "address": hdb.address,
                'qualifying_members': family_members
            })

        # response
        return jsonify({
            "households_eligible_for_YOLO_GST_Grant": result
        }), HTTP_200_OK 

