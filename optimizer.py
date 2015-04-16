from opcodes import OpCode
from compiler import DISABLE_OPTIMIZATIONS


OPTIMIZATIONS = set()


def opt_opcodes(section, compiler):
    if DISABLE_OPTIMIZATIONS:
        return section

    opcodes = []
    for oc in tag_opcodes(section):
        opcodes.append(oc)

        for pattern, plen, opt in OPTIMIZATIONS:
            if len(opcodes) < plen:
                continue
            maybe_pattern = opcodes[-plen:]
            #print tuple(opcode_tags(maybe_pattern)), pattern
            if tuple(opcode_tags(maybe_pattern)) != pattern:
                continue

            # At this point, we've matched an optimization to the instructions.
            print "Found optimization: ip=%d, pattern=%s" % (len(opcodes), str(pattern))
            opcodes = opcodes[:-plen] + opt(maybe_pattern)

    return untag_opcodes(opcodes)


def tag_opcodes(section):
    return ((oc.name, oc) for oc in section if
            issubclass(type(oc), OpCode))


def untag_opcodes(section):
    return [oc for name, oc in section]


def opcode_tags(opcodes):
    return [name for name, oc in opcodes]


def opt(*args):
    def decorator(func):
        OPTIMIZATIONS.add((tuple(args), len(args), func))
        return func
    return decorator


@opt("ALLOC(0)",
     "DUP",
     "CONST",
     "ARRAYCPY",
     "SWAP",
     "CONST",
     "REFCNT(-1)")
def zero_len_array_opt(opcodes):
    return [opcodes[0]]


@opt("OVER",
     "OVER",
     "CONST",
     "ARRAYCAT",
     "SWAP2",
     "CONST",
     "REFCNT(-1)",
     "CONST",
     "REFCNT(-1)")
def fast_arraycat(opcodes):
    from opcodes import OC_ALT_ARRAYCAT

    type_const = opcodes[2]
    cat_name, cat = opcodes[3]
    aac = OC_ALT_ARRAYCAT(cat.compiler, cat.ip)
    aac.raw = "[generated]"
    return [type_const,
            ("ALT_ARRAYCAT", aac)]

@opt("OVER",
     "OVER",
     "SWAP",
     "CONST",
     "ARRAYCAT",
     "SWAP2",
     "CONST",
     "REFCNT(-1)",
     "CONST",
     "REFCNT(-1)")
def fast_arraycat_fork(opcodes):
    from opcodes import OC_ALT_ARRAYCAT

    type_const = opcodes[3]
    cat_name, cat = opcodes[4]
    aac = OC_ALT_ARRAYCAT(cat.compiler, cat.ip)
    aac.raw = "[generated]"
    return [opcodes[2],
            type_const,
            ("ALT_ARRAYCAT", aac)]


@opt("JOIN", "DROP")
def unimlpemented_join_output(opcodes):
    return [opcodes[0]]


@opt("OVER", "STORE")
def fast_store(opcodes):
    from opcodes import OC_ALT_STORE

    st_name, st = opcodes[1]
    ast = OC_ALT_STORE(st.compiler, st.ip)
    ast.raw = "[generated]"
    ast.properties = st.properties
    return [("ALT_STORE", ast)]


@opt("DUP", "GOTO0")
def fast_goto0(opcodes):
    from opcodes import OC_ALT_GOTO0

    g_name, g = opcodes[1]
    ag = OC_ALT_GOTO0(g.compiler, g.ip)
    ag.raw = "[generated]"
    ag.properties = g.properties
    return [("ALT_GOTO0", ag)]
