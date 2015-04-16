#!/usr/bin/env python
import sys

from compiler import Compiler
from linker import link_opcodes, link_constants
from optimizer import opt_opcodes


def compile(vm_file):
    f = open(vm_file)

    section = -1
    sections = {0: [], 1: []}

    for line in f.xreadlines():
        line = line[:-1]
        if line == "PROGRAMMEMORY":
            section = 0
        elif line == "DATAMEMORY":
            section = 1
        else:
            sections[section].append(line)

    # Trim away the first value. It's not useful.
    for section in sections:
        sections[section] = sections[section][1:]

    c = Compiler(sections[0])

    link_constants(sections, c)
    sections[0] = link_opcodes(sections[0], c)

    sections[0] = opt_opcodes(sections[0], c)
    c.instructions = sections[0]

    f.close()

    generated_code = "\n".join(c.run())

    def get_virtual_memory(item):
        value = sections[1][item]
        if isinstance(value, int):
            wrapper = "new_long"
        elif isinstance(value, float):
            wrapper = "new_double"
        else:
            wrapper = "new_string"
        return c.indent(1, "virtual_memory[%d] = %s(%s);" %
                   (item, wrapper, value))

    virtual_memory = "\n".join(get_virtual_memory(i) for i in
                               range(len(sections[1])))

    template_file = open("templates/main.cpp")
    template = template_file.read()
    template_file.close()

    main_file = open("buildbox/main.cpp", "w")
    main_file.write(template % {"instructions": generated_code,
                                "virtual_mem_size": len(sections[1]),
                                "virtual_mem": virtual_memory})
    main_file.close()


if __name__ == "__main__":
    compile(*sys.argv[1:])
