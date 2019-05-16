from odoo import models, fields, api
from odoo.exceptions import UserError, AccessError
import logging

class archiveMultiplePurchaseOrder(models.TransientModel):
    _name = 'purchase.archive.multiple.wizard'
    _description = "Archive multiple purchase order wizard"

    purchase_order_ids = fields.Many2many(
            'purchase.order',
            string=""
            )
    # name = fields.Char(required=True, index=True, copy=False)
    active = fields.Boolean(
        'Active', default=True,
        help="If unchecked, it will allow you to hide the purchase order without removing it.")
    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', track_visibility='onchange')

    @api.model
    def default_get(self, field_names):
        defaults = super().default_get(field_names)
        purchase_order_ids = self.env.context['active_ids']
        logging.warning(purchase_order_ids)

        # Raise error when purchase orders are not done and cancel
        self._check_purchase_order_state(purchase_order_ids)

        defaults['purchase_order_ids'] = purchase_order_ids
        return defaults

    # Note : button_archive_multiple run two times
    @api.multi
    def button_archive_multiple(self):
        self.ensure_one()
        for order in self.with_context(active_test=False).purchase_order_ids:
            order.active = not order.active

    def _check_purchase_order_state(self, purchase_order_ids):
        orders = self.env['purchase.order'].browse(purchase_order_ids)
        for order in orders:
            if order.state not in ['done', 'cancel']:
                raise UserError("Only 'Cancel' or 'Lock' Purchase Order is allowed ")