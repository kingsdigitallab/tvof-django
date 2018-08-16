/*
 * Text Viewer code. 
 * 
 * Content:
 * 
 * - Viewer: manages the layout, lifecycle and synchronisation of multiple panes 
 * - Pane: handles the navigation logic and server requests for a text pane
 * - Helper functions
 * - text-pane: a vue.js module for rendering a pane
 * - f-sticky: vue.js directive for a sticky div
 * - f-dropdown: vue.js directive for a Foundation dropdown menu
 * - initialisation of the interface
 * 
 * TODO: split the different modules/layers into separate source files.
 */
(function(TextViewer, $, undefined) {

    /*****************************************************
     * Viewer
     */
    function Viewer(options) {
        this.options = options;
        this.api_url = this.options.api_url || (window.location.pathname + 'api/');
        this.panes = {};
        this.cache = {};
        this.uimodel = {
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
    };
    
    Viewer.prototype.onPaneAddressChanged = function(pane) {
        for (var k in this.panes) {
            if (this.panes.hasOwnProperty(k)) {
                if (this.panes[k] !== pane) {
                    this.panes[k].syncWith(pane.address);
                }
            }
        }
    };
    
    Viewer.prototype.updateQueryString = function() {
        // update the title and the browsing history
        var title = '';
        var query_string = '';
            
        for (var k in this.panes) {
            if (this.panes.hasOwnProperty(k)) {
                if (query_string) query_string += '&';
                query_string += k + '=' + this.panes[k].address;
                
                if (title) title += ' | ';
                title += this.panes[k].getTitleFromAddress();
            }
        }
        
        change_broswer_query_string(query_string, title);
    };

    Viewer.prototype.createPanesFromQueryString = function() {
        var self = this;
        
        // create panes from the query string
        var qs = get_query_string();
        
        if ($.isEmptyObject(qs)) {
            qs = {'p1': 'default/default/default/default'};
        }
        
        $.each(qs, function(pane_slug, value) {
            if (pane_slug && typeof self.panes !== 'undefined') {
                self.createPaneFromAddress(value, pane_slug);
            }
        });
    };
    
    Viewer.prototype.cloneAPane = function() {
        var address = null;
        for (var k in this.panes) {
            if (this.panes.hasOwnProperty(k)) {
                this.createPaneFromAddress(this.panes[k].address);
                break;
            }
        }
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
            var pane = self.panes[pane_slug] = new Pane(self, pane_slug, {'query_string': address});
            if (self.options.on_create_pane) {
                self.options.on_create_pane(pane);
            }
            self.uimodel.panes.push({slug: pane_slug});
        }
    };
    
    Viewer.prototype.getSyncedWithAddress = function(pane) {
        var ret = '';
        
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
    };
    
    Viewer.prototype.closePane = function(apane) {
        for (var i = 0; i < this.uimodel.panes.length; i++) {
            if (this.uimodel.panes[i].slug == apane.uimodel.pane_slug) {
                this.uimodel.panes.splice(i, 1);
                delete this.panes[apane.uimodel.pane_slug];
                this.updateQueryString();
                break;
            }
        }
    };

    Viewer.prototype.getPane = function(slug) {
        return this.panes[slug];
    };
    
    Viewer.prototype.getPaneCount = function() {
        return this.uimodel.panes.length;
    };

    // Returns true if <pane> can be synced.
    // That is, if there is at least one other non-synced pane in the text viewer 
    Viewer.prototype.canPaneBeSynced = function(pane) {
        var cnt = 0;

        var first_pane = null;
        $.each(this.panes, function(idx, apane) {
            first_pane = first_pane || apane;
            if (!apane.isSynced() && apane != pane) {
                cnt += 1;
            }
        });
        
        return ((first_pane != pane) && (cnt > 0));
    };

    // Request the list of documents from the API and pass it to the callback
    Viewer.prototype.copyDocumentList = function(callback) {
        var self = this;
        if (this.cache.documents && !$.isEmptyObject(this.cache.documents)) {
            callback(this.cache.documents);
        } else {
            $(document).on('tv.documents.received', function(event, documents) {
                callback(documents);
            });
            
            if (!this.cache.hasOwnProperty('documents')) {
                this.cache.documents = [];
                call_api(this.api_url, function(data) {
                    self.cache.documents = data.documents;
                    $(document).trigger('tv.documents.received', [data.documents]);
                });
            }
        }
    };

    
    /*****************************************************
     * Pane
     */
    function Pane(panes, slug, options) {
        this.uimodel = {
            pane_slug: slug,

            document: {
                slug: '',
                label: '',
            },
            documents: [],
            
            view: 'critical',
            //views: ['critical'],
            
            location_type: 'location',
            //location_types: ['1', '2'],

            location: '1',
            //locations: ['1', '2'],
            
            addresses: {},
            
            conventions: '',
            
            chunk: 'chunk',
            
            is_synced: 0,

            display_settings: [],
            
            errors: [],
        };
        
        this.panes = panes;
        this.options = options;
        this.address = null;
        this.addresses = {};
        this.requested_chunk_hash = '';
        
        this.init();
    }

    Pane.prototype.init = function() {
        // create pane from query string
        // self.options.query_string = "Fr_20125/semi-diplomatic/"
        this.requestAddress(this.options.query_string);
    };
    
    Pane.prototype.canClosePane = function() {
        return this.panes.getPaneCount() > 1;
    };
    
    Pane.prototype.closePane = function() {
        this.panes.closePane(this);
    };
    
    Pane.prototype.isSynced = function() {
        //return (~this.address_requested.indexOf('synced'));
        //return (this.view.location_type.slug == 'synced');
        return this.uimodel.is_synced;
    };

    Pane.prototype.canBeSynced = function(part_name, value) {
        // make sure we don't end up with all panes synced
        return this.panes.canPaneBeSynced(this);
    };
    
    Pane.prototype.syncWith = function(address) {
        if (this.isSynced()) {
            // todo: sync with that specific address
            //this.changeAddressPart('location_type', 'synced');
            this.requestAddress(this.address);
        }
    };
    
    Pane.prototype.openViewInNewPane = function(view_slug) {
        var parts = this.getAddressParts();
        parts.view = view_slug;
        var address = this.getAddressFromParts(parts);
        this.panes.createPaneFromAddress(address);
    };
    
    Pane.prototype.getTitleFromAddress = function() {
        var ret = '';
        var parts = this.getAddressParts();
        
        ret = parts.document + ', ' + parts.location + ' (' + parts.view + ')';
        
        return ret;
    };

    Pane.prototype.getAddressParts = function(address) {
        address = address || this.address || '';
        address = address.replace(/\/?(.*)\/?/, '$1');
        var parts = address.split('/');
        var ret = {
            'document': parts.shift() || 'default',
            'view': parts.shift() || 'default',
            'location_type': parts.shift() || 'default',
            'location': parts.shift() || 'default',
        };
        return ret;
    };

    Pane.prototype.getAddressFromParts = function(parts) {
        var ret = parts.document + '/' + parts.view + '/' + parts.location_type + '/' + parts.location;
        return ret;
    };
    
    Pane.prototype.getUIAddress = function() {
        return [this.uimodel.document.slug, this.uimodel.view.slug, this.uimodel.location_type.slug, this.uimodel.location.slug].join('/');
    };

    Pane.prototype.changeAddressPart = function(part_name, value) {
        //var parts = this.getAddressParts(this.isSynced() ? this.getUIAddress() : this.address);
        var parts = this.getAddressParts(this.address);
        parts[part_name] = value;
        return this.requestAddress(this.getAddressFromParts(parts));
    };
    
    Pane.prototype.changeAddressParts = function(aparts) {
        //var parts = this.getAddressParts(this.isSynced() ? this.getUIAddress() : this.address);
        var parts = this.getAddressParts(this.address);
        $.extend(parts, aparts);
        return this.requestAddress(this.getAddressFromParts(parts));
    };

    Pane.prototype.requestAddress = function(address) {
        // api call
        if (!this.isSynced() && address === this.address) {
            // no need for a new request
            // but we may need to update the requested address
            // in case user switched from /section/1 to /synced/1 to /section/1
            this.onReceivedAddress(address);
            return;
        }
        var self = this;
        
        var parts = this.getAddressParts(address);

        // bm: best match, if exact match doesn't work the API will return the
        // best match
        var data = {'bm': 1};
        if (this.isSynced()) {
            // we don't want best match, just exact sync
            data = {'sw': this.panes.getSyncedWithAddress(this)};
            // TVOF 133: force location_type = master.location_type
            // because at the moment the UI hides the location_type dropdown.
            // So if we starts with Whole we are stuck with it.
            parts.location_type = this.getAddressParts(data.sw).location_type;
        }

        // 2 get initial chunk
        var url = this.panes.api_url + this.getAddressFromParts(parts);
        var on_success = function(data, jqXHR, textStatus) {
            self.onRequestSuccessful(data, jqXHR, textStatus);
        };
        var on_complete = function(jqXHR, textStatus) {
            self.onRequestComplete(textStatus, jqXHR);
        };

        this.uimodel.errors = [];
        
        $('#text-viewer-glass').stop().css({'opacity': 0}).show().animate({'opacity': 0.5}, 1000);
        
        var req = call_api(url, on_success, on_complete, data, false, [this.requested_chunk_hash]);
        if (this.requested_chunk_hash === req.request_hash) {
            this.onReceivedAddress(address);
        }
        this.requested_chunk_hash = req.request_hash;
    };

    Pane.prototype.onRequestSuccessful = function(response, textStatus, jqXHR) {
        if (!response.errors) {
            this.uimodel.chunk = response.chunk;
            this.onReceivedAddress(response.address);
            this.uimodel.errors = [];
        } else {
            this.uimodel.errors = response.errors;
            this.uimodel.chunk = response.errors[0].message; 
        }
    };

    Pane.prototype.getPartMeta = function(dict) {
        var ret = {
            'slug': dict.slug,
            'label': dict.label,
        };
        if (dict.label_long) ret.label_long = dict.label_long;
        return ret;
    };
    
    // Copy document_list into this.view.documents
    // document_list is an array of {label:, slug:}
    // If document_list is undefined, retrieve it from this.panels
    // Which may incur an API request
    Pane.prototype.setDocumentList = function(document_list) {
        var self = this;
        if (document_list) {
            this.uimodel.documents.splice(0, this.uimodel.documents.length);
            for (var i = 0; i < document_list.length; i++) {
                this.uimodel.documents.push({
                    'label': document_list[i].label,
                    'slug': document_list[i].slug,
                });
            }
        } else {
            if (this.uimodel.documents.length < 1) {
                this.panes.copyDocumentList(function(document_list) {
                    self.setDocumentList(document_list);
                });
            }
        }
    };
    
    // set all the views, location types and locations for this document
    // make a request if necessary and set up temporary values
    Pane.prototype.requestAddresses = function() {
        var self = this;
        
        this.setDocumentList();
        
        var parts = this.getAddressParts();
        
        if (!self.addresses || (parts.document != self.addresses.slug)) {
            // temp values
            self.setAddresses({
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
            });
            
            if (1) {
                // let's make a new request about this document
                var url_document = this.panes.api_url + parts.document;
                call_api(url_document, function(response, jqXHR, textStatus) {
                    // save doc metadata
                    self.setAddresses(response);
                    self.renderAddresses();
                }, null, null, false);
            }
        }
        
        // TODO: why is it needed here? even if branch not executed?
        self.renderAddresses();
    };
    
    Pane.prototype.setAddresses = function(addresses) {
        this.addresses = addresses;
        $(document).trigger(this.uimodel.pane_slug+'.'+'addresses.updated', addresses);
    };

    // Update the address of the loaded chunk in self.view
    // Based on self.address and self.addresses
    Pane.prototype.renderAddresses = function() {
        var self = this;
        
        // document
        self.uimodel.document = self.getPartMeta(self.addresses);
        
        var parts = this.getAddressParts();
        
        // views
        self.uimodel.views = [];
        self.addresses.views.map(function(aview) {
            self.uimodel.views.push(self.getPartMeta(aview));
        });
        
        // Update the lists in self.view
        // by doing simple lookups in the self.views from the address parts.
        this.addresses.views.map(function(aview) {
            if (aview.slug == parts.view) {
                // view
                self.uimodel.view = self.getPartMeta(aview);
                
                // conventions
                self.uimodel.conventions = aview.conventions || '';
                
                // display_settings
                self.uimodel.display_settings = aview.display_settings || [];
                
                //var user_location_type = self.isSynced() ? 'synced': parts.location_type;
                
                // location_types
                //self.view.location_types = [];
                // locations
                //self.view.locations = [];

                aview.location_types.map(function(location_type) {
                    // location_types
                    //self.view.location_types.push(self.getPartMeta(location_type));
                    
                    if (location_type.slug == parts.location_type) {
                        
                        // location_type
                        self.uimodel.location_type = self.getPartMeta(location_type);
                        
                        location_type.locations.map(function(location) {
                            // locations
                            //self.view.locations.push(self.getPartMeta(location));
                            if (location.slug == parts.location) {
                                // location
                                self.uimodel.location = self.getPartMeta(location);
                            }
                        });
                    }
                });
            }
        });
    };

    // update the chunk address in self.view
    Pane.prototype.onReceivedAddress = function(address) {
        // update the loaded address
        // this is the real address of our this.view.chunk
        //console.log('received '+address+' had '+this.address)
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
    };

    Pane.prototype.onRequestComplete = function(textStatus, jqXHR) {
        //$('#text-viewer-glass').hide();
        $('#text-viewer-glass').stop().animate({'opacity': 0.0}, 100).hide();
        // TODO
    };

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

    function call_api(url, onSuccess, onComplete, requestData, synced, inhibiters) {
        // See http://stackoverflow.com/questions/9956255.
        // This tricks prevents caching of the fragment by the browser.
        // Without this if you move away from the page and then click back
        // it will show only the last Ajax response instead of the full HTML page.
        url = url ? url : '';
        var url_ajax = url + ((url.indexOf('?') === -1) ? '?' : '&') + 'jx=1&client=textviewer';

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
        
        var request_hash = JSON.stringify({url: getData.url, data: getData.data});
        
        var ret = {};
        if (!inhibiters || inhibiters.indexOf(request_hash) == -1) {
            ret = $.ajax(getData);
        }
        ret.request_hash = request_hash;

        return ret;
    }
    
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
        
        window.Vue.component('text-pane', {
            template: template,
            // this.apane: the attribute when creating/updating the html element
            // this.pane: the initial pane when creating the html element
            props: ['apane'],
            mounted: function() {
                var self = this;
                $(document).on(this.apane.uimodel.pane_slug+'.addresses.updated', function(event, addresses) {
                    //self.$set(self, {yo: 2};
                    // TODO: make sure this reactive
                    self.addresses = addresses;
                });
                $(window).trigger('text_viewer.pane_count_change');
            },
            data: function() {
                this.pane = this.apane;
                var ret = this.apane.uimodel;
                ret.display_settings_active = {};
                ret.location_type_filters = {};
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
                    this.pane_slug = pane.uimodel.pane_slug;
                    this.pane.requestAddress(pane.getUIAddress());
                },
                'location.slug.bk': function(val) {
                    // TODO: no longer used?
                    this.pane.changeAddressPart('location', val);
                },
                'chunk': function(val) {
                    var self = this;
                    this.$nextTick(function() {
                        // convert the hrefs to the bibliography page
                        $(this.$el).find(".text-chunk a.bibliography[href]").each(function() {
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
                            // TODO: GN: use proper server-side django html template for this
                            // would be faster, get less data from Kiln and easier for designers to edit
                            var $reveal = $(this);
                            $reveal.attr('data-panel', self.pane_slug).addClass('tv-reveal');
                            new window.Foundation.Reveal($reveal);
                        });
                                                
                        // recalc stickies...
                        var $stickies = $('.sticky:visible');
                        if ($stickies.length > 0) {
                            $stickies.foundation('_calc', true);
                        }
                        
                        // scroll to top
                        $(this.$el).find('.text-chunk').scrollTop(0);
                    });
                },
                'is_synced': function(val) {
                    this.pane.requestAddress(this.pane.address);
                },
            },
            computed: {
                views: function() {
                    return this.addresses.views;
                },
                location_types: function() {
                    var self = this;
                    var ret = null;
                    if (this.views) {
                        this.views.map(function(aview) {
                            if (aview.slug == self.view.slug) {
                                ret = aview.location_types;
                            }
                        });
                    }
                    return ret;
                },
                canBeSynced: function() {
                    return this.pane.canBeSynced(); 
                },
                getSyncTitle: function() {
                    return this.canBeSynced ? (this.is_synced ? 'Click to unsync this pane' : 'Click to synchronise this pane with another') : 'This pane cannot be synced';
                },
            },
            methods: {
                clearLocationFilter: function(location_type) {
                    this.location_type_filters[location_type.slug] = '';
                    this.filterLocations(location_type);
                },
                getPrintUrl: function() {
                    return 'print/' + this.pane.address;
                },
                filterLocations: function(location_type, event) {
                    var filter = this.location_type_filters[location_type.slug] || '';
                    filter = filter.trim().toLowerCase();
                    location_type.locations.map(function(location) {
                        window.Vue.set(location, 'hidden', location.label_long.toLowerCase().indexOf(filter) === -1);
                    });
                    
                    if (event) {
                        var target = event.srcElement || event.originalTarget;
                        var key = event.key || event.keyCode;
                        var is_enter = (key === 'Enter' || key === 13);
                        if (is_enter || key === 'ArrowDown' || key === 40) {
                            // focus on the first item in the filtered list
                            var $first_option = $(target).parents('.is-dropdown-submenu-parent').find('.submenu li').not('.hidden').first().find('a');
                            if ($first_option.length) {
                                $first_option.focus();
                                if (is_enter) {
                                    $first_option[0].click();
                                }
                            }
                        }
                    }
                },
                getFAIcon: function(location_type) {
                    var ltypes_icon = {
                        'whole': 'book',
                        'section': 'files-o',
                        'folio': 'file-text-o',
                        'paragraph': 'paragraph',
                        'seg': 'outdent',
                    };
                    return 'fa fa-'+ (ltypes_icon[location_type] || '');
                },
                onClickDocument: function(document) {
                    //this.pane.requestAddress(this.pane.getAddressFromParts(this.pane.getAddressParts(document)));
                    // We assume here that all docs support the same location_types, 
                    // so we preserve it across doc change.
                    // But we can't make the same assumption about the view
                    //this.pane.changeAddressParts({'document': document, 'view': 'default', 'location': 'default'});
                    this.pane.changeAddressParts({'document': document});
                },
                onClickView: function(view) {
                    this.pane.changeAddressPart('view', view);
                },
                onClickViewExternal: function(view) {
                    this.pane.openViewInNewPane(view);
                },
                onClickLocationType: function(location_type) {
                    this.pane.changeAddressPart('location_type', location_type);
                },
                onClickLocation: function(location, location_type) {
                    this.pane.changeAddressParts({location: location, location_type: location_type});
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
                toggleSynced: function() {
                    if (this.is_synced || this.canBeSynced) {
                        this.is_synced = !this.is_synced;
                    }
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
                    
                    var errors = this.pane.uimodel.errors;
                    if (errors && errors.length) {
                        ret += ' tv-error';
                        $.each(errors, function(idx, error) {
                            ret += ' tv-error-' + error.code;
                        });
                    }
                                        
                    return ret;
                },
                canClosePane: function() {
                    return this.pane.canClosePane();
                },
                closePane: function(apane) {
                    return this.pane.closePane();
                },
                areLocationsHidden: function() {
                    return (this.locations.length < 2 || this.is_synced); 
                },
            },
        });
    }
    
    // customisation
    
    // ===============================================================
    // Initialisation
    // TODO: move this out

    $(function() {
        window.Vue.directive('f-sticky', {
            bind: function(el) {
                window.Vue.nextTick(function () {
                    // http://foundation.zurb.com/sites/docs/sticky.html
                    var $el = $(el);
                    $el.attr('data-sticky', '');
                    $el.addClass('sticky');
                    
                    var $container = $el.parent().first();
                    $container.attr('data-sticky-container', '');
                    
                    new window.Foundation.Sticky($el);
                });
            },
            unbind: function(el) {
                // TODO: check that it actually works...
                // it seems to leave attributes with internal ids behind.
                $(el).foundation('destroy');
            },
        });
        
        function bindZFDropdownMenu($el) {
            window.Vue.nextTick(function () {
                var $opened_element = $el.find('.js-dropdown-active');
                //var $focused_filter = $el.find('.list-filter input:focus');

                // http://foundation.zurb.com/sites/docs/dropdown-menu.html
                $el.attr('data-dropdown-menu', '');
                $el.addClass('dropdown menu');
                // <!-- is-dropdown-submenu-parent: prevent FOUC -->
                $el.find('> li:has(ul)').addClass('is-dropdown-submenu-parent');
                $el.find('> li > ul').addClass('menu');

                $el.on('mouseleave.text_viewer', function() {
                    $el.find('.js-dropdown-active li a').click();
                });
                
                var options = {
                    closingTime: 50,
                    closeOnClick: true,
                    closeOnClickInside: true,
                    autoClose: true,
                    clickOpen: true,
                };
                
                // let Foundation manage the bahaviour and appearance of the DD
                new window.Foundation.DropdownMenu($el, options);

                // Leave DD open if it was already open (e.g. reinitialised)
                //$opened_element.addClass('js-dropdown-active');
                $opened_element.trigger('mouseover');
                // restore focus on filter input
                //$focused_filter.focus();
            });
        }
        
        function unbindZFDropdownMenu($el) {
            //console.log('UNBIND');
            //console.log($el);
            $el.off('mouseleave.text_viewer');
            $el.foundation('destroy');
        }

        // When a scrollable dropdown opens, we scroll to the first active item.
        // If no active element, we scroll to top (e.g. autocomplete).
        $(document).on('show.zf.dropdownmenu', function(ev, $el) {
            var $parent = $el;
            if ($parent.parent().hasClass('scrollable')) {
                var $i0 = $parent.find('.active:visible').first();
                var pos = 0;
                if ($i0.length > 0) {
                    pos = $parent.scrollTop() + $i0.position().top;
                }
                $parent.scrollTop(pos);
                $parent.parent().find('.list-filter input').focus();
            }
        });
        
        window.Vue.directive('f-dropdown', {
            componentUpdated: function(el) {
                // Foundation won't behave well with controls modified by Vue.js
                // E.g. vue adds <li> item, dropdown won't close when clicking them
                // So we re-initialise foundation on the modified control.
                // We only do it when we detect a non-initialised dropdown item.
                var $el = $(el);
                // VERY Expensive: Foundation changes all other drop downs each time
                // one selection is made in any other.
                // So we destroy and reinitialise all the drop downs each time.
                // Without this Vue.js loses track of the DOM because of 
                // Foundation's excessive manipulations.
                // TODO: implement the dropdown with Vue.js
                if ($el.find('li:not([role])').length || ($el.find('.is-dropdown-submenu-parent').length === 0)) {
                //if (1) {
                    //console.log('componentUpdated');
                    //console.log($el.find('a:first').text());
                    unbindZFDropdownMenu($el);
                    bindZFDropdownMenu($el);
                }
            },
            bind: function(el) {
                bindZFDropdownMenu($(el));
            },
            unbind: function(el) {
                unbindZFDropdownMenu($(el));
            },
        });
        
        var options = {
            //'on_create_pane': on_create_pane,
            //'on_create_viewer': on_create_viewer,
        };
        var viewer = window.text_viewer = new Viewer(options);
        
        var layout = new window.Vue({
            el: '#text-viewer',
            data: viewer.uimodel,
            methods: {
                getPane: function(slug) {
                    return viewer.getPane(slug);
                }
            }
        });
        
        // auto resize panes
        function autosize_text_viewer_contents($text_viewer) {
            var margin = 20;
            var height = $text_viewer.height() - ($('.text-chunk:first').offset().top - $text_viewer.offset().top);
            $('.text-chunk').css('height', height - margin);
            $('.pane-sidebar').css('height', height - margin);
        }
        
        $(window).on('text_viewer.pane_count_change', function() {
            autosize_text_viewer_contents($('#text-viewer'));
        });
        
        window.elastic_element(
            $('#text-viewer'), 
            autosize_text_viewer_contents,
            300, 
            $('footer').outerHeight()
        );
        
        // viewer.load('Fr_20125/critical/section/588/');
        
        // events
        
        $('section.main').on('click', 'div[data-corresp]', function() {
            if (0) {
                // GN: disabled the yellow highlight to help user find 
                // corresponding text units in // view.
                // we don't support this for the moment.
                $('section.main div[data-corresp]').removeClass('highlight');
                $(this).addClass('highlight');
            }
        });
        
        $('#btn-open-panel').on('click', function() {
            window.text_viewer.cloneAPane();
            return false;
        });
    });
    
}( window.TextViewer = window.TextViewer || {}, jQuery ));
