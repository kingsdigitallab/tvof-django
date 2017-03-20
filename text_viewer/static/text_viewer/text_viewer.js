(function(TextViewer, $, undefined) {

    /*****************************************************
     * Viewer
     */
    function Viewer(options) {
        this.options = options;
        this.api_url = this.options.api_url || (window.location.pathname + 'api/');
        this.panes = {'center': null};
        
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
        if (history.pushState) {
            var newurl = window.location.protocol + "//" + window.location.host + window.location.pathname + '?';
            for (var k in this.panes) {
                if (this.panes.hasOwnProperty(k)) {
                    newurl += k + '=' + this.panes[k].address;
                    newurl += '&';
                }
            }
            window.history.pushState({path:newurl},'',newurl);
        }
    }
    
    Viewer.prototype.createPanesFromQueryString = function() {
        var self = this;
        
        // create panes from the query string
        var qs = get_query_string();
        
        $.each(qs, function(pane_slug, value) {
            if (pane_slug && typeof self.panes !== 'undefined') {
                if (self.panes[pane_slug]) {
                    self.panes[pane_slug].requestAddress(value);
                } else {
                    var pane = self.panes[pane_slug] = new Pane(self, pane_slug, {'query_string': value})
                    if (self.options.on_create_pane) {
                        self.options.on_create_pane(pane);
                    }
                }
            }
        });
    };
    
    Viewer.prototype.getSyncedWithAddress = function(pane) {
        ret = '';
        
        for (var k in this.panes) {
            if (this.panes.hasOwnProperty(k)) {
                if (this.panes[k] !== pane) {
                    // TODO: synced with a specific pane rather than first other
                    // one we find.
                    ret = this.panes[k].address;
                    break;
                }
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
    
    Pane.prototype.isSynced = function() {
        return (~this.address_requested.indexOf('synced'));
    }
    
    Pane.prototype.syncWith = function(address) {
        if (this.isSynced()) {
            // todo: sync with that specific address
            this.changeAddressPart('location_type', 'synced');
        }
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
        parts[part_name] = value;
        return this.requestAddress(this.getAddressFromParts(parts));
    }

    Pane.prototype.requestAddress = function(address) {
        // api call
        if (address === this.address) return;
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
        this.address = address;
        
        // update address in URL
        this.panes.updateQueryString();

        // request and render the addresses
        this.requestAddresses();
        
        // broadcast our address to other panes so they can sync with us
        this.panes.onPaneAddressChanged(this);
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
        var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
        for(var i = 0; i < hashes.length; i++)
        {
            hash = hashes[i].split('=');
            vars[hash[0]] = hash[1];
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
    
    // ===============================================================
    // User Interface
    // ===============================================================
    
    function on_create_pane(pane) {
        // A new pane was created.
        // We generate the html with Vue.js
        // by cloning the existing template into the div for this pane.
        var $template = $('#text-pane-template').clone();
        $template.removeAttr('id');
        var containerid = '#text-pane-'+pane.view.pane_slug
        var $container = $(containerid);
        $container.html($template);
        
        pane.view.display_settings_active = {};
        
        new Vue({
            el: containerid,
            data: pane.view,
            watch: {
                'view.slug': function(val) {
                    pane.changeAddressPart('view', val);
                },
                'location.slug': function(val) {
                    pane.changeAddressPart('location', val);
                }
            },
            methods: {
                onClickView: function(view) {
                    pane.changeAddressPart('view', view);
                },
                onClickLocationType: function(location_type) {
                    pane.changeAddressPart('location_type', location_type);
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
                }
            },
        });
    }
    
    // customisation
    
    function on_chunk_loaded(vue) {
        
    }

    // ===============================================================
    // Initialisation
    // TODO: move this out

    $(function() {
        Vue.directive('f-dropdown', {
            bind: function(el) {
                Vue.nextTick(function () {
                    $(el).addClass('dropdown menu');
                    new Foundation.DropdownMenu($(el));
                })
            },
            unbind: function(el) {
                $(el).foundation.destroy();
            },
        });
        
        var options = {
            'on_create_pane': on_create_pane,
            'on_chunk_loaded': on_chunk_loaded,
        };
        var viewer = new Viewer(options);
        // viewer.load('Fr_20125/critical/section/588/');
        
        $('section.main').on('click', 'div[data-corresp]', function() {
            $('section.main div[data-corresp]').removeClass('highlight');
            $(this).addClass('highlight');
        });
    });
    
}( window.TextViewer = window.TextViewer || {}, jQuery ));
