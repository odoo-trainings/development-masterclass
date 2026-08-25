# ODOP assignments 2.02, 2.03, 2.07 and 2.08 — the loan.application model.
#
# Fill in every field marked TODO, working through the sections in order. Each
# section starts with one field written out as a worked example — copy its
# shape for the rest.
#
# Two things to get right once the fields are done, or none of this will load:
#   models/__init__.py            must import this file.
#   kawiil_financing/__init__.py  must import the models folder.

from odoo import fields, models


class LoanApplication(models.Model):
    _name = "loan.application"
    _description = "Loan Application"


    name = fields.Char(string="Application Number")

    loan_term = fields.Integer(string="Term (Months)", default=36)

    interest_rate = fields.Float(string="Interest Rate", required=True, digits=(5, 2))

    date_applied = fields.Date(string="Application Date", default=fields.Date.context_today)

    state = fields.Selection(selection=[
        ("draft", "Draft"), 
        ("sent", "Sent"), 
        ("approved", "Approved"), 
        ("rejected", "Rejected"),], default="draft", copy=False)

    active = fields.Boolean(default=True)
    
    notes = fields.Html(string="Internal Notes", copy=False)
    
    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Customer", required=True
    )

    user_id = fields.Many2one(
        comodel_name="res.users", string="Salesperson", default=lambda self: self.env.user)

    product_id = fields.Many2one(
        comodel_name="product.product", string="Motorcycle")

    currency_id = fields.Many2one(
        comodel_name="res.currency", default=lambda self: self.env.company.currency_id)

    loan_amount = fields.Monetary(required=True, currency_field="currency_id")

    down_payment = fields.Monetary(currency_field="currency_id")

    tag_ids = fields.Many2many(comodel_name="loan.application.tag", string="Tags")
    
    document_ids = fields.One2many(comodel_name='loan.application.document', inverse_name='application_id', string='Compliance Documents')
