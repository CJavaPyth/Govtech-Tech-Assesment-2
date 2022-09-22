# Govtech-Tech-Assesment-2

Assumptions made for:
  - Endpoint 1:
    - Apart from "housing_type" as the only field for a Household, i have added "address" as a field as well
    
  - Endpoint 2:
    - MaritalStatus can only be: single, married, divorced, widowed
    - Spouse can be: nil, or assumed to be the name of their actual spouse
    - DOB is assumed to be in the format: DD/MM/YY
    
 - Endpoint 4:
    - The endpoint takes in 'household_id' as request parameter
    - E.g
    {
      "household_id" : 1
    }

- Endpoint 5:
    - The endpoint takes in 'grant_disbursement' as request parameter
    - "SEB" is used to denote Student Encouragement Bonus, "MSG" for Multigeneration Scheme, "EB" for Elder Bonus, "BSG" for Baby Sunshine Grant, "YOLO_GST" for YOLO  GST Grant
   
    - E.g.
    {
      "grant_disbursement" : "SEB"
    }
