from   __future__     import unicode_literals
from   collections    import OrderedDict
import pytest
from   javaproperties import InvalidUEscapeError, loads

def test_loads_simple():
    assert loads('key=value') == {"key": "value"}

def test_loads_key_only():
    assert loads("key") == {"key": ""}

def test_loads_key_space_only():
    assert loads("key ") == {"key": ""}

def test_loads_space_equals():
    assert loads("key =value") == {"key": "value"}

def test_loads_equals_space():
    assert loads("key= value") == {"key": "value"}

def test_loads_padded_equals():
    assert loads("key = value") == {"key": "value"}

def test_loads_nokey():
    assert loads("=value") == {"": "value"}

def test_loads_spacekey():
    assert loads(" =value") == {"": "value"}

def test_loads_trailing_space():
    assert loads("key=value ") == {"key": "value "}

def test_loads_leading_space():
    assert loads(" key=value") == {"key": "value"}

def test_loads_space_equals_space():
    assert loads(' = ') == {"": ""}

def test_loads_equals_only():
    assert loads('=') == {"": ""}

def test_loads_nothing():
    assert loads('') == {}

def test_loads_space():
    assert loads(' ') == {}

def test_loads_linefeed():
    assert loads('\n') == {}

def test_loads_crlf():
    assert loads('\r\n') == {}

def test_loads_cr():
    assert loads('\r') == {}

def test_loads_comment():
    assert loads('#This is a comment.') == {}

def test_loads_comment_key_value():
    assert loads('#This is a comment.\nkey = value') == {"key": "value"}

def test_loads_key_value_comment():
    assert loads('key = value\n#This is a comment.') == {"key": "value"}

def test_loads_bang_comment():
    assert loads('!This is a comment.') == {}

def test_loads_bang_comment_key_value():
    assert loads('!This is a comment.\nkey = value') == {"key": "value"}

def test_loads_key_value_bang_comment():
    assert loads('key = value\n!This is a comment.') == {"key": "value"}

def test_loads_continued_value():
    assert loads('key = val\\\nue') == {"key": "value"}

def test_loads_continued_value_spaced():
    assert loads('key = val\\\n    ue') == {"key": "value"}

def test_loads_space_continued_value():
    assert loads('key = val \\\nue') == {"key": "val ue"}

def test_loads_space_continued_value_spaced():
    assert loads('key = val \\\n  ue') == {"key": "val ue"}

def test_loads_continued_key():
    assert loads('ke\\\ny = value') == {"key": "value"}

def test_loads_continued_key_spaced():
    assert loads('ke\\\n    y = value') == {"key": "value"}

def test_loads_three_words():
    assert loads('one two three') == {"one": "two three"}

def test_loads_simple_linefeed():
    assert loads('key=value\n') == {"key": "value"}

def test_loads_simple_crlf():
    assert loads('key=value\r\n') == {"key": "value"}

def test_loads_simple_cr():
    assert loads('key=value\r') == {"key": "value"}

def test_loads_key_colon_value():
    assert loads('key:value') == {"key": "value"}

def test_loads_key_space_value():
    assert loads('key value') == {"key": "value"}

def test_loads_surrogate_pair():
    assert loads('goat = \\uD83D\\uDC10') == {"goat": "\U0001F410"}

def test_loads_bad_surrogate():
    assert loads('taog = \\uDC10\\uD83D') == {"taog": "\uDC10\uD83D"}

def test_loads_raw_surrogate_pair():
    assert loads('goat = \uD83D\uDC10') == {"goat": "\U0001F410"}

def test_loads_half_raw_surrogate_pair():
    assert loads('goat = \uD83D\\uDC10') == {"goat": "\U0001F410"}

def test_loads_raw_half_surrogate_pair():
    assert loads('goat = \\uD83D\uDC10') == {"goat": "\U0001F410"}

def test_loads_bad_raw_surrogate():
    assert loads('taog = \uDC10\uD83D') == {"taog": "\uDC10\uD83D"}

def test_loads_blank_continue_comment():
    assert loads('\\\n# comment') == {"#": "comment"}

def test_loads_space_continue_comment():
    assert loads('   \\\n# comment') == {"#": "comment"}

def test_loads_continue_comment():
    assert loads('key = value\\\n    # comment') == {"key": "value# comment"}

def test_loads_continue_empty():
    assert loads('key = value\\\n') == {"key": "value"}

def test_loads_continue_EOF():
    assert loads('key = value\\') == {"key": "value"}

def test_loads_continue_space():
    assert loads('key = value\\\n    ') == {"key": "value"}

def test_loads_comment_continue():
    assert loads('# comment\\\nkey = value') == {"key": "value"}

def test_loads_blank_continue():
    assert loads('\\\n') == {}

def test_loads_continue_pair():
    assert loads('\\\nkey = value') == {"key": "value"}

def test_loads_space_continue_pair():
    assert loads(' \\\nkey = value') == {"key": "value"}

def test_loads_multiple():
    assert loads('key = value\nfoo = bar') == {"key": "value", "foo": "bar"}

def test_loads_multiple_crlf():
    assert loads('key = value\r\nfoo = bar') == {"key": "value", "foo": "bar"}

def test_loads_multiple_cr():
    assert loads('key = value\rfoo = bar') == {"key": "value", "foo": "bar"}

def test_loads_multiple_ordereddict():
    assert loads('key = value\nfoo = bar', object_pairs_hook=OrderedDict) == \
        OrderedDict([("key", "value"), ("foo", "bar")])

def test_loads_multiple_ordereddict_rev():
    assert loads('foo = bar\nkey = value', object_pairs_hook=OrderedDict) == \
        OrderedDict([("foo", "bar"), ("key", "value")])

def test_loads_reassign():
    assert loads('key = value1\nkey = value2') == {"key": "value2"}

def test_loads_bmp_escape():
    assert loads('snowman = \\u2603') == {"snowman": "\u2603"}

def test_loads_latin1_escape():
    assert loads('pokmon = \\u00E9') == {"pokmon": "\u00E9"}

def test_loads_long_escape():
    assert loads('newline = \\u000a') == {"newline": "\n"}

def test_loads_continue_continue():
    assert loads('key = value\\\n\\\nend') == {"key": "valueend"}

def test_loads_continue_space_continue():
    assert loads('key = value\\\n    \\\nend') == {"key": "valueend"}

def test_loads_escaped_continue():
    assert loads('key = value\\\\\nend') == {"key": "value\\", "end": ""}

def test_loads_hash_in_key():
    assert loads('c#sharp = sucks') == {"c#sharp": "sucks"}

def test_loads_hash_in_value():
    assert loads('fifth = #5') == {"fifth": "#5"}

def test_loads_latin_1():
    assert loads('edh = \xF0') == {"edh": "\xF0"}

def test_loads_non_latin_1():
    assert loads('snowman = \u2603') == {"snowman": "\u2603"}

def test_loads_astral_plane():
    assert loads('goat = \U0001F410') == {"goat": "\U0001F410"}

def test_loads_esc_n():
    assert loads('newline = \\n') == {"newline": "\n"}

def test_loads_esc_r():
    assert loads('carriage.return = \\r') == {"carriage.return": "\r"}

def test_loads_esc_t():
    assert loads('tab = \\t') == {"tab": "\t"}

def test_loads_esc_f():
    assert loads('form.feed = \\f') == {"form.feed": "\f"}

def test_loads_space_in_key():
    assert loads('two\\ words = one key') == {"two words": "one key"}

def test_loads_colon_in_key():
    assert loads('hour\\:minute = 1440') == {"hour:minute": "1440"}

def test_loads_equals_in_key():
    assert loads('E\\=mc^2 = Einstein') == {"E=mc^2": "Einstein"}

def test_loads_double_backslash():
    assert loads('two\\\\ words = not a key') == {"two\\": "words = not a key"}

def test_loads_triple_backslash():
    assert loads('two\\\\\\ words = one key') == {"two\\ words": "one key"}

def test_loads_bad_esc_zero():
    assert loads('invalid-escape = \\0') == {"invalid-escape": "0"}

def test_loads_bad_esc_q():
    assert loads('invalid-escape = \\q') == {"invalid-escape": "q"}

def test_loads_bad_esc_question():
    assert loads('invalid-escape = \\?') == {"invalid-escape": "?"}

def test_loads_bad_esc_hex():
    assert loads('invalid-escape = \\x40') == {"invalid-escape": "x40"}

def test_loads_leading_space_in_key():
    assert loads(' \\ key = value') == {" key": "value"}

def test_loads_leading_unicode_space_in_key():
    assert loads(' \\u0020key = value') == {" key": "value"}

def test_loads_leading_space_before_key():
    assert loads(' \\  key = value') == {" ": "key = value"}

def test_loads_leading_space_in_value():
    assert loads('key = \\  value') == {"key": "  value"}

def test_loads_blank_simple():
    assert loads('\nkey = value') == {"key": "value"}

def test_loads_space_blank_simple():
    assert loads(' \nkey = value') == {"key": "value"}

def test_loads_simple_blank():
    assert loads('key = value\n') == {"key": "value"}

def test_loads_simple_blank_space():
    assert loads('key = value\n ') == {"key": "value"}

def test_loads_simple_blank_simple():
    assert loads('key = value\n\nfoo = bar') == {"key": "value", "foo": "bar"}

def test_loads_simple_blank_space_simple():
    assert loads('key = value\n \nfoo = bar') == {"key": "value", "foo": "bar"}

def test_loads_latin1_bytes():
    assert loads(b'key=value\nedh=\xF0') == {"key": "value", "edh": "\xF0"}

def test_loads_utf8_bytes():
    assert loads(
        b'key=value\n'
        b'edh=\xC3\xB0\n'
        b'snowman=\xE2\x98\x83\n'
        b'goat=\xF0\x9F\x90\x90'
    ) == {
        'key': 'value',
        'edh': '\xC3\xB0',
        'snowman': '\xE2\x98\x83',
        'goat': '\xF0\x9F\x90\x90',
    }

def test_loads_tab_separator():
    assert loads('key\tvalue=pair') == {"key": "value=pair"}

def test_loads_escaped_tab():
    assert loads('key\\\tvalue=pair') == {"key\tvalue": "pair"}

def test_loads_form_feed_separator():
    assert loads('key\fvalue=pair') == {"key": "value=pair"}

def test_loads_escaped_form_feed():
    assert loads('key\\\fvalue=pair') == {"key\fvalue": "pair"}

def test_loads_u_hex_invalid():
    with pytest.raises(InvalidUEscapeError) as excinfo:
        loads('bad = \\uabcx')
    assert excinfo.value.escape == '\\uabcx'
    assert str(excinfo.value) == 'Invalid \\u escape sequence: \\uabcx'
    with pytest.raises(InvalidUEscapeError) as excinfo:
        loads('\\uabcx = bad')
    assert excinfo.value.escape == '\\uabcx'
    assert str(excinfo.value) == 'Invalid \\u escape sequence: \\uabcx'

def test_loads_u_hex_space():
    with pytest.raises(InvalidUEscapeError) as excinfo:
        loads('bad = \\uabc ')
    assert excinfo.value.escape == '\\uabc '
    assert str(excinfo.value) == 'Invalid \\u escape sequence: \\uabc '
    with pytest.raises(InvalidUEscapeError) as excinfo:
        loads('\\uabc  = bad')
    assert excinfo.value.escape == '\\uabc'
    assert str(excinfo.value) == 'Invalid \\u escape sequence: \\uabc'

def test_loads_u_hex_eof():
    with pytest.raises(InvalidUEscapeError) as excinfo:
        loads('bad = \\uabc')
    assert excinfo.value.escape == '\\uabc'
    assert str(excinfo.value) == 'Invalid \\u escape sequence: \\uabc'
    with pytest.raises(InvalidUEscapeError) as excinfo:
        loads('\\uabc = bad')
    assert excinfo.value.escape == '\\uabc'
    assert str(excinfo.value) == 'Invalid \\u escape sequence: \\uabc'

def test_loads_u_invalid_hex():
    with pytest.raises(InvalidUEscapeError) as excinfo:
        loads('bad = \\uxabc')
    assert excinfo.value.escape == '\\uxabc'
    assert str(excinfo.value) == 'Invalid \\u escape sequence: \\uxabc'
    with pytest.raises(InvalidUEscapeError) as excinfo:
        loads('\\uxabc = bad')
    assert excinfo.value.escape == '\\uxabc'
    assert str(excinfo.value) == 'Invalid \\u escape sequence: \\uxabc'

def test_loads_u_space_hex():
    with pytest.raises(InvalidUEscapeError) as excinfo:
        loads('bad = \\u abcx')
    assert excinfo.value.escape == '\\u abc'
    assert str(excinfo.value) == 'Invalid \\u escape sequence: \\u abc'
    with pytest.raises(InvalidUEscapeError) as excinfo:
        loads('\\u abcx = bad')
    assert excinfo.value.escape == '\\u'
    assert str(excinfo.value) == 'Invalid \\u escape sequence: \\u'

def test_loads_u_eof():
    with pytest.raises(InvalidUEscapeError) as excinfo:
        loads('bad = \\u')
    assert excinfo.value.escape == '\\u'
    assert str(excinfo.value) == 'Invalid \\u escape sequence: \\u'
    with pytest.raises(InvalidUEscapeError) as excinfo:
        loads('\\u')
    assert excinfo.value.escape == '\\u'
    assert str(excinfo.value) == 'Invalid \\u escape sequence: \\u'

def test_loads_u_invalid_eof():
    with pytest.raises(InvalidUEscapeError) as excinfo:
        loads('bad = \\ux')
    assert excinfo.value.escape == '\\ux'
    assert str(excinfo.value) == 'Invalid \\u escape sequence: \\ux'
    with pytest.raises(InvalidUEscapeError) as excinfo:
        loads('\\ux = bad')
    assert excinfo.value.escape == '\\ux'
    assert str(excinfo.value) == 'Invalid \\u escape sequence: \\ux'

def test_loads_u_space_eof():
    with pytest.raises(InvalidUEscapeError) as excinfo:
        loads('bad = \\u ')
    assert excinfo.value.escape == '\\u '
    assert str(excinfo.value) == 'Invalid \\u escape sequence: \\u '
    with pytest.raises(InvalidUEscapeError) as excinfo:
        loads('\\u  = bad')
    assert excinfo.value.escape == '\\u'
    assert str(excinfo.value) == 'Invalid \\u escape sequence: \\u'

def test_loads_u_hex_sep():
    with pytest.raises(InvalidUEscapeError) as excinfo:
        loads('\\uab=bad')
    assert excinfo.value.escape == '\\uab'
    assert str(excinfo.value) == 'Invalid \\u escape sequence: \\uab'
    with pytest.raises(InvalidUEscapeError) as excinfo:
        loads('\\uab:bad')
    assert excinfo.value.escape == '\\uab'
    assert str(excinfo.value) == 'Invalid \\u escape sequence: \\uab'
    with pytest.raises(InvalidUEscapeError) as excinfo:
        loads('\\uab bad')
    assert excinfo.value.escape == '\\uab'
    assert str(excinfo.value) == 'Invalid \\u escape sequence: \\uab'

def test_loads_u_escaped_escape():
    with pytest.raises(InvalidUEscapeError) as excinfo:
        loads('bad = \\uab\\cd')
    assert excinfo.value.escape == '\\uab\\c'
    assert str(excinfo.value) == 'Invalid \\u escape sequence: \\uab\\c'

def test_loads_u_u_escape_escape():
    with pytest.raises(InvalidUEscapeError) as excinfo:
        loads('bad = \\uab\\u0063d')
    assert excinfo.value.escape == '\\uab\\u'
    assert str(excinfo.value) == 'Invalid \\u escape sequence: \\uab\\u'

def test_loads_u_extra():
    assert loads('the = \\u00f0e') == {"the": "\xF0e"}
    assert loads('\\u00f0e = the') == {"\xF0e": "the"}

def test_loads_big_U_escape():
    assert loads('goat = \\U0001F410') == {"goat": "U0001F410"}

def test_loads_key_unicode_eq_value():
    assert loads('key\\u003Dvalue') == {"key=value": ""}

def test_loads_key_unicode_colon_value():
    assert loads('key\\u003Avalue') == {"key:value": ""}

def test_loads_key_unicode_space_value():
    assert loads('key\\u0020value') == {"key value": ""}

def test_loads_escaped_u():
    assert loads('key=\\\\u2603') == {"key": "\\u2603"}

def test_loads_escaped_u_invalid():
    assert loads('key=\\\\u260x') == {"key": "\\u260x"}
