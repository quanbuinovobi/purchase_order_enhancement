import datetime

from odoo import api, fields, models
from odoo.exceptions import UserError, AccessError
import logging
# logging.warning(vals) => console.log

class PurchaseOrder(models.Model):
    # Inherit model
    _inherit = 'purchase.order'

    # Define fields (variables)
    active = fields.Boolean(
        'Active', default=True,
        help="If unchecked, it will allow you to hide the purchase order without removing it.")
    lifespan = fields.Integer(string="Life Span" ,default=1 ,store = True)

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
        logging.warning("THIS IS MY CRON")
        self._check_old_purchase_order()

    # Check archived purchase order status function
    def _check_archived_state(self, values):
        if 'active' in values:
            for order in self:
                logging.warning(order.state)
                if order.state not in ['cancel', 'done']:
                    raise UserError("Only 'Cancel' or 'Lock' Purchase Order is allowed ")

    def _check_archive_user_role(self, values):
        if 'active' in values :
            if not self.env.user.has_group('purchase.group_purchase_manager') :
                raise UserError("Only 'Manager' can archive Purchase Order ")

    def _check_old_purchase_order(self):
        logging.warning("HERE")
        current_date = fields.datetime.now()

        for order in self.search([]):
            write_date = order.write_date
            # If current date > write date + lifespan
            logging.warning("lifespan : " + str(order.lifespan))
            logging.warning(current_date > write_date + datetime.timedelta(minutes = order.lifespan))
            if current_date > write_date + datetime.timedelta(minutes = order.lifespan):
                if order.state in ['cancel', 'done'] and order.active == True:
                    logging.warning("RUN RUN RUN ")
                    order.active = False


