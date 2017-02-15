#  Copyright 2008-2015 Nokia Solutions and Networks
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import copy
import os.path

from robotide.lib.robot.output import LOGGER
from robotide.lib.robot.errors import FrameworkError
from robotide.lib.robot.utils import normpath, seq2str2, is_string

from .builder import ResourceFileBuilder
from .handlerstore import HandlerStore
from .testlibraries import TestLibrary


class Importer(object):

    def __init__(self):
        self._library_cache = ImportCache()
        self._resource_cache = ImportCache()

    def reset(self):
        self.__init__()

    def import_library(self, name, args, alias, variables):
        lib = TestLibrary(name, args, variables, create_handlers=False)
        positional, named = lib.positional_args, lib.named_args
        lib = self._import_library(name, positional, named, lib)
        if alias:
            alias = variables.replace_scalar(alias)
            lib = self._copy_library(lib, alias)
            LOGGER.info("Imported library '%s' with name '%s'" % (name, alias))
        return lib

    def import_resource(self, path):
        if path in self._resource_cache:
            LOGGER.info("Found resource file '%s' from cache" % path)
        else:
            resource = ResourceFileBuilder().build(path)
            self._resource_cache[path] = resource
        return self._resource_cache[path]

    def _import_library(self, name, positional, named, lib):
        args = positional + ['%s=%s' % arg for arg in sorted(named.items())]
        key = (name, positional, named)
        if key in self._library_cache:
            LOGGER.info("Found test library '%s' with arguments %s from cache"
                        % (name, seq2str2(args)))
            return self._library_cache[key]
        lib.create_handlers()
        self._library_cache[key] = lib
        self._log_imported_library(name, args, lib)
        return lib

    def _log_imported_library(self, name, args, lib):
        type = lib.__class__.__name__.replace('Library', '').lower()[1:]
        listener = ', with listener' if lib.has_listener else ''
        LOGGER.info("Imported library '%s' with arguments %s "
                    "(version %s, %s type, %s scope, %d keywords%s)"
                    % (name, seq2str2(args), lib.version or '<unknown>',
                       type, lib.scope.lower(), len(lib), listener))
        if not lib and not lib.has_listener:
            LOGGER.warn("Imported library '%s' contains no keywords" % name)

    def _copy_library(self, lib, newname):
        # TODO: This won't work if lib.handlers has kws w/ embedded args.
        # Need better way to re-initialize libs when imported using WITH NAME.
        libcopy = copy.copy(lib)
        libcopy.name = newname
        libcopy.init_scope_handling()
        libcopy.handlers = HandlerStore(lib.handlers._source)
        for handler in lib.handlers:
            handcopy = copy.copy(handler)
            handcopy.library = libcopy
            libcopy.handlers.add(handcopy)
        return libcopy


class ImportCache:
    """Keeps track on and optionally caches imported items.

    Handles paths in keys case-insensitively on case-insensitive OSes.
    Unlike dicts, this storage accepts mutable values in keys.
    """

    def __init__(self):
        self._keys = []
        self._items = []

    def __setitem__(self, key, item):
        if not is_string(key) and not isinstance(key, tuple):
            raise FrameworkError('Invalid key for ImportCache')
        key = self._norm_path_key(key)
        if key not in self._keys:
            self._keys.append(key)
            self._items.append(item)
        else:
            self._items[self._keys.index(key)] = item

    def add(self, key, item=None):
        self.__setitem__(key, item)

    def __getitem__(self, key):
        key = self._norm_path_key(key)
        if key not in self._keys:
            raise KeyError
        return self._items[self._keys.index(key)]

    def __contains__(self, key):
        return self._norm_path_key(key) in self._keys

    def values(self):
        return self._items

    def _norm_path_key(self, key):
        if self._is_path(key):
            return normpath(key, case_normalize=True)
        if isinstance(key, tuple):
            return tuple(self._norm_path_key(k) for k in key)
        return key

    def _is_path(self, key):
        return is_string(key) and os.path.isabs(key) and os.path.exists(key)
