from odoo import api, fields, models

# TODO (3.02): raising a ValidationError means importing it first:
#     from odoo.exceptions import ValidationError

# TODO (3.03): UserError comes from the same module, so one import line covers
# both: from odoo.exceptions import UserError, ValidationError

# TODO (3.04): Command joins the odoo import. Mind the order ruff wants —
# capitals sort first: from odoo import Command, api, fields, models


class LoanApplication(models.Model):
    _name = "loan.application"
    _description = "Loan Application"

    # TODO (3.06): mix the chatter into this model by adding _inherit alongside the
    # two lines above — keep _name, do not replace it:
    #
    #     _inherit = ["mail.thread", "mail.activity.mixin"]
    #
    # mail.thread brings the message history and followers; mail.activity.mixin
    # brings scheduled activities. Both are AbstractModels: they have no table of
    # their own, so nothing is copied at the database level, their fields and methods
    # are simply folded into this model. That is why they are called mixins, though
    # the mechanism is the same _name-plus-_inherit pairing you will use for real
    # prototype inheritance in the final task.
    #
    # The mail module is already in the dependency graph, through product, so the
    # manifest needs no change. Worth knowing that a module normally declares what it
    # uses directly rather than leaning on someone else's dependency — this one is
    # a deliberate shortcut, not the habit to take home.

    # Database-level constraints, written with the models.Constraint API that
    # replaced _sql_constraints in Odoo 19: a class attribute holding the SQL and
    # the message shown when it is violated. Postgres enforces them, so they hold
    # however the record was made — the form, an import, or the shell — which is
    # exactly what makes them worth having.
    _name_uniq = models.Constraint(
        "UNIQUE(name)",
        "Two applications cannot share the same reference.",
    )

    # TODO (3.02): a second one, following the example above: a CHECK that keeps
    # principal_amount strictly above zero. Nobody finances a motorcycle that costs
    # nothing, and a principal of zero would make the loan arithmetic meaningless.

    name = fields.Char(string="Application Number")

    loan_term = fields.Integer(string="Term (Months)", default=36)

    interest_rate = fields.Float(string="Interest Rate", required=True, digits=(5, 2))

    date_applied = fields.Date(
        string="Application Date", default=fields.Date.context_today
    )

    # No default on these two: they are stamped by the action methods when the
    # decision is actually taken, not when the record is created.
    date_approved = fields.Date(string="Approval Date")

    date_rejected = fields.Date(string="Rejection Date")

    # TODO (3.06): once the chatter is in place, add tracking=True to this field and
    # to principal_amount. Every change to a tracked field is then written into the
    # record's message history by itself, with the old and new values side by side.
    #
    # Only these two. Tracking every field turns the chatter into noise nobody reads,
    # which is worse than not having it: pick the ones somebody would be asked to
    # account for later.
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

    email = fields.Char(related="partner_id.email")
    
    phone = fields.Char(related="partner_id.phone")

    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )

    product_id = fields.Many2one(comodel_name="product.product", string="Motorcycle")

    currency_id = fields.Many2one(
        comodel_name="res.currency", default=lambda self: self.env.company.currency_id
    )

    # The full price of the motorcycle, and the figure the user actually types.
    # required here rather than on loan_amount: once loan_amount is derived it is
    # not something anyone can be asked to fill in, and a required column with
    # nothing writing to it only produces NOT NULL errors.
    principal_amount = fields.Monetary(
        string="Principal Amount", required=True, currency_field="currency_id"
    )

    loan_amount = fields.Monetary(currency_field="currency_id", compute="_compute_loan_amount", inverse="_inverse_loan_amount")

    down_payment = fields.Monetary(currency_field="currency_id")

    tag_ids = fields.Many2many(comodel_name="loan.application.tag", string="Tags")

    document_ids = fields.One2many(
        comodel_name="loan.application.document",
        inverse_name="application_id",
        string="Compliance Documents",
    )

    # ---------------------------------------------------------
    # COMPUTE / INVERSE METHODS
    # ---------------------------------------------------------

    @api.depends("principal_amount", "down_payment")
    def _compute_loan_amount(self):
        for application in self:
            application.loan_amount = application.principal_amount - application.down_payment

    def _inverse_loan_amount(self):
        for application in self:
            application.down_payment = application.principal_amount - application.loan_amount

    # ---------------------------------------------------------
    # CONSTRAINTS
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # ACTION METHODS
    # ---------------------------------------------------------

    # The three buttons in the form header call these methods by name. A method
    # behind a type="object" button takes no arguments beyond self, and whatever it
    # returns goes back to the web client — returning nothing simply reloads the
    # record, which is all a transition needs to do.
    #
    # action_approve_loan below is written out as the worked example. The other two
    # follow its shape: loop over self, skip any record that is not in the state the
    # transition starts from, then write the change.

    def action_approve_loan(self):
        """Worked example: the approval transition, start to finish."""
        for loan in self:
            if loan.state != "sent":
                continue
            # Both values in one write, deliberately. Each assignment would be a
            # write of its own with its own access check, and the Day 1 record rule
            # only lets group_kawiil_financing_user write to applications that are
            # not yet approved — so a second write arriving once the state is already
            # "approved" is refused for those users. Testing as an admin hides it:
            # rules from different groups are OR'd, and the admin rule lets it pass.
            loan.write(
                {
                    "state": "approved",
                    "date_approved": fields.Date.context_today(loan),
                }
            )

    # TODO (3.03): the other two transitions, following the method above.

    def action_reject_loan(self):
        # TODO (3.03): state to "rejected", date_rejected to today. Same shape as
        # action_approve_loan, including the single write.
        pass

    def action_submit(self):
        # TODO (3.03): the guard first, the state change second.
        #
        # Ask each line whether it counts, instead of reaching into the document type
        # from here — the document already knows:
        #
        #     required_docs = loan.document_ids.filtered(
        #         lambda doc: doc._is_required_for_submit()
        #     )
        #
        # Refuse with a UserError if there are none at all, and again if any of them
        # fails _is_valid_for_submit(). Wrap both messages in self.env._(), the same
        # call you used for the ValidationError at 3.02. It takes arguments too, so
        # self.env._("Document '%s' is not approved.", doc.name) stays translatable —
        # never build the sentence with an f-string, or the translation export sees a
        # different string every time.
        #
        # Only once that passes: state to "sent", and date_applied to today.
        # fields.Date.context_today(self) gives the user's today; fields.Date.today()
        # gives UTC's, which is a different day for some of them.
        #
        # TODO (3.06): once the chatter is in place, post a note here, straight after
        # the state changes:
        #
        #     loan.message_post(
        #         body=self.env._("Application successfully submitted for review!"),
        #         subtype_xmlid="mail.mt_note",
        #     )
        #
        # On loan, not on self: message_post writes to one record. mail.mt_note is
        # the internal-note subtype, so it lands in the history without emailing the
        # followers — leave it out and everyone following the record gets mail.
        pass

    # ---------------------------------------------------------
    # CRUD OVERRIDES
    # ---------------------------------------------------------

    # TODO (3.04): the compliance checklist should build itself. Nobody should have
    # to click "Add a line" five times to record the documents the dealership always
    # asks for.
    #
    # Two methods, deliberately kept apart: a helper that decides which document
    # types belong on a new application, and a create() override that turns them into
    # lines. Split that way, a module inheriting this one can change what lands on
    # the checklist by overriding the helper alone — the same reasoning that put
    # _is_required_for_submit() on the document rather than here.

    # TODO (3.04): this one needs a decorator. It runs before any record exists, so
    # there is no recordset for it to work on: add @api.model above it once `api` is
    # imported. The body is already written for you.

    def _get_default_document_types(self):
        """The document types that belong on a new application's checklist."""
        # search([]) already leaves out the archived types: the model has an `active`
        # field, and Odoo filters on it unless you tell it otherwise.
        return self.env["loan.application.document.type"].search([])

    # TODO (3.04): then the override itself. It is not stubbed here on purpose: a
    # create() that forgets to return super()'s result breaks every record creation
    # in the module, demo data included, so it is better written whole than left
    # half-finished. Write it as:
    #
    #     @api.model_create_multi
    #     def create(self, vals_list):
    #         ...
    #         return super().create(vals_list)
    #
    # Between those, for each vals dict in vals_list, turn each document type into a
    # line with Command.create({"type_id": doc_type.id}) and add the list to
    # vals["document_ids"]. Use vals.get("document_ids", []) + commands so that lines
    # somebody already filled in during creation survive.
    #
    # Command is the named form of the old "magic tuples" — Command.create(...)
    # instead of (0, 0, {...}). Import it only in the chapter you use it: an unused
    # import is an F401 and the Quality Gate will stop you.
