# -*- coding: utf-8 -*-
# Helper Functions copied from DigiPal utils.py
import re
from datetime import datetime, timedelta, tzinfo


def get_csv_response_from_rows(rows, charset='latin-1', headings=None,
                               filename='response.csv'):
    # returns a http response with a CSV content created from rows
    # rows is a list of dictionaries

    from django.http import StreamingHttpResponse
    ret = StreamingHttpResponse(generate_csv_lines_from_rows(
        rows, encoding=charset, headings=headings), content_type="text/csv")
    ret['Content-Disposition'] = 'attachment; filename="%s"' % filename

    return ret


class Echo(object):

    def write(self, value):
        return value


def generate_csv_lines_from_rows(rows, encoding=None, headings=None):
    '''
    Returns a generator of lines of comma separated values
    from a list of rows
    each row is a dictionary: column_name => value
    '''
    encoding = encoding or 'Latin-1'
    if len(rows):
        import csv
        pseudo_buffer = Echo()
        # Can't use DictWriter b/c it .writerow() doesn't return anything.
        # Normal csv.writer does return the buffer.
        writer = csv.writer(pseudo_buffer)

        headings = headings or list(rows.keys())

        yield writer.writerow(headings)
        for row in rows:
            row_encoded = [str(row.get(k, '')).encode(
                encoding, 'replace') for k in headings]
            yield writer.writerow(row_encoded)


def get_json_response(data):
    '''Returns a HttpResponse with the given data variable encoded as json'''
    from django.http.response import HttpResponse
    ret = HttpResponse(json_dumps(
        data), content_type='application/json; charset=utf-8', )
    ret['Access-Control-Allow-Origin'] = '*'
    return ret


def json_dumps(data):
    from datetime import datetime
    import json

    def json_serial(obj):
        """JSON serializer for objects not serializable by default json code"""
        if isinstance(obj, datetime):
            serial = obj.isoformat()
            return serial
        raise TypeError("Type not serializable")
    return json.dumps(data, default=json_serial)


def json_loads(data):
    # from datetime import datetime
    from django.utils.dateparse import parse_datetime
    import json

    # convert all dates in a list of dictionary from string to datetime
    def convert_dates(dic):
        if isinstance(dic, list):
            for i in range(0, len(dic)):
                if isinstance(dic[i], str):
                    # 2016-10-28T13:27:38.944298+00:00
                    v = dic[i]
                    if re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.*', v):
                        v = re.sub('(\+\d{2}):(\d{2})$', r'\1\2', v)
                        dic[i] = parse_datetime(v)
                elif isinstance(dic[i], dict) or isinstance(dic[i], list):
                    convert_dates(dic[i])
        if isinstance(dic, dict):
            for k, v in dic.items():
                if isinstance(v, str):
                    # 2016-10-28T13:27:38.944298+00:00
                    if re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.*', v):
                        v = re.sub('(\+\d{2}):(\d{2})$', r'\1\2', v)
                        dic[k] = parse_datetime(v)
                elif isinstance(v, dict) or isinstance(v, list):
                    convert_dates(v)

    ret = None
    if data and data.strip():
        ret = json.loads(data)
        convert_dates(ret)

    return ret


# A UTC class.
# Core Python has limited support time-zone aware datetimes
# We add UTC
# http://stackoverflow.com/a/2331635/3748764
class UTC(tzinfo):
    """UTC"""

    zero_offset = timedelta(0)

    def utcoffset(self, dt):
        return self.zero_offset

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return self.zero_offset


utc = UTC()


def now():
    '''Returns UTC now datetime with time-zone'''
    return datetime.now(utc)


def get_short_uid(adatetime=None):
    # The time in milliseconds in base 36
    # e.g. 2016-11-12 23:14:29.337677+05:00 -> LMXOd7f65 (9 chars)
    # result is URL safe
    # If adatetime is None, uses now()
    from datetime import datetime
    b64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.'
    BASE = len(b64)

    def num_encode(n):
        s = []
        while True:
            n, r = divmod(n, BASE)
            s.append(b64[r])
            if n == 0:
                break
        return ''.join(reversed(s))

    ret = adatetime or datetime.utcnow()
    ret = '%s%s%s%s%s%s' % (b64[ret.month], b64[ret.day], b64[ret.hour],
                            b64[ret.minute], b64[ret.second],
                            num_encode(int('%s%s' % (ret.year - 2000,
                                                      ret.microsecond))))
    # ret = ret.isoformat()
    # ret = long(re.sub(ur'\D', '', ret))
    # ret = str(ret)
    # ret = base64.b64encode(str(ret), 'ascii')
    # return parseInt((new Date()).toISOString().replace(/\D/g,
    # '')).toString(36);
    return ret


def get_int(obj, default=0):
    '''Returns an int from an obj (e.g. string)
        If the conversion fails, returns default.
    '''
    try:
        ret = int(obj)
    except:
        ret = default
    return ret


def get_int_from_roman_number(input):
    """
    From
    http://code.activestate.com/recipes/81611-roman-numerals/

    Convert a roman numeral to an integer.

    >>> r = range(1, 4000)
    >>> nums = [int_to_roman(i) for i in r]
    >>> ints = [roman_to_int(n) for n in nums]
    >>> print r == ints
    1

    >>> roman_to_int('VVVIV')
    Traceback (most recent call last):
    ...
    ValueError: input is not a valid roman numeral: VVVIV
    >>> roman_to_int(1)
    Traceback (most recent call last):
    ...
    TypeError: expected string, got <type 'int'>
    >>> roman_to_int('a')
    Traceback (most recent call last):
    ...
    ValueError: input is not a valid roman numeral: A
    >>> roman_to_int('IL')
    Traceback (most recent call last):
    ...
    ValueError: input is not a valid roman numeral: IL
    """
    if not isinstance(input, str):
        return None
    input = input.upper()
    nums = ['M', 'D', 'C', 'L', 'X', 'V', 'I']
    ints = [1000, 500, 100, 50, 10, 5, 1]
    places = []
    for c in input:
        if c not in nums:
            # raise ValueError, "input is not a valid roman num: %s" % input
            return None
    for i in range(len(input)):
        c = input[i]
        value = ints[nums.index(c)]
        # If the next place holds a larger number, this value is negative.
        try:
            nextvalue = ints[nums.index(input[i + 1])]
            if nextvalue > value:
                value *= -1
        except IndexError:
            # there is no next place.
            pass
        places.append(value)
    sum = 0
    for n in places:
        sum += n
    return sum


# _nsre = re.compile(ur'(?iu)([0-9]+|(?:\b[mdclxvi]+\b))')
REGEXP_ROMAN_NUMBER = re.compile(r'(?iu)\b[ivxlcdm]+\b')
_nsre_romans = re.compile(r'(?iu)(?:\.\s*)([ivxlcdm]+\b)')
_nsre = re.compile(r'(?iu)([0-9]+)')


def is_roman_number(astring):
    return REGEXP_ROMAN_NUMBER.match(astring) is not None


def sorted_natural(l, roman_numbers=False, is_locus=False):
    '''Sorts l and returns it. Natural sorting is applied.'''
    ret = sorted(l, key=lambda e: natural_sort_key(e, roman_numbers, is_locus))
    # make sure the empty values are at the end
    for v in [None, '', '']:
        if v in ret:
            ret.remove(v)
            ret.append(v)
    return ret


def natural_sort_key(s, roman_numbers=False, is_locus=False):
    '''
        Returns a list of tokens from a string.
        This list of tokens can be feed into a sorting function to come up with
        a natural sorting.
        Natural sorting is number-aware: e.g. 'word 2' < 'word 100'.

        If roman_numbers is True, roman numbers will be converted to ints.
        Note that there is no fool-proof was to detect roman numerals
        e.g. MS A; MS B; MS C. In this case C is a letter and not 500.
            MS A.ix In this case ix is a number
        So as a heuristic we only consider roman number if preceded by '.'

        If is_locus is True, 'face' will appear before 'dorse', etc.
    '''
    if s is None:
        s = ''

    if is_locus:
        s = re.sub(r'(?i)\b(cover)\b', '50', s)
        s = re.sub(r'(?i)\b(face|recto)\b', '100', s)
        s = re.sub(r'(?i)\b(dorse|verso)\b', '200', s)
        s = re.sub(r'(?i)\bseal\b', '300', s)

    if roman_numbers:
        while True:
            m = _nsre_romans.search(s)
            if m is None:
                break
            # convert the roman number into base 10 number
            number = get_int_from_roman_number(m.group(1))
            if number:
                # substition
                s = s[:m.start(1)] + str(number) + s[m.end(1):]

    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre, s)]


def is_unit_in_range(unitid, ranges):
    ''' e.g. ('13a1', '1a1-10b3;45b1-45b2;60b4') => True
    '''
    ret = False

    ranges = ranges.strip()

    if not ranges:
        return True

    unit_keys = natural_sort_key(unitid)

    for range in ranges.split(','):
        parts = range.split('-')
        if len(parts) == 2:
            ret = (unit_keys >= natural_sort_key(parts[0])) and (
                unit_keys <= natural_sort_key(parts[1]))
        else:
            ret = unitid == parts[0]
        if ret:
            break

    return ret


# increment the value of an item in a counter dictionary
# {item: count, item: count}
def inc_counter(dic, item, count=1):
    dic[item] = dic.get(item, 0)
    dic[item] += count
    return dic[item]


def remove_accents(input_str):
    '''Returns the input string without accented character.
        This is useful for accent-insensitive matching (e.g. autocomplete).
        >> remove_accents(u'c\\u0327   \\u00c7')
        u'c   c'
    '''
    import unicodedata
    # use 'NFD' instead of 'NFKD'
    # Otherwise the ellipsis \u2026 is tranformed into '...' and the output
    # string will have a different length
    # return remove_combining_marks(unicodedata.normalize('NFKD',
    # unicode(input_str)))
    return remove_combining_marks(unicodedata.normalize('NFD',
                                                        str(input_str)))


def remove_combining_marks(input_str):
    '''Returns the input unicode string without the combining marks found
    as 'individual character'
        >> remove_combining_marks(u'c\\u0327   \\u00c7')
        u'c   \\u00c7'
    '''
    import unicodedata
    return "".join([c for c in str(input_str)
                     if not unicodedata.combining(c)])
