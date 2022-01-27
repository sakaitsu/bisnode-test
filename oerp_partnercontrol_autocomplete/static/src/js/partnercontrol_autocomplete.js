odoo.define('bisnode.partner.autocomplete', function (require) {
'use strict';

var rpc = require('web.rpc');
var AutoComplete = require('partner.autocomplete.core');

/**
 * Use Odoo Autocomplete API to return suggestions
 *
 * @param {string} value
 * @param {boolean} isVAT
 * @returns {Deferred}
 * @private
 */
AutoComplete._getOdooSuggestions = function (value, isVAT) {
    var method = isVAT ? 'read_by_vat' : 'autocomplete';

    var def = rpc.query({
        model: 'res.partner',
        method: method,
        args: [value],
    }, {
        shadow: true,
    }).then(function (suggestions) {
        suggestions.map(function (suggestion) {
            suggestion.logo = suggestion.logo || '';
            suggestion.label = suggestion.legal_name || suggestion.name;
            if (suggestion.vat_hu) suggestion.description = suggestion.vat_hu;
            else if (suggestion.vat) suggestion.description = suggestion.vat;
            else if (suggestion.website) suggestion.description = suggestion.website;

            if (suggestion.country_id && suggestion.country_id.display_name) {
                if (suggestion.description) suggestion.description += _.str.sprintf(' (%s)', suggestion.country_id.display_name);
                else suggestion.description += suggestion.country_id.display_name;
            }

            return suggestion;
        });
        return suggestions;
    });

    return this._dropPreviousOdoo.add(def);
};

/**
 * Check if searched value is possibly a VAT : 2 first chars = alpha + min 5 numbers
 * or it could be a hungarian VAT nunber also
 *
 * @param {string} search_val
 * @returns {boolean}
 * @private
 */
AutoComplete._isVAT = function (search_val) {
    // hungarian
    var str = this._sanitizeOnlyNumeric(search_val);
    // 14933477213
    if (str.length == 11 && search_val.length == 11) return true;
    // 14933477-2-13
    if (str.length == 11 && search_val.length == 13 && search_val.charAt(8) == "-" && search_val.charAt(10) == "-") return true;
    // other
    var str = this._sanitizeVAT(search_val);
    return checkVATNumber(str);
};

/**
 * Sanitize search value by removing all not numeric
 *
 * @param {string} search_value
 * @returns {string}
 * @private
 */
AutoComplete._sanitizeOnlyNumeric = function (search_value) {
    return search_value ? search_value.replace(/[^0-9]/g, '') : '';
};


});
