import datetime

from odoo import api, fields, models
from odoo.exceptions import UserError, AccessError
from logging import warning
# logging.warning(vals) => console.log

class PurchaseOrder(models.Model):
    # Inherit model
    _inherit = 'purchase.order'

    # Define fields (variables)
    active = fields.Boolean(
        'Active', default=True,
        help="If unchecked, it will allow you to hide the purchase order without removing it.")

    # @api.multi
    # def action_toggle_active(self):
    #     for order in self:
    #         logging.warning(order.state)
    #         if order.state not in ['cancel', 'done']:
    #             raise UserError("Only 'Cancel' or 'Lock' Purchase Order is allowed ")
    #         else:
    #             order.active = not order.active

    @api.multi
    def write(self, values):
        # Check archived purchase order status
        self._check_archived_state(values)

        # Check user group
        self._check_archive_user_role(values)

        return super().write(values)

    @api.model
    def archive_purchase_order(self):
        warning("THIS IS MY CRON")
        self._check_old_purchase_order()

    # Check archived purchase order status function
    def _check_archived_state(self, values):
        if 'active' in values:
            for order in self:
                warning(order.state)
                if order.state not in ['cancel', 'done']:
                    raise UserError("Only 'Cancel' or 'Lock' Purchase Order is allowed ")

    def _check_archive_user_role(self, values):
        if 'active' in values :
            if not self.env.user.has_group('purchase.group_purchase_manager') :
                raise UserError("Only 'Manager' can archive Purchase Order ")

    def _check_old_purchase_order(self):
        current_date = fields.datetime.now()

        for order in self.search([]):
            write_date = order.write_date

            # Get life span from global data
            lifespan = int(self.env['ir.config_parameter'].sudo().get_param('purchase.order.lifespan'))
            lifespan_unit = self.env['ir.config_parameter'].sudo().get_param('purchase.order.lifespan_unit')

            # Convert lifespan_unit from string to variable
            timestamp = str(lifespan_unit) + "=" + str(lifespan)

            # If current date > write date + lifespan
            if current_date > write_date + eval("datetime.timedelta(" + str(timestamp) + ")") :
                if order.state in ['cancel', 'done'] and order.active == True:
                    order.active = False


