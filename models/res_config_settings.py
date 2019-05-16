from odoo import fields, api, models
from logging import warning

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    # _name = 'purchase.order.enhancement.config.settings'

    lifespan_title = fields.Boolean(string="Config lifespan", default=False)
    lifespan = fields.Integer(string="Lifespan", default=3)
    lifespan_unit = fields.Selection(
        [
            ('seconds', 'Seconds'),
            ('minutes', 'Minutes'),
            ('hours', 'Hours'),
            ('days', 'Days'),
            ('months', 'Months'),
            ('years', 'Years'),
        ], string="Unit", default="months",
        help='Lifespan unit '
    )

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            lifespan=int(self.env['ir.config_parameter'].sudo().get_param('purchase.order.lifespan')),
            lifespan_unit=self.env['ir.config_parameter'].sudo().get_param('purchase.order.lifespan_unit')
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()

        # Set values to global variables
        self.env['ir.config_parameter'].sudo().set_param('purchase.order.lifespan', int(self.lifespan))
        self.env['ir.config_parameter'].sudo().set_param('purchase.order.lifespan_unit', self.lifespan_unit)

