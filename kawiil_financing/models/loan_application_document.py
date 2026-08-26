from odoo import fields, models


class LoanApplicationDocument(models.Model):
    _name = "loan.application.document"
    _description = "Loan Application Document"

    name = fields.Char(string='Reference/Notes')
    state = fields.Selection([
        ('new', 'New'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Status', default='new', required=True)
    
    # Links to the configuration table
    type_id = fields.Many2one(comodel_name='loan.application.document.type', string='Document Type', required=True)
    
    # The crucial foreign key that links this line back to the parent Loan
    application_id = fields.Many2one(comodel_name='loan.application', string='Application', 
                                     ondelete='cascade' # If the loan is deleted, delete these lines too
    )
    
    # Links to Odoo's native attachment model to handle actual file uploads
    attachment_id = fields.Many2one(comodel_name='ir.attachment', string='File')
