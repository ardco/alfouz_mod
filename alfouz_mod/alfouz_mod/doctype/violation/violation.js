// Copyright (c) 2023, ARD and contributors
// For license information, please see license.txt

frappe.ui.form.on('Violation', {
	refresh: function (frm) {
		// frm.toggle_reqd('duration_of_the_violation', frm.doc.add_duration_for_violation)
		// frm.set_value('override_deduction', 0)
		if(frm.is_new() && frm.is_dirty() || frm.is_new()){
			frm.toggle_display('override_deduction', 0)
		}
	},
	validate: function (frm) {
		// frappe.call({
		// 		"method": "complement.complement.tools.get_daily_rate",
		// 		args: {
		//             employee: frm.doc.employee,
		//             start_date: frappe.datetime.month_start(frm.doc.posting_date),
		// 						end_date:frappe.datetime.month_end(frm.doc.posting_date)
		//         },

		// 		callback: function (data) {
		// 			console.log(data);
		// 		}
		// });
	},
	violation_category: function (frm) {
		if (!frm.doc.violation_category) {
			frm.set_value('violation_type', null);
		}
	},
	// add_duration_for_violation: function(frm){
	// 	frm.toggle_reqd('duration_of_the_violation', frm.doc.add_duration_for_violation)
	// },
	override_deduction: function (frm) {
		frm.toggle_enable('deduction', frm.doc.override_deduction)
	},
	before_save: function (frm) {
		frm.set_value('override_deduction', 0)
	},
	after_save: function(frm){
		frm.toggle_display('override_deduction', 1)
	}
});
cur_frm.fields_dict['violation_type'].get_query = function (doc) {
	return {
		filters: {
			"violation_category": cur_frm.get_field('violation_category').get_value()
		}
	}
}
