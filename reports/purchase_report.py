from odoo import fields, api, models, tools
from logging import warning

class PurchaseReport(models.Model):
    _inherit = "purchase.report"
    _description = "Purchase Report extend Payment Term"

    payment_term_id = fields.Many2one('account.payment.term', 'Payment Terms', readonly='true')

    def _select(self):
        return super(PurchaseReport, self)._select() + """,
            s.payment_term_id as payment_term_id"""

    def _group_by(self):
        return super(PurchaseReport, self)._group_by() + """,
            s.payment_term_id
        """