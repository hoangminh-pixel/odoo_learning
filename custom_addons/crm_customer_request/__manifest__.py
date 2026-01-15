{
    'name': 'CRM Customer Request',
    'version': '1.0.0',
    'depends': ['crm', 'product', 'sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead_views.xml',
        'views/crm_customer_request_views.xml',
        'views/crm_customer_request_details.xml',
        'views/menu.xml',
    ],
    'application': True,
    'installable': True,
}
