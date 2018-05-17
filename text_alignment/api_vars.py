from collections import OrderedDict


class API_Vars(object):
    '''
    Holds the definition and values of a list of variables.
    Allows the defs and values to be interchanged with a query string
    or a dictionary.
    Support different types of variables:
        * multi-select (multi)
        * single-select (single)
        * interval of numbers (range)
    '''

    def __init__(self, vars=None):
        self.vars = OrderedDict()
        if vars:
            for var in vars:
                self.add(var)

    def add(self, var):
        # complete and transform the dictionary

        options_selected = var.get('selected', [])
        options_default = var.get('default', [])
        if var['options'] and not isinstance(var['options'][0], dict):
            options = []
            for name in var['options']:
                option_key = get_key_from_name(name)
                options.append({
                    'key': option_key,
                    'name': name,
                    'selected': option_key in options_selected,
                    'default': option_key in options_default,
                })

            var['options'] = options

        assert(var.get('key') or var.get('name'))
        assert(var.get('type'))

        var['key'] = var.get('key', var.get('name'))
        var['name'] = var.get('name', var.get('key').title())

        # add it to our list of vars

        self.vars[var['key']] = var

    def _set_selected(self):
        # Help vue.js to manage radio button
        # by placing a single selected value directly under the var.
        # Also helps javascript to quickly access selected values.
        for var in self.vars.values():
            var['selected'] = self.get(var['key'], var['type'] == 'single')

    def get_dict(self):
        self._set_selected()
        return dict(self.vars)

    def get_list(self):
        self._set_selected()
        ret = [var for var in self.vars.values()]
        return ret

    def set_vars(self, keys_values):
        for name, values in keys_values:
            self.set(name, values)

    def reset_vars_from_request(self, request):
        for var in self.vars.values():
            values = request.GET.get(var['key'], None)

            self.set(var['key'], values)

    def set(self, akey, values=None):
        '''
        values = ['option1_key', 'option3_key']
        values = 'option1_key,option3_key'
        values = 'all'
        values = None => reset to default
        values = []
        '''

        if hasattr(values, 'split'):
            values = values.split(',')

        if values:
            values = [v.strip() for v in values]

        for option in self.vars[akey]['options']:
            if values is None:
                option['selected'] = option['default']
                continue
            option['selected'] = ('all' in values) or (option['key'] in values)

    def get(self, akey, first=False, prop='key'):
        ret = [
            option.get(prop)
            for option
            in self.vars[akey]['options']
            if option.get('selected')
        ]

        if first:
            ret = ret[0]

        return ret

    def get_str(self, akey, first=False):
        ret = self.get(akey, first)
        ret = ','.join(ret)
        return ret

    def get_query_string(self):
        import urllib
        ret = '&'.join([
            ('%s=%s' % (
                urllib.quote(akey, ','),
                urllib.quote(self.get_str(akey), ',')
            ))
            for akey
            in self.vars
        ])
        return ret


def get_key_from_name(name):
    import re
    return re.sub(ur'[^\w_]+', r'-', name.lower()).strip()


def get_name_from_key(akey):
    import re
    return re.sub(ur'[_]', r' ', akey.title()).strip()
