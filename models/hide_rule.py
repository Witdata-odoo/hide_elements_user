from odoo import models, fields

class HideElementsRule(models.Model):
    _name = 'hide.elements.rule'
    _description = 'Rules for Hiding Elements from Users'

    name = fields.Char(string='Description', required=True)
    model_id = fields.Many2one('ir.model', string='Model', required=True, ondelete='cascade')
    user_ids = fields.Many2many('res.users', string='Restricted Users')
    
    company_ids = fields.Many2many('res.company', string='Company', 
                                 default=lambda self: self.env.company,
                                 help='Leave blank to apply to all companies.')
    
    restriction_type = fields.Selection([
        ('readonly', 'Read-Only Form (Hides Create/Edit/Delete)'),
        ('hide_button', 'Hide Specific Button'),
    ], string='Type of Restriction', required=True, default='hide_button')
    
    element_name = fields.Char(string='Technical Name of the Button')
    
    condition = fields.Char(string='Condition for Hiding (Optional)', 
                            help="Example for Supplier Payments: payment_type == 'outbound'")