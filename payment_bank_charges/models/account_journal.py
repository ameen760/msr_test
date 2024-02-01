from odoo import fields, models, api, _


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    bank_charge_percent = fields.Integer('Bank Charge %')
    bank_charge_account_id = fields.Many2one(
        comodel_name='account.account', check_company=True,
        domain="[('deprecated', '=', False), ('company_id', '=', company_id),]",
        string='Bank Charge Account', copy=False,
        help="This account is used as default bank charges account"
    )
