import uuid


def clean_statement(func):
    """
    A decorator to clean the output of an as_statement function. Processes the
    output to remove suprious indentation.
    """
    def wrap(*args, **kwargs):
        output = func(*args, **kwargs)
        if output is None:
            return None
        output = output.split("\n")
        output = filter(lambda x: x.strip(), output)
        indent = min(len(line) - len(line.lstrip()) for line in output)
        return "\n".join(line[indent:] for line in output)
    return wrap


STATEMENT = 1
EXPRESSION = 2
EXPRESSIONS = 4


class WrappedString(object):
    """
    A wrapper for strings. Allows strings to be passed into WrappedTypes
    and be evaluated as pointers when they need to be, but also unwrapped
    as string literals when they don't need to be used as pointers.
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "(new string(%s))" % self.value


class WrappedType(object):
    """
    A wrapper for literal values. Allows literals to be unwrapped by opcode
    classes to improve performance.
    """

    def __init__(self, value, type):
        self.value = value
        self.type = type

    def __str__(self):
        return "new_%s(%s)" % (self.type, self.value)


class WrappedFetchedType(WrappedType):
    """
    A wrapper for data objects that exist in the stack that are fetched with
    FETCH_REGISTER. Since the objects aren't popped and the data is immutable,
    these can be successfully evaluated from directly without wrapping and
    unwrapping. This significantly improves perforamnce because it avoids the
    need to read, copy, and subsequently destroy a data object.
    """
    def __init__(self, address_expression):
        self.value = "(*data_stack)[%s]" % address_expression

    def __str__(self):
        return "(new DataObject(*%s))" % self.value


class PADDWrap(object):
    """
    A wrapper for array references that have been PADDed to. This allows for
    STEP_STORE to detect that and generate the appropriate code.
    """
    def __init__(self, expr, offset):
        # If we're PADDing to a PADD, just collapse it.
        if isinstance(expr, PADDWrap):
            offset += expr.offset
            expr = expr.expr

        self.expr = expr
        self.offset = offset

    def __str__(self):
        return "%s->padd(%s)" % (self.expr, self.offset)


def unwrap(expression, expected_type="long"):
    """
    Generate the code necessary to unwrap a WrappedType object when the expected
    value for a literal is the same type as the requested value output.
    """
    if isinstance(expression, WrappedFetchedType):
        return "%s->v_%s" % (expression.value, expected_type)

    if (isinstance(expression, WrappedType) and
        expression.type == expected_type):
        return expression.value

    return "%s->get_%s()" % (expression, expected_type)


class OpCode(object):
    def __init__(self, compiler, ip):
        self.name = self.__class__.__name__[3:]

        self.opcodes_used = 0
        self.dumps_expression_queue = False
        self.instruction_type = STATEMENT
        self.ip = ip

        self.properties = []

        self.compiler = compiler
        self.setup()

        # Declare a way to access the opcodes used generator function.
        if self.opcodes_used:
            expressions = self.compiler.use_expressions(self.opcodes_used)
            self._use_expression = expressions.next

    def _get_parameter(self, num=0):
        return self.properties[num]

    def _peek_prev_const(self, delta=-1):
        return self.compiler.instructions[self.ip + delta]


class OC_BinaryOperator(OpCode):
    def setup(self):
        self.opcodes_used = 2
        self.instruction_type = EXPRESSION
        self.dereference = False
        self.extra_setup()

    def as_expression(self):
        p2 = self._use_expression()
        p1 = self._use_expression()
        if not self.dereference:
            expression = "(%s %s %s)"
        else:
            expression = "(*%s %s *%s)"

        expression = expression % (unwrap(p1, self.expected_type),
                                   self.operator,
                                   unwrap(p2, self.expected_type))
        return WrappedType(expression, self.expected_type)


class OC_Comparison(OpCode):
    def setup(self):
        self.opcodes_used = 2
        self.instruction_type = EXPRESSION
        self.extra_setup()

    def as_expression(self):
        p2 = self._use_expression()
        p1 = self._use_expression()
        expression = "(%s %s %s ? 1 : 0)" % (unwrap(p1, self.expected_type),
                                             self.operator,
                                             unwrap(p2, self.expected_type))
        # Comparisons always yield a long.
        return WrappedType(expression, "long")


class OC_ZComparison(OC_Comparison):
    def as_expression(self):
        p1 = self._use_expression()
        expression = "(%s %s 0 ? 1 : 0)" % (unwrap(p1, self.expected_type),
                                            self.operator)
        return WrappedType(expression, "long")


class OC_ALLOC(OpCode):
    def setup(self):
        self.name = "ALLOC(%d)" % self._peek_prev_const()
        self.opcodes_used = 1
        self.instruction_type = STATEMENT
        self.dumps_expression_queue = True

    @clean_statement
    def as_statement(self):
        length = unwrap(self._use_expression())
        output = []

        output.append("data_stack->push_back(get_new_array(%s));" % length)

        return "\n".join(output)


class OC_ARRAYCAT(OpCode):
    def setup(self):
        self.opcodes_used = 3
        self.dumps_expression_queue = True

    @clean_statement
    def as_statement(self):
        typeflag = unwrap(self._use_expression())
        array1 = self._use_expression()
        array2 = self._use_expression()

        if (isinstance(array1, WrappedType) and array1.value == 0 and
            int(typeflag) == 0):
            return "data_stack->push_back(%s);" % array2

        return """
            {
                HeapObj * rheap = %(rarr)s->get_heap_obj(virtual_memory);
                HeapObj * lheap = %(larr)s->get_heap_obj(virtual_memory);
                data_stack->push_back(new DataObject(lheap->concat(rheap, %(tf)s)));
                if(lheap->refcount == 0)
                    lheap->dereference();
                if(rheap->refcount == 0)
                    rheap->dereference();
            }
        """ % {"larr": array2,
               "rarr": array1,
               "tf": typeflag}


class OC_ALT_ARRAYCAT(OpCode):
    def setup(self):
        self.opcodes_used = 3
        self.dumps_expression_queue = True

    @clean_statement
    def as_statement(self):
        typeflag = unwrap(self._use_expression())
        array1 = self._use_expression()
        array2 = self._use_expression()

        if (isinstance(array1, WrappedType) and array1.value == 0 and
            int(typeflag) == 0):
            return "data_stack->push_back(%s);" % array2

        return """
            {
                HeapObj * rheap = %(rarr)s->get_heap_obj(virtual_memory);
                HeapObj * lheap = %(larr)s->get_heap_obj(virtual_memory);
                data_stack->push_back(new DataObject(lheap->alt_concat(rheap, %(tf)s)));
            }
        """ % {"larr": array2,
               "rarr": array1,
               "tf": typeflag}


class OC_ARRAYCOUNT(OpCode):
    def setup(self):
        self.opcodes_used = 1
        self.instruction_type = EXPRESSION

    def as_expression(self):
        array = self._use_expression()
        if isinstance(array, WrappedFetchedType):
            return WrappedType("%s->get_size(false, virtual_memory)" %
                                   array.value, "long")
        else:
            return WrappedType("%s->get_size(true, virtual_memory)" %
                                   array, "long")


class OC_ARRAYCPY(OpCode):
    def setup(self):
        self.opcodes_used = 2
        self.dumps_expression_queue = True

    @clean_statement
    def as_statement(self):
        typecast = int(self._use_expression().value)
        array = self._use_expression()

        typecasting = ""
        if typecast > 0:
            typecasting = "temp->v_array->cast_type = DOUBLE;"
        else:
            typecasting = "temp->v_array->cast_type = LONG;"

        return """
        {
            DataObject * temp = new DataObject(new HeapObj(%(array)s->get_heap_obj(virtual_memory)));
            %(typecasting)s
            data_stack->push_back(temp);
        }
        """ % {"array": array,
               "typecasting": typecasting}


class OC_CALL_SECONDARY(OpCode):
    def setup(self):
        self.dumps_expression_queue = True
        self.compiler.ips_to_save.add(self.compiler.get_parameter(self.ip))
        self.compiler.ips_to_save.add(self.ip + 2)
        self.compiler.call_ips.add(self.ip + 2)

    @clean_statement
    def as_statement(self):
        param = self._get_parameter()
        return """
        frame_pointers.push(data_stack->size());
        fp_cache = data_stack->size();
        instruction_pointers.push(%d);
        goto ip%d;
        """ % (self.ip + 2, param)


class OC_CAST_DOUBLE(OpCode):
    def setup(self):
        self.opcodes_used = 1
        self.instruction_type = EXPRESSION

    def as_expression(self):
        array = self._use_expression()
        if isinstance(array, WrappedFetchedType):
            array = unicode(array)

        if isinstance(array, WrappedType):
            if array.type == "string":
                array.value = "atof(%s)" % array.value
            else:
                array.value = "(double)%s" % array.value
            array.type = "double"
            return array
        else:
            return "%s->set_type(DOUBLE)" % array


class OC_CAST_LONG(OpCode):
    def setup(self):
        self.opcodes_used = 1
        self.instruction_type = EXPRESSION

    def as_expression(self):
        array = self._use_expression()
        if isinstance(array, WrappedFetchedType):
            array = unicode(array)

        if isinstance(array, WrappedType):
            if array.type == "string":
                array.value = "atol(%s)" % array.value
            else:
                array.value = "(long)%s" % array.value
            array.type = "long"
            return array
        else:
            return "%s->set_type(LONG)" % array


class OC_CAST_STRING(OpCode):
    def setup(self):
        self.opcodes_used = 1
        self.instruction_type = EXPRESSION

    def as_expression(self):
        array = self._use_expression()
        # We can't just use inline type casting because C++ makes it damn near
        # impossible to do it. This way is the best balance between LoC, perf,
        # and sanity.
        return "%s->set_type(STRING)" % array


class OC_CONST(OpCode):
    def setup(self):
        self.opcodes_used = 0
        self.instruction_type = EXPRESSION

    def as_expression(self):
        param = self._get_parameter()
        if isinstance(param, int):
            return WrappedType(param, "long")
        elif isinstance(param, float):
            return WrappedType(param, "double")
        elif isinstance(param, (str, unicode)):
            # NOTE: Line breaks aren't processed here.
            param = param.replace("\\", "\\\\").replace('"', '\\"')
            param = '"%s"' % param
            param = WrappedString(param)
            return WrappedType(param, "string")


class OC_CRLF(OpCode):
    def setup(self): pass
    def as_statement(self):
        return "cout << endl;"


class OC_DABS(OpCode):
    pass


class OC_DADD(OC_BinaryOperator):
    def extra_setup(self):
        self.operator = "+"
        self.expected_type = "double"


class OC_DDIV(OC_BinaryOperator):
    def extra_setup(self):
        self.operator = "/"
        self.expected_type = "double"


class OC_DEQ(OC_Comparison):
    def extra_setup(self):
        self.operator = "=="
        self.expected_type = "double"


class OC_DGE(OC_Comparison):
    def extra_setup(self):
        self.operator = ">="
        self.expected_type = "double"


class OC_DGT(OC_Comparison):
    def extra_setup(self):
        self.operator = ">"
        self.expected_type = "double"


class OC_DLE(OC_Comparison):
    def extra_setup(self):
        self.operator = "<="
        self.expected_type = "double"


class OC_DLT(OC_Comparison):
    def extra_setup(self):
        self.operator = "<"
        self.expected_type = "double"


class OC_DMINUS(OpCode):
    def setup(self):
        self.opcodes_used = 1
        self.instruction_type = EXPRESSION

    def as_expression(self):
        p1 = self._use_expression()
        expression = "-%s" % unwrap(p1, "double")
        return WrappedType(expression, "double")


class OC_DMULT(OC_BinaryOperator):
    def extra_setup(self):
        self.operator = "*"
        self.expected_type = "double"


class OC_DNEQ(OC_Comparison):
    def extra_setup(self):
        self.operator = "!="
        self.expected_type = "double"


class OC_DROP(OpCode):
    def setup(self):
        self.opcodes_used = 1;

    def as_statement(self):
        if self.compiler.expression_queue:
            exp = self._use_expression()
            return None

        exp = self._use_expression()
        return "delete %s;" % exp


class OC_DROP2(OpCode):
    def setup(self):
        self.opcodes_used = 2;

    def as_statement(self):
        output = []
        for i in range(2):
            if self.compiler.expression_queue:
                exp = self._use_expression()
                continue

            exp = self._use_expression()
            output.append("delete %s;" % exp)
        return output.join("\n")


class OC_DROPFRAME(OpCode):
    def setup(self):
        self.dumps_expression_queue = True
        self.opcodes_used = 2

    @clean_statement
    def as_statement(self):
        t_offset = self._use_expression()
        b_offset = self._use_expression()

        return """
        data_stack->erase(
            data_stack->begin() + fp_cache + %(bottom)s,
            data_stack->begin() + fp_cache + %(top)s + 1
        );
        """ % {"bottom": unwrap(b_offset),
               "top": unwrap(t_offset)}


class OC_DROPN(OpCode):
    def setup(self):
        self.opcodes_used = -1;
        self.dumps_expression_queue = True

    @clean_statement
    def as_statement(self):
        n = self._use_expression()
        return """
        for(int i = 0; i < %s; i++)
            delete pop_stack(data_stack);
        """ % unwrap(n)


class OC_DSIGN(OpCode):
    pass


class OC_DSUB(OC_BinaryOperator):
    def extra_setup(self):
        self.operator = "-"
        self.expected_type = "double"


class OC_DUP(OpCode):
    def setup(self):
        self.opcodes_used = 1;

    @clean_statement
    def as_statement(self):
        # If we can optimize this away, just compile it right in.
        if self.compiler.expression_queue:
            top = self._use_expression()
            self.compiler.expression_queue.append(top)
            self.compiler.expression_queue.append(top)
            return None

        # We can't optimize by pushing `top` to the expression queue
        return "data_stack->push_back(new DataObject(*data_stack->back()));"


class OC_DUP2(OpCode):
    pass

class OC_DUP_I(OpCode):
    pass

class OC_DZEQ(OpCode):
    pass

class OC_DZGE(OpCode):
    pass

class OC_DZGT(OpCode):
    pass

class OC_DZLE(OpCode):
    pass

class OC_DZLT(OpCode):
    pass

class OC_DZNEQ(OpCode):
    pass


class OC_FETCH(OpCode):
    def setup(self):
        self.opcodes_used = 1
        self.instruction_type = EXPRESSION

    def as_expression(self):
        address = self._use_expression()
        if not isinstance(address, PADDWrap):
            return "virtual_memory[%s]" % unwrap(address)
        else:
            expr = address.expr
            if isinstance(expr, WrappedFetchedType):
                expr = expr.value
            return ("(new DataObject(*%s->retrieve(%s, virtual_memory)))" %
                        (expr, address.offset))


class OC_FETCH_REGISTER(OpCode):
    def setup(self):
        self.instruction_type = EXPRESSION
        self.dumps_expression_queue = "ask"

    def dump_expression_queue(self):
        # We don't need to dump if we're looking up parameters or the static
        # link because they get pushed with the function call.
        return int(self._get_parameter()) >= 0

    def as_expression(self):
        param = self._get_parameter()
        if param:
            return WrappedFetchedType("fp_cache + %d" % param)
        else:
            return WrappedFetchedType("fp_cache")


class OC_FETCH_STACK(OpCode):
    def setup(self):
        #self.dumps_expression_queue = True
        self.opcodes_used = 1
        self.instruction_type = EXPRESSION

    def as_expression(self):
        location = self._use_expression()
        return WrappedFetchedType(unwrap(location))
        #return "(new DataObject(*data_stack->at(%s)))" % unwrap(location)


class OC_FORK(OpCode):
    def setup(self):
        self.opcodes_used = 0
        self.dumps_expression_queue = True
        self.compiler.ips_to_save.add(self.compiler.get_parameter(self.ip))
        self.compiler.call_ips.add(self.compiler.get_parameter(self.ip))

    @clean_statement
    def as_statement(self):
        ip = self._get_parameter(0)
        params = self._get_parameter(1)
        return """
        {
            // Flatten everything on the stack.
            unsigned int ds_s = data_stack->size();
            vector<DataObject *> * params = new vector<DataObject *>;
            for(unsigned int i = 0; i < %(pcount)d; i++) {
                DataObject * v = (*data_stack)[ds_s - %(pcount)d + i];
                if(v->type == ARRAY && v->v_array != NULL && v->v_array->ccount)
                    v->v_array->flatten();
                params->push_back(v);
            }

            for(unsigned int i = 0; i < %(pcount)d; ++i)
                data_stack->pop_back();

            threads.push_back(new ThreadMan(bootstrap_context, params, %(location)d));
        }
        """ % {"pcount": params,
               "location": ip}


class OC_GOTO(OpCode):
    def setup(self):
        self.compiler.ips_to_save.add(self.compiler.get_parameter(self.ip))
        self.dumps_expression_queue = True

    @clean_statement
    def as_statement(self):
        location = self._get_parameter()
        return """
        goto ip%d;
        """ % location


class OC_GOTO0(OpCode):
    def setup(self):
        self.opcodes_used = 1
        self.compiler.ips_to_save.add(self.compiler.get_parameter(self.ip))
        self.dumps_expression_queue = True

    @clean_statement
    def as_statement(self):
        value = self._use_expression()
        location = self._get_parameter()
        return """
        if(%s == 0)
            goto ip%d;
        """ % (unwrap(value), location)


class OC_ALT_GOTO0(OpCode):
    def setup(self):
        self.opcodes_used = 0
        self.compiler.ips_to_save.add(self.compiler.get_parameter(self.ip))
        self.dumps_expression_queue = True

    @clean_statement
    def as_statement(self):
        location = self._get_parameter()
        return """
        if(data_stack->back()->v_long == 0)
            goto ip%d;
        """ % location


class OC_JOIN(OpCode):
    def setup(self):
        self.opcodes_used = 0
        self.dumps_expression_queue = True

    @clean_statement
    def as_statement(self):
        return """
        {
            while(!threads.empty()) {
                ThreadMan * thread = threads.back();
                data_stack->push_back(thread->join());
                delete thread;
                threads.pop_back();
            }
        }
        """


class OC_LABS(OpCode):
    def setup(self):
        self.opcodes_used = 1
        self.instruction_type = EXPRESSION

    def as_expression(self):
        p1 = self._use_expression()
        expression = "abs(%s)" % unwrap(p1)
        return WrappedType(expression, "long")


class OC_LADD(OC_BinaryOperator):
    def extra_setup(self):
        self.operator = "+"
        self.expected_type = "long"


class OC_LDIV(OC_BinaryOperator):
    def extra_setup(self):
        self.operator = "/"
        self.expected_type = "long"


class OC_LEQ(OC_Comparison):
    def extra_setup(self):
        self.operator = "=="
        self.expected_type = "long"


class OC_LGE(OC_Comparison):
    def extra_setup(self):
        self.operator = ">="
        self.expected_type = "long"


class OC_LGT(OC_Comparison):
    def extra_setup(self):
        self.operator = ">"
        self.expected_type = "long"


class OC_LLE(OC_Comparison):
    def extra_setup(self):
        self.operator = "<="
        self.expected_type = "long"


class OC_LLT(OC_Comparison):
    def extra_setup(self):
        self.operator = "<"
        self.expected_type = "long"


class OC_LMINUS(OpCode):
    def setup(self):
        self.opcodes_used = 1
        self.instruction_type = EXPRESSION

    def as_expression(self):
        p1 = self._use_expression()
        expression = "-%s" % unwrap(p1)
        return WrappedType(expression, "long")


class OC_LMOD(OC_BinaryOperator):
    def extra_setup(self):
        self.operator = "%"
        self.expected_type = "long"


class OC_LMULT(OC_BinaryOperator):
    def extra_setup(self):
        self.operator = "*"
        self.expected_type = "long"


class OC_LNEQ(OC_Comparison):
    def extra_setup(self):
        self.operator = "!="
        self.expected_type = "long"


class OC_LSIGN(OpCode):
    pass


class OC_LSUB(OC_BinaryOperator):
    def extra_setup(self):
        self.operator = "-"
        self.expected_type = "long"


class OC_LZEQ(OC_ZComparison):
    def extra_setup(self):
        self.operator = "=="
        self.expected_type = "long"


class OC_LZGE(OC_ZComparison):
    def extra_setup(self):
        self.operator = ">="
        self.expected_type = "long"


class OC_LZGT(OC_ZComparison):
    def extra_setup(self):
        self.operator = ">"
        self.expected_type = "long"


class OC_LZLE(OC_ZComparison):
    def extra_setup(self):
        self.operator = ">="
        self.expected_type = "long"


class OC_LZLT(OC_ZComparison):
    def extra_setup(self):
        self.operator = "<"
        self.expected_type = "long"


class OC_LZNEQ(OC_ZComparison):
    def extra_setup(self):
        self.operator = "!="
        self.expected_type = "long"


class OC_OVER(OpCode):
    def setup(self):
        self.opcodes_used = 2;
        self.dumps_expression_queue = "ask"

    def dump_expression_queue(self):
        # We don't need to dump if there are at least two values on the stack.
        return len(self.compiler.expression_queue) < 2

    @clean_statement
    def as_statement(self):
        # If we can optimize this away, just compile it right in.
        if len(self.compiler.expression_queue) >= 2:
            top = self._use_expression()
            bottom = self._use_expression()
            self.compiler.expression_queue.append(bottom)
            self.compiler.expression_queue.append(top)
            self.compiler.expression_queue.append(bottom)
            return None
        else:
            return "data_stack->push_back(new DataObject(*(*data_stack)[data_stack->size() - 2]));"


class OC_OVER2(OpCode):
    def setup(self):
        self.opcodes_used = 2;
        self.dumps_expression_queue = "ask"

    def dump_expression_queue(self):
        # We don't need to dump if there are at least two values on the stack.
        return len(self.compiler.expression_queue) < 3

    @clean_statement
    def as_statement(self):
        # If we can optimize this away, just compile it right in.
        if len(self.compiler.expression_queue) >= 3:
            topest = self._use_expression()
            top = self._use_expression()
            bottom = self._use_expression()
            self.compiler.expression_queue.append(bottom)
            self.compiler.expression_queue.append(top)
            self.compiler.expression_queue.append(topest)
            self.compiler.expression_queue.append(bottom)
            return None
        else:
            return "data_stack->push_back(new DataObject(*(*data_stack)[data_stack->size() - 3]));"


class OC_PADD(OpCode):
    def setup(self):
        self.opcodes_used = 2;
        self.instruction_type = EXPRESSION

    def as_expression(self):
        offset = self._use_expression()
        array = self._use_expression()
        return PADDWrap(array, unwrap(offset))


class OC_PAUSE(OpCode):
    def setup(self): pass
    def as_statement(self):
        return "return NULL;";


class OC_PRINT(OpCode):
    def setup(self):
        self.opcodes_used = 1

    def as_statement(self):
        output = self._use_expression()
        if isinstance(output, WrappedFetchedType):
            return "%s->safe_print();" % output.value
        elif isinstance(output, WrappedType):
            if output.type == "string":
                val = output.value
                if isinstance(val, WrappedString):
                    val = val.value
                else:
                    val = "*(%s)" % val
                return "cout << %s;" % val;
            else:
                return "cout << %s;" % output.value
        else:
            return "%s->print();" % output


class OC_PUSH_FP(OpCode):
    def setup(self):
        self.opcodes_used = 1
        self.instruction_type = EXPRESSION

    def as_expression(self):
        return WrappedType("fp_cache", "long")


class OC_REFCNT(OpCode):
    def setup(self):
        self.name = "REFCNT(%d)" % self._peek_prev_const()
        self.opcodes_used = 2
        self.instruction_type = STATEMENT

    @clean_statement
    def as_statement(self):
        # We know that the delta is never generated dynamically. It should
        # really be passed as a parameter, but for now, we can hack it and just
        # use its value now.
        delta = int(self._use_expression().value)
        array = self._use_expression()

        operation = "dereference" if delta < 0 else "reference"

        # TODO: Support deltas that aren't 1/-1
        if isinstance(array, WrappedFetchedType):
            return "%s_do(%s);" % (operation, array.value)

        return """
        {
            DataObject * temp = %s;
            %s_do(temp);
            delete temp;
        }
        """ % (array, operation)


class OC_RETURN(OpCode):
    def setup(self):
        self.dumps_expression_queue = True
        self.compiler.ips_to_save.add(self.ip + 1)

    @clean_statement
    def as_statement(self):
        ips = []

        for ip in self.compiler.call_ips:
            ips.append("""
            case %d: goto ip%d;
            """ % (ip, ip))

        return """
        // For FORKs
        if(instruction_pointers.size() == 0)
            return data_stack->back();

        frame_pointers.pop();
        fp_cache = frame_pointers.top();
        ip = instruction_pointers.top();

        instruction_pointers.pop();
        switch(ip) {%s
        }
        """ % "\n".join(ips)


class OC_SADD(OpCode):
    def setup(self):
        self.opcodes_used = 2
        self.instruction_type = EXPRESSION

    def as_expression(self):
        p2 = self._use_expression()
        p1 = self._use_expression()
        if (isinstance(p1, WrappedType) and isinstance(p2, WrappedType) and
            isinstance(p1.value, WrappedString) and
            isinstance(p2.value, WrappedString)):
            ret = WrappedString("%s + %s" % (p1.value.value, p2.value.value))
            return WrappedType(ret, "string")
        expression = "(new string(*%s + *%s))" % (unwrap(p1, "string"),
                                                  unwrap(p2, "string"))
        return WrappedType(expression, "string")


class OC_SEQ(OC_Comparison):
    def extra_setup(self):
        self.operator = "=="
        self.dereference = True
        self.expected_type = "string"


class OC_SGE(OC_Comparison):
    def extra_setup(self):
        self.operator = ">="
        self.dereference = True
        self.expected_type = "string"


class OC_SGT(OC_Comparison):
    def extra_setup(self):
        self.operator = ">"
        self.dereference = True
        self.expected_type = "string"


class OC_SLE(OC_Comparison):
    def extra_setup(self):
        self.operator = "<="
        self.dereference = True
        self.expected_type = "string"


class OC_SLT(OC_Comparison):
    def extra_setup(self):
        self.operator = "<"
        self.dereference = True
        self.expected_type = "string"


class OC_SNEQ(OC_Comparison):
    def extra_setup(self):
        self.operator = "!="
        self.dereference = True
        self.expected_type = "string"


class OC_STORE(OpCode):
    def setup(self):
        self.opcodes_used = 2

    @clean_statement
    def as_statement(self):
        address = self._use_expression()
        value = self._use_expression()
        if isinstance(address, PADDWrap):
            return """
            {
                DataObject * arr = %(address)s;
                arr->v_array->set(%(offset)s, %(value)s);
                delete arr;
            }
            """ % {"address": address.expr,
                   "offset": address.offset,
                   "value": value}
        else:
            return """
            {
                DataObject * arr = %(address)s;
                arr->v_array->set(arr->heap_offset, %(value)s);
                delete arr;
            }
            """ % {"address": address,
                   "value": value}

        if False:
            # This isn't used, and the heuristic isn't great, so it's disabled
            # for now.
            return "virtual_memory[%s] = %s;" % (unwrap(address), value)


class OC_ALT_STORE(OpCode):
    def setup(self):
        self.opcodes_used = 2

    @clean_statement
    def as_statement(self):
        # This special version of OC_STORE takes the value as the first
        # parameter. This prevents thrash of the stack.
        value = self._use_expression()
        address = self._use_expression()
        if isinstance(address, PADDWrap):
            return """
            {
                DataObject * arr = %(address)s;
                arr->v_array->set(%(offset)s, %(value)s);
                delete arr;
            }
            """ % {"address": address.expr,
                   "offset": address.offset,
                   "value": value}
        else:
            return """
            data_stack->back()->v_array->set(data_stack->back()->heap_offset, %(value)s);
            """ % {"address": address,
                   "value": value}


class OC_STORE_I(OpCode):
    pass

class OC_STORE_REGISTER(OpCode):
    pass

class OC_STORE_STACK(OpCode):
    pass


class OC_SWAP(OpCode):
    def setup(self):
        self.opcodes_used = 2;
        self.dumps_expression_queue = "ask"

    def dump_expression_queue(self):
        # We don't need to dump if there are at least two values on the stack.
        return len(self.compiler.expression_queue) < 2

    @clean_statement
    def as_statement(self):
        # If we can optimize this away, just compile it right in.
        if len(self.compiler.expression_queue) >= 2:
            top = self._use_expression()
            bottom = self._use_expression()
            self.compiler.expression_queue.append(top)
            self.compiler.expression_queue.append(bottom)
            return None
        else:
            return """
            {
                DataObject * temp1 = data_stack->back();
                data_stack->pop_back();
                DataObject * temp2 = data_stack->back();
                data_stack->pop_back();
                data_stack->push_back(temp1);
                data_stack->push_back(temp2);
            }
            """


class OC_SWAP2(OpCode):
    def setup(self):
        self.opcodes_used = 3;

    @clean_statement
    def as_statement(self):
        # If we can optimize this away, just compile it right in.
        if len(self.compiler.expression_queue) >= 3:
            top = self._use_expression()
            middle = self._use_expression()
            bottom = self._use_expression()
            self.compiler.expression_queue.append(top)
            self.compiler.expression_queue.append(middle)
            self.compiler.expression_queue.append(bottom)
            return None

        top = self._use_expression()
        middle = self._use_expression()
        bottom = self._use_expression()
        return """
        {
            DataObject * temp1 = %s;
            DataObject * temp2 = %s;
            DataObject * temp3 = %s;
            data_stack->push_back(temp1);
            data_stack->push_back(temp2);
            data_stack->push_back(temp3);
        }
        """ % (top, middle, bottom)


OPCODES = {
    "STEP_ALLOC": OC_ALLOC,
    "STEP_ARRAYCAT": OC_ARRAYCAT,
    "STEP_ALT_ARRAYCAT": OC_ALT_ARRAYCAT,
    "STEP_ARRAYCOUNT": OC_ARRAYCOUNT,
    "STEP_ARRAYCPY": OC_ARRAYCPY,
    "STEP_CALL_SECONDARY": OC_CALL_SECONDARY,
    "STEP_CAST_DOUBLE": OC_CAST_DOUBLE,
    "STEP_CAST_LONG": OC_CAST_LONG,
    "STEP_CAST_STRING": OC_CAST_STRING,
    "STEP_CONST": OC_CONST,
    "STEP_CRLF": OC_CRLF,
    "STEP_DABS": OC_DABS,
    "STEP_DADD": OC_DADD,
    "STEP_DDIV": OC_DDIV,
    "STEP_DEQ": OC_DEQ,
    "STEP_DGE": OC_DGE,
    "STEP_DGE": OC_DGE,
    "STEP_DGT": OC_DGT,
    "STEP_DLE": OC_DLE,
    "STEP_DLT": OC_DLT,
    "STEP_DMINUS": OC_DMINUS,
    "STEP_DMULT": OC_DMULT,
    "STEP_DNEQ": OC_DNEQ,
    "STEP_DROP": OC_DROP,
    "STEP_DROP2": OC_DROP2,
    "STEP_DROPFRAME": OC_DROPFRAME,
    "STEP_DROPN": OC_DROPN,
    "STEP_DSIGN": OC_DSIGN,
    "STEP_DSUB": OC_DSUB,
    "STEP_DUP": OC_DUP,
    "STEP_DUP_I": OC_DUP_I,
    "STEP_DZEQ": OC_DZEQ,
    "STEP_DZGE": OC_DZGE,
    "STEP_DZLE": OC_DZLE,
    "STEP_DZLT": OC_DZLT,
    "STEP_DZNEQ": OC_DZNEQ,
    "STEP_FETCH": OC_FETCH,
    "STEP_FETCH_REGISTER": OC_FETCH_REGISTER,
    "STEP_FETCH_STACK": OC_FETCH_STACK,
    "STEP_FORK": OC_FORK,
    "STEP_GOTO": OC_GOTO,
    "STEP_GOTO0": OC_GOTO0,
    "STEP_ALT_GOTO0": OC_ALT_GOTO0,
    "STEP_JOIN": OC_JOIN,
    "STEP_LABS": OC_LABS,
    "STEP_LADD": OC_LADD,
    "STEP_LDIV": OC_LDIV,
    "STEP_LEQ": OC_LEQ,
    "STEP_LGE": OC_LGE,
    "STEP_LGT": OC_LGT,
    "STEP_LLE": OC_LLE,
    "STEP_LLT": OC_LLT,
    "STEP_LMINUS": OC_LMINUS,
    "STEP_LMOD": OC_LMOD,
    "STEP_LMULT": OC_LMULT,
    "STEP_LNEQ": OC_LNEQ,
    "STEP_LSIGN": OC_LSIGN,
    "STEP_LSUB": OC_LSUB,
    "STEP_LZEQ": OC_LZEQ,
    "STEP_LZGE": OC_LZGE,
    "STEP_LZGT": OC_LZGT,
    "STEP_LZLE": OC_LZLE,
    "STEP_LZLT": OC_LZLT,
    "STEP_LZNEQ": OC_LZNEQ,
    "STEP_OVER": OC_OVER,
    "STEP_OVER2": OC_OVER2,
    "STEP_PADD": OC_PADD,
    "STEP_PAUSE": OC_PAUSE,
    "STEP_PRINT": OC_PRINT,
    "STEP_PUSH_FP": OC_PUSH_FP,
    "STEP_REFCNT": OC_REFCNT,
    "STEP_RETURN": OC_RETURN,
    "STEP_SADD": OC_SADD,
    "STEP_SEQ": OC_SEQ,
    "STEP_SGE": OC_SGE,
    "STEP_SGT": OC_SGT,
    "STEP_SLE": OC_SLE,
    "STEP_SLT": OC_SLT,
    "STEP_SNEQ": OC_SNEQ,
    "STEP_STORE": OC_STORE,
    "STEP_STORE_I": OC_STORE_I,
    "STEP_STORE_REGISTER": OC_STORE_REGISTER,
    "STEP_STORE_STACK": OC_STORE_STACK,
    "STEP_SWAP": OC_SWAP,
    "STEP_SWAP2": OC_SWAP2,
}
