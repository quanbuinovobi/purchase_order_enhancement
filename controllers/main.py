from odoo import http
from odoo.http import request
from odoo.exceptions import UserError, AccessError

import logging


class PurchasePortal(http.Controller):

    @http.route('/purchase/archive', type='json', auth='public')
    def archiveController(self, *args, **kwargs):

        if 'method' not in kwargs or 'orders' not in kwargs:
            return PurchasePortal.badRequest()
        elif kwargs.get('method') != "archive":
            return PurchasePortal.badRequest()

        for x in kwargs.get('orders'):
            if not str(x).isdigit():
                return PurchasePortal.badRequest()

        purchase_order_ids = kwargs.get('orders')

        # Search purchase order with the list of po_ids
        orders = request.env['purchase.order'].browse(purchase_order_ids).sudo()

        for order in orders:
            try:
                # Reject if state is not 'cancel' and 'done'
                if order.state not in ['cancel', 'done']:
                    PurchasePortal.purchaseOrderNotFound()
                # Change 'active' value
                order.active = not order.active
            except:
                return PurchasePortal.purchaseOrderNotFound()

        return PurchasePortal.purchaseOrderFound(purchase_order_ids)

    @staticmethod
    def badRequest():
        return {
            "code": 400,
            "message": "Bad Request"
        }

    @staticmethod
    def purchaseOrderNotFound():
        return {
            "archived_orders": 'False',
            "code": 404,
            "message": "Could not found"
        }

    @staticmethod
    def purchaseOrderFound(list_order_archive):
        return {
            "archived_orders": list_order_archive,
            "code": 200,
            "message": "Successful"
        }


