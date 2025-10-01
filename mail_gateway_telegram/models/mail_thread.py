# Copyright 2024 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import UserError


class MailThread(models.AbstractModel):

    _inherit = "mail.thread"

    def _get_telegram_channel_vals(self, token, gateway, partner):
        result = {
            "gateway_channel_token": token,
            "gateway_id": gateway.id,
        }
        if partner:
            result["partner_id"] = partner.id
            result["name"] = partner.display_name
        return result

    def _telegram_get_channel(self, field_name, gateway, telegram_user_id):
        partner = self._telegram_get_partner()
        if not partner:
            raise UserError(_("No partner found for this record"))

        # Check if channel exists for this partner and gateway with the telegram user ID
        if not self.env["res.partner.gateway.channel"].search(
            [
                ("partner_id", "=", partner.id),
                ("gateway_id", "=", gateway.id),
                ("gateway_token", "=", str(telegram_user_id)),
            ]
        ):
            self.env["res.partner.gateway.channel"].create(
                {
                    "name": gateway.name,
                    "partner_id": partner.id,
                    "gateway_id": gateway.id,
                    "gateway_token": str(telegram_user_id),
                }
            )

        return self.env["mail.gateway.telegram"]._get_channel(
            gateway,
            str(telegram_user_id),
            {
                "contacts": [
                    {
                        "telegram_id": str(telegram_user_id),
                        "profile": {"name": partner.display_name},
                    }
                ],
                "messages": [{"from": str(telegram_user_id)}],
            },
            force_create=True,
        )

    def _telegram_get_partner(self):
        if "partner_id" in self._fields:
            return self.partner_id
        return None
