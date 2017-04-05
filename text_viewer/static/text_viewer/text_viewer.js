(function(TextViewer, $, undefined) {

    /*****************************************************
     * Viewer
     */
    function Viewer(options) {
        this.options = options;
        this.api_url = this.options.api_url || (window.location.pathname + 'api/');
        this.panes = {};
        this.view = {
            'panes': [
            ],
        };
        
        if (options.on_create_viewer) {
            options.on_create_viewer({});
        }

        this.createPanesFromQueryString();
        
        var self = this;
        $(window).on('popstate', function() {
            self.onQueryStringUpdated();
        });
    }
    
    Viewer.prototype.onQueryStringUpdated = function() {
        this.createPanesFromQueryString();
    }
    
    Viewer.prototype.onPaneAddressChanged = function(pane) {
        for (var k in this.panes) {
            if (this.panes.hasOwnProperty(k)) {
                if (this.panes[k] !== pane) {
                    this.panes[k].syncWith(pane.address);
                }
            }
        }
    }
    
    Viewer.prototype.updateQueryString = function() {
        // update the title and the browsing history
        var title = '';
        
        var query_string = ''
        for (var k in this.panes) {
            if (this.panes.hasOwnProperty(k)) {
                if (query_string) query_string += '&';
                query_string += k + '=' + this.panes[k].address;
                
                if (title) title += ' | ';
                title += this.panes[k].getTitleFromAddress();
            }
        }
        change_broswer_query_string(query_string, title);
    }

    Viewer.prototype.createPanesFromQueryString = function() {
        var self = this;
        
        // create panes from the query string
        var qs = get_query_string();
        
        if ($.isEmptyObject(qs)) {
            qs = {'p1': 'default/default/default/default'}
        } 
        
        $.each(qs, function(pane_slug, value) {
            if (pane_slug && typeof self.panes !== 'undefined') {
                self.createPaneFromAddress(value, pane_slug);
            }
        });
    };
    
    Viewer.prototype.createPaneFromAddress = function(address, pane_slug) {
        var self = this;

        if (!pane_slug) {
            for (var i = 1; this.panes['p'+i]; i++);
            pane_slug = 'p'+i;
        }
        if (self.panes[pane_slug]) {
            self.panes[pane_slug].requestAddress(address);
        } else {
            var pane = self.panes[pane_slug] = new Pane(self, pane_slug, {'query_string': address})
            if (self.options.on_create_pane) {
                self.options.on_create_pane(pane);
            }
            self.view.panes.push({slug: pane_slug});
        }
    };
    
    Viewer.prototype.getSyncedWithAddress = function(pane) {
        ret = '';
        
        for (var k in this.panes) {
            if (this.panes.hasOwnProperty(k)) {
                if (this.panes[k] !== pane && !this.panes[k].isSynced()) {
                    // TODO: synced with a specific pane rather than first other
                    // one we find.
                    ret = this.panes[k].address;
                    break;
                }
            }
        }
        
        return ret;
    }
    
    Viewer.prototype.closePane = function(apane) {
        for (var i = 0; i < this.view.panes.length; i++) {
            if (this.view.panes[i].slug == apane.view.pane_slug) {
                this.view.panes.splice(i, 1);
                delete this.panes[apane.view.pane_slug];
                this.updateQueryString();
                break;
            }
        }
    }

    Viewer.prototype.getPane = function(slug) {
        return this.panes[slug];
    }
    
    Viewer.prototype.getPaneCount = function() {
        return this.view.panes.length;
    }
    
    Viewer.prototype.getNonSyncedCount = function() {
        var ret = 0;

        for (var k in this.panes) {
            if (this.panes.hasOwnProperty(k) && !this.panes[k].isSynced()) {
                ret += 1;
            }
        }
        
        return ret;
    }

    
    /*****************************************************
     * Pane
     */
    function Pane(panes, slug, options) {
        this.view = {
            document: {
                slug: '',
                label: '',
            },
            pane_slug: slug,
            
            view: 'critical',
            views: ['critical'],
            
            display_settings: [],

            location_type: 'location',
            location_types: ['1', '2'],

            location: 'location',
            locations: ['1', '2'],
            
            conventions: '',
            
            chunk: 'chunk',
            errors: [],
        };
        
        this.panes = panes;
        this.options = options;
        this.address = null;
        this.address_requested = '';
        this.addresses = {};
        
        this.init();
    }

    Pane.prototype.init = function() {
        // create pane from query string
        // self.options.query_string = "Fr_20125/semi-diplomatic/"
        this.requestAddress(this.options.query_string);
    };
    
    Pane.prototype.canClosePane = function() {
        return this.panes.getPaneCount() > 1;
    }
    
    Pane.prototype.closePane = function() {
        this.panes.closePane(this);
    }
    
    Pane.prototype.isSynced = function() {
        return (~this.address_requested.indexOf('synced'));
    }
    
    Pane.prototype.syncWith = function(address) {
        if (this.isSynced()) {
            // todo: sync with that specific address
            this.changeAddressPart('location_type', 'synced');
        }
    }
    
    Pane.prototype.openViewInNewPane = function(view_slug) {
        var parts = this.getAddressParts();
        parts['view'] = view_slug;
        var address = this.getAddressFromParts(parts);
        this.panes.createPaneFromAddress(address);
    }
    
    Pane.prototype.getTitleFromAddress = function() {
        var ret = '';
        var parts = this.getAddressParts();
        
        ret = parts.document + ', ' + parts.location + ' (' + parts.view + ')';
        
        return ret;
    }

    Pane.prototype.getAddressParts = function(address) {
        address = address || this.address || '';
        address = address.replace(/\/?(.*)\/?/, '$1');
        var parts = address.split('/');
        ret = {
            'document': parts.shift() || 'default',
            'view': parts.shift() || 'default',
            'location_type': parts.shift() || 'default',
            'location': parts.shift() || 'default',
        }
        return ret;
    }

    Pane.prototype.getAddressFromParts = function(parts) {
        var ret = parts.document + '/' + parts.view + '/' + parts.location_type + '/' + parts.location;
        return ret;
    }

    Pane.prototype.changeAddressPart = function(part_name, value) {
        var parts = this.getAddressParts(this.address_requested);
        // make sure we don't end up with all panes synced
        if (!(part_name == 'location_type' && value == 'synced' && this.panes.getNonSyncedCount() < 2)) {
            parts[part_name] = value;
        }
        return this.requestAddress(this.getAddressFromParts(parts));
    }

    Pane.prototype.requestAddress = function(address) {
        // api call
        if (address === this.address) {
            // no need for a new request
            // but we may need to update the requested address
            // in case user switched from /section/1 to /synced/1 to /section/1
            this.onReceivedAddress(address);
            return;
        }
        var self = this;
        
        parts = this.getAddressParts(address);
        
        // 2 get initial chunk
        var url = this.panes.api_url + this.getAddressFromParts(parts);
        var on_success = function(data, jqXHR, textStatus) {
            self.address_requested = address;
            self.onRequestSuccessful(data, jqXHR, textStatus);
        };
        var on_complete = function(jqXHR, textStatus) {
            self.onRequestComplete(textStatus, jqXHR);
        };

        this.view.errors = [];
        var data = null;
        
        if (parts.location_type == 'synced') {
            data = {
               'sw': this.panes.getSyncedWithAddress(this)
            }
        }
        
        call_api(url, on_success, on_complete, data);
    }

    Pane.prototype.onRequestSuccessful = function(response, textStatus, jqXHR) {
        if (!response.errors) {
            this.view.chunk = response.chunk;
            this.onReceivedAddress(response.address);
        } else {
            this.view.errors = response.errors;
        }
    }

    Pane.prototype.getPartMeta = function(dict) {
        var ret = {
            'slug': dict.slug,
            'label': dict.label,
        };
        if (dict.label_long) ret.label_long = dict.label_long;
        return ret;
    };
    
    // set all the views, location types and locations for this document
    // make a request if necessary and set up temporary values
    Pane.prototype.requestAddresses = function() {
        var self = this;
        var parts = this.getAddressParts();
        
        if (!self.addresses || (parts.document != self.addresses.slug)) {
            // temp values
            self.addresses = {
                'slug': parts.document,
                'label': parts.document,
                'views': [{
                    slug: parts.view,
                    label: parts.view,
                    location_types: [{
                        slug: parts.location_type,
                        label: parts.location_type,
                        locations: [{
                            slug: parts.location,
                            label: parts.location,
                            label_long: parts.location,
                        }]
                    }]
                }]
            };
            
            if (1) {
                // let's make a new request about this document
                var url_document = this.panes.api_url + parts.document;
                call_api(url_document, function(response, jqXHR, textStatus) {
                    // save doc metadata
                    self.addresses = response;
                    self.renderAddresses();
                }, null, null, false);
            }
        }

        self.renderAddresses();
    }

    // Update the address of the loaded chunk in self.view
    // Based on self.address and self.addresses
    Pane.prototype.renderAddresses = function() {
        var self = this;
        
        // update self.view
        self.view.document = self.getPartMeta(self.addresses);
        
        var parts = this.getAddressParts();

        // update the view list
        self.view.views = [];
        self.addresses.views.map(function(aview) {
            self.view.views.push(self.getPartMeta(aview));
        });
        
        // http://localhost:8000/textviewer/api/Fr20125/
        // Update the lists in self.view
        // by doing simple lookups in the self.views from the address parts.
        this.addresses.views.map(function(aview) {
            // update the view list
            if (aview.slug == parts.view) {
                self.view.view = self.getPartMeta(aview);
                
                // currently selected view 
                // location_types
                self.view.location_types = [];
                self.view.locations = [];
                
                self.view.conventions = aview.conventions || '';
                
                // TODO: clone?
                self.view.display_settings = aview.display_settings || [];
                
                var user_location_type = self.isSynced() ? 'synced': parts.location_type;
                
                aview.location_types.map(function(location_type) {
                    self.view.location_types.push(self.getPartMeta(location_type));
                    
                    if (location_type.slug == user_location_type) {
                        
                        self.view.location_type = self.getPartMeta(location_type);
                        
                        location_type.locations.map(function(location) {
                            self.view.locations.push(self.getPartMeta(location));
                            if (location.slug == parts.location) {
                                self.view.location = self.getPartMeta(location);
                            }
                        });
                    }
                });
            }
        });
    }

    // update the chunk address in self.view
    Pane.prototype.onReceivedAddress = function(address) {
        // update the loaded address
        // this is the real address of our this.view.chunk
        var has_address_changed = (this.address !== address);
        this.address = address;
        
        // update address in URL
        this.panes.updateQueryString();

        // request and render the addresses
        this.requestAddresses();
        
        // broadcast our address to other panes so they can sync with us
        if (has_address_changed && !this.isSynced()) {
            this.panes.onPaneAddressChanged(this);
        }
    }

    Pane.prototype.onRequestComplete = function(textStatus, jqXHR) {
        // TODO
    }

    /*****************************************************
    *     Helpers 
    */
    // TODO: move this to another JS
    
    function get_query_string() {
        var vars = {}, hash;
        var query_string_pos = window.location.href.indexOf('?');
        if (query_string_pos >=0) {
            var hashes = window.location.href.slice(query_string_pos + 1).split('&');
            for(var i = 0; i < hashes.length; i++) {
                hash = hashes[i].split('=');
                vars[hash[0]] = hash[1];
            }
        }
        return vars;
    }

    function call_api(url, onSuccess, onComplete, requestData, synced) {
        // See http://stackoverflow.com/questions/9956255.
        // This tricks prevents caching of the fragment by the browser.
        // Without this if you move away from the page and then click back
        // it will show only the last Ajax response instead of the full HTML page.
        url = url ? url : '';
        var url_ajax = url + ((url.indexOf('?') === -1) ? '?' : '&') + 'jx=1';

        var getData = {
            url: url_ajax,
            data: requestData,
            async: (synced ? false : true),
            complete: onComplete,
            success: onSuccess
        };
        if (requestData && requestData.method) {
            getData.type = requestData.method;
            delete requestData.method;
        }
        var ret = $.ajax(getData);

        return ret;
    };
    
    /*
     * Change the browser URL, push it to the history
     * Also set the document title
     * 
    */
    function change_broswer_query_string(query_string, title) {
        var newurl = window.location.protocol + "//" + window.location.host + window.location.pathname;
        query_string = query_string || '';
        if (query_string) newurl += '?' + query_string;
        if (history.pushState && window.location.href !== newurl) {
            // ! this title is ignored; document.title HAS to be modified AFTER
            // this, see below
            window.history.pushState({path:newurl}, title, newurl);
        }
        document.title = title;
    }

    // ===============================================================
    // User Interface
    // ===============================================================
    
    //function on_create_pane(pane) {
    //layout.addPane(pane.view.pane_slug);

    if (1) {
        // A new pane was created.
        // We generate the html with Vue.js
        // by cloning the existing template into the div for this pane.
        var $template = $('#vue-template-text-pane').detach();
        $template.removeAttr('id');
        var template = $template.prop('outerHTML');
        
        Vue.component('text-pane', {
            template: template,
            // this.apane: the attribute when creating/updating the html element
            // this.pane: the initial pane when creating the html element
            props: ['apane'],
            data: function() {
                this.pane = this.apane;
                var ret = this.apane.view;
                ret.display_settings_active = {};
                return ret;
            },
            // var elem = new Foundation.Tooltip(element, options);
            watch: {
                'apane': function(pane) {
                    // This is a trick. Because vue.js has no way of knowing
                    // which element correspond to which instance when it 
                    // re-renders the viewer/layout. The only thing that is preserved
                    // is the order of the pane. 
                    // If p1, p2, p3. User closes p2. Then vue.js will
                    // keep p1 & p2 components but pass 3rd Pane to p3 component.
                    // We can't replace this.$data so instead we request the
                    // incoming address and update the slug of the pane.
                    this.pane_slug = pane.view.pane_slug;
                    this.pane.requestAddress(pane.address_requested);
                },
                'view.slug': function(val) {
                    this.pane.changeAddressPart('view', val);
                },
                'location.slug': function(val) {
                    this.pane.changeAddressPart('location', val);
                },
                'chunk': function(val) {
                    this.$nextTick(function() {
                        // convert the hrefs to the bibliography page
                        $(this.$el).find(".text-chunk a[href]").each(function() {
                            var link = $(this).attr('href');
                            // TODO: we shouldn't hard-code this link
                            link = '/k/bibliography/#' + link;
                            $(this).attr('href', link);
                        });
                        // we remove all reveals initialised by foundation
                        // to avoid endless accumulation and duplicates
                        $('.reveal[data-panel="'+this.pane_slug+'"]').remove();
                        // we init Foundation on all the new reveals
                        $(this.$el).find('.reveal').each(function() {
                            var $reveal = $(this);
                            $reveal.attr('data-panel', this.pane_slug);
                            new Foundation.Reveal($reveal);
                        })
                    });
                }
            },
            methods: {
                onClickView: function(view) {
                    this.pane.changeAddressPart('view', view);
                },
                onClickViewExtrenal: function(view) {
                    this.pane.openViewInNewPane(view);
                },
                onClickLocationType: function(location_type) {
                    this.pane.changeAddressPart('location_type', location_type);
                },
                // TODO: that logic should move to Panel
                // TODO: the list of available display settings should be 
                // determined by this class instead of the web api.
                isDisplaySettingActive: function(setting) {
                    return !!this.display_settings_active[setting.slug];
                },
                onClickDisplaySetting: function(setting) {
                    this.$set(this.display_settings_active, setting.slug, !!!(this.display_settings_active[setting.slug]));
                },
                getClassesFromDisplaySettings: function() {
                    var self = this;
                    var ret = '';
                    if (this.display_settings) {
                        this.display_settings.map(function(setting) {
                            if (self.isDisplaySettingActive(setting)) {
                                if (ret) ret += ' ';
                                ret += setting.classes;
                            }
                        });
                    }
                    
                    return ret;
                },
                canClosePane: function() {
                    return this.pane.canClosePane();
                },
                closePane: function(apane) {
                    return this.pane.closePane();
                }
            },
        });
    }
    
    // customisation
    
    // ===============================================================
    // Initialisation
    // TODO: move this out

    $(function() {
        Vue.directive('f-dropdown', {
            bind: function(el) {
                Vue.nextTick(function () {
                    $(el).addClass('dropdown menu');
                    var options = {
                        closingTime: 50,
                    };
                    new Foundation.DropdownMenu($(el), options);
                })
            },
            unbind: function(el) {
                $(el).foundation('destroy');
            },
        });
        
        var options = {
            //'on_create_pane': on_create_pane,
            //'on_create_viewer': on_create_viewer,
        };
        var viewer = new Viewer(options);
        
        var layout = new Vue({
            el: '#text-viewer',
            data: viewer.view,
            methods: {
                getPane: function(slug) {
                    return viewer.getPane(slug)
                }
            }
        });
        
        // viewer.load('Fr_20125/critical/section/588/');
        
        $('section.main').on('click', 'div[data-corresp]', function() {
            $('section.main div[data-corresp]').removeClass('highlight');
            $(this).addClass('highlight');
        });
    });
    
}( window.TextViewer = window.TextViewer || {}, jQuery ));
