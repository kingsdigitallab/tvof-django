// Main
require([
    'requirejs',
    'jquery',
    'fn',
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
    });

});
