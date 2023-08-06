# Author: echel0n <echel0n@sickrage.ca>
# URL: https://sickrage.ca
#
# This file is part of SickRage.
#
# SickRage is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SickRage is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SickRage.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import codecs
import functools
import importlib
import locale
import os
import sys
import types
import unicodedata

import six
from chardet import detect

import sickrage


def get_sys_encoding():
    # map the following codecs to utf-8
    codecs.register(lambda name: codecs.lookup('utf-8') if name == 'cp65001' else None)
    codecs.register(lambda name: codecs.lookup('utf-8') if name == 'cp1252' else None)

    # get locale encoding
    try:
        locale.setlocale(locale.LC_ALL, "")
        encoding = locale.getpreferredencoding()
    except (locale.Error, IOError):
        encoding = None

    # enforce UTF-8
    if not encoding or codecs.lookup(encoding).name == 'ascii':
        encoding = 'UTF-8'

    # wrap i/o in unicode
    sys.stdout = codecs.getwriter(encoding)(sys.stdout)
    sys.stdin = codecs.getreader(encoding)(sys.stdin)

    return encoding


def ek(f):
    """
    Encoding Kludge: Call function with arguments and six.text_type-encode output

    :param f:  Function to call
    :return: Unicode-converted function output (string, list or tuple, depends on input)
    """

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if os.name == 'nt':
            result = f(*args, **kwargs)
        else:
            result = f(*[ss(x) if isinstance(x, six.string_types) else x for x in args], **kwargs)

        return convert(result)

    return wrapper


def ss(var):
    """
    Converts six.string_types to SYS_ENCODING, fallback encoding is forced UTF-8

    :param var: String to convert
    :return: Converted string
    """

    var = to_unicode(var)

    try:
        var = var.encode(sickrage.app.sys_encoding)
    except Exception:
        try:
            var = var.encode('utf-8')
        except Exception:
            try:
                var = var.encode(sickrage.app.sys_encoding, 'replace')
            except Exception:
                try:
                    var = var.encode('utf-8', 'ignore')
                except Exception:
                    pass

    return var


def convert(var):
    if isinstance(var, dict):
        return {convert(key): convert(value) for key, value in var.iteritems()}
    elif isinstance(var, (types.GeneratorType, list, tuple)):
        return [convert(element) for element in var]
    elif isinstance(var, str):
        return to_unicode(var)

    return var


def to_unicode(var):
    """
    Converts string to Unicode, using in order: UTF-8, Latin-1, System encoding or finally what chardet wants

    :param var: String to convert
    :return: Converted string as six.text_type, fallback is System encoding
    """

    if isinstance(var, str):
        try:
            var = six.text_type(var)
        except Exception:
            try:
                var = six.text_type(var, 'utf-8')
            except Exception:
                try:
                    var = six.text_type(var, 'latin-1')
                except Exception:
                    try:
                        var = six.text_type(var, sickrage.app.sys_encoding)
                    except Exception:
                        try:
                            # Chardet can be wrong, so try it last
                            var = six.text_type(var, detect(var).get('encoding'))
                        except Exception:
                            var = six.text_type(var, sickrage.app.sys_encoding, 'replace')

    return var


def strip_accents(name):
    try:
        # strip accents
        try:
            name.decode('ascii')
        except UnicodeEncodeError:
            pass

        name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore')
    except UnicodeDecodeError:
        pass

    return name


def patch_modules():
    _modules = ['io.open',
                'os.access',
                'os.makedirs',
                'os.remove',
                'os.chdir',
                'os.listdir',
                'os.unlink',
                'os.symlink',
                'os.rmdir',
                'os.stat',
                'os.mkdir',
                'os.chmod',
                'os.chown',
                'os.utime',
                'os.walk',
                'os.statvfs',
                'os.rename',
                'os.renames',
                'os.path.join',
                'os.path.normpath',
                'os.path.basename',
                'os.path.exists',
                'os.path.abspath',
                'os.path.isfile',
                'os.path.isdir',
                'os.path.islink',
                'os.path.isabs',
                'os.path.realpath',
                'os.path.normcase',
                'os.path.dirname',
                'shutil.rmtree',
                'shutil.copymode',
                'shutil.move',
                'shutil.copyfileobj',
                'shutil.copy',
                'shutil.copyfile']

    def decorate_modules(modules, decorator):
        for module in modules:
            module_name, method_name = module.rsplit('.', 1)
            pkg = importlib.import_module(module_name)
            method = getattr(pkg, method_name, None)
            if isinstance(method, (types.FunctionType, types.BuiltinFunctionType)):
                setattr(pkg, method_name, decorator(method))

    decorate_modules(_modules, ek)
