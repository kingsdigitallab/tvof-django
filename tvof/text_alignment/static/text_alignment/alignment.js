$(function() {
    var config = window.ALIGNMENT_CONFIG;

    var $win = $(window);
    var $body = $('body');
    var $settings = $('#settings');
    var $fragment = $('#alignment-fragment');
    var vue_config = new_vue_config(config);
    var $plink = $('#plink').detach();

    // returns a URL to the textviewer opened
    // at a specific paragraph for a given manuscript.
    // ms_name is a manuscript name.
    // para_number is an integer paragraph number.
    // Note that apart from Royal, all other MS will be
    // redirected to Fr20125.
    function get_text_href(ms_name, para_number) {
        var ms_name_normalised = ms_name.replace(/\W+/gi, '').toLowerCase();
        // MS is not viewable in the Text Viewer we don't return a link.
        if (window.ALIGNMENT_LINKABLE_MSS.join(',').indexOf(ms_name_normalised) <= -1) {
            return null;
        }
        var doc = 'Fr20125';
        if (/royal.*20.*d.*1/i.test(ms_name)) {
            doc = 'Royal';
        }
        var ret = '/textviewer/?p1='+doc+'/semi-diplomatic/paragraph/'+para_number;

        return ret;
    }

    window.get_text_href = get_text_href;

    // https://tvof-stg.kdl.kcl.ac.uk/textviewer/?p1=Royal/semi-diplomatic/section/3
    // User click Link on a para to go the text viewer
    $('body').on('mouseleave', '[data-plink]', function(e) {
        $plink.detach();
    });
    $('body').on('mouseenter', '[data-plink]', function(e) {
        var $para_div = $(this);
        var plink_data = $para_div.data('plink');
        var parts = plink_data.split('/');
        var ms_idx = parseInt(parts[0]);
        var href = null;
        // TODO: shouldn't be hard-coded
        $.each(config, function(idx, field) {
            if (field.key == 'mss') {
                var ms_key = field.options[ms_idx].key;
                href = get_text_href(ms_key, parts[1]);
            }
        });

        if (href) {
            $plink.attr('href', href);
            $para_div.prepend($plink.detach());
            $plink.show();
        }
    });

    // Visualisation Settings modal
    function new_vue_config(config) {
        var ret = new window.Vue({
            el: '#settings .settings-body',
            data: {
                vars: config
            },
            methods: {
                'select_all': function(avar) {
                    $.each(avar.options, function(idx, option) {
                        option.selected = true;
                    });
                },
                'select_none': function(avar) {
                    $.each(avar.options, function(idx, option) {
                        option.selected = false;
                    });
                },
                'get_request_data': function() {
                    // We convert the config vars into a
                    // dictionary: {field: [values]}
                    var ret = {};
                    $.each(this.vars, function(idx, avar) {
                        var values = [];
                        if (avar.type == 'single') {
                            // selection is help in var.selected
                            ret[avar.key] = avar.selected;
                        } else {
                            // selctions are held in var.options.X.selected
                            $.each(avar.options, function(idx, option) {
                                if (option.selected) {
                                    values.push(option.key);
                                }
                            });
                            ret[avar.key] = values.join(',');
                        }
                    });
                    //console.log(ret);
                    return ret;
                }
            }
        });
        return ret;
    }

    $('.toggle-settings').on('click', function(e) {
        toggle_settings();
        return false;
    });

    function toggle_settings() {
        if ($settings.is(':visible')) {
            close_settings();
        } else {
            open_settings();
        }
    }

    function open_settings() {
        $body.addClass('settings-visible');
    }

    function close_settings() {
        $body.removeClass('settings-visible');

        // update results
        request_fragment();
    }

    function request_fragment() {
        $fragment.stop(true, true).fadeTo('slow', 0.2);

        var url = document.location.href;
        var params = {};

        if (0) {
            var argjs = (url.indexOf('?') > -1) ? '&' : '?';
            argjs += 'js=1';
            url = url.replace(/(#|$)/i, argjs + '$1');
        } else {
            url = url.replace(/(#|\?).*/i, '');
            params = vue_config.get_request_data();
            params.js = 1;
        }

        var req = $.getJSON({
            url: url,
            data: params,
        });

        req.done(function(data, textStatus, jqXHR) {
            window.Vue.set(vue_config, 'vars', data.config);
            replace_fragment(data);
            $fragment.stop(true, true).css('opacity', 1);
            // remove
            //open_settings();
        });
    }
    request_fragment();
    //open_settings();

    function replace_fragment(data) {
        $fragment.html(data.html);
        if (history.pushState) {
            var newurl = window.location.protocol + "//" + window.location.host + window.location.pathname + '?' + data.qs;
            window.history.pushState({path:newurl},'',newurl);
        }
        fix_thead($fragment);
    }

    var row_top = 0;
    function fix_width_row($row_fixed, $row) {
        let $children_fixed = $row_fixed.children()
        $row.children().each(function(index, th) {
            var $th = $(th);
            $($children_fixed[index]).css('min-width', $th.outerWidth(true));
        });
    }
    function fix_thead($root) {
        // diy sticky for column & table views.
        // todo: replace with foundation sticky
        $('.fixed-tr').remove();

        var $row = $root.find('.sticky-diy');

        if ($row.length === 0) return;

        var $row_fixed = $row.clone();
        $row_fixed.addClass('fixed-tr');
        $row_fixed.css('display', $row.css('display'));
        $row.parent().append($row_fixed);
        fix_width_row($row_fixed, $row);

        $row_fixed.data('threshold', $row.offset().top);

        update_table_heads();
    }

    $win.on('keyup', function(ev) {
        if (ev.which == 27) {
            toggle_settings();
            return false;
        }
    });

    $win.on('scroll', function() {
        update_table_heads();
    });

    $win.on('resize', function() {
        fix_thead($('body'));
    });

    function update_table_heads() {
        var top = $win.scrollTop();
        $('.fixed-tr').each(function(index, row) {
            var $row = $(row);
            $row.toggle(top > $row.data('threshold')).css('top', top);
        });
    }
});

