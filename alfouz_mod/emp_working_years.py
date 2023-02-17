import frappe
from datetime import datetime


def calculating_employee_life():
    today = frappe.utils.nowdate()
    docs = frappe.get_list('Employee', pluck='name')
    for doc in docs:
        doc = frappe.get_doc('Employee', doc)
        if doc.status == 'Active':
            date_of_joining = doc.date_of_joining
            month_of_joining = int(str(date_of_joining).split('-')[1])
            if month_of_joining <= 5:
                doc.working_years = frappe.utils.date_diff(
                    today, date_of_joining) / 365
            else:
                doc.working_years = frappe.utils.date_diff(
                    today, frappe.utils.datetime.date(date_of_joining.year + 1,
                                                      1, date_of_joining.day)) / 365
            doc.save()
            frappe.db.commit()


def recalculate_years_of_work():
    current_date = datetime.now()
    for employee in frappe.get_all("Employee", filters={"status": "Active"}):
        joining_date = frappe.db.get_value(
            "Employee", employee.name, "date_of_joining")
        years_of_work = current_date.year - joining_date.year
        if joining_date.month > 6:
            years_of_work -= 1
        if years_of_work < 1:
            years_of_work = 0
        frappe.db.set_value("Employee", employee.name,
                            "working_years", years_of_work)
    frappe.db.commit()
