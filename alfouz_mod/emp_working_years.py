import frappe


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
