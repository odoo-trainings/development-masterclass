# TODO (3.01): the compute method you write below is decorated with
# @api.depends, so `api` has to join this import.
from odoo import fields, models

# TODO (3.02): raising a ValidationError means importing it first:
#     from odoo.exceptions import ValidationError

# TODO (3.03): UserError comes from the same module, so one import line covers
# both: from odoo.exceptions import UserError, ValidationError


class LoanApplication(models.Model):
    _name = "loan.application"
    _description = "Loan Application"

    # TODO (3.02): two database-level constraints, written with the
    # models.Constraint API that replaced _sql_constraints in Odoo 19. Each is a
    # class attribute holding the SQL and the message shown when it is violated:
    #
    #     _<name> = models.Constraint(
    #         "<SQL definition>",
    #         "<message the user sees>",
    #     )
    #
    # Add a UNIQUE one that stops two applications sharing the same name, and a
    # CHECK one keeping principal_amount strictly above zero. Postgres enforces
    # both, so they hold however the record was made — the form, an import, or the
    # shell — which is exactly what makes them worth having.

    name = fields.Char(string="Application Number")

    loan_term = fields.Integer(string="Term (Months)", default=36)

    interest_rate = fields.Float(string="Interest Rate", required=True, digits=(5, 2))

    date_applied = fields.Date(
        string="Application Date", default=fields.Date.context_today
    )

    # TODO (3.03): add `date_approved` and `date_rejected`, both Date fields, so the
    # workflow leaves a trail of when each decision was taken. No default — they are
    # stamped by the action methods, not at creation.

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("sent", "Sent"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        default="draft",
        copy=False,
    )

    active = fields.Boolean(default=True)

    notes = fields.Html(string="Internal Notes", copy=False)

    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Customer", required=True
    )

    # TODO (3.01): add two related fields that pull the customer's contact details
    # onto this form: `email` from the partner's email, `phone` from the partner's
    # phone. Both are Char. A related field is a computed field underneath, so
    # leave the defaults alone — read-only, and not stored in the database.

    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )

    product_id = fields.Many2one(comodel_name="product.product", string="Motorcycle")

    currency_id = fields.Many2one(
        comodel_name="res.currency", default=lambda self: self.env.company.currency_id
    )

    # TODO (3.01): add `principal_amount`, a Monetary field holding the full price
    # of the motorcycle, next to the two fields below.

    # TODO (3.01): loan_amount stops being a figure anyone types in.
    #   - compute it from principal_amount - down_payment, in a method that
    #     iterates explicitly with `for record in self:`
    #   - decorate that method with @api.depends on both source fields
    #   - give the field an inverse method as well, so that typing a loan_amount
    #     works the deposit back out: down_payment = principal_amount - loan_amount
    #   - move required=True off this field and onto principal_amount. A derived
    #     figure is not something the user can be asked to fill in.
    # Two things to expect once it is computed: a computed field is read-only
    # unless it declares an inverse, and an unstored one cannot be searched or
    # sorted, so COMMANDS.md's search([("loan_amount", ">", 10000)]) snippet stops
    # working and the list view column stops sorting. store=True, or a search=
    # method, brings those back.
    loan_amount = fields.Monetary(required=True, currency_field="currency_id")

    down_payment = fields.Monetary(currency_field="currency_id")

    tag_ids = fields.Many2many(comodel_name="loan.application.tag", string="Tags")

    document_ids = fields.One2many(
        comodel_name="loan.application.document",
        inverse_name="application_id",
        string="Compliance Documents",
    )

    # TODO (3.01): the two methods behind loan_amount. The names are not free
    # choices — they are the strings you pass to compute= and inverse= on the
    # field, and the quality gate expects a compute method to start with
    # `_compute_`.
    #
    # _compute_loan_amount also needs a decorator, once `api` is imported:
    #     @api.depends("principal_amount", "down_payment")
    # Leave it off and the field is computed once and never refreshed again.

    def _compute_loan_amount(self):
        # TODO (3.01): loan_amount = principal_amount - down_payment, assigned one
        # record at a time with `for record in self:`.
        pass

    def _inverse_loan_amount(self):
        # TODO (3.01): the same arithmetic rearranged. Odoo calls this on save for
        # the records whose loan_amount was typed in by hand, and principal_amount
        # is the figure that stays put:
        #     down_payment = principal_amount - loan_amount
        pass

    # Optional (3.01) — how to make loan_amount searchable again.
    #
    # An unstored computed field has no column behind it, so a domain cannot reach
    # it and search([("loan_amount", ">", 10000)]) raises. Either store the field,
    # or give it a search method: Odoo hands you the operator and the value out of
    # the domain, and you hand back a domain it can actually run.
    #
    # Wire it onto the field:
    #
    #     loan_amount = fields.Monetary(
    #         compute="_compute_loan_amount",
    #         inverse="_inverse_loan_amount",
    #         search="_search_loan_amount",
    #         currency_field="currency_id",
    #     )
    #
    # def _search_loan_amount(self, operator, value):
    #     # Domains cannot do arithmetic, so the sum is worked out in Python and
    #     # the answer handed back as a plain list of ids. search([]) is safe
    #     # here: an empty domain never reads loan_amount, so this cannot recurse.
    #     applications = self.search([])
    #     matching = applications.filtered_domain([("loan_amount", operator, value)])
    #     return [("id", "in", matching.ids)]
    #
    # Note what it costs: every application is loaded to answer one filter. That is
    # the price of searching a field the database cannot see, and it is why
    # store=True is usually the better answer when the arithmetic is this simple.

    # TODO (3.02): a Python constraint, for the rule SQL is the wrong tool for: a
    # customer cannot put down a deposit as large as the motorcycle itself.
    #
    # Decorate the method with @api.constrains("principal_amount", "down_payment")
    # so Odoo re-runs it whenever either field is written. Note the difference from
    # the SQL constraints above: this one only fires on writes that go through the
    # ORM, and it can say something specific about what went wrong.

    def _check_down_payment(self):
        # TODO (3.02): loop over self, and raise ValidationError where down_payment
        # is greater than or equal to principal_amount. Wrap the message in
        # self.env._("...") so it can be exported to the translation files — that
        # is the Odoo 19 idiom, and it replaces the older `from odoo import _`.
        pass

    # TODO (3.03): the three buttons in the form header call these by name. A method
    # behind a type="object" button takes no arguments beyond self, and whatever it
    # returns is handed back to the web client — returning nothing simply reloads
    # the record, which is all these need to do.

    def action_submit(self):
        # TODO (3.03): the guard first, the state change second.
        #
        # Pull the mandatory documents out of document_ids with filtered(), keyed on
        # the document type: type_id.is_required. Note the field name — the task
        # sheet calls it is_mandatory, but the model defines `is_required`.
        #
        # Refuse the submission with a UserError if there are no mandatory documents
        # at all, or if any of them is not yet in the "approved" state. Wrap the
        # message in self.env._() exactly as you did for the ValidationError at 3.02.
        #
        # Only once that passes: state to "sent", date_applied to today
        # (fields.Date.context_today(self) gives you the user's today, not UTC's).
        pass

    def action_approve_loan(self):
        # TODO (3.03): state to "approved", date_approved to today.
        #
        # Write both in one go — self.write({...}) — rather than as two separate
        # assignments. The Day 1 record rule only lets the financing *user* group
        # write to applications that are not yet approved, so a second write landing
        # after the state is already "approved" can be refused for those users.
        pass

    def action_reject_loan(self):
        # TODO (3.03): state to "rejected", date_rejected to today.
        pass
