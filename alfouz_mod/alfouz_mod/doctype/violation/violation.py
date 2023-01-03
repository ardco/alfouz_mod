# Copyright (c) 2023, ARD and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import flt, today, getdate, add_years, time_diff, get_datetime_str
from frappe.utils import get_first_day, add_months, get_last_day


class Violation(Document):

    def before_insert(self):
        if self.additional_salary_earning or self.additional_salary_deduction:
            frappe.throw("Not allow to amend a cancelled Violation")

        dv = frappe.db.get_value(
            "Violation Type", self.violation_type, 'duration_of_the_violation')
        violation_list = frappe.get_list(
            "Violation", filters={
                "docstatus": 1,
                "employee": self.employee,
                "violation_type": self.violation_type,
                "posting_date": ["between",
                                 [
                                     # to check last 6 months
                                     add_months(self.posting_date, -(dv)),
                                     self.posting_date
                                 ]
                                 ]
            },
            order_by="posting_date")

        count = len(violation_list)
        count = count + 1
        self.frequency_count = count
        violation_type = frappe.get_doc('Violation Type', self.violation_type)
        violation_actions = violation_type.violation_action

        for action in violation_actions:
            if self.frequency_count == action.frequency:
                v_action = frappe.get_doc(
                    "Violation Action", action.violation_action)

                self.violation_action = action.violation_action
                self.deduction_type = v_action.deduction_type
                self.deduction_amountrate = v_action.deduction_valuerate or ''
                break

        violation_frequency = [va.frequency for va in violation_actions]

        violation_frequency.sort()
        target = count
        for i, f in enumerate(violation_frequency):
            if f > target:
                target = violation_frequency[i-1]
                break
            elif f == target:
                target = f
                break

        self.make_deduction(target, violation_actions)

    def on_cancel(self):
        doc = frappe.get_doc({
            "doctype": "Additional Salary",
            "employee": self.employee,
            "employee_name": self.employee_name,
            "payroll_date": today(),
            "salary_component": "تسويات اضافة",
            "company": self.company,
            "type": "Earning",
            "amount": self.deduction,
        })
        doc = doc.insert()
        doc.submit()
        frappe.db.set(self, 'additional_salary_earning', doc.name)
        frappe.db.commit()

    def on_submit(self):
        doc = frappe.get_doc({
            "doctype": "Additional Salary",
            "employee": self.employee,
            "employee_name": self.employee_name,
            "payroll_date": today(),
            "salary_component": "تسويات خصم",
            "company": self.company,
            "type": "Deduction",
            "amount": self.deduction,
        })
        doc = doc.insert()
        doc.submit()
        frappe.db.set(self, 'additional_salary_deduction', doc.name)
        frappe.db.commit()
        # frappe.db.sql(
        #     """update `tabAdditional Salary` set workflow_state ="Approved" where name='{}'""".format(doc.name))

    def get_daily_rate(self, employee, start_date, end_date):
        doc = self.get_salary(employee, start_date, end_date)
        return doc.gross_pay / 30

    def get_salary(self, employee, start_date, end_date):
        doc = frappe.get_doc({"doctype": "Salary Slip", "employee": employee,
                              "start_date": start_date, "end_date": end_date, "payroll_frequency": "Monthly"})
        doc.get_emp_and_leave_details()
        if doc.gross_pay is not None:
            return doc
        else:
            frappe.throw(
                _("Please create Salary Structure for employee {}".format(employee)))

    def make_deduction(self, target_frequency, violation_actions):
        daily = self.get_daily_rate(self.employee,
                                    get_first_day(self.posting_date),
                                    get_last_day(self.posting_date))

        for violation_action in violation_actions:
            if target_frequency == violation_action.frequency:
                va = frappe.get_doc('Violation Action',
                                    violation_action.violation_action)
                if va.deduction_type == 'Deduction By Day':
                    self.deduction = daily * int(va.deduction_valuerate)
                elif va.deduction_type == 'Deduction By Percentage':
                    self.deduction = daily * \
                        float(va.deduction_valuerate) / 100
                elif va.deduction_type == 'Fixed Amount':
                    self.deduction = int(va.deduction_valuerate)
                else:
                    self.deduction = 0
