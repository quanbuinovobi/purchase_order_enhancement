odoo.define('purchase.us_phone', function(require) {
    "use strict";

var Phone = require('web.basic_fields').FieldPhone;
var fieldRegistry = require('web.field_registry');

var US_Phone = Phone.extend({
    events: _.extend({}, Phone.prototype.events, {
        'keyup': '_onKeyUp',
    }),

    _onKeyUp() {
        let phoneNum = this._getValue();
        phoneNum = PhoneNumUsFormat(phoneNum);
        this.$input.val(phoneNum);
    },

});

function PhoneNumUsFormat(phoneNum) {
    let cleaned = phoneNum.replace(/[^0-9]/gi, '')
    let phoneLen = cleaned.length;

    if (phoneLen == 0) {
        return "";
    }
    else if (phoneLen < 4) {
        return '(' + cleaned.substr(0,3) ;
    }
    else if (phoneLen < 7) {
        return '(' + cleaned.substr(0,3) + ') ' + cleaned.substr(3,3);
    }
    else {
        return '(' + cleaned.substr(0,3) + ') ' + cleaned.substr(3,3) + '-' + cleaned.substr(6,4);
    }
}

fieldRegistry.add('us_phone', US_Phone);

});