# from erpnext.hr.doctype.employee_checkin.employee_checkin import EmployeeCheckin
import frappe
from erpnext.payroll.doctype.salary_slip.salary_slip import SalarySlip
from erpnext.hr.doctype.shift_assignment.shift_assignment import get_actual_start_end_datetime_of_shift
from frappe.model.document import Document
import datetime, math
from frappe.utils import now, cint, get_datetime ,getdate
from frappe.utils import add_days, cint, cstr, flt, getdate, rounded, date_diff, money_in_words, formatdate, get_first_day
from frappe import _


class overrid_salary_slip(SalarySlip):
	def get_working_days_details(self, joining_date=None, relieving_date=None, lwp=None, for_preview=0):
		payroll_based_on = frappe.db.get_value("Payroll Settings", None, "payroll_based_on")
		include_holidays_in_total_working_days = frappe.db.get_single_value("Payroll Settings", "include_holidays_in_total_working_days")

		working_days = date_diff(self.end_date, self.start_date) + 1
		if for_preview:
			self.total_working_days = working_days
			self.payment_days = working_days
			return

		holidays = self.get_holidays_for_employee(self.start_date, self.end_date)

		if not cint(include_holidays_in_total_working_days):
			working_days -= len(holidays)
			if working_days < 0:
				frappe.throw(_("There are more holidays than working days this month."))

		if not payroll_based_on:
			frappe.throw(_("Please set Payroll based on in Payroll settings"))

		if payroll_based_on == "Attendance":
			actual_lwp, absent = self.calculate_lwp_ppl_and_absent_days_based_on_attendance(holidays)
			self.absent_days = absent
			calculate_late_houres(self)
			self.forget_fingerprint=calculate_forget_fingerprints(self)
		else:
			actual_lwp = self.calculate_lwp_or_ppl_based_on_leave_application(holidays, working_days)

		if not lwp:
			lwp = actual_lwp
		elif lwp != actual_lwp:
			frappe.msgprint(_("Leave Without Pay does not match with approved {} records")
				.format(payroll_based_on))

		self.leave_without_pay = lwp
		self.total_working_days = working_days

		payment_days = self.get_payment_days(joining_date,
			relieving_date, include_holidays_in_total_working_days)

		if flt(payment_days) > flt(lwp):
			self.payment_days = flt(payment_days) - flt(lwp)

			if payroll_based_on == "Attendance":
				self.payment_days -= flt(absent)

			unmarked_days = self.get_unmarked_days(include_holidays_in_total_working_days)
# 			unmarked_days = self.get_unmarked_days()
			consider_unmarked_attendance_as = frappe.db.get_value("Payroll Settings", None, "consider_unmarked_attendance_as") or "Present"

			if payroll_based_on == "Attendance" and consider_unmarked_attendance_as =="Absent":
				self.absent_days += unmarked_days #will be treated as absent
				self.payment_days -= unmarked_days
				if include_holidays_in_total_working_days:
					for holiday in holidays:
						if not frappe.db.exists("Attendance", {"employee": self.employee, "attendance_date": holiday, "docstatus": 1 }):
							self.payment_days += 1
		else:
			self.payment_days = 0
		
def calculate_late_houres(doc):
    shift_type=fetch_shift(doc)
    # shift_type=doc.shift
    if not (shift_type):
        frappe.msgprint(_("This employee dose not have shift assignment active to determine the delay time"))
    attendances = frappe.db.sql('''
    SELECT attendance_date, status, leave_type ,  in_time
    FROM `tabAttendance`
    WHERE
    status = "Present" AND late_entry = 1
    AND employee = %s
    AND docstatus = 1
    AND attendance_date between %s and %s
    ''', values=(doc.employee, doc.start_date, doc.end_date), as_dict=1)
    total_minutes_delay = 0
    for t in attendances:
        shift_actual_timings = get_actual_start_end_datetime_of_shift(doc.employee, get_datetime(t.in_time), True)
        start = shift_actual_timings[2].start_datetime
        end =get_datetime(t.in_time)
        diff_time = end - start
        # print(diff_time)
        # if(diff_time.total_seconds() / 60 >= 6):
        total_minutes_delay += round(diff_time.total_seconds() / 60)
    doc.minutes_delay= total_minutes_delay 

def fetch_shift(self):
        shift_actual_timings = get_actual_start_end_datetime_of_shift(self.employee, get_datetime(self.start_date), True)
        if shift_actual_timings[2]:
            return (shift_actual_timings[2].shift_type.name)
        else:
            return ( None)
def calculate_forget_fingerprints(doc):
	total_number_of_forget_fingerprints= 40
	attendances = frappe.db.sql('''
    SELECT attendance_date, status, leave_type ,  in_time
    FROM `tabAttendance`
    WHERE
    (status = "Absent") AND (out_time is NULL) AND (in_time is not NULL)
    AND employee = %s
    AND docstatus = 1
    AND attendance_date between %s and %s
    ''', values=(doc.employee, doc.start_date, doc.end_date), as_dict=1)
	total_number_of_forget_fingerprints = len(attendances)
	return total_number_of_forget_fingerprints 
