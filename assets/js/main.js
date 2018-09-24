// Main
require([
    'requirejs',
    'jquery',
    'fn',
    'cookie',
    'ga'
], function(r, $) {
    'use strict';

    $(document).ready(function() {
        // Expand / Collapse
        $('.expand').on("click", function () {
            $(this).children().next('p').slideToggle(400).toggleClass("hide show");
            $(this).toggleClass("active");
            return false;
        });

        // Cookie consent
        if (!cookie.get('tvof-cookie')) {
            $("#cookie-disclaimer").removeClass('hide');
        }
        // Set cookie
        $('#cookie-disclaimer .closeme').on("click", function() {
            cookie.set('tvof-cookie', 'tvof-cookie-set', { expires: 30 });
        });
    });

});
