# Copyright 2024 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class TelegramComposer(models.TransientModel):

    _name = "telegram.composer"
    _description = "Compose a telegram message"

    res_model = fields.Char("Document Model Name")
    res_id = fields.Integer("Document ID")
    number_field_name = fields.Char()
    find_gateway = fields.Boolean()
    gateway_id = fields.Many2one(
        "mail.gateway", domain=[("gateway_type", "=", "telegram")], required=True
    )
    body = fields.Text("Message")
    telegram_user_id = fields.Char(
        "Telegram User ID",
        required=True,
        help="The Telegram user ID to send the message to. "
        "This can be found when the user contacts you via Telegram.",
    )

    @api.model
    def default_get(self, fields):
        result = super().default_get(fields)
        gateways = self.env["mail.gateway"].search([("gateway_type", "=", "telegram")])
        result["find_gateway"] = len(gateways) != 1
        if not result["find_gateway"]:
            result["gateway_id"] = gateways.id
        return result

    def _action_send_telegram(self):
        record = self.env[self.res_model].browse(self.res_id)
        if not record:
            return
        channel = record._telegram_get_channel(
            self.number_field_name, self.gateway_id, self.telegram_user_id
        )
        channel.message_post(
            body=self.body, subtype_xmlid="mail.mt_comment", message_type="comment"
        )

    def action_view_telegram(self):
        self.ensure_one()
        record = self.env[self.res_model].browse(self.res_id)
        if not record:
            return
        channel = record._telegram_get_channel(
            self.number_field_name, self.gateway_id, self.telegram_user_id
        )
        if channel:
            return {
                "type": "ir.actions.client",
                "tag": "mail.action_discuss",
                "params": {"active_id": "{}_{}".format(channel._name, channel.id)},
            }
        return False

    def action_send_telegram(self):
        self.ensure_one()
        if not self.body:
            raise UserError(_("Body is required"))
        self._action_send_telegram()
        return False
