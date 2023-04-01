# -*- coding: utf-8 -*-
# Copyright (c) 2023, ARD and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import datetime, math
from frappe.utils import now, cint, get_datetime ,getdate
from frappe.model.document import Document
from frappe import _

class exitpermit(Document):
    # pass
	def before_validate(self):
		start = get_datetime(self.from_time)
		end = get_datetime(self.to_time)
		diff = end - start
		if diff.total_seconds() <= 0:
			frappe.throw(_("From time must be greater than to time"))
		else:
			self.duration = round( diff.total_seconds() / 3600 , 2)
		
