# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields, api


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    lang = fields.Many2one(
        comodel_name="res.lang", string="Force language")

    @api.multi
    def onchange_lang(
            self, lang, template_id, composition_mode, model, res_id):
        if lang:
            lang = self.env['res.lang'].browse(lang)
            obj = self.with_context(force_lang=lang.code)
            res = obj.onchange_template_id(
                composition_mode=composition_mode, model=model,
                template_id=template_id, res_id=res_id)
            return res

    @api.multi
    def send_mail(self):
        if self.lang:
            obj = self.with_context(lang=self.lang.code)
        else:
            obj = self
        return super(MailComposeMessage, obj).send_mail()
