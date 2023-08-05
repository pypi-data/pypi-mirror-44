# Python module
# Common functions

# Copyright (c) 2005-2014 Red Hat, Inc.
#
#    Koji is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation;
#    version 2.1 of the License.
#
#    This software is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this software; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
# Authors:
#       Mike McLean <mikem@redhat.com>
#       Mike Bonnet <mikeb@redhat.com>


from __future__ import absolute_import
from __future__ import division
import sys
from six.moves import range
from six.moves import zip
import six
krbV = None
try:
    import krbV
except ImportError:  # pragma: no cover
    pass
import base64
import datetime
dns_resolver = None
try:
    import dns.resolver as dns_resolver
except ImportError:  # pragma: no cover
    pass
import six.moves.configparser
import errno
from fnmatch import fnmatch
import six.moves.http_client
import imp
import logging
import logging.handlers
SSL_Error = None
try:
    from OpenSSL.SSL import Error as SSL_Error
except Exception:  # pragma: no cover
    # the hub imports koji, and sometimes this import fails there
    # see: https://cryptography.io/en/latest/faq/#starting-cryptography-using-mod-wsgi-produces-an-internalerror-during-a-call-in-register-osrandom-engine
    # unfortunately the workaround at the above link does not always work, so
    # we ignore it here
    pass
import optparse
import os
import os.path
import pwd
import random
import re
import requests
try:
    import requests_kerberos
except ImportError:  # pragma: no cover
    requests_kerberos = None
import rpm
import shutil
import signal
import socket
import struct
import tempfile
import time
import traceback
import warnings
import xml.sax
import xml.sax.handler
import six.moves.urllib
from . import util
from koji.xmlrpcplus import getparser, loads, dumps, Fault, xmlrpc_client


PROFILE_MODULES = {}  # {module_name: module_instance}

def _(args):
    """Stub function for translation"""
    return args  # pragma: no cover

## Constants ##

RPM_HEADER_MAGIC = six.b('\x8e\xad\xe8')
RPM_TAG_HEADERSIGNATURES = 62
RPM_TAG_FILEDIGESTALGO = 5011
RPM_SIGTAG_PGP = 1002
RPM_SIGTAG_MD5 = 1004
RPM_SIGTAG_GPG = 1005

RPM_FILEDIGESTALGO_IDS = {
    # Taken from RFC 4880
    # A missing algo ID means md5
    None: 'MD5',
    1:    'MD5',
    2:    'SHA1',
    3:    'RIPEMD160',
    8:    'SHA256',
    9:    'SHA384',
    10:   'SHA512',
    11:   'SHA224'
    }

# rpm 4.12 introduces optional deps, but they can also be backported in some
# rpm installations. So, we need to check their real support, not only rpm
# version.
SUPPORTED_OPT_DEP_HDRS = {}
for h in (
        'SUGGESTNAME', 'SUGGESTVERSION', 'SUGGESTFLAGS',
        'ENHANCENAME', 'ENHANCEVERSION', 'ENHANCEFLAGS',
        'SUPPLEMENTNAME', 'SUPPLEMENTVERSION', 'SUPPLEMENTFLAGS',
        'RECOMMENDNAME', 'RECOMMENDVERSION', 'RECOMMENDFLAGS'):
    SUPPORTED_OPT_DEP_HDRS[h] = hasattr(rpm, 'RPMTAG_%s' % h)


class Enum(dict):
    """A simple class to track our enumerated constants

    Can quickly map forward or reverse
    """

    def __init__(self, *args):
        self._order = tuple(*args)
        super(Enum, self).__init__([(value, n) for n, value in enumerate(self._order)])

    def __getitem__(self, key):
        if isinstance(key, (int, slice)):
            return self._order.__getitem__(key)
        else:
            return super(Enum, self).__getitem__(key)

    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except (IndexError, KeyError):
            return default

    def getnum(self, key, default=None):
        try:
            value = self.__getitem__(key)
        except (IndexError, KeyError):
            return default
        if isinstance(key, int):
            return key
        else:
            return value

    def _notImplemented(self, *args, **opts):
        raise NotImplementedError

    # deprecated
    getvalue = _notImplemented
    #read-only
    __setitem__ = _notImplemented
    __delitem__ = _notImplemented
    clear = _notImplemented
    pop = _notImplemented
    popitem = _notImplemented
    update = _notImplemented
    setdefault = _notImplemented

API_VERSION = 1

TASK_STATES = Enum((
    'FREE',
    'OPEN',
    'CLOSED',
    'CANCELED',
    'ASSIGNED',
    'FAILED',
))

BUILD_STATES = Enum((
    'BUILDING',
    'COMPLETE',
    'DELETED',
    'FAILED',
    'CANCELED',
))

USERTYPES = Enum((
    'NORMAL',
    'HOST',
    'GROUP',
))

USER_STATUS = Enum((
    'NORMAL',
    'BLOCKED',
))

# authtype values
# normal == username/password
AUTHTYPE_NORMAL = 0
AUTHTYPE_KERB = 1
AUTHTYPE_SSL = 2
AUTHTYPE_GSSAPI = 3

#dependency types
DEP_REQUIRE = 0
DEP_PROVIDE = 1
DEP_OBSOLETE = 2
DEP_CONFLICT = 3
DEP_SUGGEST = 4
DEP_ENHANCE = 5
DEP_SUPPLEMENT = 6
DEP_RECOMMEND = 7

#dependency flags
RPMSENSE_LESS = 2
RPMSENSE_GREATER = 4
RPMSENSE_EQUAL = 8

# repo states
REPO_STATES = Enum((
    'INIT',
    'READY',
    'EXPIRED',
    'DELETED',
    'PROBLEM',
))
# for backwards compatibility
REPO_INIT = REPO_STATES['INIT']
REPO_READY = REPO_STATES['READY']
REPO_EXPIRED = REPO_STATES['EXPIRED']
REPO_DELETED = REPO_STATES['DELETED']
REPO_PROBLEM = REPO_STATES['PROBLEM']

REPO_MERGE_MODES = set(['koji', 'simple'])

# buildroot states
BR_STATES = Enum((
    'INIT',
    'WAITING',
    'BUILDING',
    'EXPIRED',
))

BR_TYPES = Enum((
    'STANDARD',
    'EXTERNAL',
))

TAG_UPDATE_TYPES = Enum((
    'VOLUME_CHANGE',
    'IMPORT',
    'MANUAL',
))

CHECKSUM_TYPES = Enum((
    'md5',
    'sha1',
    'sha256',
))

#PARAMETERS
BASEDIR = '/mnt/koji'
# default task priority
PRIO_DEFAULT = 20

# default timeouts
DEFAULT_REQUEST_TIMEOUT = 60 * 60 * 12
DEFAULT_AUTH_TIMEOUT = 60

## BEGIN kojikamid dup

#Exceptions
PythonImportError = ImportError # will be masked by koji's one

class GenericError(Exception):
    """Base class for our custom exceptions"""
    faultCode = 1000
    fromFault = False
    def __str__(self):
        try:
            return str(self.args[0]['args'][0])
        except:
            try:
                return str(self.args[0])
            except:
                return str(self.__dict__)
## END kojikamid dup

class LockError(GenericError):
    """Raised when there is a lock conflict"""
    faultCode = 1001

class AuthError(GenericError):
    """Raised when there is an error in authentication"""
    faultCode = 1002

class TagError(GenericError):
    """Raised when a tagging operation fails"""
    faultCode = 1003

class ActionNotAllowed(GenericError):
    """Raised when the session does not have permission to take some action"""
    faultCode = 1004

## BEGIN kojikamid dup

class BuildError(GenericError):
    """Raised when a build fails"""
    faultCode = 1005
## END kojikamid dup

class AuthLockError(AuthError):
    """Raised when a lock prevents authentication"""
    faultCode = 1006

class AuthExpired(AuthError):
    """Raised when a session has expired"""
    faultCode = 1007

class SequenceError(AuthError):
    """Raised when requests are received out of sequence"""
    faultCode = 1008

class RetryError(AuthError):
    """Raised when a request is received twice and cannot be rerun"""
    faultCode = 1009

class PreBuildError(BuildError):
    """Raised when a build fails during pre-checks"""
    faultCode = 1010

class PostBuildError(BuildError):
    """Raised when a build fails during post-checks"""
    faultCode = 1011

class BuildrootError(BuildError):
    """Raised when there is an error with the buildroot"""
    faultCode = 1012

class FunctionDeprecated(GenericError):
    """Raised by a deprecated function"""
    faultCode = 1013

class ServerOffline(GenericError):
    """Raised when the server is offline"""
    faultCode = 1014

class LiveCDError(GenericError):
    """Raised when LiveCD Image creation fails"""
    faultCode = 1015

class PluginError(GenericError):
    """Raised when there is an error with a plugin"""
    faultCode = 1016

class CallbackError(PluginError):
    """Raised when there is an error executing a callback"""
    faultCode = 1017

class ApplianceError(GenericError):
    """Raised when Appliance Image creation fails"""
    faultCode = 1018

class ParameterError(GenericError):
    """Raised when an rpc call receives incorrect arguments"""
    faultCode = 1019

class ImportError(GenericError):
    """Raised when an import fails"""
    faultCode = 1020

class ConfigurationError(GenericError):
    """Raised when load of koji configuration fails"""
    faultCode = 1021

class LiveMediaError(GenericError):
    """Raised when LiveMedia Image creation fails"""
    faultCode = 1022

class MultiCallInProgress(object):
    """
    Placeholder class to be returned by method calls when in the process of
    constructing a multicall.
    """
    pass


#A function to get create an exception from a fault
def convertFault(fault):
    """Convert a fault to the corresponding Exception type, if possible"""
    code = getattr(fault, 'faultCode', None)
    if code is None:
        return fault
    for v in globals().values():
        if isinstance(v, type(Exception)) and issubclass(v, GenericError) and \
                code == getattr(v, 'faultCode', None):
            ret = v(fault.faultString)
            ret.fromFault = True
            return ret
    #otherwise...
    return fault

def listFaults():
    """Return a list of faults

    Returns a list of dictionaries whose keys are:
        faultCode: the numeric code used in fault conversion
        name: the name of the exception
        desc: the description of the exception (docstring)
    """
    ret = []
    for n, v in globals().items():
        if isinstance(v, type(Exception)) and issubclass(v, GenericError):
            code = getattr(v, 'faultCode', None)
            if code is None:
                continue
            info = {}
            info['faultCode'] = code
            info['name'] = n
            info['desc'] = getattr(v, '__doc__', None)
            ret.append(info)
    ret.sort(key=lambda x: x['faultCode'])
    return ret

#functions for encoding/decoding optional arguments

def encode_args(*args, **opts):
    """The function encodes optional arguments as regular arguments.

    This is used to allow optional arguments in xmlrpc calls
    Returns a tuple of args
    """
    if opts:
        opts['__starstar'] = True
        args = args + (opts,)
    return args

def decode_args(*args):
    """Decodes optional arguments from a flat argument list

    Complementary to encode_args
    Returns a tuple (args,opts) where args is a tuple and opts is a dict
    """
    opts = {}
    if len(args) > 0:
        last = args[-1]
        if isinstance(last, dict) and last.get('__starstar', False):
            opts = last.copy()
            del opts['__starstar']
            args = args[:-1]
    return args, opts

def decode_args2(args, names, strict=True):
    "An alternate form of decode_args, returns a dictionary"
    args, opts = decode_args(*args)
    if strict and len(names) < len(args):
        raise TypeError("Expecting at most %i arguments" % len(names))
    ret = dict(zip(names, args))
    ret.update(opts)
    return ret

def decode_int(n):
    """If n is not an integer, attempt to convert it"""
    if isinstance(n, six.integer_types):
        return n
    #else
    return int(n)

#commonly used functions

def safe_xmlrpc_loads(s):
    """Load xmlrpc data from a string, but catch faults"""
    try:
        return loads(s)
    except Fault as f:
        return f

## BEGIN kojikamid dup

def ensuredir(directory):
    """Create directory, if necessary."""
    if os.path.exists(directory):
        if not os.path.isdir(directory):
            raise OSError("Not a directory: %s" % directory)
    else:
        head, tail = os.path.split(directory)
        if not tail and head == directory:
            # can only happen if directory == '/' or equivalent
            # (which obviously should not happen)
            raise OSError("root directory missing? %s" % directory)
        if head:
            ensuredir(head)
        # note: if head is blank, then we've reached the top of a relative path
        try:
            os.mkdir(directory)
        except OSError:
            #thrown when dir already exists (could happen in a race)
            if not os.path.isdir(directory):
                #something else must have gone wrong
                raise
    return directory

## END kojikamid dup

def daemonize():
    """Detach and run in background"""
    pid = os.fork()
    if pid:
        os._exit(0)
    os.setsid()
    signal.signal(signal.SIGHUP, signal.SIG_IGN)
    #fork again
    pid = os.fork()
    if pid:
        os._exit(0)
    os.chdir("/")
    #redirect stdin/stdout/sterr
    fd0 = os.open('/dev/null', os.O_RDONLY)
    fd1 = os.open('/dev/null', os.O_RDWR)
    fd2 = os.open('/dev/null', os.O_RDWR)
    os.dup2(fd0, 0)
    os.dup2(fd1, 1)
    os.dup2(fd2, 2)
    os.close(fd0)
    os.close(fd1)
    os.close(fd2)

def multibyte(data):
    """Convert a list of bytes to an integer (network byte order)"""
    sum = 0
    n = len(data)
    for i in range(n):
        sum += data[i] << (8 * (n - i - 1))
    return sum

def find_rpm_sighdr(path):
    """Finds the offset and length of the signature header."""
    # see Maximum RPM Appendix A: Format of the RPM File

    # The lead is a fixed sized section (96 bytes) that is mostly obsolete
    sig_start = 96
    sigsize = rpm_hdr_size(path, sig_start)
    return (sig_start, sigsize)

def rpm_hdr_size(f, ofs=None):
    """Returns the length (in bytes) of the rpm header

    f = filename or file object
    ofs = offset of the header
    """
    if isinstance(f, six.string_types):
        fo = open(f, 'rb')
    else:
        fo = f
    if ofs != None:
        fo.seek(ofs, 0)
    magic = fo.read(3)
    if magic != RPM_HEADER_MAGIC:
        raise GenericError("Invalid rpm: bad magic: %r" % magic)

    # skip past section magic and such
    #   (3 bytes magic, 1 byte version number, 4 bytes reserved)
    fo.seek(ofs + 8, 0)

    # now read two 4-byte integers which tell us
    #  - # of index entries
    #  - bytes of data in header
    data = [_ord(x) for x in fo.read(8)]
    il = multibyte(data[0:4])
    dl = multibyte(data[4:8])

    #this is what the section data says the size should be
    hdrsize = 8 + 16 * il + dl

    # hdrsize rounded up to nearest 8 bytes
    hdrsize = hdrsize + (8 - (hdrsize % 8)) % 8

    # add eight bytes for section header
    hdrsize = hdrsize + 8

    if not isinstance(f, six.string_types):
        fo.close()
    return hdrsize


class RawHeader(object):

    # see Maximum RPM Appendix A: Format of the RPM File

    def __init__(self, data):
        if data[0:3] != RPM_HEADER_MAGIC:
            raise GenericError("Invalid rpm header: bad magic: %r" % (data[0:3],))
        self.header = data
        self._index()

    def version(self):
        #fourth byte is the version
        return _ord(self.header[3])

    def _index(self):
        # read two 4-byte integers which tell us
        #  - # of index entries  (each 16 bytes long)
        #  - bytes of data in header
        data = [_ord(x) for x in self.header[8:12]]
        il = multibyte(data[:4])
        dl = multibyte(data[4:8])

        #read the index (starts at offset 16)
        index = {}
        for i in range(il):
            entry = []
            for j in range(4):
                ofs = 16 + i*16 + j*4
                data = [_ord(x) for x in self.header[ofs:ofs+4]]
                entry.append(multibyte(data))
            #print("Tag: %d, Type: %d, Offset: %x, Count: %d" % tuple(entry))
            index[entry[0]] = entry
        self.datalen = dl
        self.index = index

    def dump(self):
        print("HEADER DUMP:")
        #calculate start of store
        il = len(self.index)
        store = 16 + il * 16
        #print("start is: %d" % start)
        #print("index length: %d" % il)
        print("Store at offset %d (%0x)" % (store, store))
        #sort entries by offset, dtype
        #also rearrange: tag, dtype, offset, count -> offset, dtype, tag, count
        order = sorted([(x[2], x[1], x[0], x[3]) for x in six.itervalues(self.index)])
        next = store
        #map some rpmtag codes
        tags = {}
        for name, code in six.iteritems(rpm.__dict__):
            if name.startswith('RPMTAG_') and isinstance(code, int):
                tags[code] = name[7:].lower()
        for entry in order:
            #tag, dtype, offset, count = entry
            offset, dtype, tag, count = entry
            pos = store + offset
            if next is not None:
                if pos > next:
                    print("** HOLE between entries")
                    print("Hex: %s" % hex_string(self.header[next:pos]))
                    print("Data: %r" % self.header[next:pos])
                elif pos < next:
                    print("** OVERLAPPING entries")
            print("Tag: %d [%s], Type: %d, Offset: %x, Count: %d" \
                    % (tag, tags.get(tag, '?'), dtype, offset, count))
            if dtype == 0:
                #null
                print("[NULL entry]")
                next = pos
            elif dtype == 1:
                #char
                for i in range(count):
                    print("Char: %r" % self.header[pos])
                    pos += 1
                next = pos
            elif dtype >= 2 and dtype <= 5:
                #integer
                n = 1 << (dtype - 2)
                for i in range(count):
                    data = [_ord(x) for x in self.header[pos:pos+n]]
                    print("%r" % data)
                    num = multibyte(data)
                    print("Int(%d): %d" % (n, num))
                    pos += n
                next = pos
            elif dtype == 6:
                # string (null terminated)
                end = self.header.find(six.b('\0'), pos)
                print("String(%d): %r" % (end-pos, self.header[pos:end]))
                next = end + 1
            elif dtype == 7:
                print("Data: %s" % hex_string(self.header[pos:pos+count]))
                next = pos+count
            elif dtype == 8:
                # string array
                for i in range(count):
                    end = self.header.find(six.b('\0'), pos)
                    print("String(%d): %r" % (end-pos, self.header[pos:end]))
                    pos = end + 1
                next = pos
            elif dtype == 9:
                # unicode string array
                for i in range(count):
                    end = self.header.find(six.b('\0'), pos)
                    print("i18n(%d): %r" % (end-pos, self.header[pos:end]))
                    pos = end + 1
                next = pos
            else:
                print("Skipping data type %x" % dtype)
                next = None
        if next is not None:
            pos = store + self.datalen
            if next < pos:
                print("** HOLE at end of data block")
                print("Hex: %s" % hex_string(self.header[next:pos]))
                print("Data: %r" % self.header[next:pos])
            elif pos > next:
                print("** OVERFLOW in data block")

    def __getitem__(self, key):
        tag, dtype, offset, count = self.index[key]
        assert tag == key
        return self._getitem(dtype, offset, count)

    def _getitem(self, dtype, offset, count):
        #calculate start of store
        il = len(self.index)
        store = 16 + il * 16
        pos = store + offset
        if dtype >= 2 and dtype <= 5:
            n = 1 << (dtype - 2)
            # n-byte integer
            data = [_ord(x) for x in self.header[pos:pos+n]]
            return multibyte(data)
        elif dtype == 6:
            # string (null terminated)
            end = self.header.find('\0', pos)
            return self.header[pos:end]
        elif dtype == 7:
            #raw data
            return self.header[pos:pos+count]
        else:
            #XXX - not all valid data types are handled
            raise GenericError("Unable to read header data type: %x" % dtype)

    def get(self, key, default=None):
        entry = self.index.get(key)
        if entry is None:
            return default
        else:
            return self._getitem(*entry[1:])


def rip_rpm_sighdr(src):
    """Rip the signature header out of an rpm"""
    (start, size) = find_rpm_sighdr(src)
    fo = open(src, 'rb')
    fo.seek(start, 0)
    sighdr = fo.read(size)
    fo.close()
    return sighdr

def rip_rpm_hdr(src):
    """Rip the main header out of an rpm"""
    (start, size) = find_rpm_sighdr(src)
    start += size
    size = rpm_hdr_size(src, start)
    fo = open(src, 'rb')
    fo.seek(start, 0)
    hdr = fo.read(size)
    fo.close()
    return hdr

def _ord(s):
    # in python2 it is char/str, while in py3 it is already int/bytes
    if isinstance(s, int):
        return s
    else:
        return ord(s)

def __parse_packet_header(pgp_packet):
    """Parse pgp_packet header, return tag type and the rest of pgp_packet"""
    byte0 = _ord(pgp_packet[0])
    if (byte0 & 0x80) == 0:
        raise ValueError('Not an OpenPGP packet')
    if (byte0 & 0x40) == 0:
        tag = (byte0 & 0x3C) >> 2
        len_type = byte0 & 0x03
        if len_type == 3:
            offset = 1
            length = len(pgp_packet) - offset
        else:
            (fmt, offset) = {0:('>B', 2), 1:('>H', 3), 2:('>I', 5)}[len_type]
            length = struct.unpack(fmt, pgp_packet[1:offset])[0]
    else:
        tag = byte0 & 0x3F
        byte1 = _ord(pgp_packet[1])
        if byte1 < 192:
            length = byte1
            offset = 2
        elif byte1 < 224:
            length = ((byte1 - 192) << 8) + _ord(pgp_packet[2]) + 192
            offset = 3
        elif byte1 == 255:
            length = struct.unpack('>I', pgp_packet[2:6])[0]
            offset = 6
        else:
            # Who the ... would use partial body lengths in a signature packet?
            raise NotImplementedError(
                'OpenPGP packet with partial body lengths')
    if len(pgp_packet) != offset + length:
        raise ValueError('Invalid OpenPGP packet length')
    return (tag, pgp_packet[offset:])

def __subpacket_key_ids(subs):
    """Parse v4 signature subpackets and return a list of issuer key IDs"""
    res = []
    while len(subs) > 0:
        byte0 = _ord(subs[0])
        if byte0 < 192:
            length = byte0
            off = 1
        elif byte0 < 255:
            length = ((byte0 - 192) << 8) + _ord(subs[1]) + 192
            off = 2
        else:
            length = struct.unpack('>I', subs[1:5])[0]
            off = 5
        if _ord(subs[off]) == 16:
            res.append(subs[off+1 : off+length])
        subs = subs[off+length:]
    return res

def get_sigpacket_key_id(sigpacket):
    """Return ID of the key used to create sigpacket as a hexadecimal string"""
    (tag, sigpacket) = __parse_packet_header(sigpacket)
    if tag != 2:
        raise ValueError('Not a signature packet')
    if _ord(sigpacket[0]) == 0x03:
        key_id = sigpacket[11:15]
    elif _ord(sigpacket[0]) == 0x04:
        sub_len = struct.unpack('>H', sigpacket[4:6])[0]
        off = 6 + sub_len
        key_ids = __subpacket_key_ids(sigpacket[6:off])
        sub_len = struct.unpack('>H', sigpacket[off : off+2])[0]
        off += 2
        key_ids += __subpacket_key_ids(sigpacket[off : off+sub_len])
        if len(key_ids) != 1:
            raise NotImplementedError(
                'Unexpected number of key IDs: %s' % len(key_ids))
        key_id = key_ids[0][-4:]
    else:
        raise NotImplementedError(
            'Unknown PGP signature packet version %s' % _ord(sigpacket[0]))
    return hex_string(key_id)

def get_sighdr_key(sighdr):
    """Parse the sighdr and return the sigkey"""
    rh = RawHeader(sighdr)
    sig = rh.get(RPM_SIGTAG_GPG)
    if not sig:
        sig = rh.get(RPM_SIGTAG_PGP)
    if not sig:
        return None
    else:
        return get_sigpacket_key_id(sig)

def splice_rpm_sighdr(sighdr, src, dst=None, bufsize=8192):
    """Write a copy of an rpm with signature header spliced in"""
    (start, size) = find_rpm_sighdr(src)
    if dst is None:
        (fd, dst) = tempfile.mkstemp()
        os.close(fd)
    src_fo = open(src, 'rb')
    dst_fo = open(dst, 'wb')
    dst_fo.write(src_fo.read(start))
    dst_fo.write(sighdr)
    src_fo.seek(size, 1)
    while True:
        buf = src_fo.read(bufsize)
        if not buf:
            break
        dst_fo.write(buf)
    src_fo.close()
    dst_fo.close()
    return dst

def get_rpm_header(f, ts=None):
    """Return the rpm header."""
    if ts is None:
        ts = rpm.TransactionSet()
        ts.setVSFlags(rpm._RPMVSF_NOSIGNATURES|rpm._RPMVSF_NODIGESTS)
    if isinstance(f, six.string_types):
        fo = open(f, "rb")
    else:
        fo = f
    hdr = ts.hdrFromFdno(fo.fileno())
    if fo is not f:
        fo.close()
    return hdr


def _decode_item(item):
    """Decode rpm header byte strings to str in py3"""
    if six.PY2:
        return item
    elif isinstance(item, bytes):
        try:
            return item.decode()
        except UnicodeDecodeError:
            # typically signatures
            return item
    elif isinstance(item, list):
        return [_decode_item(x) for x in item]
    else:
        return item


def get_header_field(hdr, name, src_arch=False):
    """Extract named field from an rpm header"""
    name = name.upper()
    # if field is not supported by host's rpm (>4.12), return empty list
    if not SUPPORTED_OPT_DEP_HDRS.get(name, True):
        return []

    if (src_arch and name == "ARCH"
                and get_header_field(hdr, "sourcepackage")):
        # return "src" or "nosrc" arch instead of build arch for src packages
        if (get_header_field(hdr, "nosource")
                    or get_header_field(hdr, "nopatch")):
            return "nosrc"
        return "src"

    # REMOVED?
    result = _get_header_field(hdr, name)

    if name in ("NOSOURCE", "NOPATCH"):
        # HACK: workaround for https://bugzilla.redhat.com/show_bug.cgi?id=991329
        if result is None:
            result = []
        elif isinstance(result, six.integer_types):
            result = [result]

    sizetags = ('SIZE', 'ARCHIVESIZE', 'FILESIZES', 'SIGSIZE')
    if name in sizetags and (result is None or result == []):
        try:
            result = _get_header_field(hdr, 'LONG' + name)
        except GenericError:
            # no such header
            pass

    return _decode_item(result)


def _get_header_field(hdr, name):
    '''Just get the header field'''
    hdr_key = getattr(rpm, "RPMTAG_%s" % name, None)
    if hdr_key is None:
        # HACK: nosource and nopatch may not be in exported rpm tags
        if name == "NOSOURCE":
            hdr_key = 1051
        elif name == "NOPATCH":
            hdr_key = 1052
        else:
            raise GenericError("No such rpm header field: %s" % name)
    return hdr[hdr_key]


def get_header_fields(X, fields, src_arch=False):
    """Extract named fields from an rpm header and return as a dictionary

    X may be either the rpm header or the rpm filename
    """
    if isinstance(X, str):
        hdr = get_rpm_header(X)
    else:
        hdr = X
    ret = {}
    for f in fields:
        ret[f] = get_header_field(hdr, f, src_arch=src_arch)
    return ret

def parse_NVR(nvr):
    """split N-V-R into dictionary of data"""
    ret = {}
    p2 = nvr.rfind("-", 0)
    if p2 == -1 or p2 == len(nvr) - 1:
        raise GenericError("invalid format: %s" % nvr)
    p1 = nvr.rfind("-", 0, p2)
    if p1 == -1 or p1 == p2 - 1:
        raise GenericError("invalid format: %s" % nvr)
    ret['release'] = nvr[p2+1:]
    ret['version'] = nvr[p1+1:p2]
    ret['name'] = nvr[:p1]
    epochIndex = ret['name'].find(':')
    if epochIndex == -1:
        ret['epoch'] = ''
    else:
        ret['epoch'] = ret['name'][:epochIndex]
        ret['name'] = ret['name'][epochIndex + 1:]
    return ret

def parse_NVRA(nvra):
    """split N-V-R.A.rpm into dictionary of data

    also splits off @location suffix"""
    parts = nvra.split('@', 1)
    location = None
    if len(parts) > 1:
        nvra, location = parts
    if nvra.endswith(".rpm"):
        nvra = nvra[:-4]
    p3 = nvra.rfind(".")
    if p3 == -1 or p3 == len(nvra) - 1:
        raise GenericError("invalid format: %s" % nvra)
    arch = nvra[p3+1:]
    ret = parse_NVR(nvra[:p3])
    ret['arch'] = arch
    if arch == 'src':
        ret['src'] = True
    else:
        ret['src'] = False
    if location:
        ret['location'] = location
    return ret


def check_NVR(nvr, strict=False):
    """Perform basic validity checks on an NVR

    nvr may be a string or a dictionary with keys name, version, and release

    This function only performs minimal, basic checking. It does not enforce
    the sort of constraints that a project might have in their packaging
    guidelines.
    """

    try:
        return _check_NVR(nvr)
    except GenericError:
        if strict:
            raise
        else:
            return False

def _check_NVR(nvr):
    if isinstance(nvr, six.string_types):
        nvr = parse_NVR(nvr)
    if '-' in nvr['version']:
        raise GenericError('The "-" character not allowed in version field')
    if '-' in nvr['release']:
        raise GenericError('The "-" character not allowed in release field')
    # anything else?
    return True


def check_NVRA(nvra, strict=False):
    """Perform basic validity checks on an NVRA

    nvra may be a string or a dictionary with keys name, version, and release

    This function only performs minimal, basic checking. It does not enforce
    the sort of constraints that a project might have in their packaging
    guidelines.
    """
    try:
        return _check_NVRA(nvra)
    except GenericError:
        if strict:
            raise
        else:
            return False


def _check_NVRA(nvra):
    if isinstance(nvra, six.string_types):
            nvra = parse_NVRA(nvra)
    if '-' in nvra['version']:
        raise GenericError('The "-" character not allowed in version field')
    if '-' in nvra['release']:
        raise GenericError('The "-" character not allowed in release field')
    if '.' in nvra['arch']:
        raise GenericError('The "." character not allowed in arch field')
    return True


def is_debuginfo(name):
    """Determines if an rpm is a debuginfo rpm, based on name"""
    return (name.endswith('-debuginfo') or name.endswith('-debugsource') or
            '-debuginfo-' in name)

def canonArch(arch):
    """Given an arch, return the "canonical" arch"""
    #XXX - this could stand to be smarter, and we should probably
    #   have some other related arch-mangling functions.
    if fnmatch(arch, 'i?86') or arch == 'athlon':
        return 'i386'
    elif arch == 'ia32e':
        return 'x86_64'
    elif fnmatch(arch, 'ppc64le'):
        return 'ppc64le'
    elif fnmatch(arch, 'ppc64*'):
        return 'ppc64'
    elif fnmatch(arch, 'sparc64*'):
        return 'sparc64'
    elif fnmatch(arch, 'sparc*'):
        return 'sparc'
    elif fnmatch(arch, 'alpha*'):
        return 'alpha'
    elif fnmatch(arch, 'arm*h*'):
        return 'armhfp'
    elif fnmatch(arch, 'arm*'):
        return 'arm'
    else:
        return arch

class POMHandler(xml.sax.handler.ContentHandler):
    def __init__(self, values, fields):
        xml.sax.handler.ContentHandler.__init__(self)
        self.tag_stack = []
        self.tag_content = None
        self.values = values
        self.fields = fields

    def startElement(self, name, attrs):
        self.tag_stack.append(name)
        self.tag_content = ''

    def characters(self, content):
        self.tag_content += content

    def endElement(self, name):
        if len(self.tag_stack) in (2, 3) and self.tag_stack[-1] in self.fields:
            if self.tag_stack[-2] == 'parent':
                # Only set a value from the "parent" tag if we don't already have
                # that value set
                if self.tag_stack[-1] not in self.values:
                    self.values[self.tag_stack[-1]] = self.tag_content.strip()
            elif self.tag_stack[-2] == 'project':
                self.values[self.tag_stack[-1]] = self.tag_content.strip()
        self.tag_content = ''
        self.tag_stack.pop()

    def reset(self):
        self.tag_stack = []
        self.tag_content = None
        self.values.clear()

ENTITY_RE = re.compile(r'&[A-Za-z0-9]+;')

def parse_pom(path=None, contents=None):
    """
    Parse the Maven .pom file return a map containing information
    extracted from it.  The map will contain at least the following
    fields:

    groupId
    artifactId
    version
    """
    fields = ('groupId', 'artifactId', 'version')
    values = {}
    handler = POMHandler(values, fields)
    if path:
        fd = open(path)
        contents = fd.read()
        fd.close()

    if not contents:
        raise GenericError('either a path to a pom file or the contents of a pom file must be specified')

    # A common problem is non-UTF8 characters in XML files, so we'll convert the string first

    contents = fixEncoding(contents)

    try:
        xml.sax.parseString(contents, handler)
    except xml.sax.SAXParseException:
        # likely an undefined entity reference, so lets try replacing
        # any entity refs we can find and see if we get something parseable
        handler.reset()
        contents = ENTITY_RE.sub('?', contents)
        xml.sax.parseString(contents, handler)

    for field in fields:
        if field not in util.to_list(values.keys()):
            raise GenericError('could not extract %s from POM: %s' % (field, (path or '<contents>')))
    return values

def pom_to_maven_info(pominfo):
    """
    Convert the output of parsing a POM into a format compatible
    with Koji.
    The mapping is as follows:
    - groupId: group_id
    - artifactId: artifact_id
    - version: version
    """
    maveninfo = {'group_id': pominfo['groupId'],
                 'artifact_id': pominfo['artifactId'],
                 'version': pominfo['version']}
    return maveninfo

def maven_info_to_nvr(maveninfo):
    """
    Convert the maveninfo to NVR-compatible format.
    The release cannot be determined from Maven metadata, and will
    be set to None.
    """
    nvr = {'name': maveninfo['group_id'] + '-' + maveninfo['artifact_id'],
           'version': maveninfo['version'].replace('-', '_'),
           'release': None,
           'epoch': None}
    # for backwards-compatibility
    nvr['package_name'] = nvr['name']
    return nvr

def mavenLabel(maveninfo):
    """
    Return a user-friendly label for the given maveninfo.  maveninfo is
    a dict as returned by kojihub:getMavenBuild().
    """
    return '%(group_id)s-%(artifact_id)s-%(version)s' % maveninfo

def hex_string(s):
    """Converts a string to a string of hex digits"""
    return ''.join(['%02x' % _ord(x) for x in s])


def make_groups_spec(grplist, name='buildsys-build', buildgroup=None):
    """Return specfile contents representing the group"""
    if buildgroup is None:
        buildgroup = name
    data = [
"""#
# This specfile represents buildgroups for mock
# Autogenerated by the build system
#
Summary: The base set of packages for a mock chroot\n""",
"""Name: %s\n""" % name,
"""Version: 1
Release: 1
License: GPL
Group: Development/Build Tools
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch

#package requirements
"""]
    #add a requires entry for all the packages in buildgroup, and in
    #groups required by buildgroup
    need = [buildgroup]
    seen_grp = {}
    seen_pkg = {}
    #index groups
    groups = dict([(g['name'], g) for g in grplist])
    for group_name in need:
        if group_name in seen_grp:
            continue
        seen_grp[group_name] = 1
        group = groups.get(group_name)
        if group is None:
            data.append("#MISSING GROUP: %s\n" % group_name)
            continue
        data.append("#Group: %s\n" % group_name)
        pkglist = list(group['packagelist'])
        pkglist.sort(key=lambda x: x['package'])
        for pkg in pkglist:
            pkg_name = pkg['package']
            if pkg_name in seen_pkg:
                continue
            data.append("Requires: %s\n" % pkg_name)
        for req in group['grouplist']:
            req_name = req['name']
            if req_name in seen_grp:
                continue
            need.append(req_name)
    data.append("""
%description
This is a meta-package that requires a defined group of packages

%prep
%build
%install
%clean

%files
%defattr(-,root,root,-)
%doc
""")
    return ''.join(data)

def generate_comps(groups, expand_groups=False):
    """Generate comps content from groups data"""
    def boolean_text(x):
        if x:
            return "true"
        else:
            return "false"
    data = [
"""<?xml version="1.0"?>
<!DOCTYPE comps PUBLIC "-//Red Hat, Inc.//DTD Comps info//EN" "comps.dtd">

<!-- Auto-generated by the build system -->
<comps>
"""]
    groups = list(groups)
    group_idx = dict([(g['name'], g) for g in groups])
    groups.sort(key=lambda x: x['name'])
    for g in groups:
        group_id = g['name']
        name = g['display_name']
        description = g['description']
        langonly = boolean_text(g['langonly'])
        default = boolean_text(g['is_default'])
        uservisible = boolean_text(g['uservisible'])
        data.append(
"""  <group>
    <id>%(group_id)s</id>
    <name>%(name)s</name>
    <description>%(description)s</description>
    <default>%(default)s</default>
    <uservisible>%(uservisible)s</uservisible>
""" % locals())
        if g['biarchonly']:
            data.append(
"""    <biarchonly>%s</biarchonly>
""" % boolean_text(True))

        #print grouplist, if any
        if g['grouplist'] and not expand_groups:
            data.append(
"""    <grouplist>
""")
            grouplist = list(g['grouplist'])
            grouplist.sort(key=lambda x: x['name'])
            for x in grouplist:
                #['req_id','type','is_metapkg','name']
                name = x['name']
                thetype = x['type']
                tag = "groupreq"
                if x['is_metapkg']:
                    tag = "metapkg"
                if thetype:
                    data.append(
"""      <%(tag)s type="%(thetype)s">%(name)s</%(tag)s>
""" % locals())
                else:
                    data.append(
"""      <%(tag)s>%(name)s</%(tag)s>
""" % locals())
            data.append(
"""    </grouplist>
""")

        #print packagelist, if any
        def package_entry(pkg):
            #p['package_id','type','basearchonly','requires','name']
            name = pkg['package']
            opts = 'type="%s"' % pkg['type']
            if pkg['basearchonly']:
                opts += ' basearchonly="%s"' % boolean_text(True)
            if pkg['requires']:
                opts += ' requires="%s"' % pkg['requires']
            return "<packagereq %(opts)s>%(name)s</packagereq>" % locals()

        data.append(
"""    <packagelist>
""")
        if g['packagelist']:
            packagelist = list(g['packagelist'])
            packagelist.sort(key=lambda x: x['package'])
            for p in packagelist:
                data.append(
"""      %s
""" % package_entry(p))
            # also include expanded list, if needed
        if expand_groups and g['grouplist']:
            #add a requires entry for all packages in groups required by buildgroup
            need = [req['name'] for req in g['grouplist']]
            seen_grp = {g['name'] : 1}
            seen_pkg = {}
            for p in g['packagelist']:
                seen_pkg[p['package']] = 1
            for group_name in need:
                if group_name in seen_grp:
                    continue
                seen_grp[group_name] = 1
                group = group_idx.get(group_name)
                if group is None:
                    data.append(
"""      <!-- MISSING GROUP: %s -->
""" % group_name)
                    continue
                data.append(
"""      <!-- Expanding Group: %s -->
""" % group_name)
                pkglist = list(group['packagelist'])
                pkglist.sort(key=lambda x: x['package'])
                for pkg in pkglist:
                    pkg_name = pkg['package']
                    if pkg_name in seen_pkg:
                        continue
                    data.append(
"""      %s
""" % package_entry(pkg))
                for req in group['grouplist']:
                    req_name = req['name']
                    if req_name in seen_grp:
                        continue
                    need.append(req_name)
        data.append(
"""    </packagelist>
""")
        data.append(
"""  </group>
""")
    data.append(
"""</comps>
""")
    return ''.join(data)


def genMockConfig(name, arch, managed=False, repoid=None, tag_name=None, **opts):
    """Generate a mock config

    Returns a string containing the config
    The generated config is compatible with mock >= 0.8.7
    """
    mockdir = opts.get('mockdir', '/var/lib/mock')
    if 'url' in opts:
        util.deprecated('The url option for genMockConfig is deprecated')
        urls = [opts['url']]
    else:
        if not (repoid and tag_name):
            raise GenericError("please provide a repo and tag")
        topurls = opts.get('topurls')
        if not topurls:
            #cli command still passes plain topurl
            topurl = opts.get('topurl')
            if topurl:
                topurls = [topurl]
        if topurls:
            #XXX - PathInfo isn't quite right for this, but it will do for now
            pathinfos = [PathInfo(topdir=_u) for _u in topurls]
            urls = ["%s/%s" % (_p.repo(repoid, tag_name), arch) for _p in pathinfos]
        else:
            pathinfo = PathInfo(topdir=opts.get('topdir', '/mnt/koji'))
            repodir = pathinfo.repo(repoid, tag_name)
            urls = ["file://%s/%s" % (repodir, arch)]
    if managed:
        buildroot_id = opts.get('buildroot_id')

    # rely on the mock defaults being correct
    # and only includes changes from the defaults here
    config_opts = {
        'root' : name,
        'basedir' : mockdir,
        'target_arch' : opts.get('target_arch', arch),
        'chroothome': '/builddir',
        # Use the group data rather than a generated rpm
        'chroot_setup_cmd': 'groupinstall %s' % opts.get('install_group', 'build'),
        # don't encourage network access from the chroot
        'rpmbuild_networking': opts.get('use_host_resolv', False),
        'use_host_resolv': opts.get('use_host_resolv', False),
        # Don't let a build last more than 24 hours
        'rpmbuild_timeout': opts.get('rpmbuild_timeout', 86400)
    }
    if opts.get('package_manager'):
        config_opts['package_manager'] = opts['package_manager']

    # bind_opts are used to mount parts (or all of) /dev if needed.
    # See kojid::LiveCDTask for a look at this option in action.
    bind_opts = opts.get('bind_opts')

    files = {}
    if opts.get('use_host_resolv', False) and os.path.exists('/etc/hosts'):
        # if we're setting up DNS,
        # also copy /etc/hosts from the host
        etc_hosts = open('/etc/hosts')
        files['etc/hosts'] = etc_hosts.read()
        etc_hosts.close()
    mavenrc = ''
    if opts.get('maven_opts'):
        mavenrc = 'export MAVEN_OPTS="%s"\n' % ' '.join(opts['maven_opts'])
    if opts.get('maven_envs'):
        for name, val in six.iteritems(opts['maven_envs']):
            mavenrc += 'export %s="%s"\n' % (name, val)
    if mavenrc:
        files['etc/mavenrc'] = mavenrc

    #generate yum.conf
    yc_parts = ["[main]\n"]
    # HTTP proxy for yum
    if opts.get('yum_proxy'):
        yc_parts.append("proxy=%s\n" % opts['yum_proxy'])
    # Rest of the yum options
    yc_parts.append("""\
cachedir=/var/cache/yum
debuglevel=1
logfile=/var/log/yum.log
reposdir=/dev/null
retries=20
obsoletes=1
gpgcheck=0
assumeyes=1
keepcache=1
install_weak_deps=0
strict=1

# repos

[build]
name=build
""")
    yc_parts.append("baseurl=%s\n" % urls[0])
    for url in urls[1:]:
        yc_parts.append("        %s\n" % url)
    config_opts['yum.conf'] = ''.join(yc_parts)

    plugin_conf = {
        'ccache_enable': False,
        'yum_cache_enable': False,
        'root_cache_enable': False
    }

    #XXX - this needs to be configurable
    macros = {
        '%_topdir' : '%s/build' % config_opts['chroothome'],
        '%_rpmfilename' : '%%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm',
        '%_host_cpu' : opts.get('target_arch', arch),
        '%_host': '%s-%s' % (opts.get('target_arch', arch), opts.get('mockhost', 'koji-linux-gnu')),
        '%vendor' : opts.get('vendor', 'Koji'),
        '%packager' : opts.get('packager', 'Koji'),
        '%distribution': opts.get('distribution', 'Unknown')
        #TODO - track some of these in the db instead?
    }

    parts = ["""# Auto-generated by the Koji build system
"""]
    if managed:
        parts.append("""
# Koji buildroot id: %(buildroot_id)s
# Koji buildroot name: %(name)s
# Koji repo id: %(repoid)s
# Koji tag: %(tag_name)s
""" % locals())

    if bind_opts:
        # disable internal_dev_setup unless opts explicitly say otherwise
        opts.setdefault('internal_dev_setup', False)

    if 'internal_dev_setup' in opts:
        config_opts['internal_dev_setup'] = opts['internal_dev_setup']

    parts.append("\n")
    for key in sorted(config_opts):
        value = config_opts[key]
        parts.append("config_opts[%r] = %r\n" % (key, value))
    parts.append("\n")
    for key in sorted(plugin_conf):
        value = plugin_conf[key]
        parts.append("config_opts['plugin_conf'][%r] = %r\n" % (key, value))
    parts.append("\n")

    if bind_opts:
        for key in bind_opts.keys():
            for mnt_src, mnt_dest in six.iteritems(bind_opts.get(key)):
                parts.append("config_opts['plugin_conf']['bind_mount_opts'][%r].append((%r, %r))\n" % (key, mnt_src, mnt_dest))
        parts.append("\n")

    for key in sorted(macros):
        value = macros[key]
        parts.append("config_opts['macros'][%r] = %r\n" % (key, value))
    parts.append("\n")
    for key in sorted(files):
        value = files[key]
        parts.append("config_opts['files'][%r] = %r\n" % (key, value))

    return ''.join(parts)

def get_sequence_value(cursor, sequence):
    cursor.execute("""SELECT nextval(%(sequence)s)""", locals())
    return cursor.fetchone()[0]

# From Python Cookbook 2nd Edition, Recipe 8.6
def format_exc_plus():
    """ Format the usual traceback information, followed by a listing of
        all the local variables in each frame.
    """
    exc_type, exc_value, tb = sys.exc_info()
    while tb.tb_next:
        tb = tb.tb_next
    stack = []
    f = tb.tb_frame
    while f:
        stack.append(f)
        f = f.f_back
    stack.reverse()
    rv = ''.join(traceback.format_exception(exc_type, exc_value, tb))
    rv += "Locals by frame, innermost last\n"
    for frame in stack:
        rv += "Frame %s in %s at line %s\n" % (frame.f_code.co_name,
                                               frame.f_code.co_filename,
                                               frame.f_lineno)
        for key, value in frame.f_locals.items():
            rv += "  %20s = " % key
            # we must _absolutely_ avoid propagating eceptions, and str(value)
            # COULD cause any exception, so we MUST catch any...:
            try:
                rv += "%s\n" % value
            except:
                rv += "<ERROR WHILE PRINTING VALUE>\n"
    return rv

def openRemoteFile(relpath, topurl=None, topdir=None, tempdir=None):
    """Open a file on the main server (read-only)

    This is done either via a mounted filesystem (nfs) or http, depending
    on options"""
    if topurl:
        url = "%s/%s" % (topurl, relpath)
        src = six.moves.urllib.request.urlopen(url)
        fo = tempfile.TemporaryFile(dir=tempdir)
        shutil.copyfileobj(src, fo)
        src.close()
        fo.seek(0)
    elif topdir:
        fn = "%s/%s" % (topdir, relpath)
        fo = open(fn)
    else:
        raise GenericError("No access method for remote file: %s" % relpath)
    return fo


def config_directory_contents(dir_name):
    configs = []
    try:
        conf_dir_contents = os.listdir(dir_name)
    except OSError as exception:
        if exception.errno != errno.ENOENT:
            raise
    else:
        for name in sorted(conf_dir_contents):
            if not name.endswith('.conf'):
                continue
            config_full_name = os.path.join(dir_name, name)
            configs.append(config_full_name)
    return configs


def read_config(profile_name, user_config=None):
    config_defaults = {
        'server' : 'http://localhost/kojihub',
        'weburl' : 'http://localhost/koji',
        'topurl' : None,
        'pkgurl' : None,
        'topdir' : '/mnt/koji',
        'max_retries' : None,
        'retry_interval': None,
        'anon_retry' : None,
        'offline_retry' : None,
        'offline_retry_interval' : None,
        'keepalive' : True,
        'timeout' : DEFAULT_REQUEST_TIMEOUT,
        'auth_timeout' : DEFAULT_AUTH_TIMEOUT,
        'use_fast_upload': False,
        'upload_blocksize': 1048576,
        'poll_interval': 6,
        'krbservice': 'host',
        'krb_rdns': True,
        'krb_canon_host': False,
        'principal': None,
        'keytab': None,
        'cert': None,
        'ca': '',  # FIXME: remove in next major release
        'serverca': None,
        'no_ssl_verify': False,
        'authtype': None,
        'debug': False,
        'debug_xmlrpc': False,
        'pyver' : None,
    }

    result = config_defaults.copy()

    #note: later config files override earlier ones

    # /etc/koji.conf.d
    configs = config_directory_contents('/etc/koji.conf.d')

    # /etc/koji.conf
    if os.access('/etc/koji.conf', os.F_OK):
        configs.append('/etc/koji.conf')

    # User specific configuration
    if user_config:
        # Config file specified on command line
        fn = os.path.expanduser(user_config)
        if os.path.isdir(fn):
            # Specified config is a directory
            contents = config_directory_contents(fn)
            if not contents:
                raise ConfigurationError("No config files found in directory: %s" % fn)
            configs.extend(contents)
        else:
            # Specified config is a file
            if not os.access(fn, os.F_OK):
                raise ConfigurationError("No such file: %s" % fn)
            configs.append(fn)
    else:
        # User config
        user_config_dir = os.path.expanduser("~/.koji/config.d")
        configs.extend(config_directory_contents(user_config_dir))
        fn = os.path.expanduser("~/.koji/config")
        if os.access(fn, os.F_OK):
            configs.append(fn)

    # Load the configs in a particular order
    got_conf = False
    for configFile in configs:
        config = read_config_files(configFile)
        if config.has_section(profile_name):
            got_conf = True
            for name, value in config.items(profile_name):
                #note the config_defaults dictionary also serves to indicate which
                #options *can* be set via the config file. Such options should
                #not have a default value set in the option parser.
                if name in result:
                    if name in ('anon_retry', 'offline_retry', 'keepalive',
                                'use_fast_upload', 'krb_rdns', 'debug',
                                'debug', 'debug_xmlrpc', 'krb_canon_host'):
                        result[name] = config.getboolean(profile_name, name)
                    elif name in ('max_retries', 'retry_interval',
                                  'offline_retry_interval', 'poll_interval',
                                  'timeout', 'auth_timeout',
                                  'upload_blocksize', 'pyver'):
                        try:
                            result[name] = int(value)
                        except ValueError:
                            raise ConfigurationError("value for %s config option must be a valid integer" % name)
                    else:
                        result[name] = value

    # Check if the specified profile had a config specified
    if configs and not got_conf:
        raise ConfigurationError("no configuration for profile name: %s" % profile_name)

    # special handling for cert defaults
    cert_defaults = {
        'cert': '~/.koji/client.crt',
        'serverca': '~/.koji/serverca.crt',
        }
    for name in cert_defaults:
        if result.get(name) is None:
            fn = os.path.expanduser(cert_defaults[name])
            if os.path.exists(fn):
                result[name] = fn
            else:
                result[name] = ''
        else:
            result[name] = os.path.expanduser(result[name])

    return result


def get_profile_module(profile_name, config=None):
    """
    Create module for a koji instance.
    Override profile specific module attributes:
     * BASEDIR
     * config
     * pathinfo

    profile_name is str with name of the profile
    config is instance of optparse.Values()
    """
    global PROFILE_MODULES  # Dict with loaded modules

    # If config is passed use it and don't load koji config files by yourself
    if config is None:
        result = read_config(profile_name)
        config = optparse.Values(result)

    # Prepare module name
    mod_name = "__%s__%s" % (__name__, profile_name)

    imp.acquire_lock()
    try:
        # Check if profile module exists and if so return it
        if mod_name in PROFILE_MODULES:
            return PROFILE_MODULES[mod_name]

        # Load current module under a new name
        koji_module_loc = imp.find_module(__name__)
        mod = imp.load_module(mod_name,
                              None,
                              koji_module_loc[1],
                              koji_module_loc[2])

        # Tweak config of the new module
        mod.config = config
        mod.BASEDIR = config.topdir
        mod.pathinfo.topdir = config.topdir

        # Be sure that get_profile_module is only called from main module
        mod.get_profile_module = get_profile_module

        PROFILE_MODULES[mod_name] = mod
    finally:
        imp.release_lock()

    return mod


def read_config_files(config_files, raw=False):
    """Use parser to read config file(s)

    :param config_files: config file(s) to read (required).
    :type config_files: str or list
    :param bool raw: enable 'raw' parsing (no interpolation). Default: False

    :return: object of parser which contains parsed content
    """
    if not isinstance(config_files, (list, tuple)):
        config_files = [config_files]
    if raw:
        parser = six.moves.configparser.RawConfigParser
    elif six.PY2:
        parser = six.moves.configparser.SafeConfigParser
    else:
        # In python3, ConfigParser is "safe", and SafeConfigParser is a
        # deprecated alias
        parser = six.moves.configparser.ConfigParser
    config = parser()
    for config_file in config_files:
        with open(config_file, 'r') as f:
            if six.PY2:
                config.readfp(f)
            else:
                config.read_file(f)
    return config


class PathInfo(object):
    # ASCII numbers and upper- and lower-case letter for use in tmpdir()
    ASCII_CHARS = [chr(i) for i in list(range(48, 58)) + list(range(65, 91)) + list(range(97, 123))]

    def __init__(self, topdir=None):
        self._topdir = topdir

    def topdir(self):
        if self._topdir is None:
            self._topdir = str(BASEDIR)
        return self._topdir

    def _set_topdir(self, topdir):
        self._topdir = topdir

    topdir = property(topdir, _set_topdir)

    def volumedir(self, volume):
        if volume == 'DEFAULT' or volume is None:
            return self.topdir
        #else
        return self.topdir + ("/vol/%s" % volume)

    def build(self, build):
        """Return the directory where a build belongs"""
        return self.volumedir(build.get('volume_name')) + ("/packages/%(name)s/%(version)s/%(release)s" % build)

    def mavenbuild(self, build):
        """Return the directory where the Maven build exists in the global store (/mnt/koji/packages)"""
        return self.build(build) + '/maven'

    def mavenrepo(self, maveninfo):
        """Return the relative path to the artifact directory in the repo"""
        group_path = maveninfo['group_id'].replace('.', '/')
        artifact_id = maveninfo['artifact_id']
        version = maveninfo['version']
        return "%(group_path)s/%(artifact_id)s/%(version)s" % locals()

    def mavenfile(self, maveninfo):
        """Return the relative path to the artifact in the repo"""
        return self.mavenrepo(maveninfo) + '/' + maveninfo['filename']

    def winbuild(self, build):
        """Return the directory where the Windows build exists"""
        return self.build(build) + '/win'

    def winfile(self, wininfo):
        """Return the relative path from the winbuild directory where the
           file identified by wininfo is located."""
        filepath = wininfo['filename']
        if wininfo['relpath']:
            filepath = wininfo['relpath'] + '/' + filepath
        return filepath

    def imagebuild(self, build):
        """Return the directory where the image for the build are stored"""
        return self.build(build) + '/images'

    def typedir(self, build, btype):
        """Return the directory where typed files for a build are stored"""
        if btype == 'maven':
            return self.mavenbuild(build)
        elif btype == 'win':
            return self.winbuild(build)
        elif btype == 'image':
            return self.imagebuild(build)
        else:
            return "%s/files/%s" % (self.build(build), btype)

    def rpm(self, rpminfo):
        """Return the path (relative to build_dir) where an rpm belongs"""
        return "%(arch)s/%(name)s-%(version)s-%(release)s.%(arch)s.rpm" % rpminfo

    def signed(self, rpminfo, sigkey):
        """Return the path (relative to build dir) where a signed rpm lives"""
        return "data/signed/%s/" % sigkey + self.rpm(rpminfo)

    def sighdr(self, rpminfo, sigkey):
        """Return the path (relative to build_dir) where a cached sig header lives"""
        return "data/sigcache/%s/" % sigkey + self.rpm(rpminfo) + ".sig"

    def build_logs(self, build):
        """Return the path for build logs"""
        return "%s/data/logs" % self.build(build)

    def repo(self, repo_id, tag_str):
        """Return the directory where a repo belongs"""
        return self.topdir + ("/repos/%(tag_str)s/%(repo_id)s" % locals())

    def distrepo(self, repo_id, tag):
        """Return the directory with a dist repo lives"""
        return os.path.join(self.topdir, 'repos-dist', tag, str(repo_id))

    def repocache(self, tag_str):
        """Return the directory where a repo belongs"""
        return self.topdir + ("/repos/%(tag_str)s/cache" % locals())

    def taskrelpath(self, task_id):
        """Return the relative path for the task work directory"""
        return "tasks/%s/%s" % (task_id % 10000, task_id)

    def work(self, volume=None):
        """Return the work dir"""
        return self.volumedir(volume) + '/work'

    def tmpdir(self, volume=None):
        """Return a path to a unique directory under work()/tmp/"""
        tmp = None
        while tmp is None or os.path.exists(tmp):
            tmp = self.work(volume) + '/tmp/' + ''.join([random.choice(self.ASCII_CHARS) for dummy in '123456'])
        return tmp

    def scratch(self):
        """Return the main scratch dir"""
        return self.topdir + '/scratch'

    def task(self, task_id, volume=None):
        """Return the output directory for the task with the given id"""
        return self.work(volume=volume) + '/' + self.taskrelpath(task_id)

pathinfo = PathInfo()


def is_requests_cert_error(e):
    """Determine if a requests error is due to a bad cert"""

    if not isinstance(e, requests.exceptions.SSLError):
        return False

    # Using str(e) is slightly ugly, but the error stacks in python-requests
    # are way more ugly.
    errstr = str(e)
    if ('Permission denied' in errstr or  # certificate not readable
        'certificate revoked' in errstr or
        'certificate expired' in errstr or
        'certificate verify failed' in errstr):
        return True

    return False


def is_cert_error(e):
    """Determine if an OpenSSL error is due to a bad cert"""

    if SSL_Error is None:  #pragma: no cover
        # import failed, so we can't determine
        raise Exception("OpenSSL library did not load")
    if not isinstance(e, SSL_Error):
        return False

    # pyOpenSSL doesn't use different exception
    # subclasses, we have to actually parse the args
    for arg in e.args:
        # First, check to see if 'arg' is iterable because
        # it can be anything..
        try:
            iter(arg)
        except TypeError:
            continue

        # We do all this so that we can detect cert expiry
        # so we can avoid retrying those over and over.
        for items in arg:
            try:
                iter(items)
            except TypeError:
                continue

            if len(items) != 3:
                continue

            _, _, ssl_reason = items

            if ('certificate revoked' in ssl_reason or
                    'certificate expired' in ssl_reason):
                return True

    #otherwise
    return False


def is_conn_error(e):
    """Determine if an error seems to be from a dropped connection"""
    # This is intended for the case where e is a socket error.
    # as `socket.error` is just an alias for `OSError` in Python 3
    # there is no value to an `isinstance` check here; let's just
    # assume that if the exception has an 'errno' and it's one of
    # these values, this is a connection error.
    if getattr(e, 'errno', None) in (errno.ECONNRESET, errno.ECONNABORTED, errno.EPIPE):
        return True
    if isinstance(e, six.moves.http_client.BadStatusLine):
        return True
    try:
        if isinstance(e, requests.exceptions.ConnectionError):
            # we see errors like this in keep alive timeout races
            # ConnectionError(ProtocolError('Connection aborted.', BadStatusLine("''",)),)
            e2 = getattr(e, 'args', [None])[0]
            if isinstance(e2, requests.packages.urllib3.exceptions.ProtocolError):
                e3 = getattr(e2, 'args', [None, None])[1]
                if isinstance(e3, six.moves.http_client.BadStatusLine):
                    return True
            # same check as unwrapped socket error
            if getattr(e2, 'errno', None) in (errno.ECONNRESET, errno.ECONNABORTED, errno.EPIPE):
                return True
    except (TypeError, AttributeError):
        pass
    # otherwise
    return False


class VirtualMethod(object):
    # some magic to bind an XML-RPC method to an RPC server.
    # supports "nested" methods (e.g. examples.getStateName)
    # supports named arguments (if server does)
    def __init__(self, func, name):
        self.__func = func
        self.__name = name
    def __getattr__(self, name):
        return type(self)(self.__func, "%s.%s" % (self.__name, name))
    def __call__(self, *args, **opts):
        return self.__func(self.__name, args, opts)


def grab_session_options(options):
    """Convert optparse options to a dict that ClientSession can handle;
    If options is already a dict, filter out meaningless and None value items"""
    s_opts = (
        'user',
        'password',
        'krbservice',
        'debug_xmlrpc',
        'debug',
        'max_retries',
        'retry_interval',
        'offline_retry',
        'offline_retry_interval',
        'anon_retry',
        'keepalive',
        'timeout',
        'auth_timeout',
        'use_fast_upload',
        'upload_blocksize',
        'krb_rdns',
        'krb_canon_host',
        'no_ssl_verify',
        'serverca',
    )
    # cert is omitted for now
    if isinstance(options, dict):
        return dict((k, v) for k, v in six.iteritems(options) if k in s_opts and v is not None)
    ret = {}
    for key in s_opts:
        if not hasattr(options, key):
            continue
        value = getattr(options, key)
        if value is not None:
            ret[key] = value
    return ret


class ClientSession(object):

    def __init__(self, baseurl, opts=None, sinfo=None):
        assert baseurl, "baseurl argument must not be empty"
        if opts == None:
            opts = {}
        else:
            opts = opts.copy()
        self.baseurl = baseurl
        self.opts = opts
        self.authtype = None
        self.setSession(sinfo)
        self.multicall = False
        self._calls = []
        self.logger = logging.getLogger('koji')
        self.rsession = None
        self.new_session()
        self.opts.setdefault('timeout', DEFAULT_REQUEST_TIMEOUT)


    def new_session(self):
        self.logger.debug("Opening new requests session")
        if self.rsession:
            self.rsession.close()
        self.rsession = requests.Session()

    def setSession(self, sinfo):
        """Set the session info

        If sinfo is None, logout."""
        if sinfo is None:
            self.logged_in = False
            self.callnum = None
            # do we need to do anything else here?
            self.authtype = None
        else:
            self.logged_in = True
            self.callnum = 0
        self.sinfo = sinfo

    def login(self, opts=None):
        sinfo = self.callMethod('login', self.opts['user'], self.opts['password'], opts)
        if not sinfo:
            return False
        self.setSession(sinfo)
        self.authtype = AUTHTYPE_NORMAL
        return True

    def subsession(self):
        "Create a subsession"
        sinfo = self.callMethod('subsession')
        return type(self)(self.baseurl, self.opts, sinfo)

    def krb_login(self, principal=None, keytab=None, ccache=None, proxyuser=None, ctx=None):
        """Log in using Kerberos.  If principal is not None and keytab is
        not None, then get credentials for the given principal from the given keytab.
        If both are None, authenticate using existing local credentials (as obtained
        from kinit).  ccache is the absolute path to use for the credential cache. If
        not specified, the default ccache will be used.  If proxyuser is specified,
        log in the given user instead of the user associated with the Kerberos
        principal.  The principal must be in the "ProxyPrincipals" list on
        the server side.  ctx is the Kerberos context to use, and should be unique
        per thread.  If ctx is not specified, the default context is used."""

        try:
            # Silently try GSSAPI first
            if self.gssapi_login(principal, keytab, ccache, proxyuser=proxyuser):
                return True
        except Exception as e:
            if krbV:
                e_str = ''.join(traceback.format_exception_only(type(e), e))
                self.logger.debug('gssapi auth failed: %s', e_str)
                pass
            else:
                raise

        if not krbV:
            raise PythonImportError(
                "Please install python-krbV to use kerberos."
            )

        if not ctx:
            ctx = krbV.default_context()

        if ccache != None:
            ccache = krbV.CCache(name=ccache, context=ctx)
        else:
            ccache = ctx.default_ccache()

        if principal != None:
            if keytab != None:
                cprinc = krbV.Principal(name=principal, context=ctx)
                keytab = krbV.Keytab(name=keytab, context=ctx)
                ccache.init(cprinc)
                ccache.init_creds_keytab(principal=cprinc, keytab=keytab)
            else:
                raise AuthError('cannot specify a principal without a keytab')
        else:
            # We're trying to log ourself in.  Connect using existing credentials.
            cprinc = ccache.principal()

        self.logger.debug('Authenticating as: %s', cprinc.name)
        sprinc = krbV.Principal(name=self._serverPrincipal(cprinc), context=ctx)

        ac = krbV.AuthContext(context=ctx)
        ac.flags = krbV.KRB5_AUTH_CONTEXT_DO_SEQUENCE | krbV.KRB5_AUTH_CONTEXT_DO_TIME
        ac.rcache = ctx.default_rcache()

        # create and encode the authentication request
        (ac, req) = ctx.mk_req(server=sprinc, client=cprinc,
                               auth_context=ac, ccache=ccache,
                               options=krbV.AP_OPTS_MUTUAL_REQUIRED)
        req_enc = base64.encodestring(req)

        # ask the server to authenticate us
        (rep_enc, sinfo_enc, addrinfo) = self.callMethod('krbLogin', req_enc, proxyuser)
        # Set the addrinfo we received from the server
        # (necessary before calling rd_priv())
        # addrinfo is in (serveraddr, serverport, clientaddr, clientport)
        # format, so swap the pairs because clientaddr is now the local addr
        ac.addrs = tuple((addrinfo[2], addrinfo[3], addrinfo[0], addrinfo[1]))

        # decode and read the reply from the server
        rep = base64.b64decode(rep_enc)
        ctx.rd_rep(rep, auth_context=ac)

        # decode and decrypt the login info
        sinfo_priv = base64.b64decode(sinfo_enc)
        sinfo_str = ac.rd_priv(sinfo_priv)
        sinfo = dict(zip(['session-id', 'session-key'], sinfo_str.split()))

        if not sinfo:
            self.logger.warn('No session info received')
            return False
        self.setSession(sinfo)

        self.authtype = AUTHTYPE_KERB
        return True

    def _serverPrincipal(self, cprinc):
        """Get the Kerberos principal of the server we're connecting
        to, based on baseurl."""

        host = six.moves.urllib.parse.urlparse(self.baseurl).hostname
        servername = self._fix_krb_host(host)
        realm = cprinc.realm
        service = self.opts.get('krbservice', 'host')

        ret = '%s/%s@%s' % (service, servername, realm)
        self.logger.debug('Using server principal: %s', ret)
        return ret

    def _fix_krb_host(self, host):
        if self.opts.get('krb_canon_host', False):
            if dns_resolver is None:
                self.logger.warning('python-dns missing -- cannot resolve hostname')
            else:
                answer = dns_resolver.query(host, 'A')
                return answer.canonical_name.to_text(omit_final_dot=True)
        if self.opts.get('krb_rdns', True):
            return socket.getfqdn(host)
        # else
        return host

    def gssapi_login(self, principal=None, keytab=None, ccache=None, proxyuser=None):
        if not requests_kerberos:
            raise PythonImportError(
                "Please install python-requests-kerberos to use GSSAPI."
            )
        # force https
        old_baseurl = self.baseurl
        uri = six.moves.urllib.parse.urlsplit(self.baseurl)
        if uri[0] != 'https':
            self.baseurl = 'https://%s%s' % (uri[1], uri[2])

        # Force a new session
        self.new_session()

        sinfo = None
        old_env = {}
        old_opts = self.opts
        self.opts = old_opts.copy()
        try:
            # temporary timeout value during login
            self.opts['timeout'] = self.opts.get('auth_timeout',
                                                 DEFAULT_AUTH_TIMEOUT)
            kwargs = {}
            if keytab:
                old_env['KRB5_CLIENT_KTNAME'] = os.environ.get('KRB5_CLIENT_KTNAME')
                os.environ['KRB5_CLIENT_KTNAME'] = keytab
            if ccache:
                old_env['KRB5CCNAME'] = os.environ.get('KRB5CCNAME')
                os.environ['KRB5CCNAME'] = ccache
            if principal:
                if re.match(r'0[.][1-8]\b', requests_kerberos.__version__):
                    raise PythonImportError(
                            'python-requests-kerberos >= 0.9.0 required for '
                            'keytab auth'
                    )
                else:
                    kwargs['principal'] = principal
            self.opts['auth'] = requests_kerberos.HTTPKerberosAuth(**kwargs)
            try:
                # Depending on the server configuration, we might not be able to
                # connect without client certificate, which means that the conn
                # will fail with a handshake failure, which is retried by default.
                sinfo = self._callMethod('sslLogin', [proxyuser], retry=False)
            except Exception as e:
                e_str = ''.join(traceback.format_exception_only(type(e), e))
                self.logger.debug('gssapi auth failed: %s', e_str)
                # Auth with https didn't work. Restore for the next attempt.
                self.baseurl = old_baseurl
        finally:
            self.opts = old_opts
            for key in old_env:
                if old_env[key] is None:
                    del os.environ[key]
                else:
                    os.environ[key] = old_env[key]
        if not sinfo:
            raise AuthError('unable to obtain a session')

        self.setSession(sinfo)

        self.authtype = AUTHTYPE_GSSAPI
        return True

    def ssl_login(self, cert=None, ca=None, serverca=None, proxyuser=None):
        cert = cert or self.opts.get('cert')
        serverca = serverca or self.opts.get('serverca')
        if cert is None:
            raise AuthError('No certification provided')
        if not os.access(cert, os.R_OK):
            raise AuthError("Certificate %s doesn't exist or is not accessible" % cert)
        if serverca is not None and not os.access(serverca, os.R_OK):
            raise AuthError("Server CA %s doesn't exist or is not accessible" % serverca)
        # FIXME: ca is not useful here and therefore ignored, can be removed
        # when API is changed

        # force https
        uri = six.moves.urllib.parse.urlsplit(self.baseurl)
        if uri[0] != 'https':
            self.baseurl = 'https://%s%s' % (uri[1], uri[2])

        # Force a new session
        self.new_session()

        old_opts = self.opts
        self.opts = old_opts.copy()
        # temporary timeout value during login
        self.opts['timeout'] = self.opts.get('auth_timeout',
                                             DEFAULT_AUTH_TIMEOUT)
        self.opts['cert'] = cert
        self.opts['serverca'] = serverca
        try:
            sinfo = self.callMethod('sslLogin', proxyuser)
        finally:
            self.opts = old_opts
        if not sinfo:
            raise AuthError('unable to obtain a session')

        self.opts['cert'] = cert
        self.opts['serverca'] = serverca
        self.setSession(sinfo)

        self.authtype = AUTHTYPE_SSL
        return True

    def logout(self):
        if not self.logged_in:
            return
        try:
            # bypass _callMethod (no retries)
            # XXX - is that really what we want?
            handler, headers, request = self._prepCall('logout', ())
            self._sendCall(handler, headers, request)
        except AuthExpired:
            #this can happen when an exclusive session is forced
            pass
        self.setSession(None)

    def _forget(self):
        """Forget session information, but do not close the session

        This is intended to be used after a fork to prevent the subprocess
        from affecting the session accidentally.

        Unfortunately the term session is overloaded. We forget:
          - the login session
          - the underlying python-requests session

        But the ClientSession instance (i.e. self) persists
        """

        # forget our requests session
        self.new_session()

        # forget our login session, if any
        if not self.logged_in:
            return
        self.setSession(None)

    #we've had some trouble with this method causing strange problems
    #(like infinite recursion). Possibly triggered by initialization failure,
    #and possibly due to some interaction with __getattr__.
    #Re-enabling with a small improvement
    def __del__(self):
        if self.__dict__:
            try:
                self.logout()
            except:
                pass

    def callMethod(self, name, *args, **opts):
        """compatibility wrapper for _callMethod"""
        return self._callMethod(name, args, opts)

    def _prepCall(self, name, args, kwargs=None):
        #pass named opts in a way the server can understand
        if kwargs is None:
            kwargs = {}
        if name == 'rawUpload':
            return self._prepUpload(*args, **kwargs)
        args = encode_args(*args, **kwargs)
        if self.logged_in:
            sinfo = self.sinfo.copy()
            sinfo['callnum'] = self.callnum
            self.callnum += 1
            handler = "%s?%s" % (self.baseurl, six.moves.urllib.parse.urlencode(sinfo))
        elif name == 'sslLogin':
            handler = self.baseurl + '/ssllogin'
        else:
            handler = self.baseurl
        request = dumps(args, name, allow_none=1)
        if six.PY3:
            try:
                request.encode('latin-1')
            except UnicodeEncodeError:
                # if string is not converted to UTF, requests will raise an error
                # on identical check before sending data
                # py3 string throws UnicodeEncodeError
                request = request.encode('utf-8')
        headers = [
            # connection class handles Host
            ('User-Agent', 'koji/1'),
            ('Content-Type', 'text/xml'),
            ('Content-Length', str(len(request))),
        ]
        return handler, headers, request

    def _sendCall(self, handler, headers, request):
        # handle expired connections
        for i in (0, 1):
            try:
                return self._sendOneCall(handler, headers, request)
            except Exception as e:
                if i or not is_conn_error(e):
                    raise
                self.logger.debug("Connection Error: %s", e)
                self.new_session()

    def _sendOneCall(self, handler, headers, request):
        headers = dict(headers)
        callopts = {
            'headers': headers,
            'data': request,
            'stream': True,
        }
        verify = self.opts.get('serverca')
        if verify:
            callopts['verify'] = verify
        elif self.opts.get('no_ssl_verify'):
            callopts['verify'] = False
            # XXX - not great, but this is the previous behavior
        cert = self.opts.get('cert')
        if cert:
            # TODO: we really only need to do this for ssllogin calls
            callopts['cert'] = cert
        auth = self.opts.get('auth')
        if auth:
            callopts['auth'] = auth
        timeout = self.opts.get('timeout')
        if timeout:
            callopts['timeout'] = timeout
        if self.opts.get('debug_xmlrpc', False):
            self.logger.debug("url: %s" % handler)
            for _key in callopts:
                _val = callopts[_key]
                if _key == 'data' and len(_val) > 1024:
                    _val = _val[:1024] + '...'
                self.logger.debug("%s: %r" % (_key, _val))
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            r = self.rsession.post(handler, **callopts)
            r.raise_for_status()
            try:
                ret = self._read_xmlrpc_response(r)
            finally:
                r.close()
        return ret

    def _read_xmlrpc_response(self, response):
        p, u = getparser()
        for chunk in response.iter_content(8192):
            if self.opts.get('debug_xmlrpc', False):
                self.logger.debug("body: %r" % chunk)
            p.feed(chunk)
        p.close()
        result = u.close()
        if len(result) == 1:
            result = result[0]
        return result

    def _callMethod(self, name, args, kwargs=None, retry=True):
        """Make a call to the hub with retries and other niceties"""

        if self.multicall:
            if kwargs is None:
                kwargs = {}
            args = encode_args(*args, **kwargs)
            self._calls.append({'methodName': name, 'params': args})
            return MultiCallInProgress
        else:
            handler, headers, request = self._prepCall(name, args, kwargs)
            tries = 0
            self.retries = 0
            max_retries = self.opts.get('max_retries', 30)
            interval = self.opts.get('retry_interval', 20)
            while True:
                tries += 1
                self.retries += 1
                try:
                    return self._sendCall(handler, headers, request)
                #basically, we want to retry on most errors, with a few exceptions
                #  - faults (this means the call completed and failed)
                #  - SystemExit, KeyboardInterrupt
                # note that, for logged-in sessions the server should tell us (via a RetryError fault)
                # if the call cannot be retried. For non-logged-in sessions, all calls should be read-only
                # and hence retryable.
                except Fault as fault:
                    #try to convert the fault to a known exception
                    err = convertFault(fault)
                    if isinstance(err, ServerOffline):
                        if self.opts.get('offline_retry', False):
                            secs = self.opts.get('offline_retry_interval', interval)
                            self.logger.debug("Server offline. Retrying in %i seconds", secs)
                            time.sleep(secs)
                            #reset try count - this isn't a typical error, this is a running server
                            #correctly reporting an outage
                            tries = 0
                            continue
                    raise err
                except (SystemExit, KeyboardInterrupt):
                    #(depending on the python version, these may or may not be subclasses of Exception)
                    raise
                except Exception as e:
                    tb_str = ''.join(traceback.format_exception(*sys.exc_info()))
                    self.new_session()

                    if is_cert_error(e) or is_requests_cert_error(e):
                        # There's no point in retrying for this
                        raise

                    if not self.logged_in:
                        #in the past, non-logged-in sessions did not retry. For compatibility purposes
                        #this behavior is governed by the anon_retry opt.
                        if not self.opts.get('anon_retry', False):
                            raise

                    if not retry:
                        raise

                    if tries > max_retries:
                        raise
                    #otherwise keep retrying
                    if self.logger.isEnabledFor(logging.DEBUG):
                        self.logger.debug(tb_str)
                    self.logger.info("Try #%s for call %s (%s) failed: %s", tries, self.callnum, name, e)
                if tries > 1:
                    # first retry is immediate, after that we honor retry_interval
                    time.sleep(interval)
            #not reached

    def multiCall(self, strict=False, batch=None):
        """Execute a prepared multicall

        In a multicall, a number of calls are combined into a single RPC call
        and handled by the server in a batch. This can improve throughput.

        The server handles a multicall as a single database transaction (though
        see the note about the batch option below).

        To prepare a multicall:
          1. set the multicall attribute to True
          2. issue one or more calls in the normal fashion

        When multicall is True, the call parameters are stored rather than
        passed to the server. Each call will return the special value
        MultiCallInProgress, since the return is not yet known.

        This method executes the prepared multicall, resets the multicall
        attribute to False (so subsequent calls will work normally), and
        returns the results of the calls as a list.

        The result list will contain one element for each call added to the
        multicall, in the order it was added. Each element will be either:
          - a one-element list containing the result of the method call
          - a map containing "faultCode" and "faultString" keys, describing
            the error that occurred during the call.

        If the strict option is set to True, then this call will raise the
        first error it encounters, if any.

        If the batch option is set to a number greater than zero, the calls
        will be spread across multiple multicall batches of at most this
        number. Note that each such batch will be a separate database
        transaction.
        """
        if not self.multicall:
            raise GenericError('ClientSession.multicall must be set to True before calling multiCall()')
        self.multicall = False
        if len(self._calls) == 0:
            return []

        calls = self._calls
        self._calls = []
        if batch is not None and batch > 0:
            ret = []
            callgrp = (calls[i:i + batch] for i in range(0, len(calls), batch))
            self.logger.debug("MultiCall with batch size %i, calls/groups(%i/%i)",
                              batch, len(calls), round(len(calls) // batch))
            for c in callgrp:
                ret.extend(self._callMethod('multiCall', (c,), {}))
        else:
            ret = self._callMethod('multiCall', (calls,), {})
        if strict:
            #check for faults and raise first one
            for entry in ret:
                if isinstance(entry, dict):
                    fault = Fault(entry['faultCode'], entry['faultString'])
                    err = convertFault(fault)
                    raise err
        return ret

    def __getattr__(self, name):
        #if name[:1] == '_':
        #    raise AttributeError("no attribute %r" % name)
        return VirtualMethod(self._callMethod, name)

    def fastUpload(self, localfile, path, name=None, callback=None, blocksize=None, overwrite=False, volume=None):
        if blocksize is None:
            blocksize = self.opts.get('upload_blocksize', 1048576)

        if not self.logged_in:
            raise ActionNotAllowed('You must be logged in to upload files')
        if name is None:
            name = os.path.basename(localfile)
        self.logger.debug("Fast upload: %s to %s/%s", localfile, path, name)
        fo = open(localfile, 'rb')
        ofs = 0
        size = os.path.getsize(localfile)
        start = time.time()
        if callback:
            callback(0, size, 0, 0, 0)
        problems = False
        full_chksum = util.adler32_constructor()
        # cycle is need to run at least once (for empty files)
        first_cycle = True
        callopts = {'overwrite': overwrite}
        if volume and volume != 'DEFAULT':
            callopts['volume'] = volume
        while True:
            lap = time.time()
            chunk = fo.read(blocksize)
            if not chunk and not first_cycle:
                break
            first_cycle = False
            result = self._callMethod('rawUpload', (chunk, ofs, path, name), callopts)
            if self.retries > 1:
                problems = True
            hexdigest = util.adler32_constructor(chunk).hexdigest()
            full_chksum.update(chunk)
            if result['size'] != len(chunk):
                raise GenericError("server returned wrong chunk size: %s != %s" % (result['size'], len(chunk)))
            if result['hexdigest'] != hexdigest:
                raise GenericError('upload checksum failed: %s != %s' \
                        % (result['hexdigest'], hexdigest))
            ofs += len(chunk)
            now = time.time()
            t1 = max(now - lap, 0.00001)
            t2 = max(now - start, 0.00001)
            # max is to prevent possible divide by zero in callback function
            if callback:
                callback(ofs, size, len(chunk), t1, t2)
        if ofs != size:
            self.logger.error("Local file changed size: %s, %s -> %s", localfile, size, ofs)
        chk_opts = {}
        if volume and volume != 'DEFAULT':
            chk_opts['volume'] = volume
        if problems:
            chk_opts['verify'] = 'adler32'
        result = self._callMethod('checkUpload', (path, name), chk_opts)
        if result is None:
            raise GenericError("File upload failed: %s/%s" % (path, name))
        if int(result['size']) != ofs:
            raise GenericError("Uploaded file is wrong length: %s/%s, %s != %s" \
                    % (path, name, result['size'], ofs))
        if problems and result['hexdigest'] != full_chksum.hexdigest():
            raise GenericError("Uploaded file has wrong checksum: %s/%s, %s != %s" \
                    % (path, name, result['hexdigest'], full_chksum.hexdigest()))
        self.logger.debug("Fast upload: %s complete. %i bytes in %.1f seconds", localfile, size, t2)

    def _prepUpload(self, chunk, offset, path, name, verify="adler32", overwrite=False, volume=None):
        """prep a rawUpload call"""
        if not self.logged_in:
            raise ActionNotAllowed("you must be logged in to upload")
        args = self.sinfo.copy()
        args['callnum'] = self.callnum
        args['filename'] = name
        args['filepath'] = path
        args['fileverify'] = verify
        args['offset'] = str(offset)
        if overwrite:
            args['overwrite'] = "1"
        if volume is not None:
            args['volume'] = volume
        size = len(chunk)
        self.callnum += 1
        handler = "%s?%s" % (self.baseurl, six.moves.urllib.parse.urlencode(args))
        headers = [
            ('User-Agent', 'koji/1'),
            ("Content-Type", "application/octet-stream"),
            ("Content-length", str(size)),
        ]
        request = chunk
        if six.PY3 and isinstance(chunk, str):
            request = chunk.encode('utf-8')
        else:
            # py2 or bytes
            request = chunk
        return handler, headers, request

    def uploadWrapper(self, localfile, path, name=None, callback=None, blocksize=None, overwrite=True, volume=None):
        """upload a file in chunks using the uploadFile call"""
        if blocksize is None:
            blocksize = self.opts.get('upload_blocksize', 1048576)

        if self.opts.get('use_fast_upload'):
            self.fastUpload(localfile, path, name, callback, blocksize, overwrite, volume=volume)
            return
        if name is None:
            name = os.path.basename(localfile)

        volopts = {}
        if volume and volume != 'DEFAULT':
            volopts['volume'] = volume

        # check if server supports fast upload
        try:
            self._callMethod('checkUpload', (path, name), volopts)
            # fast upload was introduced in 1.7.1, earlier servers will not
            # recognise this call and return an error
        except GenericError:
            pass
        else:
            self.fastUpload(localfile, path, name, callback, blocksize, overwrite, volume=volume)
            return

        start = time.time()
        # XXX - stick in a config or something
        retries = 3
        fo = open(localfile, "rb")  #specify bufsize?
        totalsize = os.path.getsize(localfile)
        ofs = 0
        md5sum = util.md5_constructor()
        debug = self.opts.get('debug', False)
        if callback:
            callback(0, totalsize, 0, 0, 0)
        while True:
            lap = time.time()
            contents = fo.read(blocksize)
            md5sum.update(contents)
            size = len(contents)
            data = util.base64encode(contents)
            if size == 0:
                # end of file, use offset = -1 to finalize upload
                offset = -1
                digest = md5sum.hexdigest()
                sz = ofs
            else:
                offset = ofs
                digest = util.md5_constructor(contents).hexdigest()
                sz = size
            del contents
            tries = 0
            while True:
                if debug:
                    self.logger.debug("uploadFile(%r,%r,%r,%r,%r,...)" %(path, name, sz, digest, offset))
                if self.callMethod('uploadFile', path, name, sz, digest, offset, data, **volopts):
                    break
                if tries <= retries:
                    tries += 1
                    continue
                else:
                    raise GenericError("Error uploading file %s, offset %d" %(path, offset))
            if size == 0:
                break
            ofs += size
            now = time.time()
            t1 = now - lap
            if t1 <= 0:
                t1 = 1
            t2 = now - start
            if t2 <= 0:
                t2 = 1
            if debug:
                self.logger.debug("Uploaded %d bytes in %f seconds (%f kbytes/sec)" % (size, t1, size / t1 / 1024.0))
            if debug:
                self.logger.debug("Total: %d bytes in %f seconds (%f kbytes/sec)" % (ofs, t2, ofs / t2 / 1024.0))
            if callback:
                callback(ofs, totalsize, size, t1, t2)
        fo.close()

    def downloadTaskOutput(self, taskID, fileName, offset=0, size=-1, volume=None):
        """Download the file with the given name, generated by the task with the
        given ID.

        Note: This method does not work with multicall.
        """
        if self.multicall:
            raise GenericError('downloadTaskOutput() may not be called during a multicall')
        dlopts = {'offset': offset, 'size': size}
        if volume and volume != 'DEFAULT':
            dlopts['volume'] = volume
        result = self.callMethod('downloadTaskOutput', taskID, fileName, **dlopts)
        return base64.b64decode(result)


class DBHandler(logging.Handler):
    """
    A handler class which writes logging records, appropriately formatted,
    to a database.
    """
    def __init__(self, cnx, table, mapping=None):
        """
        Initialize the handler.

        A database connection and table name are required.
        """
        logging.Handler.__init__(self)
        self.cnx = cnx
        self.table = table
        if mapping is None:
            self.mapping = {'message': '%(message)s'}
        else:
            self.mapping = mapping

    def emit(self, record):
        """
        Emit a record.

        If a formatter is specified, it is used to format the record.
        """
        try:
            cursor = self.cnx.cursor()
            columns = []
            values = []
            data = {}
            record.message = record.getMessage()
            for key, value in six.iteritems(self.mapping):
                value = str(value)
                if value.find("%(asctime)") >= 0:
                    if self.formatter:
                        fmt = self.formatter
                    else:
                        fmt = logging._defaultFormatter
                    record.asctime = fmt.formatTime(record, fmt.datefmt)
                columns.append(key)
                values.append("%%(%s)s" % key)
                data[key] = value % record.__dict__
                #values.append(_quote(value % record.__dict__))
            columns = ",".join(columns)
            values = ",".join(values)
            command = "INSERT INTO %s (%s) VALUES (%s)" % (self.table, columns, values)
            #note we're letting cursor.execute do the escaping
            cursor.execute(command, data)
            cursor.close()
            #self.cnx.commit()
            #XXX - committing here is most likely wrong, but we need to set commit_pending or something
            #      ...and this is really the wrong place for that
        except:
            self.handleError(record)

def formatTime(value):
    """Format a timestamp so it looks nicer"""
    if not value:
        return ''
    if isinstance(value, xmlrpc_client.DateTime):
        value = datetime.datetime.strptime(value.value, "%Y%m%dT%H:%M:%S")
    if isinstance(value, datetime.datetime):
        return value.strftime('%Y-%m-%d %H:%M:%S')
    else:
        # trim off the microseconds, if present
        dotidx = value.rfind('.')
        if dotidx != -1:
            return value[:dotidx]
        else:
            return value

def formatTimeLong(value):
    """Format a timestamp to a more human-reable format, i.e.:
    Sat, 07 Sep 2002 00:00:01 GMT
    """
    if not value:
        return ''
    else:
        # Assume the string value passed in is the local time
        localtime = time.mktime(time.strptime(formatTime(value), '%Y-%m-%d %H:%M:%S'))
        return time.strftime('%a, %d %b %Y %H:%M:%S %Z', time.localtime(localtime))

def buildLabel(buildInfo, showEpoch=False):
    """Format buildInfo (dict) into a descriptive label."""
    epoch = buildInfo.get('epoch')
    if showEpoch and epoch != None:
        epochStr = '%i:' % epoch
    else:
        epochStr = ''
    name = buildInfo.get('package_name')
    if not name:
        name = buildInfo.get('name')
    return '%s%s-%s-%s' % (epochStr, name,
                           buildInfo.get('version'),
                           buildInfo.get('release'))

def _module_info(url):
    module_info = ''
    if '?' in url:
        # extract the module path
        module_info = url[url.find('?') + 1:url.find('#')]
    # Find the first / after the scheme://
    repo_start = url.find('/', url.find('://') + 3)
    # Find the ? if present, otherwise find the #
    repo_end = url.find('?')
    if repo_end == -1:
        repo_end = url.find('#')
    repo_info = url[repo_start:repo_end]
    rev_info = url[url.find('#') + 1:]
    if module_info:
        return '%s:%s:%s' % (repo_info, module_info, rev_info)
    else:
        return '%s:%s' % (repo_info, rev_info)

def taskLabel(taskInfo):
    try:
        return _taskLabel(taskInfo)
    except Exception:
        return "malformed task"

def _taskLabel(taskInfo):
    """Format taskInfo (dict) into a descriptive label."""
    method = taskInfo['method']
    arch = taskInfo['arch']
    extra = ''
    if method in ('build', 'maven'):
        if 'request' in taskInfo:
            source, target = taskInfo['request'][:2]
            if '://' in source:
                module_info = _module_info(source)
            else:
                module_info = os.path.basename(source)
            extra = '%s, %s' % (target, module_info)
    elif method in ('buildSRPMFromSCM', 'buildSRPMFromCVS'):
        if 'request' in taskInfo:
            url = taskInfo['request'][0]
            extra = _module_info(url)
    elif method == 'buildArch':
        if 'request' in taskInfo:
            srpm, tagID, arch = taskInfo['request'][:3]
            srpm = os.path.basename(srpm)
            extra = '%s, %s' % (srpm, arch)
    elif method == 'buildMaven':
        if 'request' in taskInfo:
            build_tag = taskInfo['request'][1]
            extra = build_tag['name']
    elif method == 'wrapperRPM':
        if 'request' in taskInfo:
            build_target = taskInfo['request'][1]
            build = taskInfo['request'][2]
            if build:
                extra = '%s, %s' % (build_target['name'], buildLabel(build))
            else:
                extra = build_target['name']
    elif method == 'winbuild':
        if 'request' in taskInfo:
            #vm = taskInfo['request'][0]
            url = taskInfo['request'][1]
            target = taskInfo['request'][2]
            module_info = _module_info(url)
            extra = '%s, %s' % (target, module_info)
    elif method == 'vmExec':
        if 'request' in taskInfo:
            extra = taskInfo['request'][0]
    elif method == 'buildNotification':
        if 'request' in taskInfo:
            build = taskInfo['request'][1]
            extra = buildLabel(build)
    elif method in ('newRepo', 'distRepo'):
        if 'request' in taskInfo:
            extra = str(taskInfo['request'][0])
    elif method in ('tagBuild', 'tagNotification'):
        # There is no displayable information included in the request
        # for these methods
        pass
    elif method == 'prepRepo':
        if 'request' in taskInfo:
            tagInfo = taskInfo['request'][0]
            extra = tagInfo['name']
    elif method == 'createrepo':
        if 'request' in taskInfo:
            arch = taskInfo['request'][1]
            extra = arch
    elif method == 'createdistrepo':
        if 'request' in taskInfo:
            repo_id = taskInfo['request'][1]
            arch = taskInfo['request'][2]
            extra = '%s, %s' % (repo_id, arch)
    elif method == 'dependantTask':
        if 'request' in taskInfo:
            extra = ', '.join([subtask[0] for subtask in taskInfo['request'][1]])
    elif method in ('chainbuild', 'chainmaven'):
        if 'request' in taskInfo:
            extra = taskInfo['request'][1]
    elif method == 'waitrepo':
        if 'request' in taskInfo:
            extra = str(taskInfo['request'][0])
            if len(taskInfo['request']) >= 3:
                nvrs = taskInfo['request'][2]
                if isinstance(nvrs, list):
                    extra += ', ' + ', '.join(nvrs)
    elif method in ('livecd', 'appliance', 'image', 'livemedia'):
        if 'request' in taskInfo:
            stuff = taskInfo['request']
            if method == 'image':
                kickstart = os.path.basename(stuff[-1]['kickstart'])
            else:
                kickstart = os.path.basename(stuff[4])
            extra = '%s, %s-%s, %s' % (stuff[3], stuff[0], stuff[1], kickstart)
    elif method in ('createLiveCD', 'createAppliance', 'createImage', 'createLiveMedia'):
        if 'request' in taskInfo:
            stuff = taskInfo['request']
            if method == 'createImage':
                kickstart = os.path.basename(stuff[-1]['kickstart'])
            else:
                kickstart = os.path.basename(stuff[7])
            extra = '%s, %s-%s-%s, %s, %s' % (stuff[4]['name'], stuff[0],
                stuff[1], stuff[2], kickstart, stuff[3])
    elif method == 'restart':
        if 'request' in taskInfo:
            host = taskInfo['request'][0]
            extra = host['name']
    elif method == 'restartVerify':
        if 'request' in taskInfo:
            task_id, host = taskInfo['request'][:2]
            extra = host['name']

    if extra:
        return '%s (%s)' % (method, extra)
    else:
        return '%s (%s)' % (method, arch)

CONTROL_CHARS = [chr(i) for i in range(32)]
NONPRINTABLE_CHARS = ''.join([c for c in CONTROL_CHARS if c not in '\r\n\t'])
if six.PY3:
    NONPRINTABLE_CHARS_TABLE = dict.fromkeys(map(ord, NONPRINTABLE_CHARS), None)
def removeNonprintable(value):
    # expects raw-encoded string, not unicode
    if six.PY2:
        return value.translate(None, NONPRINTABLE_CHARS)
    else:
        return value.translate(NONPRINTABLE_CHARS_TABLE)



def _fix_print(value):
    """Fix a string so it is suitable to print

    In python2, this means we return a utf8 encoded str
    In python3, this means we return unicode
    """
    if six.PY2 and isinstance(value, six.text_type):
        return value.encode('utf8')
    elif six.PY3 and isinstance(value, six.binary_type):
        return value.decode('utf8')
    else:
        return value


def fixEncoding(value, fallback='iso8859-15', remove_nonprintable=False):
    """
    Convert value to a 'str' object encoded as UTF-8.
    If value is not valid UTF-8 to begin with, assume it is
    encoded in the 'fallback' charset.
    """
    if six.PY3:
        if remove_nonprintable:
            return removeNonprintable(value)
        else:
            return value

    if not value:
        return six.b('')

    if isinstance(value, six.text_type):
        # value is already unicode(py3: str), so just convert it
        # to a utf8-encoded str(py3: bytes)
        s = value.encode('utf8')
    else:
        # value is a str, but may be encoded in utf8 or some
        # other non-ascii charset.  Try to verify it's utf8, and if not,
        # decode it using the fallback encoding.
        try:
            s = value.decode('utf8').encode('utf8')
        except UnicodeDecodeError:
            s = value.decode(fallback).encode('utf8')
    if remove_nonprintable:
        return removeNonprintable(s)
    else:
        return s


def fixEncodingRecurse(value, fallback='iso8859-15', remove_nonprintable=False):
    """Recursively fix string encoding in an object

    Similar behavior to fixEncoding, but recursive
    """
    if six.PY3 and not remove_nonprintable:
        # don't bother with fixing in py3
        return value

    if isinstance(value, tuple):
        return tuple([fixEncodingRecurse(x, fallback=fallback, remove_nonprintable=remove_nonprintable) for x in value])
    elif isinstance(value, list):
        return [fixEncodingRecurse(x, fallback=fallback, remove_nonprintable=remove_nonprintable) for x in value]
    elif isinstance(value, dict):
        ret = {}
        for k in value:
            v = fixEncodingRecurse(value[k], fallback=fallback, remove_nonprintable=remove_nonprintable)
            k = fixEncodingRecurse(k, fallback=fallback, remove_nonprintable=remove_nonprintable)
            ret[k] = v
        return ret
    elif six.PY2 and isinstance(value, six.text_type):
        if remove_nonprintable:
            return removeNonprintable(value.encode('utf8'))
        else:
            return value.encode('utf8')
    elif six.PY2 and isinstance(value, str):
        # value is a str, but may be encoded in utf8 or some
        # other non-ascii charset.  Try to verify it's utf8, and if not,
        # decode it using the fallback encoding.
        try:
            s = value.decode('utf8').encode('utf8')
        except UnicodeDecodeError:
            s = value.decode(fallback).encode('utf8')
        if remove_nonprintable:
            return removeNonprintable(s)
        else:
            return s
    elif six.PY3 and isinstance(value, str) and remove_nonprintable:
        return removeNonprintable(value)
    else:
        return value


def add_file_logger(logger, fn):
    if not os.path.exists(fn):
        try:
            fh = open(fn, 'w')
            fh.close()
        except (ValueError, IOError):
            return
    if not os.path.isfile(fn):
        return
    if not os.access(fn, os.W_OK):
        return
    handler = logging.handlers.RotatingFileHandler(fn, maxBytes=1024*1024*10, backupCount=5)
    handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s'))
    logging.getLogger(logger).addHandler(handler)

def add_stderr_logger(logger):
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] {%(process)d} %(name)s:%(lineno)d %(message)s'))
    handler.setLevel(logging.DEBUG)
    logging.getLogger(logger).addHandler(handler)

def add_sys_logger(logger):
    # For remote logging;
    # address = ('host.example.com', logging.handlers.SysLogHandler.SYSLOG_UDP_PORT)
    address = "/dev/log"
    handler = logging.handlers.SysLogHandler(address=address,
                                             facility=logging.handlers.SysLogHandler.LOG_DAEMON)
    handler.setFormatter(logging.Formatter('%(name)s: %(message)s'))
    handler.setLevel(logging.INFO)
    logging.getLogger(logger).addHandler(handler)

def add_mail_logger(logger, addr):
    if not addr:
        return
    handler = logging.handlers.SMTPHandler("localhost",
                                           "%s@%s" % (pwd.getpwuid(os.getuid())[0], socket.getfqdn()),
                                           addr,
                                           "%s: error notice" % socket.getfqdn())
    handler.setFormatter(logging.Formatter('%(pathname)s:%(lineno)d [%(levelname)s] %(message)s'))
    handler.setLevel(logging.ERROR)
    logging.getLogger(logger).addHandler(handler)

def remove_log_handler(logger, handler):
    logging.getLogger(logger).removeHandler(handler)
