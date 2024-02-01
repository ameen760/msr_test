from odoo import fields, models, api, _


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    bank_charges = fields.Monetary(
        currency_field='currency_id', string="Bank Charges",
        readonly=True, help="Additional Bank charge amount",compute="_compute_bank_charges",
    )

    @api.depends('journal_id', 'journal_id.bank_charge_percent', 'amount')
    def _compute_bank_charges(self):
        for record in self:
            if record.amount and record.journal_id.bank_charge_percent != 0:
                record.bank_charges = round((record.amount * record.journal_id.bank_charge_percent) / 100, 2)
            else:
                record.bank_charges = 0.0


    def _prepare_move_line_default_vals(self, write_off_line_vals=None):
        res = super()._prepare_move_line_default_vals(write_off_line_vals=write_off_line_vals)
        if self.bank_charges:
            liquidity_line_name = ''.join( x[1] for x in self._get_liquidity_aml_display_name_list())
            bank_charges_line_name = liquidity_line_name.replace(str(("{:,}".format(self.amount))),
                                                                 str(self.bank_charges))
            bank_journal_line = [record for record in res if record.get('account_id') in
                                 self._get_valid_liquidity_accounts().ids]
            if self.payment_type == 'inbound':
                if bank_journal_line:
                    bank_line_name = liquidity_line_name.replace(str(("{:,}".format(self.amount))),
                                                                 str(bank_journal_line[0]['debit'] - self.bank_charges))
                    bank_journal_line[0].update({"debit": bank_journal_line[0]['debit'] - self.bank_charges,
                                                 "amount_currency": bank_journal_line[0]['amount_currency'] -
                                                                    self.bank_charges,
                                                 "name":bank_line_name,
                                                 })
                res.append({
                            'name': _('Bank charge on ') + bank_charges_line_name,
                            'partner_id': self.partner_id.id,
                            'journal_id': self.journal_id.id,
                            'account_id': self.journal_id.bank_charge_account_id.id,
                            'debit': self.bank_charges,
                            'credit': 0.0,
                        })
            else:
                if bank_journal_line:
                    bank_line_name = liquidity_line_name.replace(str(("{:,}".format(self.amount))),
                                                                 str(bank_journal_line[0]['debit'] - self.bank_charges))
                    bank_journal_line[0].update({"credit": bank_journal_line[0]['credit'] - self.bank_charges,
                                                 "amount_currency": bank_journal_line[0]['amount_currency'] +
                                                                    self.bank_charges,
                                                 "name":bank_line_name,
                                                 })
                res.append({
                            'name': _('Bank charge on ') + bank_charges_line_name,
                            'partner_id': self.partner_id.id,
                            'journal_id': self.journal_id.id,
                            'account_id': self.journal_id.bank_charge_account_id.id,
                            'credit': self.bank_charges,
                            'debit': 0.0,
                        })
        return res
