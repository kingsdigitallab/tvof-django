var api_url = '/api/v1/tokens/search/facets/?format=json';
var text_viewer_url = '/textviewer/?p1=';
var id_to_viewer_slug = {
    0: 'Fr20125',
    1: 'Royal',
};
var id_to_label = {
    0: 'Fr20125',
    1: 'Royal 20 D I',
};

// This is a list of a facets to show on the front end
// the order is important and it contains a mapping
// between facet keys and display labels.
var ui_facets = [
    {
        key: 'manuscript_number',
        label: 'Manuscript',
    },
    {
        key: 'lemma',
        label: 'Lemma',
    },
    {
        key: 'token',
        label: 'Form',
    },
    {
        key: 'section_name',
        label: 'Section',
    },
    {
        key: 'pos',
        label: 'Part of speech',
    },
    {
        key: 'is_rubric',
        label: 'Rubrication',
    },
];

// /api/v1/tokens/search/?format=json&page=2&lemma=dire
var app = new window.Vue({
    el: '#tvof-search',
    data: {
        response: {
            fields: {},
            count: 0,
            objects: {
                count: 0,
                next: '',
                previous: '',
                results: [],
            },
        },
        query: {
            text: '',
            page: 1,
            facets: {},
            page_size: 10,
            order: '',
        },
        ui_facets: ui_facets,
        page_sizes: window.SETTINGS_JS.SEARCH_PAGE_SIZES,
    },
    computed: {
        last_page_index: function() {
            return Math.ceil(this.response.objects.count / this.query.page_size);
        },
        orders: function() {
          // Returns the possible orders as an array
          // Each item will have a key entry
          var orders = window.SETTINGS_JS.SEARCH_PAGE_ORDERS;

          return Object.keys(orders).map(function(key) {
            var e = orders[key];
            e.key = key;
            return e;
          });
        }
    },
    filters: {
        nice_location: function(hit) {
            var ret = '';
            ret = id_to_label[hit.manuscript_number];
            if (hit.para_number) {
                ret += ' §' + hit.para_number;
            }
            if (hit.seg_number) {
                ret += '.' + hit.seg_number;
            }
            return ret;
        }
    },
    mounted: function() {
        var self = this;
        this._call_api(window.location.search);
        window.addEventListener('popstate', function(event) {
            if (event.state) {
                self._call_api(window.location.search, true);
            }
        }, false);
    },
    methods: {
        get_option_label_from_text: function(text, facet_key) {
            var ret = text;

            // TODO: don't hardcode names here!
            if (facet_key == 'manuscript_number') {
                ret = id_to_label[ret];
            }
            if (facet_key == 'is_rubric') {
                ret = ret == 'true' ? 'rubricated' : 'not rubricated';
            }

            return ret;
        },
        get_facet_options: function(ui_facet) {
            var ret = [];

            ret = this.response.fields[ui_facet.key];

            return ret;
        },
        on_change_order: function() {
            this.query.page = 1;
            this.call_api();
        },
        on_change_page_size: function() {
            this.query.page = 1;
            this.call_api();
        },
        on_reset_search_text: function() {
            this.query.text = '';
            this.on_change_search_text();
        },
        is_option_selected: function(facet, option) {
            return (this.query.facets[facet+'__'+option.text]);
        },
        on_click_option: function(facet, option) {
            if (this.is_option_selected(facet, option)) {
                delete (this.query.facets)[facet+'__'+option.text];
            } else {
                this.query.facets[facet+'__'+option.text] = [facet, option.text];
            }
            this.query.page = 1;
            this.call_api();
        },
        on_click_token: function(hit) {
            // edfr20125_00598_08
            // => /textviewer/?p1=Fr20125/semi-diplomatic/paragraph/2
            var url = text_viewer_url + id_to_viewer_slug[hit.manuscript_number] + '/interpretive/paragraph/' + parseInt(hit.para_number, 10);
            if (hit.seg_number) {
                url += '/' + hit.seg_number;
            }
            if (url) {
              var win = window.open(url, '_blank');
              win.focus();
            }
        },
        on_click_prev: function() {
            this.query.page -= 1;
            this.call_api();
        },
        on_click_next: function() {
            this.query.page += 1;
            this.call_api();
        },
        on_change_search_text: function() {
            this.query.page = 1;
            this.query.facets = {};
            this.call_api();
        },
        call_api: function() {
            // send request to search api using data.query

            var self = this;
            // query = $.extend(self.query, query);
            // var req = $.getJSON(url || api_url, url ? null : query);
            var query = {
                page: self.query.page,
                text: self.query.text,
                selected_facets: self.get_selected_facets(),
                page_size: self.query.page_size,
                order: self.query.order,
            };

            var qs = $.param(query, true);
            this._call_api(qs);
        },
        _call_api: function(qs, is_state_popped) {
            // send request to search api using querystring qs

            // http://localhost:8000/search/?page=1&selected_facets=lemma_exact%3Aa3
            // clean qs
            // 'a=1&b=&c&d=4;4&f#23'
            // => "a=1&d=4;4#23"
            qs = qs.replace(/^\?/, '');
            qs = qs.replace(/[?&^][^=&#]*=?(?=(?:#|&|$))/ig, '');

            var self = this;
            var req = $.getJSON(api_url, qs);
            req.done(function(response) {
                self.$set(self, 'response', response);

                if (!is_state_popped) {
                    window.history.pushState(
                        qs,
                        'Search',
                        '?'+qs
                    );
                }

                self.set_state_from_query_string();
            });
        },
        set_state_from_query_string: function() {
            // http://localhost:8000/search/?page=4&text=avoir&selected_facets=manuscript_exact%3AedRoyal20D1&selected_facets=token_exact%3Aavoient

            // TODO: URLSearchParams not well supported by IE
            var qs_params = new window.URLSearchParams(window.location.search);
            this.query.text = qs_params.get('text') || '';
            // TODO: deal with non-integer in the qs
            this.query.page = parseInt(qs_params.get('page') || 1);
            this.query.page_size = parseInt(qs_params.get('page_size') || this.page_sizes[0]);

            // order
            this.query.order = qs_params.get('order') || '';
            var orders = window.SETTINGS_JS.SEARCH_PAGE_ORDERS;
            if (!orders[this.query.order]) {
              this.query.order = Object.keys(orders)[0];
            }

            // Facets
            var self = this;
            var facets_options = qs_params.getAll('selected_facets');
            if (facets_options) {
                var facets = {};
                $.each(facets_options, function(i, v) {
                    v = v.replace('_exact', '');
                    if (v) {
                        var pair = v.split(':');
                        facets[v.replace(':', '__')] = pair;
                    }
                });
                self.$set(self.query, 'facets', facets);
            }
        },
        get_selected_facets: function() {
            var ret = [];
            $.each(this.query.facets, function(k, v) {
                // lemma_exact%3AEneas
                ret.push(v[0]+'_exact:'+v[1]);
            });
            return ret;
        }
    }
});
