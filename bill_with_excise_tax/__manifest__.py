# -*- coding: utf-8 -*-
{
    "name": "MSR Vendor Bill Excise Tax",
    "version": "17.0.0.0",
    "category": "Invoicing",
    "sequence": 11,
    "summary": "Excise Tax In Vendor bill lines",
    "description": """Excise Tax in 
Vendor bill Lines
""",
    "author": "Ameen Bin Faizy",
    "depends": ["base", "account"],
    "data": [
        "views/account_account.xml",
        "views/res_config_settings.xml",
        "views/invoice_view.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
}
