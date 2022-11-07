odoo.define('mail_broker/static/src/components/discuss/discuss.js', function (require) {
'use strict';

const components = {
    Discuss: require('mail/static/src/components/discuss/discuss.js'),
};

const { patch } = require('web.utils');

patch(components.Discuss, 'mail_broker/static/src/components/discuss/discuss.js', {

    //--------------------------------------------------------------------------
    // Public
    //--------------------------------------------------------------------------

    /**
     * @override
     */
    mobileNavbarTabs(...args) {
        return [...this._super(...args), {
            icon: 'fa fa-comments',
            id: 'broker',
            label: this.env._t("Broker"),
        }];
    }

});

});
