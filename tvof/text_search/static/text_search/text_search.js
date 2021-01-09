var autocomplete_url = '/api/v2/tokens/autocomplete/?format=json&page_size=50';
var text_viewer_url = '/textviewer/?p1=';
var id_to_viewer_slug = {
    0: 'Fr20125',
    1: 'Royal',
};
var id_to_label = {
    0: 'Fr20125',
    1: 'Royal 20 D I',
};
var RESULT_TYPE_DEFAULT = 'tokens';

// This is a list of a facets to show on the front end
// the order is important and it contains a mapping
// between facet keys and display labels.
var SEARCH_CONFIG = window.SETTINGS_JS.SEARCH_CONFIG;

window.Vue.use(window.VueAutosuggest);


function sort_suggestions(suggestions, phrase) {
  // ac-368: comparison places exact matches on top
  // then consider length difference
  // then take alaphebetical difference into account (see compare_suggestions)
  if (suggestions) {
    suggestions.map(function(sug) {
      sug.cmp = 0;
      for (var k of ['lemma', 'form']) {
        var s = (sug[k] ? sug[k] : sug.lemma || '').toLowerCase();
        if (s) {
          if (s.startsWith(phrase)) sug.cmp -= 500;
          if (s == phrase) sug.cmp -= 1000;
          sug.cmp += 10 * Math.abs(s.length - phrase.length);
        }
        sug[k+'_l'] = s;
      }

      return sug;
    });
    suggestions.sort(compare_suggestions);
  }
  return suggestions;
}

function compare_suggestions(a, b) {
  var ret = a.cmp - b.cmp;
  ret += (a.lemma_l < b.lemma_l) ? -1 : (a.lemma_l == b.lemma_l) ? 0 : 1;
  ret += (a.form_l < b.form_l) ? -1 : (a.form_l == b.form_l) ? 0 : 1;
  return ret;
}


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
            page_size: window.SETTINGS_JS.SEARCH_PAGE_SIZE_DEFAULT,
            order: '',
            result_type: 'names',
        },
        suggestions: [],
        suggestion_closed: true,
        page_sizes: window.SETTINGS_JS.SEARCH_PAGE_SIZES,
        ui_facets_top: [
          {
            'key': 'result_type',
            'label': 'Result Type',
          },
        ],
    },
    computed: {
        autosuggestions: function() {
          // ac-368: sort suggestion better than haystack/solr
          // just so exact matches appear first.
          return [{data: sort_suggestions(this.suggestions, this.query.text)}];
        },
        last_page_index: function() {
            return Math.ceil(
                Math.min(
                    window.SETTINGS_JS.SEARCH_RESULT_MAX_SIZE,
                    this.response.objects.count
                ) / this.query.page_size
            );
        },
        is_result_truncated: function() {
            // returns true if elasticsearch can't return all hits
            return (this.response.objects.count > window.SETTINGS_JS.SEARCH_RESULT_MAX_SIZE);
        },
        orders: function() {
          // returns dictionary ORDER_KEY: {label: ORDER_LABEL}
          return this.config.orders;
        },
        config: function() {
            var result_type = this.query.result_type || RESULT_TYPE_DEFAULT;
            return SEARCH_CONFIG[result_type];
        },
        ui_facets: function() {
            var self = this;
            return window.SEARCH_FACETS.filter(function(facet) {
                if (!facet.is_hidden && self.response && self.response.fields[facet.key]) {
                    // <!-- AC-392 8/7/2020 -->
                    // if (self.query.result_type != 'names' || facet.key != 'pos') {
                    if (self.query.result_type == 'tokens' || facet.key != 'pos') {
                        return true;
                    }
                }
                return false;
            });
        },
        max_hits: function() {
            return window.SETTINGS_JS.SEARCH_RESULT_MAX_SIZE;
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
            if (hit.token_number && window.SETTINGS_JS.SEARCH_SHOW_TOKEN_NUMBER) {
                ret += ' #' + hit.token_number + '';
            }
            return ret;
        },
        hide_unspecified: function(value) {
            return (value == 'Unspecified' || value == 'Other') ? '' : value;
        },
        pluralize: function(count, word) {
            if (count !== 1) {
                if (count === 0) {
                    count = 'no'
                }
                word += 's'
            }
            return count + ' ' + word
        }
    },
    mounted: function() {
        var self = this;

        // initial search request
        this._call_api(window.location.search);

        // back button trigger a new search
        window.addEventListener('popstate', function(event) {
            if (event.state) {
                self._call_api(window.location.search, true);
            }
        }, false);

        // foundation tooltips
        window.Vue.nextTick(function () {
            $('.has-tip[data-tooltip-vue]').attr('data-tooltip', '').foundation();
        });

    },
    methods: {
        get_option_label_from_text: function(text, facet_key) {
            var ret = text;

            // TODO: don't hardcode names here!
            if (facet_key == 'manuscript_number') {
                ret = id_to_label[ret];
            }
            if (facet_key == 'is_rubric') {
                ret = (ret === true || ret == 'true') ? 'Rubric' : 'Text body';
            }
            if (facet_key == 'section_number') {
                ret = window.SETTINGS_JS.SECTIONS_NAME[ret];
            }
            if (facet_key == 'verse_cat') {
                ret = {
                  '0': 'prose',
                  '1': 'verse',
                  '2': 'verse: lineated',
                  '3': 'verse: continuous',
                  '4': 'unspecified',
                }[ret];
            }
            if (facet_key == 'speech_cat') {
                ret = {
                  '0': 'narration',
                  '1': 'speech',
                  '2': 'direct speech',
                  '3': 'indirect reported speech',
                  '4': 'speech (unspecified)',
                }[ret];
            }

            return ret;
        },
        has_facet_options: function(ui_facet) {
            for (r of this.get_facet_options(ui_facet)) {
                if (r.count) return true
            }
            return false
        },
        get_facet_options: function(ui_facet) {
            var ret = [];

            if (ui_facet.key == 'result_type') {
                var config = SEARCH_CONFIG;
                ret = [];
                Object.keys(config).forEach(function(key) {
                    ret.push({
                        'key': key,
                        'text': config[key].label,
                        'count': 1,
                    });
                });

                return ret;
            }

            ret = this.response.fields[ui_facet.key];

            return ret;
        },
        on_change_result_type: function(type) {
            this.query.result_type = type;
            this.query.page = 1;
            // reset all facets (we at least need the pos to be reset for names)
            this.$set(this.query, 'facets', {});
            this.call_api();
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
        on_click_lemma: function(hit) {
            // search for that lemma in the tokens/kwic result type.
            // exclude part after comma as it can disrupt the search
            // (e.g. 'maintas, a' would return all the tokens with lemma 'a').
            this.query.result_type = 'tokens';
            if (1) {
                // nicer b/c we get exactly what we want
                // BUT only lemma with top freq are displayed.
                // So selected lemma isn't visible!
                // http://localhost:8000/search/?result_type=tokens&page=1&selected_facets=lemma_exact%3Aquem&page_size=20&order=form
                this.query.text = '';
                let facet_option = ['lemma', hit.lemma];
                let facet_key = facet_option.join('__');
                this.$set(this.query, 'facets', {facet_key: facet_option});
            } else {
                this.query.text = hit.lemma.split(',')[0];
                this.$set(this.query, 'facets', {});
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
        on_click_first: function() {
            this.query.page = 1;
            this.call_api();
        },
        on_click_prev: function() {
            this.query.page -= 1;
            this.call_api();
        },
        on_click_next: function() {
            this.query.page += 1;
            this.call_api();
        },
        on_click_last: function() {
            this.query.page = this.last_page_index;
            this.call_api();
        },
        on_change_page_number: function() {
            this.call_api();
        },
        on_change_search_text: function() {
            this.query.page = 1;
            this.query.facets = {};
            this.call_api();
        },
        on_keyup_search_text: function(e) {
            this.fetch_suggestions(e.target.value);
        },
        on_selected_suggestion: function(suggestion) {
            // when a search text is submitted by the user.
            // (they want to update search results).
            // suggestion is null if user press enter in input
            // instead of selecting a suggestion.
            window.console.log('SELECT');
            window.console.log(suggestion);
            if (suggestion) {
                var item = suggestion.item;
                this.query.text = item.form || item.lemma;
            }
            // window.console.log(suggestion);
            this.on_change_search_text();
        },
        on_blur_suggestions: function() {
            window.console.log('BLUR');
            window.Vue.nextTick(function () {
                window.console.log('BLURRING');
                this.suggestion_closed = true;
            });
        },
        fetch_suggestions: function(search_text) {
            var self = this;
            var qs = {
                q: search_text
            };
            var req = $.getJSON(autocomplete_url, qs);
            req.done(function(response) {
                self.$set(
                  self,
                  'suggestions',
                  response.results
                );
            });
        },
        get_suggestion_value: function(suggestion) {
            // returns the string to set in the input box
            // when the user highlights a suggestion
            var item = suggestion.item;
            return item.form || item.lemma;
        },
        call_api: function() {
            // send request to search api using data.query

            var self = this;
            // query = $.extend(self.query, query);
            // var req = $.getJSON(url || api_url, url ? null : query);
            var query = {
                result_type: self.query.result_type,
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

            var result_type = qs.replace(/(.*)result_type=([^=&#]+)(.*)/, '$2');
            if (result_type == qs) result_type = RESULT_TYPE_DEFAULT;

            var self = this;
            var req = $.getJSON(SEARCH_CONFIG[result_type].api, qs);
            req.done(function(response) {
                self.filter_response(response);

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
        filter_response: function(response) {
            // transofrm the response from the search API
            // mainly facet option ordering and filtering
            var fields = response.fields;

            this.ui_facets.map(function(ui_facet) {
                var key = ui_facet.key;
                var ret = fields[key];

                if (ret) {
                    if (ret && ui_facet.whitelist) {
                        ret = ret.filter(function(v) {
                            return (ui_facet.whitelist.indexOf(v.text.toLowerCase()) > -1);
                        });
                        fields[key] = ret;
                    }

                    if (ret && key == 'section_number') {
                        // sections should be in order of their numbers
                        ret.sort(function(a, b) {
                            var na = parseInt(a.text);
                            var nb = parseInt(b.text);
                            if (na == nb) return (a.text > b.text) ? 1 : -1;
                            return na > nb ? 1 : -1;
                        });
                    }
                }

                return ui_facet;
            });
        },
        set_state_from_query_string: function() {
            // http://localhost:8000/search/?page=4&text=avoir&selected_facets=manuscript_exact%3AedRoyal20D1&selected_facets=token_exact%3Aavoient

            // TODO: URLSearchParams not well supported by IE
            var qs_params = new window.URLSearchParams(window.location.search);
            this.query.text = qs_params.get('text') || '';
            // TODO: deal with non-integer in the qs
            this.query.page = parseInt(qs_params.get('page') || 1);
            this.query.page_size = parseInt(qs_params.get('page_size') || window.SETTINGS_JS.SEARCH_PAGE_SIZE_DEFAULT);

            // result_type
            this.query.result_type = qs_params.get('result_type') || RESULT_TYPE_DEFAULT;

            // order
            this.query.order = qs_params.get('order') || '';
            if (!this.orders[this.query.order]) {
              this.query.order = Object.keys(this.orders)[0];
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
