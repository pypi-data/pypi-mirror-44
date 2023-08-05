#!/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import array
import datetime
import fcntl
import io
import os
import struct
import sys
from hidtools.hid import ReportDescriptor


def _ioctl(fd, EVIOC, code, return_type, buf=None):
    size = struct.calcsize(return_type)
    if buf is None:
        buf = size * '\x00'
    abs = fcntl.ioctl(fd, EVIOC(code, size), buf)
    return struct.unpack(return_type, abs)


# extracted from <asm-generic/ioctl.h>
_IOC_WRITE = 1
_IOC_READ = 2

_IOC_NRBITS = 8
_IOC_TYPEBITS = 8
_IOC_SIZEBITS = 14
_IOC_DIRBITS = 2

_IOC_NRSHIFT = 0
_IOC_TYPESHIFT = _IOC_NRSHIFT + _IOC_NRBITS
_IOC_SIZESHIFT = _IOC_TYPESHIFT + _IOC_TYPEBITS
_IOC_DIRSHIFT = _IOC_SIZESHIFT + _IOC_SIZEBITS


# define _IOC(dir,type,nr,size) \
# 	(((dir)  << _IOC_DIRSHIFT) | \
# 	 ((type) << _IOC_TYPESHIFT) | \
# 	 ((nr)   << _IOC_NRSHIFT) | \
# 	 ((size) << _IOC_SIZESHIFT))
def _IOC(dir, type, nr, size):
    return ((dir << _IOC_DIRSHIFT) |
            (ord(type) << _IOC_TYPESHIFT) |
            (nr << _IOC_NRSHIFT) |
            (size << _IOC_SIZESHIFT))


# define _IOR(type,nr,size)	_IOC(_IOC_READ,(type),(nr),(_IOC_TYPECHECK(size)))
def _IOR(type, nr, size):
    return _IOC(_IOC_READ, type, nr, size)


# define _IOW(type,nr,size)	_IOC(_IOC_WRITE,(type),(nr),(_IOC_TYPECHECK(size)))
def _IOW(type, nr, size):
    return _IOC(_IOC_WRITE, type, nr, size)


# define HIDIOCGRDESCSIZE	_IOR('H', 0x01, int)
def _IOC_HIDIOCGRDESCSIZE(none, len):
    return _IOR('H', 0x01, len)


def _HIDIOCGRDESCSIZE(fd):
    """ get report descriptors size """
    type = 'i'
    return int(*_ioctl(fd, _IOC_HIDIOCGRDESCSIZE, None, type))


# define HIDIOCGRDESC		_IOR('H', 0x02, struct hidraw_report_descriptor)
def _IOC_HIDIOCGRDESC(none, len):
    return _IOR('H', 0x02, len)


def _HIDIOCGRDESC(fd, size):
    """ get report descriptors """
    format = "I4096c"
    value = '\0' * 4096
    tmp = struct.pack("i", size) + value[:4096].encode('utf-8').ljust(4096, b'\0')
    _buffer = array.array('B', tmp)
    fcntl.ioctl(fd, _IOC_HIDIOCGRDESC(None, struct.calcsize(format)), _buffer)
    size, = struct.unpack("i", _buffer[:4])
    value = _buffer[4:size + 4]
    return size, value


# define HIDIOCGRAWINFO		_IOR('H', 0x03, struct hidraw_devinfo)
def _IOC_HIDIOCGRAWINFO(none, len):
    return _IOR('H', 0x03, len)


def _HIDIOCGRAWINFO(fd):
    """ get hidraw device infos """
    type = 'ihh'
    return _ioctl(fd, _IOC_HIDIOCGRAWINFO, None, type)


# define HIDIOCGRAWNAME(len)     _IOC(_IOC_READ, 'H', 0x04, len)
def _IOC_HIDIOCGRAWNAME(none, len):
    return _IOC(_IOC_READ, 'H', 0x04, len)


def _HIDIOCGRAWNAME(fd):
    """ get device name """
    type = 1024 * 'c'
    cstring = _ioctl(fd, _IOC_HIDIOCGRAWNAME, None, type)
    string = b''.join(cstring).decode('utf-8')
    return "".join(string).rstrip('\x00')


class HidrawEvent(object):
    """
    A single event from a hidraw device. The first event always has a timestamp of 0.0,
    all other events are offset accordingly.

    .. attribute:: sec

        Timestamp seconds

    .. attribute:: usec

        Timestamp microseconds

    .. attribute:: bytes

        The data bytes read for this event
    """
    def __init__(self, sec, usec, bytes):
        self.sec, self.usec = sec, usec
        self.bytes = bytes


class HidrawDevice(object):
    """
    A device as exposed by the kernel ``hidraw`` module. ``hidraw`` allows
    direct access to the HID device, both for reading and writing. ::

        with open('/dev/hidraw0', 'r+b') as fd:
            dev = HidrawDevice(fd)
            while True:
                dev.read_events()  # this blocks
                print(f'We received {len(dev.events)} events so far')

    :param File device: a file-like object pointing to ``/dev/hidrawX``

    .. attribute:: name

        The device name

    .. attribute:: bustype

        The numerical bus type (``0x3`` for USB, ``0x5`` for Bluetooth, see
        ``linux/input.h``)

    .. attribute:: vendor_id

        16-bit numerical vendor ID

    .. attribute:: product_id

        16-bit numerical product ID

    .. attribute:: report_descriptor

        The :class:`hidtools.hid.ReportDescriptor` for this device

    .. attribute:: events

        All events accumulated so far, a list of :class:`HidrawEvent`

    ... attribute:: time_offset

        The offset to be used for recording events. By default the offset is
        the timestamp of the first event. When recording multiple devices,
        the time_offset from the first device to receive an event should be
        copied to the other device to ensure all recordings are in sync.
    """
    def __init__(self, device):
        fd = device.fileno()
        self.device = device
        self.name = _HIDIOCGRAWNAME(fd)
        self.bustype, self.vendor_id, self.product_id = _HIDIOCGRAWINFO(fd)
        self.vendor_id &= 0xFFFF
        self.product_id &= 0xFFFF
        size = _HIDIOCGRDESCSIZE(fd)
        rsize, desc = _HIDIOCGRDESC(fd, size)
        assert rsize == size
        assert len(desc) == rsize
        self.report_descriptor = ReportDescriptor.from_bytes([x for x in desc])

        self.events = []

        self._dump_offset = -1
        self.time_offset = None

    def __repr__(self):
        return f'{self.name} bus: {self.bustype:02x} vendor: {self.vendor_id:04x} product: {self.product_id:04x}'

    def read_events(self):
        """
        Read events from the device and store them in the device.

        This function simply calls :func:`os.read`, it is the caller's task to
        either make sure the device is set nonblocking or to handle any
        :class:`KeyboardInterrupt` if this call does end up blocking.

        :returns: a tuple of ``(index, count)`` of the :attr:`events` added.
        """

        index = max(0, len(self.events) - 1)

        loop = True
        while loop:
            data = os.read(self.device.fileno(), 4096)
            if not data:
                break
            if len(data) < 4096:
                loop = False

            now = datetime.datetime.now()
            if self.time_offset is None:
                self.time_offset = now
            tdelta = now - self.time_offset
            bytes = struct.unpack('B' * len(data), data)

            self.events.append(HidrawEvent(tdelta.seconds, tdelta.microseconds, bytes))

        count = len(self.events) - index

        return index, count

    def _dump_event(self, event, file):
        report_id = event.bytes[0]

        rdesc = self.report_descriptor.get(report_id, len(event.bytes))
        if rdesc is not None:
            indent_2nd_line = 2
            output = rdesc.format_report(event.bytes)
            try:
                first_row = output.split('\n')[0]
            except IndexError:
                pass
            else:
                # we have a multi-line output, find where the fields are split
                try:
                    slash = first_row.index('/')
                except ValueError:
                    pass
                else:
                    # the `+1` below is to make a better visual effect
                    indent_2nd_line = slash + 1
            indent = f'\n#{" " * indent_2nd_line}'
            output = indent.join(output.split('\n'))
            print(f'# {output}')

        data = map(lambda x: f'{x:02x}', event.bytes)
        print(f'E: {event.sec:06d}.{event.usec:06d} {len(event.bytes)} {" ".join(data)}', file=file, flush=True)

    def dump(self, file=sys.stdout, from_the_beginning=False):
        """
        Format this device in a file format in the form of ::

            R: 123 43 5 52 2 ... # the report descriptor size, followed by the integers
            N: the device name
            I: 3 124 abcd # bustype, vendor, product
            # comments are allowed
            E: 00001.000002 AB 12 34 56 # sec, usec, length, data
            ...

        This method is designed to be called repeatedly and only print the
        new events on each call. To repeat the dump from the beginning, set
        ``from_the_beginning`` to True.

        :param File file: the output file to write to
        :param bool from_the_beginning: if True, print everything again
             instead of continuing where we left off
        """

        if from_the_beginning:
            self._dump_offset = -1

        if self._dump_offset == -1:
            print(f'# {self.name}', file=file)
            output = io.StringIO()
            self.report_descriptor.dump(output)
            for line in output.getvalue().split('\n'):
                print(f'# {line}', file=file)
            output.close()

            rd = " ".join([f'{b:02x}' for b in self.report_descriptor.bytes])
            sz = len(self.report_descriptor.bytes)
            print(f'R: {sz} {rd}', file=file)
            print(f'N: {self.name}', file=file)
            print(f'I: {self.bustype:x} {self.vendor_id:04x} {self.product_id:04x}', file=file, flush=True)
            self._dump_offset = 0

        for e in self.events[self._dump_offset:]:
            self._dump_event(e, file)
        self._dump_offset = len(self.events)
