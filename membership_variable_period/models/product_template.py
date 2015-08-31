# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields, api
from datetime import timedelta
from dateutil.relativedelta import relativedelta


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _get_next_date(self, date):
        """Get the date that results on incrementing given date an interval of
        time in time unit.
        @param date: Original date.
        @param unit: Interval time unit.
        @param interval: Quantity of the time unit.
        @rtype: date
        @return: The date incremented in 'interval' units of 'unit'.
        """
        if isinstance(date, str):
            date = fields.Date.from_string(date)
        if self.membership_interval_unit == 'days':
            return date + timedelta(days=self.membership_interval_qty)
        elif self.membership_interval_unit == 'weeks':
            return date + timedelta(weeks=self.membership_interval_qty)
        elif self.membership_interval_unit == 'months':
            return date + relativedelta(months=self.membership_interval_qty)
        elif self.membership_interval_unit == 'years':
            return date + relativedelta(years=self.membership_interval_qty)

    membership_type = fields.Selection(
        selection=[('fixed', 'Fixed dates'),
                   ('variable', 'Variable periods')],
        default='fixed', string="Membership type", required=True)
    membership_interval_qty = fields.Integer(
        string="Interval quantity", default=1)
    membership_interval_unit = fields.Selection(
        selection=[('days', 'days'),
                   ('weeks', 'weeks'),
                   ('months', 'months'),
                   ('years', 'years')],
        string="Interval unit", default='years')

    def _check_vals_membership_type(self, vals, membership_type):
        if membership_type == 'variable':
            if vals.get('membership_date_from'):
                del vals['membership_date_from']
            if vals.get('membership_date_to'):
                del vals['membership_date_to']
        return vals

    @api.model
    def create(self, vals):
        self._check_vals_membership_type(
            vals, vals.get('membership_type', 'fixed'))
        return super(ProductTemplate, self).create(vals)

    @api.multi
    def write(self, vals):
        self._check_vals_membership_type(
            vals, vals.get('membership_type', self.membership_type))
        return super(ProductTemplate, self).write(vals)
