/*
 * Leaflet (for image viewer), foundation (modals, tooltips) and jquery layers
 * on top of the core text viewer.
 *
 * See text_viewer.js for core logic (vue.js)
 *
*/
$(function() {
    var Foundation = window.Foundation;
    var L = window.L;

    // Note that 256 leaves small black lines between tiles.
    var image_viewer_tile_size = 512;

    window.image_modal = null;
    window.image_viewer_map = null;
    window.image_viewer_map_layer = null;

    $('body').on('click', 'figure', function() {
        destroy_tooltip();

        if (window.image_viewer_map) {
            window.image_viewer_map.remove();
            window.image_viewer_map = null;
            window.image_viewer_map_layer = null;
        }

        if (window.image_modal) {
            window.image_modal.destroy();
            window.image_modal = null;
        }

        var modal = window.image_modal = new Foundation.Reveal($('#image-viewer-modal'), {
            overlay: false,
        });

        modal.open();
        var $modal = modal.$element;
        $modal.css('display', 'flex');

        var map = window.image_viewer_map = L.map('image-viewer', {
            center: [0, 0],
            crs: L.CRS.Simple,
            zoom: 1,
        });

        var $img = $(this).find('img');
        var image_url = $img.attr('data-jp2');
        var title = $img.attr('title') || 'Image Viewer';
        var caption = $(this).find('figcaption').html() || '';
        // caption = "The temple lies in the center of a vast sanctuary, whose extent and complexity was revealed by excavations conducted from 2013 to 2016, on a site whose history goes back to Neolithic times, and which experienced an important phase of monumental constructions in the 1st Century CE. The temple was abandoned at the onset of the Early Middle Ages, and its structures were later reused in the fashioning of a Medieval defensive work. The temple has retained two sides of its square cella, at a height of over 20 meters, as well as vestiges of its ambulatory and side structure foundations. The temple's supposed dedication to the Roman god Janus is not based on any archaeological or historic fact, and the deity that was venerated in the temple is unknown.";

        $modal.find('h3').html(title);
        $modal.find('.image-viewer-caption').toggle(!!caption).html(caption);

        window.image_viewer_map_layer = L.tileLayer.iiif(
            window.SETTINGS_JS.IMAGE_SERVER_URL+image_url+'/info.json', {
                tileSize: image_viewer_tile_size,
                setMaxBounds: true,
            }
        ).addTo(map);
    });


    // Returns [xmin,ymin,xmax,ymax]
    // e.g, "19,26,42,42"
    // They represent the coordinates of the currently selected view
    // in the image viewer. Those coordinates are proportional
    // to the image size (in pc)
    /*
    window.image_viewer_map.getBounds()
        T {_southWest: M, _northEast: M}
        _northEast
        :
        M {lat: -187.64285278320312, lng: 204.98214721679688}
        _southWest
        :
        M {lat: -301.2678527832031, lng: 92.23214721679688}
        __proto__
        :
        Object

            window.get_relative_view_bounds()
        "19,26,42,41"
        window.set_relative_view_bounds("19,26,42,41")
    */
    function get_relative_view_bounds() {
        // Don't use this as bounds scale with zoom level!
        // var pbs = window.image_viewer_map.getPixelBounds();
        var bs = window.image_viewer_map.getBounds();
        var width = window.image_viewer_map_layer.x;
        var height = window.image_viewer_map_layer.y;
        ret = [
            window.image_viewer_map.project(bs.getNorthWest()),
            window.image_viewer_map.project(bs.getSouthEast()),
        ];
        var ret = [
            '',
            ret[0].x / width,
            ret[0].y / height,
            ret[1].x / width,
            ret[1].y / height,
        ];
        ret = ret.reduce(function(str, abs) {
            return (str ? str + ',' : '')+Math.round(abs*100);
        });

        return ret;
    }

    // opposite of get_ function, it takes something like
    // "19,26,42,42"
    // and returns LatLong bounds
    function set_relative_view_bounds(bounds_string) {
        var width = window.image_viewer_map_layer.x;
        var height = window.image_viewer_map_layer.y;
        var pcs = bounds_string.split(',');
        var vs = pcs.map(function(rel, idx) {
            return Math.round(parseInt(rel)/100.0*[width, height][idx % 2]);
        });
        var ret = L.latLngBounds(
            window.image_viewer_map.unproject([vs[0], vs[3]]),
            window.image_viewer_map.unproject([vs[2], vs[1]])
        );
        window.image_viewer_map.fitBounds(ret);
        return ret;
    }

    window.get_relative_view_bounds = get_relative_view_bounds;
    window.set_relative_view_bounds = set_relative_view_bounds;

    // note type="gloss"
    // .tei-note.tei-type-gloss > .note-text
    // See Dropbox 15_conversion of XML for the TExt viewer.docx
    var short_hands = window.SETTINGS_JS.SHORT_HANDS;

    function get_hand_label(hand_acronym) {
        var ret = '';
        ret = short_hands[hand_acronym || ''] || hand_acronym;
        return ret;
    }


    // TOOLTIPS
    // unclear
    window.tv_tooltip = null;

    function destroy_tooltip() {
        if (window.tv_tooltip) {
            window.tv_tooltip.destroy();
            window.tv_tooltip = null;
        }
    }

    function attach_tooltip(anchors, tooltip_fields_fct) {
        $('body').on('mouseenter mouseleave', anchors, function(ev) {
            if ($(this).parents('.text-conventions').length > 0) {
                return false;
            }
            destroy_tooltip();
            if (ev.type == 'mouseenter') {
                var tootlip_fields = tooltip_fields_fct($(this));

                var content = '';
                content = '<h3>'+tootlip_fields.title+'</h3>';
                if (tootlip_fields.body) {
                    content += '<div class="body">'+tootlip_fields.body+'</div>';
                }

                window.tv_tooltip = new Foundation.Tooltip($(this), {
                    tipText: content,
                    triggerClass: 'has-tip-tv',
                    tooltipClass: 'tooltip tv-tooltip',
                    positionClass: 'top',
                    allowHtml: true,
                });
                window.tv_tooltip.show();
            }
            return false;
        });
    }

    jQuery.expr[':'].notchildof = function(a,i,m){
        return jQuery(a).parents(m[3]).length < 1;
    };


    attach_tooltip('figure', function($el) {
        return {
            'title': 'Image (click to view / cliquez pour voir)',
            'body': $el.find('img').attr('title'),
        };
    });
    attach_tooltip('.tv-view-semi-diplomatic .tei-pc-rend-6', function() {
        return {
            'title': 'Deux barres obliques',
            'body': 'probablement pour designer la position d’un pied-de-mouche',
        };
    });
    attach_tooltip('.tei-unclear', function() {
        return {
            'title': 'Texte illisible',
        };
    });
    attach_tooltip('.tei-corr', function($el) {
        return {
            'title': 'Correction',
            'body': 'ms. ' + $el.attr('data-sic'),
        };
    });
    attach_tooltip('.tei-add:notchildof(".tei-mod")', function($el) {
        return {
            'title': 'Addition',
            'body': 'Main: ' + get_hand_label($el.data('tei-hand')),
        };
    });
    attach_tooltip('.tv-view-semi-diplomatic .tei-mod', function($el) {
        return {
            'title': 'Modification',
            'body':
                'Contenu originel: ' +
                $el.find('.tei-del').html() +
                '<br/>Main: ' +
                get_hand_label($el.data('tei-hand')),
        };
    });
    if ($('.tv-viewer-proofreader').length < 1) {
        attach_tooltip('.tei-note.tei-type-gloss', function($el) {
            return {
                'title': 'Note de lecteur médiéval',
                'body': '« ' + $el.find('.note-text').html() + ' » <br>' +
                        'Main: ' + get_hand_label($el.data('tei-resp'))
            };
        });
    }

    var reveal = null;
    $('body').on('click', '.tei-note.tei-type-note', function(ev) {
        var ret = true;
        if (reveal) {
            reveal.close();
        }
        if (ev.type == 'click') {
            var $reveal = $('#shared-reveal');
            if ($reveal.length) {
                $reveal.find('.body').html($(this).find('.note-text').html());

                var subtype_to_title = {
                    'source': 'Sources',
                    'trad':   'Tradition',
                    'gen':    'Note',
                    '':       'Note',
                };
                $reveal.find('h3').html(subtype_to_title[$(this).data('tei-subtype')] || 'Note');
                if (!reveal) {
                    reveal = new Foundation.Reveal($reveal, {
                        overlay: false,
                    });
                }
                reveal.open();
                ret = false;
            }
        }
        return ret;
    });
});
