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
            var['options'] = [
                {
                    'key': name.lower().strip(),
                    'name': name,
                    'selected': name in options_selected,
                    'default': name in options_default,
                }
                for name
                in var['options']
            ]

        assert(var.get('key') or var.get('name'))
        assert(var.get('type'))

        var['key'] = var.get('key', var.get('name'))
        var['name'] = var.get('name', var.get('key').title())

        # add it to our list of vars

        self.vars[var['key']] = var

    def get_dict(self):
        ret = [var for var in self.vars.values()]
        # Help vue.js to manage radio button
        # by placing a single selected value directly under the var.
        for var in self.vars.values():
            if var['type'] == 'single':
                var['selected'] = self.get(var['key'], True)
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

    def get(self, akey, first=False):
        ret = [
            option['key']
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
    return re.sub(ur'[^\W_]+', r'-', name.lower()).strip()


def get_name_from_key(akey):
    import re
    return re.sub(ur'[_]', r' ', akey.title()).strip()
