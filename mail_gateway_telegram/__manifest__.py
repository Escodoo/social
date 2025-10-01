# Copyright 2024 Dixmit
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Mail Telegram Gateway",
    "summary": """
        Set a gateway for telegram""",
    "version": "16.0.1.1.0",
    "license": "AGPL-3",
    "author": "Creu Blanca,Dixmit,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/social",
    "depends": ["mail_gateway"],
    "data": [
        "security/ir.model.access.csv",
        "views/mail_gateway.xml",
        "wizards/telegram_composer.xml",
    ],
    "external_dependencies": {"python": ["python-telegram-bot", "lottie", "cairosvg"]},
    "assets": {
        "mail.assets_messaging": [
            "mail_gateway_telegram/static/src/models/**/*.js",
        ],
        "web.assets_backend": [
            "mail_gateway_telegram/static/src/components/**/*.js",
            "mail_gateway_telegram/static/src/components/**/*.xml",
        ],
    },
}
