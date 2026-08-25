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
    
    # --- Assignment 2.03: links to the rest of Odoo ------------------------

    # Worked example. A Many2one holds a link to one record in another model.
    # comodel_name says which model, and Odoo stores the other record's
    # database id in a partner_id column.
    # partner_id = fields.Many2one(
    #    comodel_name="res.partner", string="Customer", required=True
    #)

    # TODO: user_id — Many2one to "res.users", labelled "Salesperson",
    #       defaulting to whoever is logged in. self.env.user is the current
    #       user, so: default=lambda self: self.env.user

    # TODO: product_id — Many2one to "product.product", labelled "Motorcycle".
    #       product.product is the variant, the record that actually gets sold
    #       and stocked. product.template is the abstract product above it.

    # TODO: currency_id — Many2one to "res.currency". A Monetary field cannot
    #       format an amount without knowing its currency, so give this one a
    #       default rather than leaving it empty:
    #       default=lambda self: self.env.company.currency_id

    # TODO: loan_amount — Monetary, required=True, with
    #       currency_field="currency_id".

    # TODO: down_payment — Monetary, with currency_field="currency_id".
    #
    #       Monetary is a Float that Odoo renders with a currency symbol and
    #       the right number of decimals. The field named in currency_field
    #       has to exist on this same model, which is why currency_id comes
    #       first.

    # --- Assignment 2.08: categorisation and compliance --------------------

    # Worked example. A Many2many links this record to many tags, and each tag
    # back to many loans. Odoo quietly creates the join table that makes that
    # work; you never touch it.
    # tag_ids = fields.Many2many(comodel_name="loan.application.tag", string="Tags")

    # TODO: document_ids — One2many to "loan.application.document", labelled
    #       "Documents". A One2many is not stored: it is the mirror image of a
    #       Many2one on the other model, so it has to be told which field over
    #       there points back here. That is the second argument,
    #       inverse_name="application_id".
