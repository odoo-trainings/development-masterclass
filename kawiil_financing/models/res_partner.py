from odoo import api, fields, models


class ResPartner(models.Model):
    # Extension inheritance: _inherit on its own, with no _name, adds to the model
    # that already exists instead of declaring a new one. Everything below lands on
    # res.partner itself, next to what base and every other installed module put
    # there. No table is created and no data is copied.
    _inherit = "res.partner"

    # The other side of loan.application.partner_id. Archived applications drop out
    # on their own, so this holds the live requests only.
    loan_application_ids = fields.One2many(
        comodel_name="loan.application",
        inverse_name="partner_id",
        string="Loan Applications",
    )

    loan_application_count = fields.Integer(
        string="Loan Applications",
        compute="_compute_loan_application_count",
    )

    @api.depends("loan_application_ids")
    def _compute_loan_application_count(self):
        for partner in self:
            partner.loan_application_count = len(partner.loan_application_ids)

    # TODO (3.05): the method the smart button calls.
    #
    # Start with self.ensure_one(). A button hands you the record it sits on, but
    # nothing stops the method being called on several at once, and self.id on a
    # multi-record set raises a confusing error much further along.
    #
    # Then return a dictionary describing a window action, which the web client
    # carries out. The keys that matter here:
    #
    #   "type"       "ir.actions.act_window"
    #   "name"       the title of the view that opens, through self.env._()
    #   "res_model"  the model to open
    #   "view_mode"  "list,form"
    #   "domain"     narrow it to this partner's applications
    #   "context"    set default_partner_id, so that creating a record from the
    #                list it opens starts with the customer already filled in
    #
    # A default_* key in the context is how Odoo pre-fills a field on a new record.
    # That is what makes the last UAT step work.

    def action_view_loan_applications(self):
        # TODO (3.05): return the window action described above.
        pass
