/** @odoo-module **/

import {PhoneField} from "@web/views/fields/phone/phone_field";
import {SendTelegramButton} from "@mail_gateway_telegram/components/send_telegram_button/send_telegram_button.esm";
import {patch} from "@web/core/utils/patch";

patch(PhoneField, "mail_gateway_telegram.PhoneField", {
    components: {
        ...PhoneField.components,
        SendTelegramButton,
    },
    defaultProps: {
        ...PhoneField.defaultProps,
        enableButton: true,
    },
    props: {
        ...PhoneField.props,
        enableButton: {type: Boolean, optional: true},
    },
    extractProps: ({attrs}) => {
        return {
            enableButton: attrs.options.enable_sms,
            placeholder: attrs.placeholder,
        };
    },
    get canShowTelegramButton() {
        // Only show button if there's a phone number and a partner
        return (
            this.props.value &&
            this.props.value.length > 0 &&
            this.props.record.data.partner_id
        );
    },
});
