# TODO (3.05): drop the noqa once the class below exists and uses these imports.
from odoo import api, fields, models  # noqa: F401

# Nothing in this file is written for you, on purpose: the declaration is the lesson.
#
# TODO (3.05): extend res.partner. Extension inheritance is one line inside a class:
#
#     class ResPartner(models.Model):
#         _inherit = "res.partner"
#
# _inherit on its own, with no _name, means "do not declare a new model, add to the
# one that already exists". No table is created and no data is copied. Everything you
# write in that class lands on res.partner itself, next to what base and every other
# installed module put there — which is why a dozen modules can each add their own
# fields to a contact without any of them knowing about the others.
#
# Add _name as well and you get something quite different: a new model that copies
# res.partner's definition and goes its own way. That is prototype inheritance, and
# it is what the final task uses. Here you want extension.
#
# In the class, add:
#
#   loan_application_ids    One2many back to loan.application, inverse partner_id.
#                           Archived applications drop out on their own, so this
#                           holds the live requests only.
#   loan_application_count  Integer, computed. Put the compute method beside it,
#                           decorated with @api.depends on the One2many, looping
#                           `for partner in self:` and assigning len() of it.
#   action_view_loan_applications   the smart button's method, described below.

# TODO (3.05): inheritance also adjusts what is already there. Redeclare a field that
# base already defines and only the attributes you name change — the rest stay as
# base set them. Do it to phone, the number your loan form has been showing since
# 3.01, by adding this line to your class:
#
#     phone = fields.Char(help="Best number for questions about a loan application.")
#
# Hover the field label on any contact afterwards and the tooltip is yours. The mail
# module does the very same thing to the very same field, adding tracking=2 to it.
# Yours does not replace that: each module contributes its attributes and the field
# ends up carrying all of them.

# TODO (3.05): the method the smart button calls.
#
# Start with self.ensure_one(). A button hands you the record it sits on, but nothing
# stops the method being called on several at once, and self.id on a multi-record set
# fails much further along, where the error makes no sense.
#
# Then return a dictionary describing a window action, which the web client carries
# out. The keys that matter here:
#
#   "type"       "ir.actions.act_window"
#   "name"       the title of the view that opens, through self.env._()
#   "res_model"  the model to open
#   "view_mode"  "list,form"
#   "domain"     narrow it to this partner's applications
#   "context"    set default_partner_id, so creating a record from the list that
#                opens starts with the customer already filled in
#
# A default_* key in the context is how Odoo pre-fills a field on a new record. That
# is what makes the last UAT step work.
