from __future__ import unicode_literals

import frappe
from frappe.utils.password import update_password
from frappe.utils import now


@frappe.whitelist(allow_guest=True)
def get_response( first_name='', last_name='', email='', phone='', password = '', date_of_birth = '1998-07-28', date_of_joining = '2025-01-01', gender = 'Male'):
    data = {
        'first name':       first_name,
        'last name':        last_name,
        'email':            email,
        'password':         password,
        'date_of_birth':    date_of_birth,
        'date_of_joining':  date_of_joining,
        'gender':           gender,
    }

    #:  (for incomplete data, reply ERROR message)
    for key in data:
        if not data[key]: 
            frappe.response["message"] = 'Please provide your {0}, thanks.'.format( key )
            return frappe.response["message"]

    #:  TODO - (send an email to the consumer)
    # frappe.sendmail( recipients=forward_to_email, sender=sender, content='We have received your message and we will get back to you ASAP.', subject='[System Message] Reply Email from IoT Eye Inc.' )
    user = frappe.get_doc({
        "doctype": "User",
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "enabled": 1,
        "user_type": "Website User",
        "phone": phone
    })
    user.flags.ignore_permissions = True
    user.insert()

    # Set password
    update_password(user.name, password)

    # Employee creation logic
    employee = frappe.get_doc({
        "doctype": "Employee",
        "first_name": first_name,
        "last_name": last_name,
        "employee_name": first_name + last_name,
        "status": "Active",
        "date_of_birth": date_of_birth,
        "gender": gender,
        "date_of_joining": date_of_joining,
        "cell_number": phone
    })
    employee.flags.ignore_permissions = True
    employee.insert()
    return 'COMPLETE_DATA'


    