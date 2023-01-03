# Copyright (c) 2023, ARD and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

import collections


class ViolationType(Document):
    def validate(self):
        if self.duration_of_the_violation <= 0:
            frappe.throw("Duration Can not be requla or less than 0")

        for va in self.violation_action:
            if va.frequency <= 0:
                frappe.throw('Frequencies Must Be > 0')

        duplicated = [item for item,
                      count in collections.Counter([va.frequency for va in self.violation_action]).items() if count > 1]
        if duplicated:
            frappe.throw('Duplicated Frequencies Not Allowed')
