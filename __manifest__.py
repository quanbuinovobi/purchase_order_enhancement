{
    'name': 'Purchase Order Enhancement',
    'description' : 'Custom Purchase App',
    'author ' : 'Quân Bùi',
    'depends' : ['purchase'],
    'application' : True,
    'data' : [
        'security/purchase_security.xml',
        'views/purchase_views.xml',
        'views/purchase_order_template.xml',
    ],
}