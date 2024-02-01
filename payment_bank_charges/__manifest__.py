{
    'name': 'MSR Bank charges in Payment',
    'version': '17.0.0',
    'category': 'Accounting',
    'description': """
Add Bank charges in Payment and Register payment:

* Based on particular percetage configured in bank journal
    """,
    'author': 'Ameen Bin faizy',
    'website': '',
    'depends': ['account'],
    'data': [
        'views/account_journal.xml',
        'views/account_payment_register_views.xml',
        'views/account_payment.xml',
    ],
    'license': 'LGPL-3',
}
