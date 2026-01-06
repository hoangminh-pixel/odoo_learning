{
    'name': 'Module Demo',
    'version': '1.0',
    'summary': 'Demo module học Odoo',
    'category': 'Training',
    'author': 'Demo',
    'depends': ['base', 'web'],
    'data': [
        'data/data.xml',
        'security/ir.model.access.csv',
        'views/course_views.xml',
        'views/test_views.xml',
        'views/menu.xml',

    ],
    'demo': [
        'data/demo.xml',
    ],
    'assets': {
      #   'web.assets_backend': [
      #       'training_demo/static/src/css/style.css',
      #       'training_demo/static/src/js/main.js',
      #   ],
    },
    'application': True,
    'installable': True,
}
