from odoo import api, fields, models
from odoo.exceptions import UserError, AccessError
import logging
# logging.warning(vals) => console.log

class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    active = fields.Boolean(
        'Active', default=True,
        help="If unchecked, it will allow you to hide the purchase order without removing it.")

    @api.multi
    def action_toggle_active(self):
        for order in self:
            logging.warning(order.state)
            if order.state not in ['cancel', 'done']:
                raise UserError("Only 'Cancel' or 'Lock' Purchase Order is allowed ")
            else:
                order.active = not order.active

    @api.multi
    def write(self, values):
        if 'active' in values:
            for order in self:
                logging.warning(order.state)
                if order.state not in ['cancel', 'done']:
                    raise UserError("Only 'Cancel' or 'Lock' Purchase Order is allowed ")
                # else:
                #     order.active = not order.active

        return super().write(values)
