
import sys
import types

from bytecode_tools.common import opcodes
from bytecode_tools.common.constants import PY_VERSION


# These are fixed as per Cpython's Lib/dis.py
_OPNAME_WIDTH = 20
_OPARG_WIDTH = 5

_have_code = (types.MethodType, types.FunctionType, types.CodeType,
              classmethod, staticmethod, type)


class DecodeCodeObject:
    """Decode code object"""

    def __init__(
            self,
            code_object,
            last_instruction=-1,
            python_version=None,
            file=None):

        self.code_object = code_object
        self.code = code_object.co_code
        self.constants = code_object.co_consts
        self.names = code_object.co_names
        self.varnames = code_object.co_varnames
        self.freevars = code_object.co_cellvars + code_object.co_freevars
        self.file = file

        # If no python version passed then, the current interpreter verion
        # will be used.
        self.python_version = python_version if python_version else PY_VERSION
        self.last_instruction = last_instruction

        # Generate opcode classes and mapper for given python version.
        opcodes.OpcodeClassFactory.gen_opcode_classes(
            python_version=self.python_version)

        self.labels = None
        self.linestarts = None
        self.reader = (
            self._unpack_wordcode
            if self.python_version >= 3.6
            else self._unpack_bytecode
        )

    @staticmethod
    def _disassemble(
            instruction,
            lineno_width=3,
            mark_as_current=False,
            offset_width=4):
        """Format instruction details for inclusion in disassembly output

        *lineno_width* sets the width of the line number field (0 omits it)
        *mark_as_current* inserts a '-->' marker arrow as part of the line
        *offset_width* sets the width of the instruction offset field
        """
        fields = []
        # Column: Source code line number
        if lineno_width:
            if instruction.line is not None:
                lineno_fmt = "%%%dd" % lineno_width
                fields.append(lineno_fmt % instruction.line)
            else:
                fields.append(' ' * lineno_width)
        # Column: Current instruction indicator
        if mark_as_current:
            fields.append('-->')
        else:
            fields.append('   ')
        # Column: Jump target marker
        if instruction.is_jump_target:
            fields.append('>>')
        else:
            fields.append('  ')
        # Column: Instruction offset from start of code sequence
        fields.append(repr(instruction.offset).rjust(offset_width))
        # Column: Opcode name
        fields.append(instruction.OPCODE_NAME.ljust(_OPNAME_WIDTH))
        # Column: Opcode argument
        if instruction.arg is not None:
            fields.append(repr(instruction.arg).rjust(_OPARG_WIDTH))
            # Column: Opcode argument details
            if instruction.arg_repr:
                fields.append('(' + instruction.arg_repr + ')')
        return ' '.join(fields).rstrip()

    def disassemble(self, line_offset=0):
        """Disassembler"""
        # Omit the line number column entirely if we have no line number info

        unpacked_code = self.unpack_code()
        show_lineno = self.linestarts is not None
        if show_lineno:
            maxlineno = max(self.linestarts.values()) + line_offset
            if maxlineno >= 1000:
                lineno_width = len(str(maxlineno))
            else:
                lineno_width = 3
        else:
            lineno_width = 0
        maxoffset = len(self.code) - 2
        if maxoffset >= 10000:
            offset_width = len(str(maxoffset))
        else:
            offset_width = 4

        for instr in unpacked_code:
            new_source_line = (show_lineno and
                               instr.line is not None and
                               instr.offset > 0)
            if new_source_line:
                print('')
            is_current_instr = instr.offset == self.last_instruction
            print(
                self._disassemble(instr, lineno_width, is_current_instr, offset_width)
            )

    def _get_const_info(self, const_index):
        """Helper to get optional details about const references

           Returns the dereferenced constant and its repr if the constant
           list is defined.
           Otherwise returns the constant index and its repr().
        """
        argval = const_index
        if self.constants is not None:
            argval = self.constants[const_index]
        return argval, repr(argval)

    @staticmethod
    def _get_name_info(name_index, name_list):
        """Helper to get optional details about named references

           Returns the dereferenced name as both value and repr if the name
           list is defined.
           Otherwise returns the name index and its repr().
        """
        argval = name_index
        if name_list is not None:
            argval = name_list[name_index]
            argrepr = argval
        else:
            argrepr = repr(argval)
        return argval, argrepr

    def line_no_table(self):
        """co_lnotab is an array of unsigned bytes, which holds differences in
        bytecode and line number increments or decrements with the previous
        instruction.

        Line number table is a map with the byte position to the line poition in the
        source code. I.e.

          Byte: Byte code offset
          Line: Source code line number

          Byte - Line
          -----  -----
          0       1
          3       2
          10      3
          44      25
          366     64
          390     298

        This code line map says, the line 1 started at byte 0 and line 2 at byte 3..

        But the actual line number map holds the differences not the actual numbers,
        this way we compress the array and store values near to a signed byte value.

        for the above byte line source the actual table looks like ........

          I.e: First line always starts at byte 0.

          Byte - Line
          -----  -----
          0       1
          3       1
          7       1
          34      22
          322     39
          24      234

        Ideally with the differences the byte code should have a table like..

          0 1 3 1 7 1 34 22 322 39 24 234

        But, byte code offset is a unsigned byte, this means it should not have
        value more than 255, and the line number is a signed byte, this means line
        number increment should not have value more than 127 and less than -128.

        WHAT IF the byte increment goes beyond 255 ?

        In the above example, we've one instance where the byte offset is more
        than 255.

          Byte:   Line
          ----    ----
          322     39

        Since 322 is not in signed byte range 0 to 255, it has to be converted to
        multiple instructions, like below....

          Byte   Line
          ----   -----
          255     0
          77      39

        The byte line map becomes, like below...

          0 1 3 1 7 1 34 22 255 0 77 39 24 234

        WHAT IF line number increment is > 127 or < -128 ?

        In the above example, we've an instance where the line incrementis more
        than 255.

          Byte:   Line
          ----    ----
          24      234

        Since 234 is not in unsigned byte range -128 to 127, it has to be converted
        to multiple instructions, like below....

          Byte   Line
          ----   -----
          0      127
          24     97

        Finally the byte line map becomes, like below...

          0 1 3 1 7 1 34 22 255 0 77 39 0 127 24 97
        """
        addr = 0  # Address start with byte index zero.
        last_lineno = None

        lineno = self.code_object.co_firstlineno
        byte_increments = self.code_object.co_lnotab[0::2]
        line_increments = self.code_object.co_lnotab[1::2]

        for byte_incr, line_incr in zip(byte_increments, line_increments):
            # No byte increment means, it's helping instruction for satsifying
            # line increment signed byte range as explained above.
            byte_incr = (
                ord(byte_incr) if isinstance(byte_incr, str) else byte_incr)
            line_incr = (
                ord(line_incr) if isinstance(line_incr, str) else line_incr)
            if byte_incr:

                # If current line and last line numbers match, this means that it's
                # a helping instruction for satsifying byte offset unsigned byte
                # range as explained above.
                if last_lineno != lineno:
                    yield (addr, lineno)
                    last_lineno = lineno
                addr += byte_incr

            # Line increments are 8 bit signed integers, if the number is gone
            # below 0, it should be stored somehow between 0 to 255 range of byte
            # line map array.
            # If the value is negative ( < 0), it will be stored as 256 - val
            # I.e: if the line increment is -10, the line map array stores it as
            #.   256 - 10 --> 246
            #
            # If line increment more than 128, we should do line_incr - 256 to get
            # the actual value.
            # Le's say if the line_incr is 246, then it should be 246 - 256 -> -10
            if line_incr >= 0x80:
                line_incr -= 0x100
            lineno += line_incr

        if last_lineno != lineno:
            yield(addr, lineno)

    def findlabels(self, unpacked_code=None):
        """Jump target label finder."""
        labels = []
        if unpacked_code is None:
            unpacked_code = self.reader()

        for offset, _, op_code, arg in unpacked_code:
            if arg:
                if op_code.has_jrel():
                    target = offset + 2 + arg
                elif op_code.has_jabs():
                    target = arg
                else:
                    continue

                if target not in labels:
                    labels.append(target)
        return labels

    def unpack_code(self):
        """Unpack the bytecode"""
        self.labels = self.findlabels(unpacked_code=self.reader())
        self.linestarts = dict(self.line_no_table())

        instruction_list = []
        for offset, end, op_code, arg in self.reader():
            argval = None
            argrepr = ''
            line_start = self.linestarts.get(offset, None)
            is_jump_target = offset in self.labels
            if not arg is None:
                argval = arg
                if op_code.has_const():
                    argval, argrepr = self._get_const_info(arg)
                elif op_code.has_name():
                    argval, argrepr = self._get_name_info(arg, self.names)
                elif op_code.has_local():
                    argval, argrepr = self._get_name_info(arg, self.varnames)
                elif op_code.has_free():
                    argval, argrepr = self._get_name_info(arg, self.freevars)
                elif op_code.has_cmp():
                    argval = opcodes.CMP_OP[arg]
                    argrepr = repr(argval)
                elif op_code.is_make_function():
                    argrepr = ', '.join(
                        s for i, s in enumerate(opcodes.MAKE_FUNCTION_FLAGS)
                        if arg & (1<<i)
                    )
                elif op_code.has_jrel():
                    argval = arg
                    argrepr = "to {val}".format(val=offset + arg + 2)

            instruction_list.append(op_code(
                offset,
                end,
                line_start,
                arg,
                argval,
                argrepr,
                is_jump_target
            ))
        return instruction_list

    def _unpack_bytecode(self):
        # Unlike wordcode, bytecode doesn't have fixed 16 byte words.
        pos = 0
        extended_arg = 0
        offset = 0
        size = len(self.code)

        while pos < size:
            arg = None
            op_code = getattr(
                opcodes, opcodes.OPCODE_MAPPER[self._code_index_val(pos)][0]
            )
            if op_code.has_arg():
                factor = 0
                if op_code.is_extended_arg():
                    assert not extended_arg
                    factor = 2

                temp_arg = (
                    self._code_index_val(pos+1) << (8 * factor) |
                    self._code_index_val(pos+2) << (8 * (factor + 1))
                )
                if factor:
                    extended_arg = temp_arg
                    arg = None
                else:
                    arg = temp_arg
                    arg |= extended_arg

                bytes_read = 3
            else:
                # EXTENDED_ARG should be infront of any opcode with arg, if not
                # there is a problem
                assert not extended_arg
                extended_arg = 0
                bytes_read = 1

            yield (offset, pos + bytes_read, op_code, arg)
            offset = pos + bytes_read
            pos += bytes_read

    def _code_index_val(self, i):
        if isinstance(self.code[i], str):
            return ord(self.code[i])
        return self.code[i]

    def _unpack_wordcode(self):
        extended_arg = 0
        for i in range(0, len(self.code), 2):
            op_code = getattr(
                opcodes, opcodes.OPCODE_MAPPER[self._code_index_val(i)][0]
            )
            if op_code.has_arg():
                arg = self._code_index_val(i + 1) | extended_arg
                extended_arg = arg << 8 if op_code.is_extended_arg() else 0
            else:
                arg = None
            yield (i, i+2, op_code, arg)