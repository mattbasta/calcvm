from opcodes import OpCode, STATEMENT, EXPRESSION, EXPRESSIONS


DISABLE_OPTIMIZATIONS = False
DISABLE_STATEMENT_FOLDING = True


class Compiler(object):

    def __init__(self, instructions):
        self.instructions = instructions
        self.ip = 0

        self.ips_to_save = set()
        self.call_ips = set()
        self.expression_queue = []

    def use_expressions(self, num_opcodes):
        for i in range(num_opcodes):
            if self.expression_queue:
                yield self.expression_queue.pop()
                continue
            yield "pop_stack(data_stack)"

    def get_parameter(self, opcode_ip=None):
        if opcode_ip is not None:
            return self.instructions[opcode_ip + 1]
        else:
            return self.instructions[self.ip + 1]

    def indent(self, amount, line):
        return "%s%s" % (" " * (4 * amount), line)

    def _dump_eq(self, leave=0):
        #leave = 0
        if len(self.expression_queue) <= leave:
            return
        for exp in self.expression_queue[:]:
            yield self.indent(1, "data_stack->push_back(%s);" % exp)
            self.expression_queue = self.expression_queue[1:]
            if len(self.expression_queue) <= leave:
                return

    def run(self):
        # Don't yield the last statement immediately in case it turns out to be
        # something that we can optimize away.
        last_statement = None
        last_statement_name = None
        last_comments = []
        last_ip = 0

        yield """
        switch(ip) {
        %s
        }
        """ % "\n        ".join("case %d: goto ip%d;" % (i, i) for i in
                                sorted(self.call_ips))

        for i in xrange(len(self.instructions)):
            oc = self.instructions[i]
            # Ignore parameters.
            if isinstance(oc, (int, str, unicode, float)):
                continue

            self.ip = oc.ip

            # Output the instruction pointer as a label if we know that it's a
            # critical instruction location.
            if self.ip in self.ips_to_save:
                if last_statement is not None:
                    for comment in last_comments:
                        yield comment
                    yield last_statement
                    last_statement = None
                    last_comments = []
                yield "ip%d:" % self.ip
                self.ips_to_save.remove(self.ip)

            if i > 0:
                for ii in range(last_ip, self.ip):
                    if ii in self.ips_to_save:
                        if last_statement is not None:
                            for comment in last_comments:
                                yield comment
                            yield last_statement
                            last_statement = None
                            last_comments = []
                        yield "ip%d:" % ii
                        self.ips_to_save.remove(ii)

            # If we come across a code boundary, dump the data stack.
            if oc.dumps_expression_queue:
                deq = oc.dumps_expression_queue
                leave = oc.opcodes_used

                # If we conditionally dump the expression queue, check to see
                # whether we need to dump.
                if isinstance(deq, str) and deq == "ask":
                    leave = 0
                    if not oc.dump_expression_queue():
                        deq = False

                # If we need to dump, dump.
                if deq:
                    if last_statement is not None:
                        for comment in last_comments:
                            yield comment
                        yield last_statement
                        last_statement = None
                        last_comments = []
                    for exp in self._dump_eq(leave):
                        yield exp

            # Output the opcode name.
            comment = self.indent(1, "// %d: %s" % (self.ip, oc.raw))
            if DISABLE_STATEMENT_FOLDING:
                yield comment
            else:
                last_comments.append(comment)
            #yield self.indent(1, "cout << %d << \"%s\" << endl;" %
            #                         (oc.ip, oc.raw))

            # Generate any of the expressions.
            if oc.instruction_type == EXPRESSION:
                self.save_expression(oc.as_expression())
            elif oc.instruction_type == EXPRESSIONS:
                for exp in oc.as_expression():
                    self.save_expression(exp)
            elif oc.instruction_type == STATEMENT:
                # Format the opcode's statement
                oc_output = oc.as_statement()
                if oc_output is not None:
                    statement = []
                    for oc_line in oc_output.split("\n"):
                        statement.append(self.indent(1, oc_line))
                    statement = "\n".join(statement)

                    if (not DISABLE_STATEMENT_FOLDING
                        and oc.name == "REFCNT(-1)" and
                        last_statement != None and
                        last_statement_name == "REFCNT(1)" and
                        last_statement == statement.replace("dereference",
                                                            "reference")):
                        # If the last statement was a reference
                        last_statement = None
                        last_statement_name = None
                        print ("Found optimization: Eliminated matching "
                               "REFCNTs, ip=%d") % oc.ip
                    else:
                        if last_statement is not None:
                            for comment in last_comments:
                                yield comment
                            last_comments = []
                            yield last_statement

                        if DISABLE_STATEMENT_FOLDING:
                            yield statement
                        else:
                            last_statement = statement
                            last_statement_name = oc.name

                # A blank line for funsies.
                yield ""

            last_ip = self.ip

            # If the next instruction is in a different flow block, make sure
            # all of the expressions for this flow block have been outputted
            # so that our expressions don't get mixed with the expressions of
            # other paths.
            if self.next_instruction_ip(i) in self.ips_to_save:
                for exp in self._dump_eq():
                    yield exp

        if not DISABLE_STATEMENT_FOLDING and last_statement is not None:
            for comment in last_comments:
                yield comment
            yield last_statement

    def next_instruction_ip(self, instruction):
        for i in self.instructions[instruction + 1:]:
            if issubclass(type(i), OpCode):
                return i.ip
        return None

    def save_expression(self, expression):
        self.expression_queue.append(expression)
