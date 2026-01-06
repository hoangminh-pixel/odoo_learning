# sale_demo/utils/response.py

import json
from odoo.http import Response

def success(data=None, status=200):
    return Response(
        json.dumps({
            'success': True,
            'data': data
        }, default=str),   # 👈 tránh lỗi date
        status=status,
        mimetype='application/json'
    )

def error(code, message, status=400):
    return Response(
        json.dumps({
            'success': False,
            'error': {
                'code': code,
                'message': message
            }
        }),
        status=status,
        mimetype='application/json'
    )
