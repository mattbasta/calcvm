import re

from opcodes import *


def _run_on_sections(func):
    def wrap(sections, compiler):
        map(lambda section: func(section, compiler), sections.values())
    return wrap


def link_opcodes(section, compiler):
    last_opcode = None
    for i in xrange(len(section)):
        line = section[i]
        if (not isinstance(line, (str, unicode)) or
            not line.startswith("StepOpCode ")):
            if last_opcode is not None:
                last_opcode.properties.append(line)
            continue

        opcode_raw = line.split(" ")[1]
        if opcode_raw not in OPCODES:
            raise "Could not find opcode: %s" % opcode_raw
        opcode = OPCODES[opcode_raw](compiler, i)
        opcode.raw = opcode_raw
        yield opcode

        last_opcode = opcode


@_run_on_sections
def link_constants(section, compiler):
    for i in xrange(len(section)):
        line = section[i]
        if not isinstance(line, (str, unicode)):
            continue
        if line.startswith("Long"):
            ret = int(line.split(" ", 1)[1])
            if ret > 2147483647:
                ret = 2147483647
                print "LONG value truncated for C++ `long` type."
            section[i] = ret
        elif line.startswith("String"):
            section[i] = unicode(line[7:])
        elif line.startswith("Double"):
            section[i] = float(line.split(" ", 1)[1])
