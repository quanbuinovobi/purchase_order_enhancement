from odoo import http

class PurchasePortal(http.Controller):

    @http.route('purchase/archive', type='json', auth='public')
    def archiveController(self, fields):
        print(fields)
        return http.request.render(
            'purchase_order_enhance.purchase_order_template', {'fields': fields})