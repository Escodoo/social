# Copyright 2024 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import UserError

from odoo.addons.phone_validation.tools import phone_validation


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

    def _telegram_get_channel(self, field_name, gateway):
        phone = self[field_name]
        sanitize_res = phone_validation.phone_sanitize_numbers_w_record([phone], self)
        sanitized_number = sanitize_res[phone].get("sanitized")
        if not sanitized_number:
            raise UserError(_("Phone cannot be sanitized"))
        sanitized_number = sanitized_number[1:]
        partner = self._telegram_get_partner()
        if not partner:
            raise UserError(_("No partner found for this record"))

        # Check if channel exists for this partner and gateway
        existing_channel = self.env["res.partner.gateway.channel"].search(
            [
                ("partner_id", "=", partner.id),
                ("gateway_id", "=", gateway.id),
            ]
        )

        if not existing_channel:
            # Create new channel if none exists
            self.env["res.partner.gateway.channel"].create(
                {
                    "name": gateway.name,
                    "partner_id": partner.id,
                    "gateway_id": gateway.id,
                    "gateway_token": sanitized_number,
                }
            )
        else:
            # Update existing channel with new token if different
            if existing_channel.gateway_token != sanitized_number:
                existing_channel.write({"gateway_token": sanitized_number})
        return self.env["mail.gateway.telegram"]._get_channel(
            gateway,
            sanitized_number,
            {
                "contacts": [
                    {
                        "telegram_id": sanitized_number,
                        "profile": {"name": partner.display_name},
                    }
                ],
                "messages": [{"from": sanitized_number}],
            },
            force_create=True,
        )

    def _telegram_get_partner(self):
        if "partner_id" in self._fields:
            return self.partner_id
        return None
