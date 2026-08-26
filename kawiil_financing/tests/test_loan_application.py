# TODO (3.07): the two exceptions your tests assert on come from the same place:
#     from odoo.exceptions import UserError, ValidationError
from odoo.tests import TransactionCase


class TestLoanApplication(TransactionCase):
    """Tests for the loan application's computes, constraints and workflow."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # setUpClass runs once for the whole class, and everything it touches is
        # rolled back when the class finishes. Records made here are shared by every
        # test below and cost one round of database work; the same code in setUp
        # would run again before each test. That is the whole reason to prefer it.
        cls.partner = cls.env["res.partner"].create({"name": "Test Rider"})
        cls.document_type = cls.env["loan.application.document.type"].create(
            {
                "name": "Test Proof of Identity",
                "is_required": True,
            }
        )

    # TODO (3.07): create an application for cls.partner with a principal of 10000
    # and a down payment of 2000, then assert two things about it:
    #
    #   - assertEqual that loan_amount computed to 8000, which is the arithmetic you
    #     wrote at 3.01
    #   - assertTrue that document_ids is not empty, which proves the create override
    #     from 3.04 built the checklist out of the document type made above
    #
    # Leave `name` out of the values. The unique constraint from 3.02 would collide
    # if every test used the same reference, and Postgres is happy with repeated
    # NULLs.

    def test_01_computes_and_crud(self):
        # TODO (3.07): write the test described above.
        pass

    # TODO (3.07): prove the constraint from 3.02 refuses a down payment that is
    # larger than the principal — try 10000 down against a principal of 5000, inside
    # a `with self.assertRaises(ValidationError):` block.
    #
    # Wrapping the create() call is enough: Odoo validates @api.constrains as part of
    # creating the record, so the error is raised before create() returns. You do not
    # need to flush anything by hand.

    def test_02_python_constraints(self):
        # TODO (3.07): write the test described above.
        pass

    # TODO (3.07): prove the guard in action_submit refuses an application whose
    # checklist is not settled.
    #
    # Create a valid draft application, leave its documents exactly as create() made
    # them — new, not approved — and call action_submit() inside a
    # `with self.assertRaises(UserError):` block.
    #
    # Note which exception this is. The constraint above raises ValidationError
    # because it is a rule about the data; this one raises UserError because it is a
    # rule about what someone is allowed to do next. Asserting the wrong one passes
    # for the wrong reason.

    def test_03_workflow_user_error(self):
        # TODO (3.07): write the test described above.
        pass
