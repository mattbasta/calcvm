from vm import DirectThreadedVM
def loadvm(vm):
    STEPCODE = []
    STEPDATA = []
    STEPPROCDBG = []
    STEPDATDBG = []
    STEPPCDBG = []
    # dumping dictionary 0 to 172,
    # 0 cmds, source selsort.stp
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 0
    STEPCODE.append(142) 	# load code record 1
    STEPCODE.append(DirectThreadedVM.STEP_HALT) 	# load code record 2
    STEPCODE.append(DirectThreadedVM.STEP_SWAP) 	# load code record 3
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 4
    STEPCODE.append(0) 	# load code record 5
    STEPCODE.append(DirectThreadedVM.STEP_STORE) 	# load code record 6
    STEPCODE.append(DirectThreadedVM.STEP_SUB1) 	# load code record 7
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 8
    STEPCODE.append(0) 	# load code record 9
    STEPCODE.append(DirectThreadedVM.STEP_OVER) 	# load code record 10
    STEPCODE.append(DirectThreadedVM.STEP_OVER) 	# load code record 11
    STEPCODE.append(DirectThreadedVM.STEP_GT) 	# load code record 12
    STEPCODE.append(DirectThreadedVM.STEP_GOTO0) 	# load code record 13
    STEPCODE.append(65) 	# load code record 14
    STEPCODE.append(DirectThreadedVM.STEP_OVER) 	# load code record 15
    STEPCODE.append(DirectThreadedVM.STEP_OVER) 	# load code record 16
    STEPCODE.append(DirectThreadedVM.STEP_ADD1) 	# load code record 17
    STEPCODE.append(DirectThreadedVM.STEP_OVER) 	# load code record 18
    STEPCODE.append(DirectThreadedVM.STEP_OVER) 	# load code record 19
    STEPCODE.append(DirectThreadedVM.STEP_GE) 	# load code record 20
    STEPCODE.append(DirectThreadedVM.STEP_GOTO0) 	# load code record 21
    STEPCODE.append(61) 	# load code record 22
    STEPCODE.append(DirectThreadedVM.STEP_OVER2) 	# load code record 23
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 24
    STEPCODE.append(0) 	# load code record 25
    STEPCODE.append(DirectThreadedVM.STEP_FETCH) 	# load code record 26
    STEPCODE.append(DirectThreadedVM.STEP_ADD) 	# load code record 27
    STEPCODE.append(DirectThreadedVM.STEP_FETCH) 	# load code record 28
    STEPCODE.append(DirectThreadedVM.STEP_OVER) 	# load code record 29
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 30
    STEPCODE.append(0) 	# load code record 31
    STEPCODE.append(DirectThreadedVM.STEP_FETCH) 	# load code record 32
    STEPCODE.append(DirectThreadedVM.STEP_ADD) 	# load code record 33
    STEPCODE.append(DirectThreadedVM.STEP_FETCH) 	# load code record 34
    STEPCODE.append(DirectThreadedVM.STEP_OVER) 	# load code record 35
    STEPCODE.append(DirectThreadedVM.STEP_OVER) 	# load code record 36
    STEPCODE.append(DirectThreadedVM.STEP_GT) 	# load code record 37
    STEPCODE.append(DirectThreadedVM.STEP_GOTO0) 	# load code record 38
    STEPCODE.append(57) 	# load code record 39
    STEPCODE.append(DirectThreadedVM.STEP_SWAP) 	# load code record 40
    STEPCODE.append(DirectThreadedVM.STEP_OVER2) 	# load code record 41
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 42
    STEPCODE.append(0) 	# load code record 43
    STEPCODE.append(DirectThreadedVM.STEP_FETCH) 	# load code record 44
    STEPCODE.append(DirectThreadedVM.STEP_ADD) 	# load code record 45
    STEPCODE.append(DirectThreadedVM.STEP_STORE) 	# load code record 46
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 47
    STEPCODE.append(3) 	# load code record 48
    STEPCODE.append(DirectThreadedVM.STEP_DUP_I) 	# load code record 49
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 50
    STEPCODE.append(0) 	# load code record 51
    STEPCODE.append(DirectThreadedVM.STEP_FETCH) 	# load code record 52
    STEPCODE.append(DirectThreadedVM.STEP_ADD) 	# load code record 53
    STEPCODE.append(DirectThreadedVM.STEP_STORE) 	# load code record 54
    STEPCODE.append(DirectThreadedVM.STEP_GOTO) 	# load code record 55
    STEPCODE.append(58) 	# load code record 56
    STEPCODE.append(DirectThreadedVM.STEP_DROP2) 	# load code record 57
    STEPCODE.append(DirectThreadedVM.STEP_ADD1) 	# load code record 58
    STEPCODE.append(DirectThreadedVM.STEP_GOTO) 	# load code record 59
    STEPCODE.append(18) 	# load code record 60
    STEPCODE.append(DirectThreadedVM.STEP_DROP2) 	# load code record 61
    STEPCODE.append(DirectThreadedVM.STEP_ADD1) 	# load code record 62
    STEPCODE.append(DirectThreadedVM.STEP_GOTO) 	# load code record 63
    STEPCODE.append(10) 	# load code record 64
    STEPCODE.append(DirectThreadedVM.STEP_DROP2) 	# load code record 65
    STEPCODE.append(DirectThreadedVM.STEP_RETURN) 	# load code record 66
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 67
    STEPCODE.append(0) 	# load code record 68
    STEPCODE.append(DirectThreadedVM.STEP_OVER) 	# load code record 69
    STEPCODE.append(DirectThreadedVM.STEP_OVER) 	# load code record 70
    STEPCODE.append(DirectThreadedVM.STEP_GT) 	# load code record 71
    STEPCODE.append(DirectThreadedVM.STEP_GOTO0) 	# load code record 72
    STEPCODE.append(83) 	# load code record 73
    STEPCODE.append(DirectThreadedVM.STEP_OVER2) 	# load code record 74
    STEPCODE.append(DirectThreadedVM.STEP_OVER) 	# load code record 75
    STEPCODE.append(DirectThreadedVM.STEP_ADD) 	# load code record 76
    STEPCODE.append(DirectThreadedVM.STEP_FETCH) 	# load code record 77
    STEPCODE.append(DirectThreadedVM.STEP_PRINTI) 	# load code record 78
    STEPCODE.append(DirectThreadedVM.STEP_CRLF) 	# load code record 79
    STEPCODE.append(DirectThreadedVM.STEP_ADD1) 	# load code record 80
    STEPCODE.append(DirectThreadedVM.STEP_GOTO) 	# load code record 81
    STEPCODE.append(69) 	# load code record 82
    STEPCODE.append(DirectThreadedVM.STEP_DROP2) 	# load code record 83
    STEPCODE.append(DirectThreadedVM.STEP_DROP) 	# load code record 84
    STEPCODE.append(DirectThreadedVM.STEP_RETURN) 	# load code record 85
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 86
    STEPCODE.append(3) 	# load code record 87
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 88
    STEPCODE.append(41) 	# load code record 89
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 90
    STEPCODE.append(DirectThreadedVM.STEP_DUP) 	# load code record 91
    STEPCODE.append(DirectThreadedVM.STEP_PRINTI) 	# load code record 92
    STEPCODE.append(DirectThreadedVM.STEP_CRLF) 	# load code record 93
    STEPCODE.append(DirectThreadedVM.STEP_SUB1) 	# load code record 94
    STEPCODE.append(DirectThreadedVM.STEP_DUP) 	# load code record 95
    STEPCODE.append(DirectThreadedVM.STEP_ZEQ) 	# load code record 96
    STEPCODE.append(DirectThreadedVM.STEP_GOTO0) 	# load code record 97
    STEPCODE.append(106) 	# load code record 98
    STEPCODE.append(DirectThreadedVM.STEP_DROP) 	# load code record 99
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 100
    STEPCODE.append(1) 	# load code record 101
    STEPCODE.append(DirectThreadedVM.STEP_GOTO) 	# load code record 102
    STEPCODE.append(112) 	# load code record 103
    STEPCODE.append(DirectThreadedVM.STEP_GOTO) 	# load code record 104
    STEPCODE.append(108) 	# load code record 105
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 106
    STEPCODE.append(0) 	# load code record 107
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 108
    STEPCODE.append(42) 	# load code record 109
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 110
    STEPCODE.append(DirectThreadedVM.STEP_CRLF) 	# load code record 111
    STEPCODE.append(DirectThreadedVM.STEP_GOTO0) 	# load code record 112
    STEPCODE.append(88) 	# load code record 113
    STEPCODE.append(DirectThreadedVM.STEP_DROP) 	# load code record 114
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 115
    STEPCODE.append(6) 	# load code record 116
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 117
    STEPCODE.append(43) 	# load code record 118
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 119
    STEPCODE.append(DirectThreadedVM.STEP_DUP) 	# load code record 120
    STEPCODE.append(DirectThreadedVM.STEP_PRINTI) 	# load code record 121
    STEPCODE.append(DirectThreadedVM.STEP_CRLF) 	# load code record 122
    STEPCODE.append(DirectThreadedVM.STEP_SUB1) 	# load code record 123
    STEPCODE.append(DirectThreadedVM.STEP_DUP) 	# load code record 124
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 125
    STEPCODE.append(3) 	# load code record 126
    STEPCODE.append(DirectThreadedVM.STEP_EQ) 	# load code record 127
    STEPCODE.append(DirectThreadedVM.STEP_GOTO0) 	# load code record 128
    STEPCODE.append(133) 	# load code record 129
    STEPCODE.append(DirectThreadedVM.STEP_PAUSE) 	# load code record 130
    STEPCODE.append(DirectThreadedVM.STEP_GOTO) 	# load code record 131
    STEPCODE.append(141) 	# load code record 132
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 133
    STEPCODE.append(44) 	# load code record 134
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 135
    STEPCODE.append(DirectThreadedVM.STEP_CRLF) 	# load code record 136
    STEPCODE.append(DirectThreadedVM.STEP_DUP) 	# load code record 137
    STEPCODE.append(DirectThreadedVM.STEP_ZEQ) 	# load code record 138
    STEPCODE.append(DirectThreadedVM.STEP_GOTO0) 	# load code record 139
    STEPCODE.append(117) 	# load code record 140
    STEPCODE.append(DirectThreadedVM.STEP_RETURN) 	# load code record 141
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 142
    STEPCODE.append(45) 	# load code record 143
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 144
    STEPCODE.append(DirectThreadedVM.STEP_CRLF) 	# load code record 145
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 146
    STEPCODE.append(1) 	# load code record 147
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 148
    STEPCODE.append(8) 	# load code record 149
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 150
    STEPCODE.append(67) 	# load code record 151
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 152
    STEPCODE.append(46) 	# load code record 153
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 154
    STEPCODE.append(DirectThreadedVM.STEP_CRLF) 	# load code record 155
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 156
    STEPCODE.append(1) 	# load code record 157
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 158
    STEPCODE.append(8) 	# load code record 159
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 160
    STEPCODE.append(3) 	# load code record 161
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 162
    STEPCODE.append(1) 	# load code record 163
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 164
    STEPCODE.append(8) 	# load code record 165
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 166
    STEPCODE.append(67) 	# load code record 167
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 168
    STEPCODE.append(86) 	# load code record 169
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 170
    STEPCODE.append(0) 	# load code record 171
    STEPCODE.append(DirectThreadedVM.STEP_RETURN) 	# load code record 172
    STEPDATA.append(0) 	# load data record 0
    STEPDATA.append(45) 	# load data record 1
    STEPDATA.append(27) 	# load data record 2
    STEPDATA.append(-100) 	# load data record 3
    STEPDATA.append(100) 	# load data record 4
    STEPDATA.append(0) 	# load data record 5
    STEPDATA.append(-1) 	# load data record 6
    STEPDATA.append(1) 	# load data record 7
    STEPDATA.append(5) 	# load data record 8
    STEPDATA.append(0) 	# load data record 9
    STEPDATA.append(0) 	# load data record 10
    STEPDATA.append(0) 	# load data record 11
    STEPDATA.append(0) 	# load data record 12
    STEPDATA.append(0) 	# load data record 13
    STEPDATA.append(0) 	# load data record 14
    STEPDATA.append(0) 	# load data record 15
    STEPDATA.append(0) 	# load data record 16
    STEPDATA.append(0) 	# load data record 17
    STEPDATA.append(0) 	# load data record 18
    STEPDATA.append(0) 	# load data record 19
    STEPDATA.append(0) 	# load data record 20
    STEPDATA.append(0) 	# load data record 21
    STEPDATA.append(0) 	# load data record 22
    STEPDATA.append(0) 	# load data record 23
    STEPDATA.append(0) 	# load data record 24
    STEPDATA.append(0) 	# load data record 25
    STEPDATA.append(0) 	# load data record 26
    STEPDATA.append(0) 	# load data record 27
    STEPDATA.append(0) 	# load data record 28
    STEPDATA.append(0) 	# load data record 29
    STEPDATA.append(0) 	# load data record 30
    STEPDATA.append(0) 	# load data record 31
    STEPDATA.append(0) 	# load data record 32
    STEPDATA.append(0) 	# load data record 33
    STEPDATA.append(0) 	# load data record 34
    STEPDATA.append(0) 	# load data record 35
    STEPDATA.append(0) 	# load data record 36
    STEPDATA.append(0) 	# load data record 37
    STEPDATA.append(0) 	# load data record 38
    STEPDATA.append(0) 	# load data record 39
    STEPDATA.append(0) 	# load data record 40
    STEPDATA.append('testing until and if with no else and continue ') 	# load data record 41
    STEPDATA.append('bypassed the continue') 	# load data record 42
    STEPDATA.append('testing until and if with no else and break ') 	# load data record 43
    STEPDATA.append('bypassed the break') 	# load data record 44
    STEPDATA.append('table1 before the sort') 	# load data record 45
    STEPDATA.append('table1 after the sort') 	# load data record 46
    STEPDATA.append(0) 	# load data record 47
    STEPDATA.append(0) 	# load data record 48
    STEPDATA.append(0) 	# load data record 49
    STEPDATA.append(0) 	# load data record 50
    STEPDATA.append(0) 	# load data record 51
    STEPDATA.append(0) 	# load data record 52
    STEPDATA.append(0) 	# load data record 53
    STEPDATA.append(0) 	# load data record 54
    STEPDATA.append(0) 	# load data record 55
    STEPDATA.append(0) 	# load data record 56
    STEPDATA.append(0) 	# load data record 57
    STEPDATA.append(0) 	# load data record 58
    STEPDATA.append(0) 	# load data record 59
    STEPDATA.append(0) 	# load data record 60
    STEPDATA.append(0) 	# load data record 61
    STEPDATA.append(0) 	# load data record 62
    STEPPROCDBG.append(('selsort',3))
    STEPPROCDBG.append(('dumparray',67))
    STEPPROCDBG.append(('nonsense',86))
    STEPPROCDBG.append(('main',142))
    STEPDATDBG.append(('my_array@@selsort',0))
    STEPDATDBG.append(('table1',1))
    STEPDATDBG.append(('array32',9))
    STEPDATDBG.append(('array16',47))
    STEPPCDBG.append('/export/home/faculty/parson/private/csc526/solutions/vectors2/vm_in_python/selsort.stp')
    STEPPCDBG.append((7,3))
    STEPPCDBG.append((12,7))
    STEPPCDBG.append((13,10))
    STEPPCDBG.append((14,13))
    STEPPCDBG.append((15,15))
    STEPPCDBG.append((16,18))
    STEPPCDBG.append((17,21))
    STEPPCDBG.append((18,23))
    STEPPCDBG.append((19,29))
    STEPPCDBG.append((20,35))
    STEPPCDBG.append((21,38))
    STEPPCDBG.append((23,40))
    STEPPCDBG.append((25,47))
    STEPPCDBG.append((26,55))
    STEPPCDBG.append((27,57))
    STEPPCDBG.append((29,58))
    STEPPCDBG.append((30,59))
    STEPPCDBG.append((31,61))
    STEPPCDBG.append((32,62))
    STEPPCDBG.append((33,63))
    STEPPCDBG.append((34,65))
    STEPPCDBG.append((35,66))
    STEPPCDBG.append((38,67))
    STEPPCDBG.append((39,69))
    STEPPCDBG.append((40,72))
    STEPPCDBG.append((41,74))
    STEPPCDBG.append((42,80))
    STEPPCDBG.append((43,81))
    STEPPCDBG.append((44,83))
    STEPPCDBG.append((45,85))
    STEPPCDBG.append((52,86))
    STEPPCDBG.append((54,88))
    STEPPCDBG.append((55,91))
    STEPPCDBG.append((56,94))
    STEPPCDBG.append((57,95))
    STEPPCDBG.append((58,96))
    STEPPCDBG.append((59,99))
    STEPPCDBG.append((60,100))
    STEPPCDBG.append((61,102))
    STEPPCDBG.append((62,104))
    STEPPCDBG.append((63,106))
    STEPPCDBG.append((65,108))
    STEPPCDBG.append((67,112))
    STEPPCDBG.append((68,114))
    STEPPCDBG.append((69,115))
    STEPPCDBG.append((71,117))
    STEPPCDBG.append((72,120))
    STEPPCDBG.append((73,123))
    STEPPCDBG.append((74,124))
    STEPPCDBG.append((75,125))
    STEPPCDBG.append((76,130))
    STEPPCDBG.append((77,131))
    STEPPCDBG.append((79,133))
    STEPPCDBG.append((80,137))
    STEPPCDBG.append((81,139))
    STEPPCDBG.append((82,141))
    STEPPCDBG.append((85,142))
    STEPPCDBG.append((86,146))
    STEPPCDBG.append((87,152))
    STEPPCDBG.append((88,156))
    STEPPCDBG.append((89,162))
    STEPPCDBG.append((90,168))
    STEPPCDBG.append((91,170))
    STEPPCDBG.append((92,172))
    return((STEPCODE,STEPDATA,STEPPROCDBG,STEPDATDBG,STEPPCDBG))


def loadivm(vm):
    ivm = vm
    INSTEPCODE = []
    INSTEPDATA = []
    INSTEPPROCDBG = []
    INSTEPDATDBG = []
    INSTEPPCDBG = []
    # dumping dictionary 0 to 126,
    # 0 cmds, source selsort.stp
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (109,))) 	# load code record 0
    INSTEPCODE.append(DirectThreadedVM.STEP_HALT) 	# load code record 1
    INSTEPCODE.append(iDirectThreadedVM.STEP_SWAP) 	# load code record 2
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (0,))) 	# load code record 3
    INSTEPCODE.append(iDirectThreadedVM.STEP_STORE) 	# load code record 4
    INSTEPCODE.append(iDirectThreadedVM.STEP_SUB1) 	# load code record 5
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (0,))) 	# load code record 6
    INSTEPCODE.append(iDirectThreadedVM.STEP_OVER) 	# load code record 7
    INSTEPCODE.append(iDirectThreadedVM.STEP_OVER) 	# load code record 8
    INSTEPCODE.append(iDirectThreadedVM.STEP_GT) 	# load code record 9
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_GOTO0, (51,))) 	# load code record 10
    INSTEPCODE.append(iDirectThreadedVM.STEP_OVER) 	# load code record 11
    INSTEPCODE.append(iDirectThreadedVM.STEP_OVER) 	# load code record 12
    INSTEPCODE.append(iDirectThreadedVM.STEP_ADD1) 	# load code record 13
    INSTEPCODE.append(iDirectThreadedVM.STEP_OVER) 	# load code record 14
    INSTEPCODE.append(iDirectThreadedVM.STEP_OVER) 	# load code record 15
    INSTEPCODE.append(iDirectThreadedVM.STEP_GE) 	# load code record 16
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_GOTO0, (48,))) 	# load code record 17
    INSTEPCODE.append(iDirectThreadedVM.STEP_OVER2) 	# load code record 18
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (0,))) 	# load code record 19
    INSTEPCODE.append(iDirectThreadedVM.STEP_FETCH) 	# load code record 20
    INSTEPCODE.append(iDirectThreadedVM.STEP_ADD) 	# load code record 21
    INSTEPCODE.append(iDirectThreadedVM.STEP_FETCH) 	# load code record 22
    INSTEPCODE.append(iDirectThreadedVM.STEP_OVER) 	# load code record 23
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (0,))) 	# load code record 24
    INSTEPCODE.append(iDirectThreadedVM.STEP_FETCH) 	# load code record 25
    INSTEPCODE.append(iDirectThreadedVM.STEP_ADD) 	# load code record 26
    INSTEPCODE.append(iDirectThreadedVM.STEP_FETCH) 	# load code record 27
    INSTEPCODE.append(iDirectThreadedVM.STEP_OVER) 	# load code record 28
    INSTEPCODE.append(iDirectThreadedVM.STEP_OVER) 	# load code record 29
    INSTEPCODE.append(iDirectThreadedVM.STEP_GT) 	# load code record 30
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_GOTO0, (45,))) 	# load code record 31
    INSTEPCODE.append(iDirectThreadedVM.STEP_SWAP) 	# load code record 32
    INSTEPCODE.append(iDirectThreadedVM.STEP_OVER2) 	# load code record 33
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (0,))) 	# load code record 34
    INSTEPCODE.append(iDirectThreadedVM.STEP_FETCH) 	# load code record 35
    INSTEPCODE.append(iDirectThreadedVM.STEP_ADD) 	# load code record 36
    INSTEPCODE.append(iDirectThreadedVM.STEP_STORE) 	# load code record 37
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (3,))) 	# load code record 38
    INSTEPCODE.append(iDirectThreadedVM.STEP_DUP_I) 	# load code record 39
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (0,))) 	# load code record 40
    INSTEPCODE.append(iDirectThreadedVM.STEP_FETCH) 	# load code record 41
    INSTEPCODE.append(iDirectThreadedVM.STEP_ADD) 	# load code record 42
    INSTEPCODE.append(iDirectThreadedVM.STEP_STORE) 	# load code record 43
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_GOTO, (46,))) 	# load code record 44
    INSTEPCODE.append(iDirectThreadedVM.STEP_DROP2) 	# load code record 45
    INSTEPCODE.append(iDirectThreadedVM.STEP_ADD1) 	# load code record 46
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_GOTO, (14,))) 	# load code record 47
    INSTEPCODE.append(iDirectThreadedVM.STEP_DROP2) 	# load code record 48
    INSTEPCODE.append(iDirectThreadedVM.STEP_ADD1) 	# load code record 49
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_GOTO, (7,))) 	# load code record 50
    INSTEPCODE.append(iDirectThreadedVM.STEP_DROP2) 	# load code record 51
    INSTEPCODE.append(iDirectThreadedVM.STEP_RETURN) 	# load code record 52
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (0,))) 	# load code record 53
    INSTEPCODE.append(iDirectThreadedVM.STEP_OVER) 	# load code record 54
    INSTEPCODE.append(iDirectThreadedVM.STEP_OVER) 	# load code record 55
    INSTEPCODE.append(iDirectThreadedVM.STEP_GT) 	# load code record 56
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_GOTO0, (66,))) 	# load code record 57
    INSTEPCODE.append(iDirectThreadedVM.STEP_OVER2) 	# load code record 58
    INSTEPCODE.append(iDirectThreadedVM.STEP_OVER) 	# load code record 59
    INSTEPCODE.append(iDirectThreadedVM.STEP_ADD) 	# load code record 60
    INSTEPCODE.append(iDirectThreadedVM.STEP_FETCH) 	# load code record 61
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTI) 	# load code record 62
    INSTEPCODE.append(iDirectThreadedVM.STEP_CRLF) 	# load code record 63
    INSTEPCODE.append(iDirectThreadedVM.STEP_ADD1) 	# load code record 64
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_GOTO, (54,))) 	# load code record 65
    INSTEPCODE.append(iDirectThreadedVM.STEP_DROP2) 	# load code record 66
    INSTEPCODE.append(iDirectThreadedVM.STEP_DROP) 	# load code record 67
    INSTEPCODE.append(iDirectThreadedVM.STEP_RETURN) 	# load code record 68
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (3,))) 	# load code record 69
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (41,))) 	# load code record 70
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 71
    INSTEPCODE.append(iDirectThreadedVM.STEP_DUP) 	# load code record 72
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTI) 	# load code record 73
    INSTEPCODE.append(iDirectThreadedVM.STEP_CRLF) 	# load code record 74
    INSTEPCODE.append(iDirectThreadedVM.STEP_SUB1) 	# load code record 75
    INSTEPCODE.append(iDirectThreadedVM.STEP_DUP) 	# load code record 76
    INSTEPCODE.append(iDirectThreadedVM.STEP_ZEQ) 	# load code record 77
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_GOTO0, (83,))) 	# load code record 78
    INSTEPCODE.append(iDirectThreadedVM.STEP_DROP) 	# load code record 79
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (1,))) 	# load code record 80
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_GOTO, (87,))) 	# load code record 81
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_GOTO, (84,))) 	# load code record 82
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (0,))) 	# load code record 83
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (42,))) 	# load code record 84
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 85
    INSTEPCODE.append(iDirectThreadedVM.STEP_CRLF) 	# load code record 86
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_GOTO0, (70,))) 	# load code record 87
    INSTEPCODE.append(iDirectThreadedVM.STEP_DROP) 	# load code record 88
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (6,))) 	# load code record 89
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (43,))) 	# load code record 90
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 91
    INSTEPCODE.append(iDirectThreadedVM.STEP_DUP) 	# load code record 92
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTI) 	# load code record 93
    INSTEPCODE.append(iDirectThreadedVM.STEP_CRLF) 	# load code record 94
    INSTEPCODE.append(iDirectThreadedVM.STEP_SUB1) 	# load code record 95
    INSTEPCODE.append(iDirectThreadedVM.STEP_DUP) 	# load code record 96
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (3,))) 	# load code record 97
    INSTEPCODE.append(iDirectThreadedVM.STEP_EQ) 	# load code record 98
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_GOTO0, (102,))) 	# load code record 99
    INSTEPCODE.append(iDirectThreadedVM.STEP_PAUSE) 	# load code record 100
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_GOTO, (108,))) 	# load code record 101
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (44,))) 	# load code record 102
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 103
    INSTEPCODE.append(iDirectThreadedVM.STEP_CRLF) 	# load code record 104
    INSTEPCODE.append(iDirectThreadedVM.STEP_DUP) 	# load code record 105
    INSTEPCODE.append(iDirectThreadedVM.STEP_ZEQ) 	# load code record 106
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_GOTO0, (90,))) 	# load code record 107
    INSTEPCODE.append(iDirectThreadedVM.STEP_RETURN) 	# load code record 108
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (45,))) 	# load code record 109
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 110
    INSTEPCODE.append(iDirectThreadedVM.STEP_CRLF) 	# load code record 111
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (1,))) 	# load code record 112
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (8,))) 	# load code record 113
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (53,))) 	# load code record 114
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (46,))) 	# load code record 115
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 116
    INSTEPCODE.append(iDirectThreadedVM.STEP_CRLF) 	# load code record 117
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (1,))) 	# load code record 118
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (8,))) 	# load code record 119
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 120
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (1,))) 	# load code record 121
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (8,))) 	# load code record 122
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (53,))) 	# load code record 123
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (69,))) 	# load code record 124
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (0,))) 	# load code record 125
    INSTEPCODE.append(iDirectThreadedVM.STEP_RETURN) 	# load code record 126
    INSTEPDATA.append(0) 	# load data record 0
    INSTEPDATA.append(45) 	# load data record 1
    INSTEPDATA.append(27) 	# load data record 2
    INSTEPDATA.append(-100) 	# load data record 3
    INSTEPDATA.append(100) 	# load data record 4
    INSTEPDATA.append(0) 	# load data record 5
    INSTEPDATA.append(-1) 	# load data record 6
    INSTEPDATA.append(1) 	# load data record 7
    INSTEPDATA.append(5) 	# load data record 8
    INSTEPDATA.append(0) 	# load data record 9
    INSTEPDATA.append(0) 	# load data record 10
    INSTEPDATA.append(0) 	# load data record 11
    INSTEPDATA.append(0) 	# load data record 12
    INSTEPDATA.append(0) 	# load data record 13
    INSTEPDATA.append(0) 	# load data record 14
    INSTEPDATA.append(0) 	# load data record 15
    INSTEPDATA.append(0) 	# load data record 16
    INSTEPDATA.append(0) 	# load data record 17
    INSTEPDATA.append(0) 	# load data record 18
    INSTEPDATA.append(0) 	# load data record 19
    INSTEPDATA.append(0) 	# load data record 20
    INSTEPDATA.append(0) 	# load data record 21
    INSTEPDATA.append(0) 	# load data record 22
    INSTEPDATA.append(0) 	# load data record 23
    INSTEPDATA.append(0) 	# load data record 24
    INSTEPDATA.append(0) 	# load data record 25
    INSTEPDATA.append(0) 	# load data record 26
    INSTEPDATA.append(0) 	# load data record 27
    INSTEPDATA.append(0) 	# load data record 28
    INSTEPDATA.append(0) 	# load data record 29
    INSTEPDATA.append(0) 	# load data record 30
    INSTEPDATA.append(0) 	# load data record 31
    INSTEPDATA.append(0) 	# load data record 32
    INSTEPDATA.append(0) 	# load data record 33
    INSTEPDATA.append(0) 	# load data record 34
    INSTEPDATA.append(0) 	# load data record 35
    INSTEPDATA.append(0) 	# load data record 36
    INSTEPDATA.append(0) 	# load data record 37
    INSTEPDATA.append(0) 	# load data record 38
    INSTEPDATA.append(0) 	# load data record 39
    INSTEPDATA.append(0) 	# load data record 40
    INSTEPDATA.append('testing until and if with no else and continue ') 	# load data record 41
    INSTEPDATA.append('bypassed the continue') 	# load data record 42
    INSTEPDATA.append('testing until and if with no else and break ') 	# load data record 43
    INSTEPDATA.append('bypassed the break') 	# load data record 44
    INSTEPDATA.append('table1 before the sort') 	# load data record 45
    INSTEPDATA.append('table1 after the sort') 	# load data record 46
    INSTEPDATA.append(0) 	# load data record 47
    INSTEPDATA.append(0) 	# load data record 48
    INSTEPDATA.append(0) 	# load data record 49
    INSTEPDATA.append(0) 	# load data record 50
    INSTEPDATA.append(0) 	# load data record 51
    INSTEPDATA.append(0) 	# load data record 52
    INSTEPDATA.append(0) 	# load data record 53
    INSTEPDATA.append(0) 	# load data record 54
    INSTEPDATA.append(0) 	# load data record 55
    INSTEPDATA.append(0) 	# load data record 56
    INSTEPDATA.append(0) 	# load data record 57
    INSTEPDATA.append(0) 	# load data record 58
    INSTEPDATA.append(0) 	# load data record 59
    INSTEPDATA.append(0) 	# load data record 60
    INSTEPDATA.append(0) 	# load data record 61
    INSTEPDATA.append(0) 	# load data record 62
    INSTEPPROCDBG.append(('selsort',2))
    INSTEPPROCDBG.append(('dumparray',53))
    INSTEPPROCDBG.append(('nonsense',69))
    INSTEPPROCDBG.append(('main',109))
    INSTEPDATDBG.append(('my_array@@selsort',0))
    INSTEPDATDBG.append(('table1',1))
    INSTEPDATDBG.append(('array32',9))
    INSTEPDATDBG.append(('array16',47))
    INSTEPPCDBG.append('/export/home/faculty/parson/private/csc526/solutions/vectors2/vm_in_python/selsort.stp')
    return((INSTEPCODE,INSTEPDATA,INSTEPPROCDBG,INSTEPDATDBG,INSTEPPCDBG))
