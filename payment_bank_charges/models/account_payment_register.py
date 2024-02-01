from odoo import fields, models, api, _


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    bank_charges = fields.Monetary(
        compute="_compute_bank_charges",
        string="Bank Charges", readonly=True,
        help="Bank charge amount"
    )

    @api.depends('journal_id', 'journal_id.bank_charge_percent', 'amount')
    def _compute_bank_charges(self):
        for record in self:
            if record.amount and record.journal_id.bank_charge_percent:
                record.bank_charges = round((record.amount * record.journal_id.bank_charge_percent) / 100, 2)
            else:
                record.bank_charges = 0.0

    def _create_payment_vals_from_wizard(self, batch_result):
        res = super()._create_payment_vals_from_wizard(batch_result)
        res['bank_charges'] = self.bank_charges
        return res

    def _create_payment_vals_from_batch(self, batch_result):
        res = super()._create_payment_vals_from_batch(batch_result)
        res['bank_charges'] = self.bank_charges
        return res