{
    'name': 'Sale Demo',
    'version': '1.0',
    'summary': 'Module đơn hàng học tập',
    'author': 'You',
    'category': 'Training',
    'depends': ['base','web'],
    'data': [
        'security/ir.model.access.csv',
        'views/order_view.xml',
        # 'views/menu.xml'
    ],
    'application': True,
    'installable': True,
}
