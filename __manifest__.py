{
    'name': 'Purchase Order Enhancement',
    'description' : 'Custom Purchase App',
    'author ' : 'Quân Bùi',
    'depends' : ['purchase'],
    'application' : True,
    'data' : [
        'security/purchase_security.xml',
        'views/purchase_views.xml',
        'views/purchase_assets.xml',
        'views/res_config_settings_views.xml',
        'wizard/purchase_archive_multiple_wizard_view.xml',
        'views/purchase_cron.xml',
        'views/purchase_order_template.xml',
    ],
}
