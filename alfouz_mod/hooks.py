from . import __version__ as app_version

app_name = "alfouz_mod"
app_title = "Alfouz Mod"
app_publisher = "ARD"
app_description = "Alfouz Customization"
app_icon = "octicon octicon-file-directory"
app_color = "green"
app_email = "ard.ly"
app_license = "Copyright"


fixtures = ['Custom Field' , 'Translation']


# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/alfouz_mod/css/alfouz_mod.css"
# app_include_js = "/assets/alfouz_mod/js/alfouz_mod.js"

# include js, css files in header of web template
# web_include_css = "/assets/alfouz_mod/css/alfouz_mod.css"
# web_include_js = "/assets/alfouz_mod/js/alfouz_mod.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "alfouz_mod/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# "Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "alfouz_mod.install.before_install"
# after_install = "alfouz_mod.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "alfouz_mod.uninstall.before_uninstall"
# after_uninstall = "alfouz_mod.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "alfouz_mod.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# "Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# "Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
# "ToDo": "custom_app.overrides.CustomToDo"
# "Employee": "alfouz_mod.overrides.Employee"
"Salary Slip":"alfouz_mod.overrid_salary_slip.overrid_salary_slip",
"Shift Type":"alfouz_mod.overrid_shift_type.overrid_shift_type"
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
# "*": {
"on_update": "alfouz_mod.emp_working_years.recalculate_years_of_work",
# # "on_cancel": "method",
# # "on_trash": "method"
}
# }
# doc_events = {
#     "Salary Slip" :{
#     "validate": "alfouz_mod.salary.calculate_late_houres"
#     }
#     }
# Scheduled Tasks
# ---------------

scheduler_events = {
    "cron":{
        "0 0 1 1 *": [
            "alfouz_mod.emp_working_years.recalculate_years_of_work"
        ]
    },
#     # "all": [
#     # "alfouz_mod.tasks.all"
#     # ],
#     # "daily": [
#     #     "alfouz_mod.emp_working_years.recalculate_years_of_work"
#     # ],
#     # "hourly": [
#     # "alfouz_mod.tasks.hourly"
#     # ],
#     # "weekly": [
#     # "alfouz_mod.tasks.weekly"
#     # ]
#     # "monthly": [
#     # "alfouz_mod.tasks.monthly"
#     # ]
}

# Testing
# -------

# before_tests = "alfouz_mod.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# "frappe.desk.doctype.event.event.get_events": "alfouz_mod.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# "Task": "alfouz_mod.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
    {
        "doctype": "{doctype_1}",
        "filter_by": "{filter_by}",
        "redact_fields": ["{field_1}", "{field_2}"],
        "partial": 1,
    },
    {
        "doctype": "{doctype_2}",
        "filter_by": "{filter_by}",
        "partial": 1,
    },
    {
        "doctype": "{doctype_3}",
        "strict": False,
    },
    {
        "doctype": "{doctype_4}"
    }
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# "alfouz_mod.auth.validate"
# ]
