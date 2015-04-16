# ESST (Embedded System Software Tools) License
# -----------------------------------------------------------------------------
# 
# SOFTWARE LICENSE
# 
# This software is provided subject to the following terms and conditions,
# which you should read carefully before using the software. Using this
# software indicates your acceptance of these terms and conditions. 
# If you do not agree with these terms and conditions, do not use the software.
# 
# Copyright (c) 1995-2002 Agere Systems Inc.
# All rights reserved.
# 
# Redistribution and use in source or binary forms, with or without
# modifications, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following Disclaimer in comments in the code
# as well as in the documentation and/or other materials provided with the
# distribution.
# * Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following Disclaimer in the documentation
# and/or other materials provided with the distribution.
# * Neither the name of Agere Systems Inc. nor the names of the contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
# 
# Disclaimer
# 
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, INFRINGEMENT AND THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# ANY USE, MODIFICATION OR DISTRIBUTION OF THIS SOFTWARE IS SOLELY AT THE
# USER'S OWN RISK. IN NO EVENT SHALL AGERE SYSTEMS INC. OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, INCLUDING,
# BUT NOT LIMITED TO, CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# stepsgs.tcl -- compiler front end for STEP stack machine.
# Modified to accept labels, May, 2001, so C compiler can use
# new opcode 'gotoaddr' (computed goto for C switch statement)
# by jumping to a label. Also added new pubops 79-82 at end.
# Also moved local variables to the end of their respective
# proc bodies, eliminated 'goto' jumps over local variables.

# MODIFIED FEBRUARY, 2009, D. PARSON, TO SEPARATE A CODE DICTIONARY FROM
# A DATA DICTIONARY, AND TO GENERATE CODE FOR CSC 580 PYTHON DIRECT AND
# INDIRECT THREADED CODE VMS.

set stepCompileFirstTime 1

set DIRDICT_LEN 0 ; # next slot in the direct threaded code dictionary
set INDDICT_LEN 0 ; # next slot in the indirect threaded code dictionary
set DATDICT_LEN 0 ; # next slot in the data dictionary
set MAIN_ADDRESS -1 ;    # Set to address when main is defined
set IMAIN_ADDRESS -1 ;    # Set to address when main is defined

set stepMaxDepth 0 ;	# depth of deepest proc.
set stepMaxProc "" ;	# name of the deepest proc

proc stepCompile {textProgram textName textLineno loadFile appendmode \
    wordSize} {
    global errorcode
    set errorcode 0
    stepCompileStartup errorcode
    if {[string compare $appendmode w] == 0} {
	stepClobberDict
    }
    if {$errorcode} {
	error "error in stepCompileStartup"
    }

    # All of the control structures generate jumps forward to
    # address not know when goto opcodes are generated.
    # A couple of tables here track all of this information:

    # 1. "if" construct:
    #
    # if
    #	test-code
    #	(CONDITIONAL GOTO ADDR1 on failure)
    # then			(fall through)
    #	success
    #	(UNCONDITIONAL GOTO ADDR2)
    # else
    #	ADDR1			(ADDR1 goto dest. on failure)
    #	failure
    # endif
    #	ADDR2			(ADDR2 is after body of if)
    #
    # When there is no else clause, GOTO ADDR2 is not generated.

    # 2. "while" construct:
    #
    # while
    # ADDR1			(ADDR1 is test code, "continue" addr.)
    #	test-code
    # (CONDITIONAL GOTO ADDR2 on failure)
    # do
    #	loop-code
    #	(UNCONDITIONAL GOTO ADDR1)
    # endwhile
    # ADDR2			(ADDR2 is after body of while, for "break")

    # 3. "dountil" construct:
    # dountil
    # ADDR3			(ADDR3 is top of loop)
    #	loop-code
    # until
    #   ADDR1 is for "continue"
    #	test-code
    #   (CONDITIONAL GOTO ADDR3 on failure)
    # enduntil
    # ADDR2 is for "break"

    # 4. "switch" construct:
    # ADDR1 is the address after the body of opcode-cases

    # 5. "proc" construct doesn't need any of this

    # MAPPINGS FOR PRIMITIVES:
    global pubop		; # text->opcode
    global privop		; # text->opcode
    global pubtext		; # opcode->text
    global privtext		; # opcode->text
    global indirectop   ; # opcode->partialtext if there is an indirect opcode

    # MAPPINGS FOR PROC opcodes:
    global procop		; # text->opcode
    global iprocop		; # text->indirect opcode
    global procdeep		; # text->depth
    global stepMaxDepth		; # depth of deepest proc.
    global stepMaxProc		; # name of the deepest proc
    set proc_topbit [expr 1 << ($wordSize -1)] ; # flag to run-time interpreter

    # MAPPINGS FOR constants and variables
    global const_value		; # constant value
    global var_addr		; # variable address
    set loc_const_value {}	; # temporary lookup for local constants
    # May, 2001 loc_var_def use to house a local variable name and
    # its address. Since the address is now unknown until the end of the
    # proc, loc_var_def now houses a 3-tuple:
    # {name num-elements list-of-values}, where list-of-values is an
    # empty list for scalar variables & aarrays, but is populated
    # for tables.
    set loc_var_def {}		; # temporary lookup for local static variables
    zaparray loc_var_ref	; # array that holds unresolved variable refs.
    zaparray iloc_var_ref	; # array that holds unresolved variable refs.
    # string literals within procs now also store at the proc end,
    # loc_string_lits is a list of ordered pairs, with a patch address
    # for the string reference, followed by a list of ASCII integers
    # NOT USED FOR PYTHON
    # set loc_string_lits {}	; # {patchref charlist} pairs
    set loc_label_addr {}	; # local label addresses tracked here
    set loc_label_fwddecls {}	; # labels declared but not yet placed
    # set iloc_label_addr {}	; # local label addresses tracked here
    # set iloc_label_fwddecls {}	; # labels declared but not yet placed
    zaparray unresolved_label_refs ; # array that holds unresolved label refs

    global DIRDICT_LEN	; # next free spot in direct code dictionary
    set DIRDICT_LEN 0
    global INDDICT_LEN	; # next free spot in direct code dictionary
    set INDDICT_LEN 0
    global DATDICT_LEN	; # next free spot in data dictionary
    set DATDICT_LEN 0
    global MAIN_ADDRESS
    global IMAIN_ADDRESS

    # Initialize output lists for this compiler pass. These are local.
    set DIRDICT_RECORD {}	; # one record's worth of load
    set DIRDICT_ARRAY {}        ; # Concatenation of all procs, etc. for dict.
    set DIRDICT_BASE $DIRDICT_LEN
    set DIRDICT_ARRAY {0 0 0}     ; # leave room for 'call main bpt'
    set DIRDICT_LEN 3
    set DIRDICT_END $DIRDICT_LEN

    set INDDICT_RECORD {}	; # one record's worth of load
    set INDDICT_ARRAY {}        ; # Concatenation of all procs, etc. for dict.
    set INDDICT_BASE $INDDICT_LEN
    set INDDICT_ARRAY {0 0}     ; # leave room for 'call main bpt'
    set INDDICT_LEN 2
    set INDDICT_END $INDDICT_LEN

    set DATDICT_BASE $DATDICT_LEN
    set DATDICT_END $DATDICT_LEN
    set DATDICT_RECORD {}	; # one record's worth of load
    set DATDICT_ARRAY {}        ; # Concatenation of all data declarations.
    set loadcmds {}		; # Immediate commands
    set debug_procs {}		; # proc name-addr pairs for debugger
    set idebug_procs {}		; # proc name-addr pairs for debugger
    set debug_datas {}		; # data name-addr pairs for debugger
    set debug_ips [list [step_abs_path $textName]] ; # {filename {line# ip} ...} for debugger
    set idebug_ips [list [step_abs_path $textName]] ; # {filename {line# ip} ...} for debugger

    # Monitors for control constructs
    global ctrlwords datawords
    # control words match to their predecessors through array 'expect'
    set expect(then) if
    set expect(else) then
    set expect(endif) {then else}
    set expect(do) while
    set expect(endwhile) do
    set expect(until) dountil
    set expect(enduntil) until
    set expect(case) switch
    set expect(endcase) case
    set controlDepth 0		; # monitor control constructs
    set controlStack(0) NOTHING
    set ifDepth 0		; # depth of if constructs
    set loopDepth 0		; # depth of loop constucts
    set isSwitch 0		; # compiling a switch series
    set isInProc 0		; # compiling a proc
    set curline $textLineno

    # Crack the input text in this main loop:
    # First separate newlines from other text as distinct tokens.
    set tokcount 0
    set curtok 0
    # change toklist to array tokarray, D. Parson, 1/99
    stepTokenize $textProgram tokarray tokcount
    while {$curtok < $tokcount} {
	stepGetToken token tokarray curtok $tokcount curline
	if {[string compare $token ""] == 0} {
	    break
	}
	# switch requires ONLY a secondary PROC address, check for
	# this error here to avoid cluttering up tests below
	if {$isSwitch && (! [info exists procop($token)]) \
		&& [string compare $token endcase]} {
	    error \
	    "call to non-proc '$token' within switch, file $textName, line $curline, proc $procname"
	}
	if {[string compare $token proc] == 0} {
	    # PROC
	    if {[info exists procname]} {
		set errorcode 1
		error \
		"nested proc definition in '$procname', file $textName line $curline"
	    }
	    stepGetToken token tokarray curtok $tokcount curline
	    if {[string compare $token ""] == 0} {
		set errorcode 1
	        error \
		"missing proc name in $textName line $curline"
	    } else {
		stepIsReserved $token $textName $curline proc 1
	    }
	    set procname $token
            if {"${token}" == "main"} {
                set MAIN_ADDRESS $DIRDICT_END
                set IMAIN_ADDRESS $INDDICT_END
            }
	    set procop($procname) $DIRDICT_END
	    set iprocop($procname) $INDDICT_END
	    set procdeep($procname) 1
	    if {[llength $DIRDICT_RECORD]} {
		set errorcode 1
		error \
		"in-line code before proc ${procname}"
		# records outside of proc are immediate commands
		### set loadcmds [concat $loadcmds $DIRDICT_RECORD]
	    }
	    set DIRDICT_RECORD {}	; # each proc starts a new record
	    set INDDICT_RECORD {}	; # each proc starts a new record
	    set loc_const_value {}	; # fresh set of local constants
	    set loc_var_def {}		; # as well as variables
	    zaparray loc_var_ref	; # and references to variables
	    zaparray iloc_var_ref	; # and references to variables
	    # set loc_string_lits {}	; # {patchref charlist} pairs
    	    set loc_label_addr {}	; # local label addresses tracked here
	    set loc_label_fwddecls {}	; # labels declared but not yet placed
    	    set iloc_label_addr {}	; # local label addresses tracked here
	    set iloc_label_fwddecls {}	; # labels declared but not yet placed
	    zaparray unresolved_label_refs	; # holds unresolved label refs
	    set isInProc 1
	} elseif {[string compare $token endproc] == 0} {
	    # ENDPROC
	    if {! $isInProc} {
		set errorcode 1
		error \
		"endproc with no proc, file $textName line $curline"
	    } elseif {$controlDepth} {
		set errorcode 1
		error \
		"unterminated control '$controlStack($controlDepth)' at endproc, file $textName line $curline"
	    }
	    # stuff return statement at proc's end
	    lappend DIRDICT_RECORD $privop(return)
	    lappend INDDICT_RECORD "i$privop(return)"
	    dbg debug_ips $curline $DIRDICT_END
	    dbg idebug_ips $curline $INDDICT_END
	    incr DIRDICT_END
	    incr INDDICT_END
	    # variables may have been declared in this proc, but their
	    # allocation doesn't happen until here.
	    foreach vardecl $loc_var_def {
		set varname [lindex $vardecl 0]
		set varelem [lindex $vardecl 1]
		set varinit [lindex $vardecl 2]
		lappend debug_datas [list "$varname@@$procname" $DATDICT_END]
		# resolve forward refs before allocating storage
		if {[info exists loc_var_ref($varname)]} {
		    foreach varref $loc_var_ref($varname) {
			set DIRDICT_RECORD [lreplace $DIRDICT_RECORD    \
                            $varref $varref $DATDICT_END]
		    }
		    unset loc_var_ref($varname)
		}
		if {[info exists iloc_var_ref($varname)]} {
		    foreach varref $iloc_var_ref($varname) {
			set INDDICT_RECORD [lreplace $INDDICT_RECORD    \
                            $varref $varref                             \
                            "$indirectop(variable)$DATDICT_END,))"]
		    }
		    unset iloc_var_ref($varname)
		}
		# Now allocate & initialize the variable/array/table.
		# varinit is non-empty for a table, empty for scalar or array.
		if {[llength $varinit]} {
		    # A table may have unresolved label references.
		    foreach initvalue $varinit {
			if {[llength $initvalue] == 2			\
				&& [string compare [lindex $initvalue 0] \
				    undefined-label] == 0} {
			    set tmplabel [lindex $initvalue 1]
			    set valslot [linsrch $loc_label_addr $tmplabel]
			    if {$valslot >= 0} {
	    		        lappend DATDICT_RECORD	\
				[lindex [lindex $loc_label_addr $valslot] 1]
			    } else {
				set errorcode 1
				error \
				"unresolved ref to label $tmplabel in table $varname, proc $procname"
			    }
			} else {
			    lappend DATDICT_RECORD $initvalue
			}
		    }
		} else {
		    for {set i 0} {$i < $varelem} {incr i} {
			lappend DATDICT_RECORD 0
		    }
		}
		incr DATDICT_END $varelem
	    }
	    set undefflag 0
	    foreach uref [array names loc_var_ref] {
		set errorcode 1
		set undefflag 1
		puts stderr "unresolved refs to variable $uref in $procname"
	    }
	    foreach uref [array names iloc_var_ref] {
		set errorcode 1
		set undefflag 1
		puts stderr "unresolved refs to variable $uref in $procname"
	    }
	    foreach uref [array names unresolved_label_refs] {
		set errorcode 1
		set undefflag 1
		puts stderr "unresolved refs to label $uref in $procname"
	    }
	    if {$undefflag} {
		error "unresolved references in $procname"
	    }
	    # string literals may have appeared in this proc, allocate
	    # their storage data dict's end, and patch up the singleton
	    # forward reference to each
#	    foreach lit_tmp $loc_string_lits {
#		set tmp_patch [lindex $lit_tmp 0]
#		set tmp_bytes [lindex $lit_tmp 1]
#		set DIRDICT_RECORD [lreplace $DIRDICT_RECORD $tmp_patch $tmp_patch \
#		    $DATDICT_END]
#		foreach tmp_ascii $tmp_bytes {
#		    lappend DATDICT_RECORD $tmp_ascii
#		}
#		incr DATDICT_END [llength $tmp_bytes]
#	    }
	    lappend debug_procs [list $procname $procop($procname)]
	    lappend idebug_procs [list $procname $iprocop($procname)]
	    if {($procdeep($procname) < 0 && $stepMaxDepth >= 0) \
		    || ($procdeep($procname) > $stepMaxDepth \
			&& $stepMaxDepth >= 0)} {
		# a stored negative indicates recursion
		set stepMaxDepth $procdeep($procname)
		set stepMaxProc $procname
	    }
	    unset procname
	    # put words at end of DIRDICT_ARRAY, we add record header info. later
	    set DIRDICT_ARRAY [concat $DIRDICT_ARRAY $DIRDICT_RECORD]
	    set DIRDICT_RECORD {}		; # clear within-proc records
	    set INDDICT_ARRAY [concat $INDDICT_ARRAY $INDDICT_RECORD]
	    set INDDICT_RECORD {}		; # clear within-proc records
	    set DATDICT_ARRAY [concat $DATDICT_ARRAY $DATDICT_RECORD]
	    set DATDICT_RECORD {}		; # clear within-proc records
	    set loc_const_value {}
	    set loc_var_def {}
	    # set loc_string_lits {}
    	    set loc_label_addr {}
	    set loc_label_fwddecls {}
	    zaparray unresolved_label_refs
	    set isInProc 0
	} elseif {[lsearch -exact $ctrlwords $token] >= 0} {
	    # CONTROL WORDS HAVE SOME TESTS AS A GROUP
	    if {! $isInProc} {
		set errorcode 1
		error \
		"control word '$token' outside proc, file $textName line $curline"
	    } elseif {[info exists expect($token)] \
		    && ($controlDepth == 0 || [lsearch $expect($token) \
			$controlStack($controlDepth)] < 0)} {
		# last unfinished control construct doesn't match token
		set errorcode 1
		error \
		"'$token' unmatched by '$controlStack($controlDepth)', expects '$expect($token)', file $textName, line $curline, proc $procname"
	    }
	    # control construct looks OK, go ahead with details
	    if {[string compare $token return] == 0} {
		lappend DIRDICT_RECORD $privop(return)
		lappend INDDICT_RECORD "i$privop(return)"
		dbg debug_ips $curline $DIRDICT_END
		dbg idebug_ips $curline $INDDICT_END
		incr DIRDICT_END
		incr INDDICT_END
	    } elseif {[string compare $token if] == 0} {
		incr controlDepth
		incr ifDepth
		set controlStack($controlDepth) if
	    } elseif {[string compare $token then] == 0} {
		set controlStack($controlDepth) then
		# generate goto0 ADDR1, resolve ADDR1 later
		lappend DIRDICT_RECORD $privop(goto0)
		# record offset needing fixup in DIRDICT_RECORD, store dummy
		set IF_ADDR1($ifDepth) [llength $DIRDICT_RECORD]
		set IND_IF_ADDR1($ifDepth) [llength $INDDICT_RECORD]
		lappend DIRDICT_RECORD IF_ADDR1_DEFERRED
		lappend INDDICT_RECORD IF_ADDR1_DEFERRED
		dbg debug_ips $curline $DIRDICT_END
		dbg idebug_ips $curline $INDDICT_END
		incr DIRDICT_END 2
                incr INDDICT_END 1
	    } elseif {[string compare $token else] == 0} {
		set controlStack($controlDepth) else
		# generate goto ADDR2 for bottom of the success branch
		lappend DIRDICT_RECORD $privop(goto)
		set IF_ADDR2($ifDepth) [llength $DIRDICT_RECORD]
		set IND_IF_ADDR2($ifDepth) [llength $INDDICT_RECORD]
		lappend DIRDICT_RECORD IF_ADDR2_DEFERRED
		lappend INDDICT_RECORD IF_ADDR2_DEFERRED
		dbg debug_ips $curline $DIRDICT_END
		dbg idebug_ips $curline $INDDICT_END
		incr DIRDICT_END 2
                incr INDDICT_END 1
		# we are at ADDR1 for the success case, backfill it
		set DIRDICT_RECORD [lreplace $DIRDICT_RECORD $IF_ADDR1($ifDepth) \
		    $IF_ADDR1($ifDepth) $DIRDICT_END]
		set INDDICT_RECORD [lreplace $INDDICT_RECORD $IND_IF_ADDR1($ifDepth) \
		    $IND_IF_ADDR1($ifDepth) "$indirectop(goto0)$INDDICT_END,))"]
	    } elseif {[string compare $token endif] == 0} {
		# endif needs to patch up 1 forward reference
		if {[string compare $controlStack($controlDepth) then] == 0} {
		    # no else, patch up ADDR1
		    set DIRDICT_RECORD [lreplace $DIRDICT_RECORD $IF_ADDR1($ifDepth) \
			$IF_ADDR1($ifDepth) $DIRDICT_END]
		    set INDDICT_RECORD [lreplace $INDDICT_RECORD $IND_IF_ADDR1($ifDepth) \
		        $IND_IF_ADDR1($ifDepth) "$indirectop(goto0)$INDDICT_END,))"]
		} else {
		    # endif follows else, patch up ADDR2
		    set DIRDICT_RECORD [lreplace $DIRDICT_RECORD $IF_ADDR2($ifDepth) \
			$IF_ADDR2($ifDepth) $DIRDICT_END]
		set INDDICT_RECORD [lreplace $INDDICT_RECORD $IND_IF_ADDR2($ifDepth) \
		    $IND_IF_ADDR2($ifDepth) "$indirectop(goto)$INDDICT_END,))"]
		    unset IF_ADDR2($ifDepth)
                    unset IND_IF_ADDR2($ifDepth)
		}
		unset IF_ADDR1($ifDepth)
		unset IND_IF_ADDR1($ifDepth)
		unset controlStack($controlDepth)
		incr ifDepth -1
		incr controlDepth -1
	    } elseif {[string compare $token while] == 0} {
		incr controlDepth
		incr loopDepth
		set controlStack($controlDepth) while
		# ADDR1 is known, needed by "continue" & bottom of loop
		set HAS_LOOP_ADDR1($loopDepth) $DIRDICT_END
		set IND_HAS_LOOP_ADDR1($loopDepth) $INDDICT_END
		set LOOPTEST($loopDepth) 1
	    } elseif {[string compare $token do] == 0} {
		set controlStack($controlDepth) do
		# generate goto0 ADDR2, resolve ADDR2 later
		lappend DIRDICT_RECORD $privop(goto0)
		lappend NEEDS_LOOP_ADDR2($loopDepth) [llength $DIRDICT_RECORD]
		lappend IND_NEEDS_LOOP_ADDR2($loopDepth) $indirectop(goto0)
		lappend IND_NEEDS_LOOP_ADDR2($loopDepth) [llength $INDDICT_RECORD]
		lappend DIRDICT_RECORD LOOP_ADDR2_DEFERRED
		lappend INDDICT_RECORD LOOP_ADDR2_DEFERRED
		dbg debug_ips $curline $DIRDICT_END
		dbg idebug_ips $curline $INDDICT_END
		incr DIRDICT_END 2
                incr INDDICT_END 1
		set LOOPTEST($loopDepth) 0
	    } elseif {[string compare $token endwhile] == 0} {
		# generate goto ADDR1, then fix up jumps to ADDR2
		lappend DIRDICT_RECORD $privop(goto)
		lappend DIRDICT_RECORD $HAS_LOOP_ADDR1($loopDepth)
                lappend INDDICT_RECORD "$indirectop(goto)$IND_HAS_LOOP_ADDR1($loopDepth),))"
		dbg debug_ips $curline $DIRDICT_END
		dbg idebug_ips $curline $INDDICT_END
		incr DIRDICT_END 2
                incr INDDICT_END 1
		# foward refs were failed while test as well as "break"
		foreach ref $NEEDS_LOOP_ADDR2($loopDepth) {
		    set DIRDICT_RECORD [lreplace $DIRDICT_RECORD $ref $ref $DIRDICT_END]
		}
		foreach {iop ref} $IND_NEEDS_LOOP_ADDR2($loopDepth) {
		    set INDDICT_RECORD [lreplace $INDDICT_RECORD $ref $ref \
                        "$iop$INDDICT_END,))"]
		}
		unset HAS_LOOP_ADDR1($loopDepth)
		unset NEEDS_LOOP_ADDR2($loopDepth)
		unset IND_HAS_LOOP_ADDR1($loopDepth)
		unset IND_NEEDS_LOOP_ADDR2($loopDepth)
		unset controlStack($controlDepth)
		unset LOOPTEST($loopDepth)
		incr loopDepth -1
		incr controlDepth -1
	    } elseif {[string compare $token dountil] == 0} {
		incr controlDepth
		incr loopDepth
		set controlStack($controlDepth) dountil
		# ADDR3 is known, needed by bottom of loop
		set HAS_LOOP_ADDR3($loopDepth) $DIRDICT_END
		set IND_HAS_LOOP_ADDR3($loopDepth) $INDDICT_END
		set LOOPTEST($loopDepth) 0
	    } elseif {[string compare $token until] == 0} {
		# ADDR1 needed by continue, just before test at bottom
		set controlStack($controlDepth) until
		set HAS_LOOP_ADDR1($loopDepth) $DIRDICT_END
		set IND_HAS_LOOP_ADDR1($loopDepth) $INDDICT_END
		set LOOPTEST($loopDepth) 1
	    } elseif {[string compare $token enduntil] == 0} {
		# generate conditional goto0 ADDR3 if "until" not satisfied
		lappend DIRDICT_RECORD $privop(goto0)
		lappend DIRDICT_RECORD $HAS_LOOP_ADDR3($loopDepth)
                lappend INDDICT_RECORD "$indirectop(goto0)$IND_HAS_LOOP_ADDR3($loopDepth),))"
		dbg debug_ips $curline $DIRDICT_END
		dbg idebug_ips $curline $INDDICT_END
		incr DIRDICT_END 2
                incr INDDICT_END 1
		# continue generates forward refs to ADDR1, break to ADDR2
		if {[info exists NEEDS_LOOP_ADDR2($loopDepth)]} {
		    foreach ref $NEEDS_LOOP_ADDR2($loopDepth) {
			set DIRDICT_RECORD [lreplace $DIRDICT_RECORD $ref $ref $DIRDICT_END]
		    }
		    unset NEEDS_LOOP_ADDR2($loopDepth)
		}
		if {[info exists IND_NEEDS_LOOP_ADDR2($loopDepth)]} {
		    foreach {iop ref} $IND_NEEDS_LOOP_ADDR2($loopDepth) {
			set INDDICT_RECORD [lreplace $INDDICT_RECORD $ref $ref \
                            "$iop$INDDICT_END,))"]
		    }
		    unset IND_NEEDS_LOOP_ADDR2($loopDepth)
		}
		if {[info exists NEEDS_LOOP_ADDR1($loopDepth)]} {
		    foreach ref $NEEDS_LOOP_ADDR1($loopDepth) {
			set DIRDICT_RECORD [lreplace $DIRDICT_RECORD $ref $ref \
			    $HAS_LOOP_ADDR1($loopDepth)]
		    }
		    unset NEEDS_LOOP_ADDR1($loopDepth)
		}
		if {[info exists IND_NEEDS_LOOP_ADDR1($loopDepth)]} {
		    foreach ref $IND_NEEDS_LOOP_ADDR1($loopDepth) {
			set INDDICT_RECORD [lreplace $INDDICT_RECORD $ref $ref \
			    "$indirectop(goto)$IND_HAS_LOOP_ADDR1($loopDepth),))"]
		    }
		    unset IND_NEEDS_LOOP_ADDR1($loopDepth)
		}
		unset HAS_LOOP_ADDR1($loopDepth)
		unset HAS_LOOP_ADDR3($loopDepth)
		unset IND_HAS_LOOP_ADDR1($loopDepth)
		unset IND_HAS_LOOP_ADDR3($loopDepth)
		unset controlStack($controlDepth)
		unset LOOPTEST($loopDepth)
		incr loopDepth -1
		incr controlDepth -1
	    } elseif {[string compare $token break] == 0 \
		    || [string compare $token continue] == 0} {
		if {$loopDepth == 0} {
		    set errorcode 1
		    error \
		    "'$token' outside of loop, file $textName, line $curline, proc $procname"
		} elseif {$LOOPTEST($loopDepth) != 0} {
		    # no jumps out of loop-test-code
		    set errorcode 1
		    error \
		    "'$token' disallowed in loop test section, file $textName, line $curline, proc $procname"
		}
		lappend DIRDICT_RECORD $privop(goto)
		if {[string compare $token break] == 0} {
		    if {[info exists HAS_LOOP_ADDR2($loopDepth)]} {
			lappend DIRDICT_RECORD $HAS_LOOP_ADDR2($loopDepth)
			lappend INDDICT_RECORD $IND_HAS_LOOP_ADDR2($loopDepth)
		    } else {
			lappend NEEDS_LOOP_ADDR2($loopDepth) \
			    [llength $DIRDICT_RECORD]
			lappend DIRDICT_RECORD LOOP_ADDR2_DEFERRED
                        lappend IND_NEEDS_LOOP_ADDR2($loopDepth)        \
                            $indirectop(goto)
			lappend IND_NEEDS_LOOP_ADDR2($loopDepth) \
			    [llength $INDDICT_RECORD]
			lappend INDDICT_RECORD LOOP_ADDR2_DEFERRED
		    }
		} else {
		    if {[info exists HAS_LOOP_ADDR1($loopDepth)]} {
			lappend DIRDICT_RECORD $HAS_LOOP_ADDR1($loopDepth)
			lappend INDDICT_RECORD $IND_HAS_LOOP_ADDR1($loopDepth)
		    } else {
			lappend NEEDS_LOOP_ADDR1($loopDepth) \
			    [llength $DIRDICT_RECORD]
			lappend DIRDICT_RECORD LOOP_ADDR1_DEFERRED
			lappend IND_NEEDS_LOOP_ADDR1($loopDepth) \
			    [llength $INDDICT_RECORD]
			lappend INDDICT_RECORD IND_LOOP_ADDR1_DEFERRED
		    }
		}
		dbg debug_ips $curline $DIRDICT_END
		dbg idebug_ips $curline $INDDICT_END
		incr DIRDICT_END 2
                incr INDDICT_END 1
	    } elseif {[string compare $token switch] == 0} {
		incr controlDepth
		# DO "set isSwitch 1" AFTER "case"--see below
		set controlStack($controlDepth) switch
	    } elseif {[string compare $token case] == 0} {
		set controlStack($controlDepth) case
		set isSwitch 1
		# generate gotox and a hole into which to plus the # cases
		lappend DIRDICT_RECORD $privop(gotox)
		lappend INDDICT_RECORD $privop(gotox)
		# case length needing fixup in DIRDICT_RECORD, store dummy
		set CASE_ADDR1 [llength $DIRDICT_RECORD]
		set IND_CASE_ADDR1 [llength $INDDICT_RECORD]
		lappend DIRDICT_RECORD CASE_ADDR1_DEFERRED
		lappend INDDICT_RECORD CASE_ADDR1_DEFERRED
		dbg debug_ips $curline $DIRDICT_END
		dbg idebug_ips $curline $INDDICT_END
		incr DIRDICT_END 2
                incr INDDICT_END 2
		set CASE_START $DIRDICT_END
		set IND_CASE_START $INDDICT_END
	    } elseif {[string compare $token endcase] == 0} {
		set CASE_LEN [expr $DIRDICT_END - $CASE_START]
		if {$CASE_LEN < 1} {
		    set errorcode 1
		    error \
		    "empty switch-case, file $textName, line $curline, proc $procname"
		}
		# fix up the compiled length entry
		set DIRDICT_RECORD [lreplace $DIRDICT_RECORD $CASE_ADDR1 $CASE_ADDR1 \
		    $CASE_LEN]
		set INDDICT_RECORD [lreplace $INDDICT_RECORD $IND_CASE_ADDR1 $IND_CASE_ADDR1 \
		    $CASE_LEN]
		# leave a slot for case to overwrite with opcode at run time
                # Feb. 2009 add a call here DALE
	        lappend DIRDICT_RECORD $pubop(call)
		lappend DIRDICT_RECORD 0
		incr DIRDICT_END 2
	        lappend INDDICT_RECORD $pubop(call)
		lappend INDDICT_RECORD 0
		incr INDDICT_END 2
		unset CASE_ADDR1
                unset IND_CASE_ADDR1
		unset CASE_LEN
		unset controlStack($controlDepth)
		set isSwitch 0
		incr controlDepth -1
	    } else {
		set errorcode 1
		error \
		"unknown control word '$token', file $textName, line $curline, proc $procname"
	    }
	} elseif {[lsearch -exact $datawords $token] >= 0} {
	    # When inside a proc both variable data (variables, arrays, etc.)
	    # and executable commands go into the dictionary. When outside a
	    # proc the data go into the dictionary, the commands into cmds.

	    # For now when a variable or array is defined inside a
	    # PROC, storage is allocated by first generating a GOTO that
	    # sends control over the dictionary data, and then compiling the
	    # data. We could put this local-static data in a different record
	    # besides DIRDICT_RECORD and then back-patch addresses for references
	    # to these vars. at the end of PROC definition, thereby avoiding
	    # the goto (the storage would be outside the proc), but that's
	    # more trouble than there is time.
	    if {$isInProc} {
		set data_scope $procname
	    } else {
		set data_scope GLOBAL
	    }
	    # We cannot shove DIRDICT_RECORD into DIRDICT_ARRAY or loadcmds & then
	    # shoot targets here at their final dest., because if we are
	    # inside a control structure, DIRDICT_RECORDs has the patch info.
	    set datatype $token
	    stepGetToken token tokarray curtok $tokcount curline
	    if {[string compare $token ""] == 0} {
		set errorcode 1
	        error \
		"missing $datatype name, scope $data_scope, file $textName line $curline"
	    } else {
		stepIsInUse $token $data_scope $textName $curline $isInProc \
		    $loc_const_value $loc_var_def $loc_label_addr
	    }
	    # If stepIsInUse returns then the name is OK to use in this
	    # scope, deal with the data type particulars
	    set dataname $token
	    if {[string compare $datatype constant] == 0} {
		# "constant negthree -3" or "constant subthree negthree"
		set conval [scanNumber token tokarray curtok $tokcount \
		    curline $loc_const_value $datatype $dataname $textName]
		if {$isInProc} {
		    lappend loc_const_value [list $dataname $conval]
		} else {
		    set const_value($dataname) $conval
		}
	    } elseif {[string compare $datatype variable] == 0} {
		# "variable bletch"
		# If inside a proc, note variable def. but don't put it into
		# dictionary until end of proc. Outside of a proc, we
		# initialize it to 0.
		if {$isInProc} {
		    lappend loc_var_def [list $dataname 1 {}]
		} else {
		    set var_addr($dataname) $DATDICT_END
		    # make a label up for the debugger
		    lappend debug_datas [list $dataname $DATDICT_END]
		    lappend DATDICT_ARRAY 0
		    incr DATDICT_END
		}
	    } elseif {[string compare $datatype fwdlabel] == 0} {
		# "fwdlabel foo" added May, 2001, it doesn't generate any code
		# or data, but asserts that a 'label' construct will appear
		# later, so that C switch statement table building code
		# can generate forward jumps within a proc.
		# rather than check for name collisions here, we let
		# the mandatory 'label' construct do it.
		if {$isInProc} {
		    if {[lsearch -exact $loc_label_fwddecls $dataname] < 0} {
			lappend loc_label_fwddecls $dataname
		    }
		} else {
		    set errorcode 1
		    error \
		    "fwdlabel outside of proc, file $textName line $curline"
		}
	    } elseif {[string compare $datatype label] == 0} {
		# "label foo" added May, 2001, it doesn't generate any code
		# or data, but merely keeps track of a dictionary address
		# for a computed goto for a C switch statement
		if {$isInProc} {
		    lappend loc_label_addr [list $dataname $DIRDICT_END]
		    # Treat label like local data for debugger.
		    lappend debug_procs [list "$dataname@@$procname" $DIRDICT_END]
		    lappend idebug_procs [list "$dataname@@$procname" $INDDICT_END]
		    # If there are any forward refs to this label, patch them.
		    if {[info exists unresolved_label_refs($dataname)]} {
			foreach fwdref_tmp $unresolved_label_refs($dataname) {
			    set DIRDICT_RECORD [lreplace $DIRDICT_RECORD	\
				$fwdref_tmp $fwdref_tmp $DIRDICT_END]
			}
			unset unresolved_label_refs($dataname)
		    }
		    set fwdref_tmp [lsearch -exact $loc_label_fwddecls $dataname]
		    # label is now resolved, remove it from fwddecls
		    if {$fwdref_tmp >= 0} {
			set loc_label_fwddecls [concat \
			    [lrange $loc_label_fwddecls 0 \
				[expr $fwdref_tmp - 1]] \
			    [lrange $loc_label_fwddecls \
				[expr $fwdref_tmp + 1] end]]
		    }
		} else {
		    set errorcode 1
		    error \
		    "label outside of proc, file $textName line $curline"
		}
	    } elseif {[string compare $datatype array] == 0} {
		# "array dog 3" or "array dog three"
		set arraydim [scanNumber token tokarray curtok $tokcount \
		    curline $loc_const_value $datatype $dataname $textName]
		if {$arraydim < 1} {
		    set errorcode 1
		    error \
		    "bad dim $arraydim on array $dataname, scope $data_scope, file $textName line $curline"
		}
		if {$isInProc} {
		    lappend loc_var_def [list $dataname $arraydim {}]
		} else {
		    set var_addr($dataname) $DATDICT_END
		    # make a label up for the debugger
		    lappend debug_datas [list $dataname $DATDICT_END]
		    # For now to keep things simple array pumps zeroes into
		    # the dict rather than using the array record.
		    for {set i 0} {$i < $arraydim} {incr i} {
			lappend DATDICT_ARRAY 0
		    }
		    incr DATDICT_END $arraydim
		}
	    } elseif {[string compare $datatype table] == 0} {
		# "table mytable 3 5 7 three 9 11 endtable"
		# May, 2001 table may also hold label or fwdlabel addr.
		set table_tmp {}
		stepGetToken token tokarray curtok $tokcount curline
		while {[string compare $token endtable]} {
		    if {$isInProc && ([linsrch $loc_label_addr $token] >= 0 \
			|| [lsearch -exact $loc_label_fwddecls $token] >= 0)} {
			set valslot [linsrch $loc_label_addr $token]
			if {$valslot >= 0} {
	    		    set conval \
				[lindex [lindex $loc_label_addr $valslot] 1]
			} else {
			    set conval [list undefined-label $token]
			}
		    } else {
		        set conval [convertNumber $token $curline \
			    $loc_const_value table $dataname $textName]
		    }
		    lappend table_tmp $conval
		    stepGetToken token tokarray curtok $tokcount curline
		}
		set table_elements [llength $table_tmp]
		if {$table_elements == 0} {
		    set errorcode 1
		    error \
		    "empty table $dataname, scope $data_scope, file $textName line $curline"
		}
		if {$isInProc} {
		    lappend loc_var_def \
			[list $dataname $table_elements $table_tmp]
		} else {
		    set var_addr($dataname) $DATDICT_END
		    # make a label up for the debugger
		    lappend debug_datas [list $dataname $DATDICT_END]
		    foreach tabele $table_tmp {
			lappend DATDICT_ARRAY $tabele
		    }
		    incr DATDICT_END $table_elements
		}
	    } elseif {[string compare $datatype endtable] == 0} {
		set errorcode 1
		error \
		"unmatched 'endtable', file $textName, line $curline, proc $procname"
	    } else {
		set errorcode 1
		error \
		"unknown data word '$datatype', file $textName, line $curline, proc $procname"
	    }
	} elseif {[string compare $token "@proc"] == 0} {
	    stepGetToken token tokarray curtok $tokcount curline
	    if {[string compare $token ""] == 0} {
		set errorcode 1
	        error \
		"missing @proc name, file $textName line $curline"
	    } elseif {! [info exists procop($token)]} {
		set errorcode 1
		error \
		"no proc '$token' found for @proc, file $textName line $curline"
	    } else {
		lappend DIRDICT_RECORD $privop(variable)
		lappend DIRDICT_RECORD $procop($token)
		lappend INDDICT_RECORD \
                    "$indirectop(variable)$iprocop($token),))"
	        if {$isInProc} {
		    dbg debug_ips $curline $DIRDICT_END
		    dbg idebug_ips $curline $INDDICT_END
		    incr DIRDICT_END 2
                    incr INDDICT_END 1
		    puts stderr \
		    "note: @proc indirection on $token, file $textName line $curline"
		    set procdeep($procname) -1
	        }
	    }
	} elseif {[linsrch $loc_const_value $token] >= 0} {
	    set valslot [linsrch $loc_const_value $token]
	    set conval [lindex [lindex $loc_const_value $valslot] 1]
	    lappend DIRDICT_RECORD $privop(constant)
	    lappend DIRDICT_RECORD $conval
            lappend INDDICT_RECORD "$indirectop(constant)$conval,))"
	    if {$isInProc} {
		dbg debug_ips $curline $DIRDICT_END
		dbg idebug_ips $curline $INDDICT_END
		incr DIRDICT_END 2
                incr INDDICT_END 1
	    }
	} elseif {[linsrch $loc_var_def $token] >= 0} {
	    # local variables can only be found inside a proc,
	    # and their addresses don't get resolved until endproc,
	    # so note a place to be patched later.
	    lappend DIRDICT_RECORD $privop(variable)
	    lappend loc_var_ref($token) [llength $DIRDICT_RECORD] ; # patch addr.
            # The opcode-datum pair go in one slot for IVM.
	    lappend iloc_var_ref($token) [llength $INDDICT_RECORD] ; # patch addr.
	    lappend DIRDICT_RECORD "undefined_var_$token"
	    lappend INDDICT_RECORD "undefined_var_$token"
	    if {$isInProc} {
		dbg debug_ips $curline $DIRDICT_END
		dbg idebug_ips $curline $INDDICT_END
		incr DIRDICT_END 2
                incr INDDICT_END 1
	    }
	} elseif {[linsrch $loc_label_addr $token] >= 0} {
	    # added May, 2001 for 'label' directive, when a label
	    # is used as an instruction, we treat just like a
	    # static variable reference, i.e., we push the address
	    # associated with the label
	    set valslot [linsrch $loc_label_addr $token]
	    set conval [lindex [lindex $loc_label_addr $valslot] 1]
	    # use the 'variable' op code, we don't need a different one
	    lappend DIRDICT_RECORD $privop(variable)
	    lappend DIRDICT_RECORD $conval
	    if {$isInProc} {
		dbg debug_ips $curline $DIRDICT_END
		dbg idebug_ips $curline $INDDICT_END
		incr DIRDICT_END 2
	    } else {
		set errorcode 1
		error \
		"label $token used outside a proc, file $textName line $curline"
	    }
	} elseif {[lsearch -exact $loc_label_fwddecls $token] >= 0} {
	    # added May, 2001 for 'fwdlabel' directive, when a label
	    # had been used within a proc before it is declared,
	    # save an address to patch later. Treatment is identical to seeing
	    # a bound label in the previous case, but we don't have the
	    # label yet.
	    lappend DIRDICT_RECORD $privop(variable)
	    lappend unresolved_label_refs($token) [llength $DIRDICT_RECORD]
	    lappend DIRDICT_RECORD "undefined_label_$token"
	    if {$isInProc} {
		dbg debug_ips $curline $DIRDICT_END
		dbg idebug_ips $curline $INDDICT_END
		incr DIRDICT_END 2
	    } else {
		set errorcode 1
		error \
		"label $token used outside a proc, file $textName line $curline"
	    }
	} elseif {[info exists const_value($token)]} {
	    lappend DIRDICT_RECORD $privop(constant)
	    lappend DIRDICT_RECORD $const_value($token)
            lappend INDDICT_RECORD "$indirectop(constant)$const_value($token),))"
	    if {$isInProc} {
		dbg debug_ips $curline $DIRDICT_END
		dbg idebug_ips $curline $INDDICT_END
		incr DIRDICT_END 2
                inct INDDICT_END 1
	    }
	} elseif {[info exists var_addr($token)]} {
	    lappend DIRDICT_RECORD $privop(variable)
	    lappend DIRDICT_RECORD $var_addr($token)
            lappend INDDICT_RECORD "$indirectop(variable)$var_addr($token),))"
	    if {$isInProc} {
		dbg debug_ips $curline $DIRDICT_END
		dbg idebug_ips $curline $INDDICT_END
		incr DIRDICT_END 2
                incr INDDICT_END 1
	    }
	} elseif {[info exists procop($token)]} {
	    # turn on top bit as flag
            # Revise 2/2009 with explicit call statement.
            set tmpwords 1
            if {! $isSwitch} {
                # Switch table of proc address does not get a call opcode.
	        lappend DIRDICT_RECORD $pubop(call)
	        lappend INDDICT_RECORD "$indirectop(call)$iprocop($token),))"
                set tmpwords 2
            } else {
                lappend INDDICT_RECORD $iprocop($token)
            }
	    lappend DIRDICT_RECORD $procop($token)
	    if {$isInProc} {
		dbg debug_ips $curline $DIRDICT_END
		dbg idebug_ips $curline $INDDICT_END
		incr DIRDICT_END $tmpwords
                incr INDDICT_END 1
		if {[string compare $token $procname] == 0} {
		    puts stderr \
		    "note: compile recursion on $token, file $textName line $curline"
		    set procdeep($procname) -1
		} elseif {$procdeep($token) >= $procdeep($procname)} {
		    set procdeep($procname) [expr $procdeep($token) + 1]
		}
	    }
	} elseif {[info exists pubop($token)]} {
	    lappend DIRDICT_RECORD $pubop($token)
	    lappend INDDICT_RECORD "i$pubop($token)"
	    if {$isInProc} {
		dbg debug_ips $curline $DIRDICT_END
		dbg idebug_ips $curline $INDDICT_END
		incr DIRDICT_END
                incr INDDICT_END
	    }
	} elseif {[stepIsNumber $token conval] \
		|| [stepIsChar $token conval $textName $curline]} {
	    lappend DIRDICT_RECORD $privop(constant)
	    lappend DIRDICT_RECORD $conval
            lappend INDDICT_RECORD "$indirectop(constant)$conval,))"
	    if {$isInProc} {
		dbg debug_ips $curline $DIRDICT_END
		dbg idebug_ips $curline $INDDICT_END
		incr DIRDICT_END 2
                incr INDDICT_END
	    }
	} elseif {[stepIsString $token strval $textName $curline]} {
	    # compile as a table address, put literal string in the table
	    # Enhanced May, 2001 to puts string at end of a proc, rather
	    # than compiling a jump over it.
            # Changed Feb. 2009 to put string in data dictionary.
	    if {$isInProc} {
                # set strval [string trim $strval]
                lappend DATDICT_RECORD "'${strval}'"
                lappend DIRDICT_RECORD $privop(variable)
                lappend DIRDICT_RECORD $DATDICT_END
                lappend INDDICT_RECORD "$indirectop(variable)$DATDICT_END,))"
                incr DATDICT_END
		dbg debug_ips $curline $DIRDICT_END
		dbg idebug_ips $curline $INDDICT_END
		incr DIRDICT_END 2
                incr INDDICT_END
	    } else {
                errorcode = 1
                error "Cannot compile literal string outside a proc"
		# The string goes into the dictionary, even in command mode.
		foreach tmpbyte $strbytes_tmp {
		    lappend DIRDICT_ARRAY $tmpbyte
		}
		# Put the string address push code here, it goes into
		# cmds buffer rather than into dictionary, so don't add
		# the opcode space into DIRDICT_END
		lappend DIRDICT_RECORD $privop(variable)
		lappend DIRDICT_RECORD $DIRDICT_END
		incr DIRDICT_END [llength $strbytes_tmp]
	    }
	} else {
	    set errorcode 1
	    error \
		"unknown symbol $token, file $textName line $curline"
	}
    }
    if {$isInProc} {
	set errorcode 1
	error \
	"unterminated proc $procname, file $textName line $curline"
    }
    if {[llength $DIRDICT_RECORD]} {
        set errorcode 1
	error \
	"Program used outside a proc, file $textName line $curline"
	# records outside of proc are immediate commands
	set loadcmds [concat $loadcmds $DIRDICT_RECORD]
	set DIRDICT_RECORD {}
    }
    # send the dictionary record, then the cmds
    if {[llength $DIRDICT_ARRAY]} {
	# set bigrecord [concat [list 0 [expr [llength $DIRDICT_ARRAY] + 3] \
	    # $DIRDICT_BASE] $DIRDICT_ARRAY]
	set bigrecord $DIRDICT_ARRAY
        set indrecord $INDDICT_ARRAY
    } else {
	set bigrecord {}
        set indrecord {}
    }
    # if {[llength $loadcmds]} {
	# set bigrecord [concat $bigrecord [list 1 \
	    # [expr [llength $loadcmds] + 2]] $loadcmds]
    # }
    set wordcnt [expr $DIRDICT_END - $DIRDICT_BASE]
    if {$MAIN_ADDRESS == -1} {
        set errorcode 1
        error \
        "stepCompile error, no function called 'main'"
    } else {
        set bigrecord [lreplace $bigrecord 0 2                \
            $pubop(call) $MAIN_ADDRESS $pubop(halt)]
        set indrecord [lreplace $indrecord 0 1                \
            "$indirectop(call)$IMAIN_ADDRESS,))" $pubop(halt)]
    }
    if {$wordcnt != [llength $DIRDICT_ARRAY]} {
	set errorcode 1
	error \
	"stepCompile error, generated [llength $DIRDICT_ARRAY] dictionary words, counted $wordcnt"
    } else {
	puts stderr \
	"stepCompile $textName, $wordcnt words to dictionary in this pass, $DIRDICT_END total"
	puts stderr \
	"stepCompile $textName, [llength $loadcmds] words to command buffer in this pass"
	if {$stepMaxDepth < 0} {
	    puts stderr \
	    "stepCompile max thread stack is RECURSIVE or @proc INDIRECT on $stepMaxProc"
	} else {
	    puts stderr \
	    "stepCompile max thread stack is $stepMaxDepth on $stepMaxProc"
	}
    }
    set DIRDICT_LEN $DIRDICT_END
    set DATDICT_LEN $DATDICT_END
    set INDDICT_LEN $INDDICT_END
    if {[string length $loadFile]} {
	set lfile [open $loadFile w]

        # DIRECT THREADED VM LOADER
    puts $lfile "from vm import DirectThreadedVM"
	puts $lfile "def loadvm(vm):"
	puts $lfile "    STEPCODE = \[\]"
	puts $lfile "    STEPDATA = \[\]"
	puts $lfile "    STEPPROCDBG = \[\]"
	puts $lfile "    STEPDATDBG = \[\]"
	puts $lfile "    STEPPCDBG = \[\]"
	puts $lfile "    \# dumping dictionary $DIRDICT_BASE to [expr $DIRDICT_END -1],"
	puts $lfile "    \# [llength $loadcmds] cmds, source $textName"
	set prtbase $DIRDICT_BASE
	foreach w $bigrecord {
	    puts $lfile "    STEPCODE.append($w) \t\# load code record $prtbase"
	    incr prtbase
	}
	set prtbase $DATDICT_BASE
	foreach w $DATDICT_ARRAY {
	    puts $lfile "    STEPDATA.append($w) \t\# load data record $prtbase"
	    incr prtbase
	}
	# foreach w $debug_procs {
	    # puts $lfile "    STEPPROCDBG.append(\'$w\')"
	# }
	foreach w $debug_procs {
            set pname [lindex $w 0]
            set paddr [lindex $w 1]
	        puts $lfile "    STEPPROCDBG.append(\('$pname',$paddr\))"
	}
	foreach w $debug_datas {
            set pname [lindex $w 0]
            set paddr [lindex $w 1]
	        puts $lfile "    STEPDATDBG.append(\('$pname',$paddr\))"
	}
	foreach w $debug_ips {
	    if {[llength $w] > 1} {
		# pairs get braces
	        # puts $lfile "    STEPPCDBG.append(\'$w\')"
                # Python tuples
                set cline [lindex $w 0]
                set caddr [lindex $w 1]
	            puts $lfile "    STEPPCDBG.append(\($cline,$caddr\))"
	    } else {
		puts $lfile "    STEPPCDBG.append('$w')"
	    }
	}
        puts $lfile     \
        "    return((STEPCODE,STEPDATA,STEPPROCDBG,STEPDATDBG,STEPPCDBG))"

        # ININDECT THREADED VM LOADER
	puts $lfile "\n\ndef loadivm(vm):"
	puts $lfile "    ivm = vm"
	puts $lfile "    INSTEPCODE = \[\]"
	puts $lfile "    INSTEPDATA = \[\]"
	puts $lfile "    INSTEPPROCDBG = \[\]"
	puts $lfile "    INSTEPDATDBG = \[\]"
	puts $lfile "    INSTEPPCDBG = \[\]"
	puts $lfile "    \# dumping dictionary $INDDICT_BASE to [expr $INDDICT_END -1],"
	puts $lfile "    \# [llength $loadcmds] cmds, source $textName"
	set prtbase $INDDICT_BASE
	foreach w $indrecord {
	    puts $lfile "    INSTEPCODE.append($w) \t\# load code record $prtbase"
	    incr prtbase
	}
	set prtbase $DATDICT_BASE
	foreach w $DATDICT_ARRAY {
	    puts $lfile "    INSTEPDATA.append($w) \t\# load data record $prtbase"
	    incr prtbase
	}
	# foreach w $idebug_procs {
	    # puts $lfile "    INSTEPPROCDBG.append(\'$w\')"
	# }
	foreach w $idebug_procs {
            set pname [lindex $w 0]
            set paddr [lindex $w 1]
	        puts $lfile "    INSTEPPROCDBG.append(\('$pname',$paddr\))"
	}
	foreach w $debug_datas {
            set pname [lindex $w 0]
            set paddr [lindex $w 1]
	        puts $lfile "    INSTEPDATDBG.append(\('$pname',$paddr\))"
	}
	foreach w $idebug_ips {
	    if {[llength $w] > 1} {
		# pairs get braces
	        # puts $lfile "    INSTEPPCDBG.append(\'$w\')"
                # Python tuples
                set cline [lindex $w 0]
                set caddr [lindex $w 1]
	            puts $lfile "    INSTEPPCDBG.append(\($cline,$caddr\))"
	    } else {
		puts $lfile "    INSTEPPCDBG.append('$w')"
	    }
	}
        puts $lfile     \
        "    return((INSTEPCODE,INSTEPDATA,INSTEPPROCDBG,INSTEPDATDBG,INSTEPPCDBG))"
	close $lfile
    }
    return $bigrecord
}

# stepTokenize added 1/99 to break tokens into an array instead
# of a list. D. Parson
proc stepTokenize {text tarray tcount} {
    upvar $tarray tokarray $tcount tokcount
    foreach line [split $text "\n"] {
        foreach tok [split $line " \t"] {
	    set tokarray($tokcount) $tok
	    incr tokcount
	}
	set tokarray($tokcount) "\n"
	incr tokcount
    }
}

proc stepLoad {loadfile} {
    source $loadfile
    return $STEPCODE
}

proc stepCompileStartup {errc} {
    upvar $errc errorcode
    global stepCompileFirstTime pubop privop env keywords SCASE SLIMIT
    global pubtext privtext DIRDICT_LEN
    global DBG_LINENO
    set DBG_LINENO -1	; # start tracking debugger symbol info from scratch
    if {! $stepCompileFirstTime} {
	return
    }
    stepClobberDict
    set DIRDICT_LEN 0
    # pump up opcode-to-name mappings
    foreach txt [array names pubop] {
	set pubtext($pubop($txt)) $txt
    }
    foreach txt [array names privop] {
	set privtext($privop($txt)) $txt
    }
    # If "stepextr.tcl" then source it & call stepExtras.
    # HERE ARE THE REQUIREMENTS FOR "PROC stepExtras":
    # Called: stepExtras(SCASE), where $SCASE is the first opcode
    # available for extension primitives.
    # It returns a list consisting of ordered-pair-lists
    # of operation-text and op-code.
    #
    # stepCompileStartup pumps these added primitives into pubop & privop
    if {[file exists stepextr.tcl]} {
	set xfile stepextr.tcl
    } elseif {[info exists env(STEPHOME)] \
	    && [file exists [file join $env(STEPHOME) stepextr.tcl]]} {
	set xfile [file join $env(STEPHOME) stepextr.tcl]
    } elseif {[info exists env(LUXHOME)] \
	    && [file exists [file join $env(LUXHOME) lib/stepextr.tcl]]} {
	set xfile [file join $env(LUXHOME) lib/stepextr.tcl]
    } elseif {[info exists env(HOME)] \
	    && [file exists [file join $env(HOME) stepextr.tcl]]} {
	set xfile [file join $env(HOME) stepextr.tcl]
    } else {
	set xfile ""
    }
    if {[string length $xfile]} {
	source $xfile
	set xpub [stepExtras $SCASE]
	foreach xtra_pair $xpub {
	    set xtra_text [lindex $xtra_pair 0]
	    set xtra_num [lindex $xtra_pair 1]
	    if {[lsearch -exact $keywords $xtra_text] >= 0 \
		    || [info exists privop($xtra_text)] \
		    || [stepIsLiteral $xtra_text $xfile -1]} {
		puts stderr \
		"error: stepExtras attempted redefinition of '$xtra_text'"
		puts stderr "'$xtra_text' RESERVED, see file $xfile"
		set errorcode 1
		continue
	    }
	    if {$xtra_num < $SCASE || $xtra_num > $SLIMIT} {
		puts stderr \
		"error: stepExtras illegal opcode '$xtra_num'"
		puts stderr \
		"operation '$xtra_text' ignored, see file $xfile"
		set errorcode 1
		continue
	    }
	    if {[info exists pubtext($xtra_num)]} {
		puts -nonewline stderr \
		"error: stepExtras tried to reassign opcode '$xtra_num'"
		puts stderr \
		"from '$pubtext($xtra_num)' to '$xtra_text', ignored"
		puts stderr "see file $xfile"
		set errorcode 1
		continue
	    }
	    if {[info exists privtext($xtra_num)]} {
		puts -nonewline stderr \
		"error: stepExtras tried to reassign opcode '$xtra_num'"
		puts stderr \
		"from '$privtext($xtra_num)' to '$xtra_text', ignored"
		puts stderr "see file $xfile"
		set errorcode 1
		continue
	    }
	    if {[info exists pubop($xtra_text)]} {
		# This one is OK, warn about it.
		puts -nonewline stderr \
		"warning: reassigning operation '$xtra_text' from opcode "
		puts stderr "'$pubop($xtra_text)' to '$xtra_num'"
		puts stderr "see file $xfile"
	    }
	    set pubop($xtra_text) $xtra_num
	    set pubtext($xtra_num) $xtra_text
	}
    }
    set stepCompileFirstTime 0
}

# compile has appendmode of 0 (i.e., create new load), clobber old defs.
proc stepClobberDict {} {
    global procop		; # text->opcode
    global iprocop		; # text->opcode
    global procdeep		; # text->depth
    global const_value		; # constant value
    global var_addr		; # variable address
    global DIRDICT_LEN	; # next free spot in dictionary
    global stepMaxDepth		; # depth of deepest proc.
    global stepMaxProc		; # name of the deepest proc
    foreach table {procop iprocop procdeep const_value var_addr} {
	foreach ele [array names $table] {
	    unset ${table}($ele)
	}
    }
    set DIRDICT_LEN 0
    set stepMaxDepth 0
    set stepMaxProc ""
}

# In order to keep run-time behavior predictable, nothing but public primitives
# may be redefined, and then only once.
proc stepIsReserved {token file lineno newuse delete} {
    global keywords privop pubob
    global const_value var_addr procop
    if {[lsearch -exact $keywords $token] >= 0 \
	    || [info exists privop($token)] \
	    || [stepIsLiteral $token $file $lineno]} {
	error \
	"attempted redefinition of '$token' in $file, line $lineno"
    } elseif {[string first @@ $token] >= 0} {
	error \
	"'@@' in definition of '$token' in $file, line $lineno"
    } elseif {[info exists procop($token)]} {
	error \
	"attempted redefinition of proc '$token' as $newuse in $file, line $lineno"
    } elseif {[info exists const_value($token)]} {
	error \
	"redefinition of constant '$token' as $newuse in $file, line $lineno"
    } elseif {[info exists var_addr($token)]} {
	error \
	"redefinition of variable '$token' as $newuse in $file, line $lineno"
    } elseif {[info exists pubop($token)]} {
	puts stderr \
	"warning: redefinition of op '$token' as $newuse in $file, line $lineno"
	if {$delete} {
	    unset pubop($token)
	}
    }
}

# stepIsInUse is close to stepIsReserved but not identical, it allows
# local redefs. of primitives, procs, constants and arrays
proc stepIsInUse {token scope file lineno isproc constpairs varpairs
    labelpairs} {
    global keywords privop pubob
    global const_value var_addr procop
    if {[lsearch -exact $keywords $token] >= 0 \
	    || [info exists privop($token)] \
	    || [stepIsLiteral $token $file $lineno]} {
	error \
	"attempted redefinition of '$token' in $scope, file $file, line $lineno"
    } elseif {[string first @@ $token] >= 0} {
	error \
	"'@@' in definition of '$token' in $scope, file $file, line $lineno"
    } elseif {$isproc && ([linsrch $constpairs $token] >= 0 \
	    || [linsrch $varpairs $token] >= 0	\
	    || [linsrch $labelpairs $token] >= 0)} {
	# locals may not be redefined
puts stderr "failed: $token $constpairs $varpairs $labelpairs"
	error \
	"attempted redefinition of '$token' in $scope, file $file, line $lineno"

    } elseif {[info exists procop($token)] \
	    || [info exists const_value($token)] \
	    || [info exists var_addr($token)] \
	    || [info exists pubop($token)]} {
	# globals may be redefined only by locals
	if {$isproc} {
	    puts stderr \
	    "compile warning: redef. of $token in $scope, file $file, line $lineno"
	} else {
	    error \
	    "attempted redefinition of '$token' in $scope, file $file, line $lineno"
	}
    }
}

proc stepIsLiteral {token file lineno} {
    return [expr [stepIsNumber $token res] \
	|| [stepIsString $token res $file $lineno] \
	|| [stepIsChar $token res $file $lineno]]
}

proc stepIsNumber {token res} {
    upvar $res result
    if {[regexp {^\-?[1-9][0-9]*$} $token] \
	    || [regexp {^\-?0x[0-9a-fA-F]+$} $token] \
	    || [regexp {^\-?0[0-7]*$} $token]} {
	set result [expr $token]
	return 1
    } else {
	return 0
    }
}

proc stepIsChar {token res file lineno} {
    upvar $res result
    global errorcode
    if {[regexp {^'(.)'$} $token all letter]} {
	scan $letter %c result
	return 1
    } elseif {[regexp {^'\\([0-7]+)'$} $token all number]} {
	# above pattern doesn't require a leading 0 for octal,
	# but expr does
	set result [expr "0$number"]
	if {$result > 0xff} {
	    puts stderr "excess character constant `$token` in $file, line $lineno"
	    set errorcode 1
	    return 0
	}
	return 1
    } elseif {[regexp {'} $token]} {
	puts stderr "bad character constant `$token` in $file, line $lineno"
	set errorcode 1
	return 0
    } else {
	return 0
    }
}

proc stepIsString {token res file lineno} {
    upvar $res result
    global errorcode
    if {[regexp {^".*"$} $token]} {
	set result ""
	set len [expr [string length $token] - 1]
	# strip off the quotes
	for {set i 1} {$i < $len} {incr i} {
	    set c [string index $token $i]
	    if {[string compare $c "\\"] == 0} {
		incr i
		set c [string index $token $i]
		if {[string compare $c n] == 0} {
		    set result "$result\n"
		} elseif {[string compare $c t] == 0} {
		    set result "$result\t"
		} else {
		    set result "$result$c"
		}
	    } else {
		set result "$result$c"
	    }
	}
	return 1
    } elseif {[regexp {"} $token]} {
	puts stderr "bad quoted string '$token' in $file, line $lineno"
	set errorcode 1
	return 0
    } else {
	return 0
    }
}

# scanNumber has to find either a numeric literal or a numeric constant
proc scanNumber {tokenname tokenarray curtoken tokencount linectr \
    constpairs datatype dataname filename} {
    upvar $tokenname token $tokenarray tokarray $linectr curline
    upvar $curtoken curtok
    stepGetToken token tokarray curtok $tokencount curline
    return [convertNumber $token $curline $constpairs $datatype $dataname \
	$filename]
}

# convertNumber has to convert either a numeric literal or a numeric constant
proc convertNumber {token curline constpairs datatype dataname filename} {
    global const_value
    if {[stepIsNumber $token val]} {
	return $val
    } elseif {[stepIsChar $token val $filename $curline]} {
	return $val
    } elseif {[linsrch $constpairs $token] >= 0} {
	set slot [linsrch $constpairs $token]
	return [lindex [lindex $constpairs $slot] 1]
    } elseif {[info exists const_value($token)]} {
	return $const_value($token)
    }
    error "compile, number expected, saw '$token' for $datatype $dataname, file $filename, line $curline"
}

proc linsrch {plist key} {
    set ix 0
    foreach r $plist {
	if {[string compare $key [lindex $r 0]] == 0} {
	    return $ix
	}
	incr ix
    }
    return -1
}

proc stepGetToken {tokenname tokenarray curtoken tokencount linectr} {
    upvar $tokenname token $tokenarray tokarray $linectr curline
    upvar $curtoken curtok
    set instring 0
    set intoolbox 0
    set incomment 0
    set aggstring ""
    while {$curtok < $tokencount} {
        set token $tokarray($curtok)
	incr curtok
	if {[string compare $token "\n"] == 0} {
	    set incomment 0
	    incr curline
	    if {$instring} {
		# premature \n, leave string unterminated
		set token $aggstring
		return
	    } elseif {$intoolbox} {
		error "unterminate \[\] Tcl escape at line $curline"
	    }
	    continue
	}
	if {[string compare $token "//"] == 0 && (! $instring) \
		&& (! $intoolbox)} {
	    set incomment 1
	    continue
	}
	if {$incomment} {
	    continue
	}
	if {[string compare $token ""] == 0} {
	    if {$instring || $intoolbox} {
		# a "quoted string" collects spaces
		set aggstring "$aggstring "
	    }
	    continue
	}
	if {$instring} {
	    if {[regexp {[^\\]"$} $token] || [regexp {^"$} $token]} {
		# terminating quote
		set token "$aggstring $token"
		return
	    } else {
		set aggstring "$aggstring $token"
		continue
	    }
	} elseif {$intoolbox} {
	    if {[string compare [string range $token end end] "\]"] == 0} {
		set prebracket [string range $token 0 \
		    [expr [string length $token] - 2]]
		set token "$aggstring $prebracket"
		set token [uplevel #0 $token]
		if {[regexp {^[ 	]*$} $token]} {
		    set intoolbox 0
		    continue
		}
		return
	    } else {
		set aggstring "$aggstring $token"
		continue
	    }
	} elseif {[regexp {^".*"$} $token]} {
	    # a spaceless quoted string
	    return
	} elseif {[regexp {^"} $token]} {
	    set aggstring $token
	    set instring 1
	    continue
	} elseif {[string compare [string range $token 0 0] "\["] == 0 \
		&& [string compare [string range $token end end] "\]"] == 0} {
	    set prebracket [string range $token 1 \
		[expr [string length $token] - 2]]
	    set token [uplevel #0 $prebracket]
	    if {[regexp {^[ 	]*$} $token]} {
		set intoolbox 0
		continue
	    }
	    return
	} elseif {[string compare [string range $token 0 0] "\["] == 0} {
	    set aggstring [string range $token 1 end]
	    set intoolbox 1
	    continue
	} else {
	    return
	}
    }
    if {$instring} {
	set token $aggstring
    } elseif {$intoolbox} {
	error "unterminate \[\] Tcl escape at line $curline"
    } else {
	set token ""
    }
}

proc step_abs_path {fname} {
    # find absolute path for $fname
    set current [pwd]
    set remote [file dirname $fname]
    set bottom [file tail $fname]
    cd $remote
    set retval [file join [pwd] $bottom]
    cd $current
    return $retval
}

# dbg record a {line# ip} pair every time the line number changes
proc dbg {dbglist lineno iploc} {
    upvar $dbglist pairlist
    global DBG_LINENO
    if {$lineno > $DBG_LINENO} {
	set DBG_LINENO $lineno
	lappend pairlist [list $lineno $iploc]
    }
}

# zaparray equivalent to "array unset" in newer Tcls -- unsets whole array
proc zaparray {arrayname} {
    upvar $arrayname ary
    foreach ele [array names ary] {
	unset ary($ele)
    }
}

# It would be nice to avoid global variables.
# Unfortunately if we make the compiler tables local,
# stepCompile would have to re-initialize them each time
# it is called. And so, they are globals.

# ctrlwords are reserved control construct words
set ctrlwords {return if then else endif while do endwhile \
    dountil until enduntil break continue switch case endcase}

# data words define symbolic data & dictionary entries
# label added May, 2001
set datawords {constant variable array table endtable label fwdlabel}

# keywords holds the full set of defining words
set keywords [concat {proc endproc @proc} $ctrlwords $datawords]

# STEP programmers get only public_opcodes, the STEP compiler
# needs the private_opcodes for control constructs
# and constant/variable run-time access

# ARRAYS pubtext and privtext to do the INVERSE mappings construct
# in proc stepCompileStartup
# FEB. 2009 privop() and pubop() converted from int values to
# object-bound method names for Python
# JAN. 2012 changed bound op codes such as vm.STEP_BPT to unbound op codes
# such as DirectThreadedVM.STEP_BPT.

set privop(bpt) DirectThreadedVM.STEP_BPT
set pubop(+) DirectThreadedVM.STEP_ADD
set pubop(-) DirectThreadedVM.STEP_SUB
set pubop(*) DirectThreadedVM.STEP_MULT
set pubop(/) DirectThreadedVM.STEP_DIV
set pubop(%) DirectThreadedVM.STEP_MOD
set pubop(&) DirectThreadedVM.STEP_BITAND
set pubop(|) DirectThreadedVM.STEP_BITOR
set pubop(^) DirectThreadedVM.STEP_BITXOR
set pubop(<<) DirectThreadedVM.STEP_SHL
set pubop(>>) DirectThreadedVM.STEP_SHR
set pubop(&&) DirectThreadedVM.STEP_LOGAND
set pubop(||) DirectThreadedVM.STEP_LOGOR
set pubop(minus) DirectThreadedVM.STEP_MINUS
set pubop(~) DirectThreadedVM.STEP_COMPLEMENT
set pubop(!) DirectThreadedVM.STEP_NOT
set pubop(==) DirectThreadedVM.STEP_EQ
set pubop(!=) DirectThreadedVM.STEP_NEQ
set pubop(<) DirectThreadedVM.STEP_LT
set pubop(>) DirectThreadedVM.STEP_GT
set pubop(<=) DirectThreadedVM.STEP_LE
set pubop(>=) DirectThreadedVM.STEP_GE
set pubop(0==) DirectThreadedVM.STEP_ZEQ
set pubop(0!=) DirectThreadedVM.STEP_ZNEQ
set pubop(0<) DirectThreadedVM.STEP_ZLT
set pubop(0<=) DirectThreadedVM.STEP_ZLE
set pubop(0>) DirectThreadedVM.STEP_ZGT
set pubop(0>=) DirectThreadedVM.STEP_ZGE
set pubop(1+) DirectThreadedVM.STEP_ADD1
set pubop(1-) DirectThreadedVM.STEP_SUB1
set pubop(2+) DirectThreadedVM.STEP_ADD2
set pubop(2-) DirectThreadedVM.STEP_SUB2
set pubop(2*) DirectThreadedVM.STEP_MULT2
set pubop(2/) DirectThreadedVM.STEP_DIV2
set pubop(1<<) DirectThreadedVM.STEP_SHL1
set pubop(1>>) DirectThreadedVM.STEP_SHR1
set pubop(dup) DirectThreadedVM.STEP_DUP
set pubop(dup2) DirectThreadedVM.STEP_DUP2
set pubop(swap) DirectThreadedVM.STEP_SWAP
set pubop(swap2) DirectThreadedVM.STEP_SWAP2
set pubop(over) DirectThreadedVM.STEP_OVER
set pubop(over2) DirectThreadedVM.STEP_OVER2
set pubop(drop) DirectThreadedVM.STEP_DROP
set pubop(drop2) DirectThreadedVM.STEP_DROP2
set pubop(sign) DirectThreadedVM.STEP_SIGN
set pubop(abs) DirectThreadedVM.STEP_ABS
set pubop(sizeof_word) DirectThreadedVM.STEP_SIZEOF
set pubop(rrot) DirectThreadedVM.STEP_RROT
set pubop(rrot16) DirectThreadedVM.STEP_RROT16
set pubop(lrot) DirectThreadedVM.STEP_LROT
set pubop(lrot16) DirectThreadedVM.STEP_LROT16
set privop(constant) DirectThreadedVM.STEP_CONST
set privop(variable) DirectThreadedVM.STEP_VAR
set privop(array) DirectThreadedVM.STEP_ARRAY
set pubop(@f) DirectThreadedVM.STEP_FETCH
set pubop(@s) DirectThreadedVM.STEP_STORE
set privop(goto) DirectThreadedVM.STEP_GOTO
set privop(goto0) DirectThreadedVM.STEP_GOTO0
set privop(gotox) DirectThreadedVM.STEP_GOTOX
set privop(return) DirectThreadedVM.STEP_RETURN
set pubop(pause) DirectThreadedVM.STEP_PAUSE
set pubop(halt) DirectThreadedVM.STEP_HALT
set pubop(prints) DirectThreadedVM.STEP_PRINTS
set pubop(printi) DirectThreadedVM.STEP_PRINTI
set pubop(crlf) DirectThreadedVM.STEP_CRLF
set pubop(decimal) DirectThreadedVM.STEP_DECIMAL
set pubop(hex) DirectThreadedVM.STEP_HEX
set pubop(octal) DirectThreadedVM.STEP_OCTAL
set pubop(inp) DirectThreadedVM.STEP_INP
set pubop(outp) DirectThreadedVM.STEP_OUTP
set pubop(inpw) DirectThreadedVM.STEP_INPW
set pubop(outpw) DirectThreadedVM.STEP_OUTPW
set pubop(ds_depth) DirectThreadedVM.STEP_DS_DEPTH
set pubop(ts_depth) DirectThreadedVM.STEP_TS_DEPTH
set pubop(code_dict_len) DirectThreadedVM.STEP_CODE_DICT_LEN
set pubop(data_dict_len) DirectThreadedVM.STEP_DATA_DICT_LEN
set pubop(dupi) DirectThreadedVM.STEP_DUP_I
set pubop(noop) DirectThreadedVM.STEP_NOOP
set pubop(@call) DirectThreadedVM.STEP_CALL
set pubop(swapi) DirectThreadedVM.STEP_SWAP_I
set pubop(dropi) DirectThreadedVM.STEP_DROP_I
set pubop(@ixs) DirectThreadedVM.STEP_IX_STORE
set pubop(gotoaddr) DirectThreadedVM.STEP_GOTO_ADDR
set pubop(call) DirectThreadedVM.STEP_CALL_SECONDARY
set indirectop(constant) "ivm.intern(ivm.incomplete_STEP_CONST, ("
set indirectop(variable) "ivm.intern(ivm.incomplete_STEP_VAR, ("
set indirectop(array) "ivm.intern(ivm.incomplete_STEP_ARRAY, ("
set indirectop(goto) "ivm.intern(ivm.incomplete_STEP_GOTO, ("
set indirectop(goto0) "ivm.intern(ivm.incomplete_STEP_GOTO0, ("
set indirectop(call) "ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, ("

# SCASE increased from 79 to 83 May, 2001 for C compiler.
# SCASE increased from 83 to 84 Feb., 2009 for Python VM.
set SCASE			84 ; # extra opcodes must start here
set SLIMIT			32767 ; # max primitive opcode

