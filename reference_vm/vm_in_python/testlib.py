from vm import DirectThreadedVM
def loadvm(vm):
    STEPCODE = []
    STEPDATA = []
    STEPPROCDBG = []
    STEPDATDBG = []
    STEPPCDBG = []
    # dumping dictionary 0 to 909,
    # 0 cmds, source testlib.stp
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 0
    STEPCODE.append(903) 	# load code record 1
    STEPCODE.append(DirectThreadedVM.STEP_HALT) 	# load code record 2
    STEPCODE.append(DirectThreadedVM.STEP_PRINTI) 	# load code record 3
    STEPCODE.append(DirectThreadedVM.STEP_CRLF) 	# load code record 4
    STEPCODE.append(DirectThreadedVM.STEP_RETURN) 	# load code record 5
    STEPCODE.append(DirectThreadedVM.STEP_DUP) 	# load code record 6
    STEPCODE.append(DirectThreadedVM.STEP_ZNEQ) 	# load code record 7
    STEPCODE.append(DirectThreadedVM.STEP_GOTO0) 	# load code record 8
    STEPCODE.append(16) 	# load code record 9
    STEPCODE.append(DirectThreadedVM.STEP_PRINTI) 	# load code record 10
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 11
    STEPCODE.append(0) 	# load code record 12
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 13
    STEPCODE.append(DirectThreadedVM.STEP_GOTO) 	# load code record 14
    STEPCODE.append(6) 	# load code record 15
    STEPCODE.append(DirectThreadedVM.STEP_PRINTI) 	# load code record 16
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 17
    STEPCODE.append(1) 	# load code record 18
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 19
    STEPCODE.append(DirectThreadedVM.STEP_DS_DEPTH) 	# load code record 20
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 21
    STEPCODE.append(3) 	# load code record 22
    STEPCODE.append(DirectThreadedVM.STEP_RETURN) 	# load code record 23
    STEPCODE.append(DirectThreadedVM.STEP_DECIMAL) 	# load code record 24
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 25
    STEPCODE.append(2) 	# load code record 26
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 27
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 28
    STEPCODE.append(-1) 	# load code record 29
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 30
    STEPCODE.append(3) 	# load code record 31
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 32
    STEPCODE.append(3) 	# load code record 33
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 34
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 35
    STEPCODE.append(1) 	# load code record 36
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 37
    STEPCODE.append(3) 	# load code record 38
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 39
    STEPCODE.append(4) 	# load code record 40
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 41
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 42
    STEPCODE.append(10) 	# load code record 43
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 44
    STEPCODE.append(3) 	# load code record 45
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 46
    STEPCODE.append(5) 	# load code record 47
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 48
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 49
    STEPCODE.append(8) 	# load code record 50
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 51
    STEPCODE.append(3) 	# load code record 52
    STEPCODE.append(DirectThreadedVM.STEP_HEX) 	# load code record 53
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 54
    STEPCODE.append(6) 	# load code record 55
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 56
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 57
    STEPCODE.append(-1) 	# load code record 58
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 59
    STEPCODE.append(3) 	# load code record 60
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 61
    STEPCODE.append(7) 	# load code record 62
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 63
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 64
    STEPCODE.append(1) 	# load code record 65
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 66
    STEPCODE.append(3) 	# load code record 67
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 68
    STEPCODE.append(8) 	# load code record 69
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 70
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 71
    STEPCODE.append(10) 	# load code record 72
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 73
    STEPCODE.append(3) 	# load code record 74
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 75
    STEPCODE.append(9) 	# load code record 76
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 77
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 78
    STEPCODE.append(8) 	# load code record 79
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 80
    STEPCODE.append(3) 	# load code record 81
    STEPCODE.append(DirectThreadedVM.STEP_OCTAL) 	# load code record 82
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 83
    STEPCODE.append(10) 	# load code record 84
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 85
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 86
    STEPCODE.append(-1) 	# load code record 87
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 88
    STEPCODE.append(3) 	# load code record 89
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 90
    STEPCODE.append(11) 	# load code record 91
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 92
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 93
    STEPCODE.append(1) 	# load code record 94
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 95
    STEPCODE.append(3) 	# load code record 96
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 97
    STEPCODE.append(12) 	# load code record 98
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 99
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 100
    STEPCODE.append(8) 	# load code record 101
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 102
    STEPCODE.append(3) 	# load code record 103
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 104
    STEPCODE.append(13) 	# load code record 105
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 106
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 107
    STEPCODE.append(10) 	# load code record 108
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 109
    STEPCODE.append(3) 	# load code record 110
    STEPCODE.append(DirectThreadedVM.STEP_DECIMAL) 	# load code record 111
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 112
    STEPCODE.append(14) 	# load code record 113
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 114
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 115
    STEPCODE.append(20) 	# load code record 116
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 117
    STEPCODE.append(5) 	# load code record 118
    STEPCODE.append(DirectThreadedVM.STEP_ADD) 	# load code record 119
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 120
    STEPCODE.append(3) 	# load code record 121
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 122
    STEPCODE.append(15) 	# load code record 123
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 124
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 125
    STEPCODE.append(20) 	# load code record 126
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 127
    STEPCODE.append(-5) 	# load code record 128
    STEPCODE.append(DirectThreadedVM.STEP_ADD) 	# load code record 129
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 130
    STEPCODE.append(3) 	# load code record 131
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 132
    STEPCODE.append(16) 	# load code record 133
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 134
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 135
    STEPCODE.append(20) 	# load code record 136
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 137
    STEPCODE.append(5) 	# load code record 138
    STEPCODE.append(DirectThreadedVM.STEP_SUB) 	# load code record 139
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 140
    STEPCODE.append(3) 	# load code record 141
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 142
    STEPCODE.append(17) 	# load code record 143
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 144
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 145
    STEPCODE.append(20) 	# load code record 146
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 147
    STEPCODE.append(-5) 	# load code record 148
    STEPCODE.append(DirectThreadedVM.STEP_SUB) 	# load code record 149
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 150
    STEPCODE.append(3) 	# load code record 151
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 152
    STEPCODE.append(18) 	# load code record 153
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 154
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 155
    STEPCODE.append(20) 	# load code record 156
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 157
    STEPCODE.append(5) 	# load code record 158
    STEPCODE.append(DirectThreadedVM.STEP_MULT) 	# load code record 159
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 160
    STEPCODE.append(3) 	# load code record 161
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 162
    STEPCODE.append(19) 	# load code record 163
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 164
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 165
    STEPCODE.append(20) 	# load code record 166
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 167
    STEPCODE.append(-5) 	# load code record 168
    STEPCODE.append(DirectThreadedVM.STEP_MULT) 	# load code record 169
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 170
    STEPCODE.append(3) 	# load code record 171
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 172
    STEPCODE.append(20) 	# load code record 173
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 174
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 175
    STEPCODE.append(20) 	# load code record 176
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 177
    STEPCODE.append(5) 	# load code record 178
    STEPCODE.append(DirectThreadedVM.STEP_DIV) 	# load code record 179
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 180
    STEPCODE.append(3) 	# load code record 181
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 182
    STEPCODE.append(21) 	# load code record 183
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 184
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 185
    STEPCODE.append(20) 	# load code record 186
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 187
    STEPCODE.append(-5) 	# load code record 188
    STEPCODE.append(DirectThreadedVM.STEP_DIV) 	# load code record 189
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 190
    STEPCODE.append(3) 	# load code record 191
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 192
    STEPCODE.append(22) 	# load code record 193
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 194
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 195
    STEPCODE.append(20) 	# load code record 196
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 197
    STEPCODE.append(5) 	# load code record 198
    STEPCODE.append(DirectThreadedVM.STEP_MOD) 	# load code record 199
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 200
    STEPCODE.append(3) 	# load code record 201
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 202
    STEPCODE.append(23) 	# load code record 203
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 204
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 205
    STEPCODE.append(20) 	# load code record 206
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 207
    STEPCODE.append(3) 	# load code record 208
    STEPCODE.append(DirectThreadedVM.STEP_MOD) 	# load code record 209
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 210
    STEPCODE.append(3) 	# load code record 211
    STEPCODE.append(DirectThreadedVM.STEP_HEX) 	# load code record 212
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 213
    STEPCODE.append(24) 	# load code record 214
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 215
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 216
    STEPCODE.append(4294901760) 	# load code record 217
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 218
    STEPCODE.append(4042322160) 	# load code record 219
    STEPCODE.append(DirectThreadedVM.STEP_BITAND) 	# load code record 220
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 221
    STEPCODE.append(3) 	# load code record 222
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 223
    STEPCODE.append(25) 	# load code record 224
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 225
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 226
    STEPCODE.append(4294901760) 	# load code record 227
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 228
    STEPCODE.append(4042322160) 	# load code record 229
    STEPCODE.append(DirectThreadedVM.STEP_BITOR) 	# load code record 230
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 231
    STEPCODE.append(3) 	# load code record 232
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 233
    STEPCODE.append(26) 	# load code record 234
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 235
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 236
    STEPCODE.append(4294901760) 	# load code record 237
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 238
    STEPCODE.append(4042322160) 	# load code record 239
    STEPCODE.append(DirectThreadedVM.STEP_BITXOR) 	# load code record 240
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 241
    STEPCODE.append(3) 	# load code record 242
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 243
    STEPCODE.append(27) 	# load code record 244
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 245
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 246
    STEPCODE.append(4294901760) 	# load code record 247
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 248
    STEPCODE.append(3) 	# load code record 249
    STEPCODE.append(DirectThreadedVM.STEP_SHL) 	# load code record 250
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 251
    STEPCODE.append(3) 	# load code record 252
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 253
    STEPCODE.append(28) 	# load code record 254
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 255
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 256
    STEPCODE.append(4294901760) 	# load code record 257
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 258
    STEPCODE.append(5) 	# load code record 259
    STEPCODE.append(DirectThreadedVM.STEP_SHR) 	# load code record 260
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 261
    STEPCODE.append(3) 	# load code record 262
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 263
    STEPCODE.append(29) 	# load code record 264
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 265
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 266
    STEPCODE.append(4042322160) 	# load code record 267
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 268
    STEPCODE.append(3) 	# load code record 269
    STEPCODE.append(DirectThreadedVM.STEP_LROT) 	# load code record 270
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 271
    STEPCODE.append(3) 	# load code record 272
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 273
    STEPCODE.append(30) 	# load code record 274
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 275
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 276
    STEPCODE.append(4042322160) 	# load code record 277
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 278
    STEPCODE.append(3) 	# load code record 279
    STEPCODE.append(DirectThreadedVM.STEP_RROT) 	# load code record 280
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 281
    STEPCODE.append(3) 	# load code record 282
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 283
    STEPCODE.append(31) 	# load code record 284
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 285
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 286
    STEPCODE.append(4042322160) 	# load code record 287
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 288
    STEPCODE.append(3) 	# load code record 289
    STEPCODE.append(DirectThreadedVM.STEP_LROT16) 	# load code record 290
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 291
    STEPCODE.append(3) 	# load code record 292
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 293
    STEPCODE.append(32) 	# load code record 294
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 295
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 296
    STEPCODE.append(4042322160) 	# load code record 297
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 298
    STEPCODE.append(3) 	# load code record 299
    STEPCODE.append(DirectThreadedVM.STEP_RROT16) 	# load code record 300
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 301
    STEPCODE.append(3) 	# load code record 302
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 303
    STEPCODE.append(33) 	# load code record 304
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 305
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 306
    STEPCODE.append(4042322160) 	# load code record 307
    STEPCODE.append(DirectThreadedVM.STEP_COMPLEMENT) 	# load code record 308
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 309
    STEPCODE.append(3) 	# load code record 310
    STEPCODE.append(DirectThreadedVM.STEP_DECIMAL) 	# load code record 311
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 312
    STEPCODE.append(34) 	# load code record 313
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 314
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 315
    STEPCODE.append(20) 	# load code record 316
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 317
    STEPCODE.append(1) 	# load code record 318
    STEPCODE.append(DirectThreadedVM.STEP_LOGAND) 	# load code record 319
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 320
    STEPCODE.append(3) 	# load code record 321
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 322
    STEPCODE.append(35) 	# load code record 323
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 324
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 325
    STEPCODE.append(20) 	# load code record 326
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 327
    STEPCODE.append(0) 	# load code record 328
    STEPCODE.append(DirectThreadedVM.STEP_LOGAND) 	# load code record 329
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 330
    STEPCODE.append(3) 	# load code record 331
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 332
    STEPCODE.append(36) 	# load code record 333
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 334
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 335
    STEPCODE.append(20) 	# load code record 336
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 337
    STEPCODE.append(1) 	# load code record 338
    STEPCODE.append(DirectThreadedVM.STEP_LOGOR) 	# load code record 339
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 340
    STEPCODE.append(3) 	# load code record 341
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 342
    STEPCODE.append(37) 	# load code record 343
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 344
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 345
    STEPCODE.append(20) 	# load code record 346
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 347
    STEPCODE.append(0) 	# load code record 348
    STEPCODE.append(DirectThreadedVM.STEP_LOGOR) 	# load code record 349
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 350
    STEPCODE.append(3) 	# load code record 351
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 352
    STEPCODE.append(38) 	# load code record 353
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 354
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 355
    STEPCODE.append(20) 	# load code record 356
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 357
    STEPCODE.append(1) 	# load code record 358
    STEPCODE.append(DirectThreadedVM.STEP_GT) 	# load code record 359
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 360
    STEPCODE.append(3) 	# load code record 361
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 362
    STEPCODE.append(39) 	# load code record 363
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 364
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 365
    STEPCODE.append(20) 	# load code record 366
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 367
    STEPCODE.append(-11) 	# load code record 368
    STEPCODE.append(DirectThreadedVM.STEP_LT) 	# load code record 369
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 370
    STEPCODE.append(3) 	# load code record 371
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 372
    STEPCODE.append(40) 	# load code record 373
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 374
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 375
    STEPCODE.append(20) 	# load code record 376
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 377
    STEPCODE.append(20) 	# load code record 378
    STEPCODE.append(DirectThreadedVM.STEP_EQ) 	# load code record 379
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 380
    STEPCODE.append(3) 	# load code record 381
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 382
    STEPCODE.append(41) 	# load code record 383
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 384
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 385
    STEPCODE.append(20) 	# load code record 386
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 387
    STEPCODE.append(1) 	# load code record 388
    STEPCODE.append(DirectThreadedVM.STEP_GE) 	# load code record 389
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 390
    STEPCODE.append(3) 	# load code record 391
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 392
    STEPCODE.append(42) 	# load code record 393
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 394
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 395
    STEPCODE.append(20) 	# load code record 396
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 397
    STEPCODE.append(-11) 	# load code record 398
    STEPCODE.append(DirectThreadedVM.STEP_LE) 	# load code record 399
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 400
    STEPCODE.append(3) 	# load code record 401
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 402
    STEPCODE.append(43) 	# load code record 403
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 404
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 405
    STEPCODE.append(20) 	# load code record 406
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 407
    STEPCODE.append(20) 	# load code record 408
    STEPCODE.append(DirectThreadedVM.STEP_GE) 	# load code record 409
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 410
    STEPCODE.append(3) 	# load code record 411
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 412
    STEPCODE.append(44) 	# load code record 413
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 414
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 415
    STEPCODE.append(20) 	# load code record 416
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 417
    STEPCODE.append(20) 	# load code record 418
    STEPCODE.append(DirectThreadedVM.STEP_LE) 	# load code record 419
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 420
    STEPCODE.append(3) 	# load code record 421
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 422
    STEPCODE.append(45) 	# load code record 423
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 424
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 425
    STEPCODE.append(20) 	# load code record 426
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 427
    STEPCODE.append(20) 	# load code record 428
    STEPCODE.append(DirectThreadedVM.STEP_NEQ) 	# load code record 429
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 430
    STEPCODE.append(3) 	# load code record 431
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 432
    STEPCODE.append(46) 	# load code record 433
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 434
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 435
    STEPCODE.append(20) 	# load code record 436
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 437
    STEPCODE.append(21) 	# load code record 438
    STEPCODE.append(DirectThreadedVM.STEP_NEQ) 	# load code record 439
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 440
    STEPCODE.append(3) 	# load code record 441
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 442
    STEPCODE.append(47) 	# load code record 443
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 444
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 445
    STEPCODE.append(100) 	# load code record 446
    STEPCODE.append(DirectThreadedVM.STEP_MINUS) 	# load code record 447
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 448
    STEPCODE.append(3) 	# load code record 449
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 450
    STEPCODE.append(48) 	# load code record 451
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 452
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 453
    STEPCODE.append(-100) 	# load code record 454
    STEPCODE.append(DirectThreadedVM.STEP_MINUS) 	# load code record 455
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 456
    STEPCODE.append(3) 	# load code record 457
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 458
    STEPCODE.append(49) 	# load code record 459
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 460
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 461
    STEPCODE.append(100) 	# load code record 462
    STEPCODE.append(DirectThreadedVM.STEP_SIGN) 	# load code record 463
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 464
    STEPCODE.append(3) 	# load code record 465
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 466
    STEPCODE.append(50) 	# load code record 467
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 468
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 469
    STEPCODE.append(-100) 	# load code record 470
    STEPCODE.append(DirectThreadedVM.STEP_SIGN) 	# load code record 471
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 472
    STEPCODE.append(3) 	# load code record 473
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 474
    STEPCODE.append(51) 	# load code record 475
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 476
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 477
    STEPCODE.append(0) 	# load code record 478
    STEPCODE.append(DirectThreadedVM.STEP_SIGN) 	# load code record 479
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 480
    STEPCODE.append(3) 	# load code record 481
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 482
    STEPCODE.append(52) 	# load code record 483
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 484
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 485
    STEPCODE.append(100) 	# load code record 486
    STEPCODE.append(DirectThreadedVM.STEP_ABS) 	# load code record 487
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 488
    STEPCODE.append(3) 	# load code record 489
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 490
    STEPCODE.append(53) 	# load code record 491
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 492
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 493
    STEPCODE.append(-100) 	# load code record 494
    STEPCODE.append(DirectThreadedVM.STEP_ABS) 	# load code record 495
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 496
    STEPCODE.append(3) 	# load code record 497
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 498
    STEPCODE.append(54) 	# load code record 499
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 500
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 501
    STEPCODE.append(0) 	# load code record 502
    STEPCODE.append(DirectThreadedVM.STEP_ABS) 	# load code record 503
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 504
    STEPCODE.append(3) 	# load code record 505
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 506
    STEPCODE.append(55) 	# load code record 507
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 508
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 509
    STEPCODE.append(1) 	# load code record 510
    STEPCODE.append(DirectThreadedVM.STEP_ZEQ) 	# load code record 511
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 512
    STEPCODE.append(3) 	# load code record 513
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 514
    STEPCODE.append(56) 	# load code record 515
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 516
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 517
    STEPCODE.append(0) 	# load code record 518
    STEPCODE.append(DirectThreadedVM.STEP_ZEQ) 	# load code record 519
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 520
    STEPCODE.append(3) 	# load code record 521
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 522
    STEPCODE.append(57) 	# load code record 523
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 524
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 525
    STEPCODE.append(-1) 	# load code record 526
    STEPCODE.append(DirectThreadedVM.STEP_ZEQ) 	# load code record 527
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 528
    STEPCODE.append(3) 	# load code record 529
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 530
    STEPCODE.append(58) 	# load code record 531
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 532
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 533
    STEPCODE.append(1) 	# load code record 534
    STEPCODE.append(DirectThreadedVM.STEP_ZNEQ) 	# load code record 535
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 536
    STEPCODE.append(3) 	# load code record 537
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 538
    STEPCODE.append(59) 	# load code record 539
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 540
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 541
    STEPCODE.append(0) 	# load code record 542
    STEPCODE.append(DirectThreadedVM.STEP_ZNEQ) 	# load code record 543
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 544
    STEPCODE.append(3) 	# load code record 545
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 546
    STEPCODE.append(60) 	# load code record 547
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 548
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 549
    STEPCODE.append(-1) 	# load code record 550
    STEPCODE.append(DirectThreadedVM.STEP_ZNEQ) 	# load code record 551
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 552
    STEPCODE.append(3) 	# load code record 553
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 554
    STEPCODE.append(61) 	# load code record 555
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 556
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 557
    STEPCODE.append(1) 	# load code record 558
    STEPCODE.append(DirectThreadedVM.STEP_ZLT) 	# load code record 559
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 560
    STEPCODE.append(3) 	# load code record 561
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 562
    STEPCODE.append(62) 	# load code record 563
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 564
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 565
    STEPCODE.append(0) 	# load code record 566
    STEPCODE.append(DirectThreadedVM.STEP_ZLT) 	# load code record 567
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 568
    STEPCODE.append(3) 	# load code record 569
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 570
    STEPCODE.append(63) 	# load code record 571
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 572
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 573
    STEPCODE.append(-1) 	# load code record 574
    STEPCODE.append(DirectThreadedVM.STEP_ZLT) 	# load code record 575
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 576
    STEPCODE.append(3) 	# load code record 577
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 578
    STEPCODE.append(64) 	# load code record 579
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 580
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 581
    STEPCODE.append(1) 	# load code record 582
    STEPCODE.append(DirectThreadedVM.STEP_ZGT) 	# load code record 583
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 584
    STEPCODE.append(3) 	# load code record 585
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 586
    STEPCODE.append(65) 	# load code record 587
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 588
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 589
    STEPCODE.append(0) 	# load code record 590
    STEPCODE.append(DirectThreadedVM.STEP_ZGT) 	# load code record 591
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 592
    STEPCODE.append(3) 	# load code record 593
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 594
    STEPCODE.append(66) 	# load code record 595
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 596
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 597
    STEPCODE.append(-1) 	# load code record 598
    STEPCODE.append(DirectThreadedVM.STEP_ZGT) 	# load code record 599
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 600
    STEPCODE.append(3) 	# load code record 601
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 602
    STEPCODE.append(67) 	# load code record 603
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 604
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 605
    STEPCODE.append(1) 	# load code record 606
    STEPCODE.append(DirectThreadedVM.STEP_ZGE) 	# load code record 607
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 608
    STEPCODE.append(3) 	# load code record 609
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 610
    STEPCODE.append(68) 	# load code record 611
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 612
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 613
    STEPCODE.append(0) 	# load code record 614
    STEPCODE.append(DirectThreadedVM.STEP_ZGE) 	# load code record 615
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 616
    STEPCODE.append(3) 	# load code record 617
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 618
    STEPCODE.append(69) 	# load code record 619
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 620
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 621
    STEPCODE.append(-1) 	# load code record 622
    STEPCODE.append(DirectThreadedVM.STEP_ZGE) 	# load code record 623
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 624
    STEPCODE.append(3) 	# load code record 625
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 626
    STEPCODE.append(70) 	# load code record 627
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 628
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 629
    STEPCODE.append(1) 	# load code record 630
    STEPCODE.append(DirectThreadedVM.STEP_ZLE) 	# load code record 631
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 632
    STEPCODE.append(3) 	# load code record 633
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 634
    STEPCODE.append(71) 	# load code record 635
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 636
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 637
    STEPCODE.append(0) 	# load code record 638
    STEPCODE.append(DirectThreadedVM.STEP_ZLE) 	# load code record 639
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 640
    STEPCODE.append(3) 	# load code record 641
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 642
    STEPCODE.append(72) 	# load code record 643
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 644
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 645
    STEPCODE.append(-1) 	# load code record 646
    STEPCODE.append(DirectThreadedVM.STEP_ZLE) 	# load code record 647
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 648
    STEPCODE.append(3) 	# load code record 649
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 650
    STEPCODE.append(73) 	# load code record 651
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 652
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 653
    STEPCODE.append(-1) 	# load code record 654
    STEPCODE.append(DirectThreadedVM.STEP_ADD1) 	# load code record 655
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 656
    STEPCODE.append(3) 	# load code record 657
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 658
    STEPCODE.append(74) 	# load code record 659
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 660
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 661
    STEPCODE.append(-1) 	# load code record 662
    STEPCODE.append(DirectThreadedVM.STEP_SUB1) 	# load code record 663
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 664
    STEPCODE.append(3) 	# load code record 665
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 666
    STEPCODE.append(75) 	# load code record 667
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 668
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 669
    STEPCODE.append(-1) 	# load code record 670
    STEPCODE.append(DirectThreadedVM.STEP_ADD2) 	# load code record 671
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 672
    STEPCODE.append(3) 	# load code record 673
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 674
    STEPCODE.append(76) 	# load code record 675
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 676
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 677
    STEPCODE.append(-1) 	# load code record 678
    STEPCODE.append(DirectThreadedVM.STEP_SUB2) 	# load code record 679
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 680
    STEPCODE.append(3) 	# load code record 681
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 682
    STEPCODE.append(77) 	# load code record 683
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 684
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 685
    STEPCODE.append(-1) 	# load code record 686
    STEPCODE.append(DirectThreadedVM.STEP_MULT2) 	# load code record 687
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 688
    STEPCODE.append(3) 	# load code record 689
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 690
    STEPCODE.append(78) 	# load code record 691
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 692
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 693
    STEPCODE.append(-1) 	# load code record 694
    STEPCODE.append(DirectThreadedVM.STEP_DIV2) 	# load code record 695
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 696
    STEPCODE.append(3) 	# load code record 697
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 698
    STEPCODE.append(79) 	# load code record 699
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 700
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 701
    STEPCODE.append(9) 	# load code record 702
    STEPCODE.append(DirectThreadedVM.STEP_SHL1) 	# load code record 703
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 704
    STEPCODE.append(3) 	# load code record 705
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 706
    STEPCODE.append(80) 	# load code record 707
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 708
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 709
    STEPCODE.append(9) 	# load code record 710
    STEPCODE.append(DirectThreadedVM.STEP_SHR1) 	# load code record 711
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 712
    STEPCODE.append(3) 	# load code record 713
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 714
    STEPCODE.append(81) 	# load code record 715
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 716
    STEPCODE.append(DirectThreadedVM.STEP_SIZEOF) 	# load code record 717
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 718
    STEPCODE.append(3) 	# load code record 719
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 720
    STEPCODE.append(82) 	# load code record 721
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 722
    STEPCODE.append(DirectThreadedVM.STEP_DS_DEPTH) 	# load code record 723
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 724
    STEPCODE.append(3) 	# load code record 725
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 726
    STEPCODE.append(83) 	# load code record 727
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 728
    STEPCODE.append(DirectThreadedVM.STEP_TS_DEPTH) 	# load code record 729
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 730
    STEPCODE.append(3) 	# load code record 731
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 732
    STEPCODE.append(84) 	# load code record 733
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 734
    STEPCODE.append(DirectThreadedVM.STEP_CODE_DICT_LEN) 	# load code record 735
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 736
    STEPCODE.append(3) 	# load code record 737
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 738
    STEPCODE.append(85) 	# load code record 739
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 740
    STEPCODE.append(DirectThreadedVM.STEP_DATA_DICT_LEN) 	# load code record 741
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 742
    STEPCODE.append(3) 	# load code record 743
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 744
    STEPCODE.append(86) 	# load code record 745
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 746
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 747
    STEPCODE.append(0) 	# load code record 748
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 749
    STEPCODE.append(10) 	# load code record 750
    STEPCODE.append(DirectThreadedVM.STEP_DUP) 	# load code record 751
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 752
    STEPCODE.append(6) 	# load code record 753
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 754
    STEPCODE.append(87) 	# load code record 755
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 756
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 757
    STEPCODE.append(0) 	# load code record 758
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 759
    STEPCODE.append(10) 	# load code record 760
    STEPCODE.append(DirectThreadedVM.STEP_DUP2) 	# load code record 761
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 762
    STEPCODE.append(6) 	# load code record 763
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 764
    STEPCODE.append(88) 	# load code record 765
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 766
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 767
    STEPCODE.append(0) 	# load code record 768
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 769
    STEPCODE.append(10) 	# load code record 770
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 771
    STEPCODE.append(20) 	# load code record 772
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 773
    STEPCODE.append(30) 	# load code record 774
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 775
    STEPCODE.append(40) 	# load code record 776
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 777
    STEPCODE.append(50) 	# load code record 778
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 779
    STEPCODE.append(2) 	# load code record 780
    STEPCODE.append(DirectThreadedVM.STEP_DUP_I) 	# load code record 781
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 782
    STEPCODE.append(6) 	# load code record 783
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 784
    STEPCODE.append(89) 	# load code record 785
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 786
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 787
    STEPCODE.append(0) 	# load code record 788
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 789
    STEPCODE.append(10) 	# load code record 790
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 791
    STEPCODE.append(20) 	# load code record 792
    STEPCODE.append(DirectThreadedVM.STEP_SWAP) 	# load code record 793
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 794
    STEPCODE.append(6) 	# load code record 795
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 796
    STEPCODE.append(90) 	# load code record 797
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 798
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 799
    STEPCODE.append(0) 	# load code record 800
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 801
    STEPCODE.append(10) 	# load code record 802
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 803
    STEPCODE.append(20) 	# load code record 804
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 805
    STEPCODE.append(30) 	# load code record 806
    STEPCODE.append(DirectThreadedVM.STEP_OVER) 	# load code record 807
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 808
    STEPCODE.append(6) 	# load code record 809
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 810
    STEPCODE.append(91) 	# load code record 811
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 812
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 813
    STEPCODE.append(0) 	# load code record 814
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 815
    STEPCODE.append(10) 	# load code record 816
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 817
    STEPCODE.append(20) 	# load code record 818
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 819
    STEPCODE.append(30) 	# load code record 820
    STEPCODE.append(DirectThreadedVM.STEP_OVER2) 	# load code record 821
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 822
    STEPCODE.append(6) 	# load code record 823
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 824
    STEPCODE.append(92) 	# load code record 825
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 826
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 827
    STEPCODE.append(0) 	# load code record 828
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 829
    STEPCODE.append(10) 	# load code record 830
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 831
    STEPCODE.append(20) 	# load code record 832
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 833
    STEPCODE.append(30) 	# load code record 834
    STEPCODE.append(DirectThreadedVM.STEP_DROP) 	# load code record 835
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 836
    STEPCODE.append(6) 	# load code record 837
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 838
    STEPCODE.append(93) 	# load code record 839
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 840
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 841
    STEPCODE.append(0) 	# load code record 842
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 843
    STEPCODE.append(10) 	# load code record 844
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 845
    STEPCODE.append(20) 	# load code record 846
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 847
    STEPCODE.append(30) 	# load code record 848
    STEPCODE.append(DirectThreadedVM.STEP_DROP2) 	# load code record 849
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 850
    STEPCODE.append(6) 	# load code record 851
    STEPCODE.append(DirectThreadedVM.STEP_RETURN) 	# load code record 852
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 853
    STEPCODE.append(94) 	# load code record 854
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 855
    STEPCODE.append(DirectThreadedVM.STEP_DUP) 	# load code record 856
    STEPCODE.append(DirectThreadedVM.STEP_PRINTI) 	# load code record 857
    STEPCODE.append(DirectThreadedVM.STEP_CRLF) 	# load code record 858
    STEPCODE.append(DirectThreadedVM.STEP_RETURN) 	# load code record 859
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 860
    STEPCODE.append(95) 	# load code record 861
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 862
    STEPCODE.append(DirectThreadedVM.STEP_DUP) 	# load code record 863
    STEPCODE.append(DirectThreadedVM.STEP_PRINTI) 	# load code record 864
    STEPCODE.append(DirectThreadedVM.STEP_CRLF) 	# load code record 865
    STEPCODE.append(DirectThreadedVM.STEP_RETURN) 	# load code record 866
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 867
    STEPCODE.append(96) 	# load code record 868
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 869
    STEPCODE.append(DirectThreadedVM.STEP_DUP) 	# load code record 870
    STEPCODE.append(DirectThreadedVM.STEP_PRINTI) 	# load code record 871
    STEPCODE.append(DirectThreadedVM.STEP_CRLF) 	# load code record 872
    STEPCODE.append(DirectThreadedVM.STEP_RETURN) 	# load code record 873
    STEPCODE.append(DirectThreadedVM.STEP_VAR) 	# load code record 874
    STEPCODE.append(97) 	# load code record 875
    STEPCODE.append(DirectThreadedVM.STEP_PRINTS) 	# load code record 876
    STEPCODE.append(DirectThreadedVM.STEP_DUP) 	# load code record 877
    STEPCODE.append(DirectThreadedVM.STEP_PRINTI) 	# load code record 878
    STEPCODE.append(DirectThreadedVM.STEP_CRLF) 	# load code record 879
    STEPCODE.append(DirectThreadedVM.STEP_RETURN) 	# load code record 880
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 881
    STEPCODE.append(-1) 	# load code record 882
    STEPCODE.append(DirectThreadedVM.STEP_DUP) 	# load code record 883
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 884
    STEPCODE.append(7) 	# load code record 885
    STEPCODE.append(DirectThreadedVM.STEP_LT) 	# load code record 886
    STEPCODE.append(DirectThreadedVM.STEP_GOTO0) 	# load code record 887
    STEPCODE.append(901) 	# load code record 888
    STEPCODE.append(DirectThreadedVM.STEP_DUP) 	# load code record 889
    STEPCODE.append(DirectThreadedVM.STEP_GOTOX) 	# load code record 890
    STEPCODE.append(4) 	# load code record 891
    STEPCODE.append(853) 	# load code record 892
    STEPCODE.append(860) 	# load code record 893
    STEPCODE.append(867) 	# load code record 894
    STEPCODE.append(874) 	# load code record 895
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 896
    STEPCODE.append(0) 	# load code record 897
    STEPCODE.append(DirectThreadedVM.STEP_ADD1) 	# load code record 898
    STEPCODE.append(DirectThreadedVM.STEP_GOTO) 	# load code record 899
    STEPCODE.append(883) 	# load code record 900
    STEPCODE.append(DirectThreadedVM.STEP_DROP) 	# load code record 901
    STEPCODE.append(DirectThreadedVM.STEP_RETURN) 	# load code record 902
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 903
    STEPCODE.append(24) 	# load code record 904
    STEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 905
    STEPCODE.append(881) 	# load code record 906
    STEPCODE.append(DirectThreadedVM.STEP_CONST) 	# load code record 907
    STEPCODE.append(0) 	# load code record 908
    STEPCODE.append(DirectThreadedVM.STEP_RETURN) 	# load code record 909
    STEPDATA.append(' ') 	# load data record 0
    STEPDATA.append(', stack at ') 	# load data record 1
    STEPDATA.append('constant -1 as decimal yields ') 	# load data record 2
    STEPDATA.append('constant 1 as decimal yields ') 	# load data record 3
    STEPDATA.append('constant 0xa as decimal yields ') 	# load data record 4
    STEPDATA.append('constant 010 as decimal yields ') 	# load data record 5
    STEPDATA.append('constant -1 as hex yields ') 	# load data record 6
    STEPDATA.append('constant 1 as hex yields ') 	# load data record 7
    STEPDATA.append('constant 0xa as hex yields ') 	# load data record 8
    STEPDATA.append('constant 010 as hex yields ') 	# load data record 9
    STEPDATA.append('constant -1 as octal yields ') 	# load data record 10
    STEPDATA.append('constant 1 as octal yields ') 	# load data record 11
    STEPDATA.append('constant 010 as octal yields ') 	# load data record 12
    STEPDATA.append('constant 0xa as octal yields ') 	# load data record 13
    STEPDATA.append('20 5 + yields ') 	# load data record 14
    STEPDATA.append('20 -5 + yields ') 	# load data record 15
    STEPDATA.append('20 5 - yields ') 	# load data record 16
    STEPDATA.append('20 -5 - yields ') 	# load data record 17
    STEPDATA.append('20 5 * yields ') 	# load data record 18
    STEPDATA.append('20 -5 * yields ') 	# load data record 19
    STEPDATA.append('20 5 / yields ') 	# load data record 20
    STEPDATA.append('20 -5 / yields ') 	# load data record 21
    STEPDATA.append('20 5 % yields ') 	# load data record 22
    STEPDATA.append('20 3 % yields ') 	# load data record 23
    STEPDATA.append('0xffff0000 0xf0f0f0f0 & yields ') 	# load data record 24
    STEPDATA.append('0xffff0000 0xf0f0f0f0 | yields ') 	# load data record 25
    STEPDATA.append('0xffff0000 0xf0f0f0f0 ^ yields ') 	# load data record 26
    STEPDATA.append('0xffff0000 3 << yields ') 	# load data record 27
    STEPDATA.append('0xffff0000 5 >> yields ') 	# load data record 28
    STEPDATA.append('0xf0f0f0f0 3 lrot yields ') 	# load data record 29
    STEPDATA.append('0xf0f0f0f0 3 rrot yields ') 	# load data record 30
    STEPDATA.append('0xf0f0f0f0 3 lrot16 yields ') 	# load data record 31
    STEPDATA.append('0xf0f0f0f0 3 rrot16 yields ') 	# load data record 32
    STEPDATA.append('0xf0f0f0f0 ~ yields ') 	# load data record 33
    STEPDATA.append('20 1 && yields ') 	# load data record 34
    STEPDATA.append('20 0 && yields ') 	# load data record 35
    STEPDATA.append('20 1 || yields ') 	# load data record 36
    STEPDATA.append('20 0 || yields ') 	# load data record 37
    STEPDATA.append('20 1 > yields ') 	# load data record 38
    STEPDATA.append('20 -11 < yields ') 	# load data record 39
    STEPDATA.append('20 20 == yields ') 	# load data record 40
    STEPDATA.append('20 1 >= yields ') 	# load data record 41
    STEPDATA.append('20 -11 <= yields ') 	# load data record 42
    STEPDATA.append('20 20 >= yields ') 	# load data record 43
    STEPDATA.append('20 20 <= yields ') 	# load data record 44
    STEPDATA.append('20 20 != yields ') 	# load data record 45
    STEPDATA.append('20 21 != yields ') 	# load data record 46
    STEPDATA.append('100 minus yields ') 	# load data record 47
    STEPDATA.append('-100 minus yields ') 	# load data record 48
    STEPDATA.append('100 sign yields ') 	# load data record 49
    STEPDATA.append('-100 sign yields ') 	# load data record 50
    STEPDATA.append('0 sign yields ') 	# load data record 51
    STEPDATA.append('100 abs yields ') 	# load data record 52
    STEPDATA.append('-100 abs yields ') 	# load data record 53
    STEPDATA.append('0 abs yields ') 	# load data record 54
    STEPDATA.append('1 0== yields ') 	# load data record 55
    STEPDATA.append('0 0== yields ') 	# load data record 56
    STEPDATA.append('-1 0== yields ') 	# load data record 57
    STEPDATA.append('1 0!= yields ') 	# load data record 58
    STEPDATA.append('0 0!= yields ') 	# load data record 59
    STEPDATA.append('-1 0!= yields ') 	# load data record 60
    STEPDATA.append('1 0< yields ') 	# load data record 61
    STEPDATA.append('0 0< yields ') 	# load data record 62
    STEPDATA.append('-1 0< yields ') 	# load data record 63
    STEPDATA.append('1 0> yields ') 	# load data record 64
    STEPDATA.append('0 0> yields ') 	# load data record 65
    STEPDATA.append('-1 0> yields ') 	# load data record 66
    STEPDATA.append('1 0>= yields ') 	# load data record 67
    STEPDATA.append('0 0>= yields ') 	# load data record 68
    STEPDATA.append('-1 0>= yields ') 	# load data record 69
    STEPDATA.append('1 0<= yields ') 	# load data record 70
    STEPDATA.append('0 0<= yields ') 	# load data record 71
    STEPDATA.append('-1 0<= yields ') 	# load data record 72
    STEPDATA.append('-1 1+ yields ') 	# load data record 73
    STEPDATA.append('-1 1- yields ') 	# load data record 74
    STEPDATA.append('-1 2+ yields ') 	# load data record 75
    STEPDATA.append('-1 2- yields ') 	# load data record 76
    STEPDATA.append('-1 2* yields ') 	# load data record 77
    STEPDATA.append('-1 2/ yields ') 	# load data record 78
    STEPDATA.append('9 1<< yields ') 	# load data record 79
    STEPDATA.append('9 1>> yields ') 	# load data record 80
    STEPDATA.append('sizeof_word is ') 	# load data record 81
    STEPDATA.append('ds_depth is ') 	# load data record 82
    STEPDATA.append('ts_depth is ') 	# load data record 83
    STEPDATA.append('code_dict_len is ') 	# load data record 84
    STEPDATA.append('data_dict_len is ') 	# load data record 85
    STEPDATA.append('0 10 dup yields ') 	# load data record 86
    STEPDATA.append('0 10 dup2 yields ') 	# load data record 87
    STEPDATA.append('0 10 20 30 40 50 2 dupi yields ') 	# load data record 88
    STEPDATA.append('0 10 20 swap yields ') 	# load data record 89
    STEPDATA.append('0 10 20 30 over yields ') 	# load data record 90
    STEPDATA.append('0 10 20 30 over2 yields ') 	# load data record 91
    STEPDATA.append('0 10 20 30 drop yields ') 	# load data record 92
    STEPDATA.append('0 10 20 30 drop2 yields ') 	# load data record 93
    STEPDATA.append('inside s_proc0 on index ') 	# load data record 94
    STEPDATA.append('inside s_proc1 on index ') 	# load data record 95
    STEPDATA.append('inside s_proc2 on index ') 	# load data record 96
    STEPDATA.append('inside s_proc3 on index ') 	# load data record 97
    STEPPROCDBG.append(('.',3))
    STEPPROCDBG.append(('dumpds',6))
    STEPPROCDBG.append(('testmath',24))
    STEPPROCDBG.append(('s_proc0',853))
    STEPPROCDBG.append(('s_proc1',860))
    STEPPROCDBG.append(('s_proc2',867))
    STEPPROCDBG.append(('s_proc3',874))
    STEPPROCDBG.append(('testswitch',881))
    STEPPROCDBG.append(('main',903))
    STEPPCDBG.append('/export/home/faculty/parson/private/csc526/solutions/vectors2/vm_in_python/testlib.stp')
    STEPPCDBG.append((4,3))
    STEPPCDBG.append((8,6))
    STEPPCDBG.append((9,8))
    STEPPCDBG.append((10,10))
    STEPPCDBG.append((11,14))
    STEPPCDBG.append((12,16))
    STEPPCDBG.append((13,23))
    STEPPCDBG.append((20,24))
    STEPPCDBG.append((21,25))
    STEPPCDBG.append((22,32))
    STEPPCDBG.append((23,39))
    STEPPCDBG.append((24,46))
    STEPPCDBG.append((25,53))
    STEPPCDBG.append((26,54))
    STEPPCDBG.append((27,61))
    STEPPCDBG.append((28,68))
    STEPPCDBG.append((29,75))
    STEPPCDBG.append((30,82))
    STEPPCDBG.append((31,83))
    STEPPCDBG.append((32,90))
    STEPPCDBG.append((33,97))
    STEPPCDBG.append((34,104))
    STEPPCDBG.append((35,111))
    STEPPCDBG.append((36,112))
    STEPPCDBG.append((37,122))
    STEPPCDBG.append((38,132))
    STEPPCDBG.append((39,142))
    STEPPCDBG.append((40,152))
    STEPPCDBG.append((41,162))
    STEPPCDBG.append((42,172))
    STEPPCDBG.append((43,182))
    STEPPCDBG.append((44,192))
    STEPPCDBG.append((45,202))
    STEPPCDBG.append((46,212))
    STEPPCDBG.append((47,213))
    STEPPCDBG.append((48,223))
    STEPPCDBG.append((49,233))
    STEPPCDBG.append((50,243))
    STEPPCDBG.append((51,253))
    STEPPCDBG.append((52,263))
    STEPPCDBG.append((53,273))
    STEPPCDBG.append((54,283))
    STEPPCDBG.append((55,293))
    STEPPCDBG.append((56,303))
    STEPPCDBG.append((57,311))
    STEPPCDBG.append((58,312))
    STEPPCDBG.append((59,322))
    STEPPCDBG.append((60,332))
    STEPPCDBG.append((61,342))
    STEPPCDBG.append((62,352))
    STEPPCDBG.append((63,362))
    STEPPCDBG.append((64,372))
    STEPPCDBG.append((65,382))
    STEPPCDBG.append((66,392))
    STEPPCDBG.append((67,402))
    STEPPCDBG.append((68,412))
    STEPPCDBG.append((69,422))
    STEPPCDBG.append((70,432))
    STEPPCDBG.append((71,442))
    STEPPCDBG.append((72,450))
    STEPPCDBG.append((73,458))
    STEPPCDBG.append((74,466))
    STEPPCDBG.append((75,474))
    STEPPCDBG.append((76,482))
    STEPPCDBG.append((77,490))
    STEPPCDBG.append((78,498))
    STEPPCDBG.append((79,506))
    STEPPCDBG.append((80,514))
    STEPPCDBG.append((81,522))
    STEPPCDBG.append((82,530))
    STEPPCDBG.append((83,538))
    STEPPCDBG.append((84,546))
    STEPPCDBG.append((85,554))
    STEPPCDBG.append((86,562))
    STEPPCDBG.append((87,570))
    STEPPCDBG.append((88,578))
    STEPPCDBG.append((89,586))
    STEPPCDBG.append((90,594))
    STEPPCDBG.append((91,602))
    STEPPCDBG.append((92,610))
    STEPPCDBG.append((93,618))
    STEPPCDBG.append((94,626))
    STEPPCDBG.append((95,634))
    STEPPCDBG.append((96,642))
    STEPPCDBG.append((97,650))
    STEPPCDBG.append((98,658))
    STEPPCDBG.append((99,666))
    STEPPCDBG.append((100,674))
    STEPPCDBG.append((101,682))
    STEPPCDBG.append((102,690))
    STEPPCDBG.append((103,698))
    STEPPCDBG.append((104,706))
    STEPPCDBG.append((105,714))
    STEPPCDBG.append((106,720))
    STEPPCDBG.append((107,726))
    STEPPCDBG.append((108,732))
    STEPPCDBG.append((109,738))
    STEPPCDBG.append((110,744))
    STEPPCDBG.append((111,754))
    STEPPCDBG.append((112,764))
    STEPPCDBG.append((113,784))
    STEPPCDBG.append((114,796))
    STEPPCDBG.append((115,810))
    STEPPCDBG.append((117,824))
    STEPPCDBG.append((118,838))
    STEPPCDBG.append((119,852))
    STEPPCDBG.append((122,853))
    STEPPCDBG.append((123,859))
    STEPPCDBG.append((126,860))
    STEPPCDBG.append((127,866))
    STEPPCDBG.append((130,867))
    STEPPCDBG.append((131,873))
    STEPPCDBG.append((134,874))
    STEPPCDBG.append((135,880))
    STEPPCDBG.append((138,881))
    STEPPCDBG.append((140,883))
    STEPPCDBG.append((141,887))
    STEPPCDBG.append((143,889))
    STEPPCDBG.append((144,890))
    STEPPCDBG.append((145,892))
    STEPPCDBG.append((146,893))
    STEPPCDBG.append((147,894))
    STEPPCDBG.append((148,895))
    STEPPCDBG.append((150,898))
    STEPPCDBG.append((151,899))
    STEPPCDBG.append((152,901))
    STEPPCDBG.append((165,902))
    STEPPCDBG.append((168,903))
    STEPPCDBG.append((169,905))
    STEPPCDBG.append((170,907))
    STEPPCDBG.append((171,909))
    return((STEPCODE,STEPDATA,STEPPROCDBG,STEPDATDBG,STEPPCDBG))


def loadivm(vm):
    ivm = vm
    INSTEPCODE = []
    INSTEPDATA = []
    INSTEPPROCDBG = []
    INSTEPDATDBG = []
    INSTEPPCDBG = []
    # dumping dictionary 0 to 567,
    # 0 cmds, source testlib.stp
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (564,))) 	# load code record 0
    INSTEPCODE.append(DirectThreadedVM.STEP_HALT) 	# load code record 1
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTI) 	# load code record 2
    INSTEPCODE.append(iDirectThreadedVM.STEP_CRLF) 	# load code record 3
    INSTEPCODE.append(iDirectThreadedVM.STEP_RETURN) 	# load code record 4
    INSTEPCODE.append(iDirectThreadedVM.STEP_DUP) 	# load code record 5
    INSTEPCODE.append(iDirectThreadedVM.STEP_ZNEQ) 	# load code record 6
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_GOTO0, (12,))) 	# load code record 7
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTI) 	# load code record 8
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (0,))) 	# load code record 9
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 10
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_GOTO, (5,))) 	# load code record 11
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTI) 	# load code record 12
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (1,))) 	# load code record 13
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 14
    INSTEPCODE.append(iDirectThreadedVM.STEP_DS_DEPTH) 	# load code record 15
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 16
    INSTEPCODE.append(iDirectThreadedVM.STEP_RETURN) 	# load code record 17
    INSTEPCODE.append(iDirectThreadedVM.STEP_DECIMAL) 	# load code record 18
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (2,))) 	# load code record 19
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 20
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (-1,))) 	# load code record 21
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 22
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (3,))) 	# load code record 23
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 24
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (1,))) 	# load code record 25
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 26
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (4,))) 	# load code record 27
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 28
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (10,))) 	# load code record 29
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 30
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (5,))) 	# load code record 31
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 32
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (8,))) 	# load code record 33
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 34
    INSTEPCODE.append(iDirectThreadedVM.STEP_HEX) 	# load code record 35
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (6,))) 	# load code record 36
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 37
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (-1,))) 	# load code record 38
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 39
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (7,))) 	# load code record 40
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 41
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (1,))) 	# load code record 42
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 43
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (8,))) 	# load code record 44
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 45
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (10,))) 	# load code record 46
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 47
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (9,))) 	# load code record 48
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 49
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (8,))) 	# load code record 50
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 51
    INSTEPCODE.append(iDirectThreadedVM.STEP_OCTAL) 	# load code record 52
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (10,))) 	# load code record 53
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 54
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (-1,))) 	# load code record 55
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 56
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (11,))) 	# load code record 57
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 58
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (1,))) 	# load code record 59
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 60
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (12,))) 	# load code record 61
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 62
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (8,))) 	# load code record 63
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 64
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (13,))) 	# load code record 65
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 66
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (10,))) 	# load code record 67
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 68
    INSTEPCODE.append(iDirectThreadedVM.STEP_DECIMAL) 	# load code record 69
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (14,))) 	# load code record 70
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 71
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (20,))) 	# load code record 72
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (5,))) 	# load code record 73
    INSTEPCODE.append(iDirectThreadedVM.STEP_ADD) 	# load code record 74
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 75
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (15,))) 	# load code record 76
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 77
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (20,))) 	# load code record 78
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (-5,))) 	# load code record 79
    INSTEPCODE.append(iDirectThreadedVM.STEP_ADD) 	# load code record 80
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 81
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (16,))) 	# load code record 82
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 83
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (20,))) 	# load code record 84
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (5,))) 	# load code record 85
    INSTEPCODE.append(iDirectThreadedVM.STEP_SUB) 	# load code record 86
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 87
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (17,))) 	# load code record 88
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 89
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (20,))) 	# load code record 90
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (-5,))) 	# load code record 91
    INSTEPCODE.append(iDirectThreadedVM.STEP_SUB) 	# load code record 92
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 93
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (18,))) 	# load code record 94
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 95
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (20,))) 	# load code record 96
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (5,))) 	# load code record 97
    INSTEPCODE.append(iDirectThreadedVM.STEP_MULT) 	# load code record 98
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 99
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (19,))) 	# load code record 100
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 101
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (20,))) 	# load code record 102
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (-5,))) 	# load code record 103
    INSTEPCODE.append(iDirectThreadedVM.STEP_MULT) 	# load code record 104
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 105
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (20,))) 	# load code record 106
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 107
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (20,))) 	# load code record 108
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (5,))) 	# load code record 109
    INSTEPCODE.append(iDirectThreadedVM.STEP_DIV) 	# load code record 110
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 111
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (21,))) 	# load code record 112
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 113
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (20,))) 	# load code record 114
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (-5,))) 	# load code record 115
    INSTEPCODE.append(iDirectThreadedVM.STEP_DIV) 	# load code record 116
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 117
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (22,))) 	# load code record 118
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 119
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (20,))) 	# load code record 120
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (5,))) 	# load code record 121
    INSTEPCODE.append(iDirectThreadedVM.STEP_MOD) 	# load code record 122
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 123
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (23,))) 	# load code record 124
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 125
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (20,))) 	# load code record 126
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (3,))) 	# load code record 127
    INSTEPCODE.append(iDirectThreadedVM.STEP_MOD) 	# load code record 128
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 129
    INSTEPCODE.append(iDirectThreadedVM.STEP_HEX) 	# load code record 130
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (24,))) 	# load code record 131
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 132
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (4294901760,))) 	# load code record 133
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (4042322160,))) 	# load code record 134
    INSTEPCODE.append(iDirectThreadedVM.STEP_BITAND) 	# load code record 135
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 136
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (25,))) 	# load code record 137
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 138
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (4294901760,))) 	# load code record 139
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (4042322160,))) 	# load code record 140
    INSTEPCODE.append(iDirectThreadedVM.STEP_BITOR) 	# load code record 141
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 142
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (26,))) 	# load code record 143
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 144
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (4294901760,))) 	# load code record 145
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (4042322160,))) 	# load code record 146
    INSTEPCODE.append(iDirectThreadedVM.STEP_BITXOR) 	# load code record 147
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 148
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (27,))) 	# load code record 149
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 150
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (4294901760,))) 	# load code record 151
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (3,))) 	# load code record 152
    INSTEPCODE.append(iDirectThreadedVM.STEP_SHL) 	# load code record 153
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 154
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (28,))) 	# load code record 155
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 156
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (4294901760,))) 	# load code record 157
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (5,))) 	# load code record 158
    INSTEPCODE.append(iDirectThreadedVM.STEP_SHR) 	# load code record 159
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 160
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (29,))) 	# load code record 161
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 162
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (4042322160,))) 	# load code record 163
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (3,))) 	# load code record 164
    INSTEPCODE.append(iDirectThreadedVM.STEP_LROT) 	# load code record 165
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 166
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (30,))) 	# load code record 167
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 168
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (4042322160,))) 	# load code record 169
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (3,))) 	# load code record 170
    INSTEPCODE.append(iDirectThreadedVM.STEP_RROT) 	# load code record 171
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 172
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (31,))) 	# load code record 173
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 174
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (4042322160,))) 	# load code record 175
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (3,))) 	# load code record 176
    INSTEPCODE.append(iDirectThreadedVM.STEP_LROT16) 	# load code record 177
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 178
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (32,))) 	# load code record 179
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 180
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (4042322160,))) 	# load code record 181
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (3,))) 	# load code record 182
    INSTEPCODE.append(iDirectThreadedVM.STEP_RROT16) 	# load code record 183
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 184
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (33,))) 	# load code record 185
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 186
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (4042322160,))) 	# load code record 187
    INSTEPCODE.append(iDirectThreadedVM.STEP_COMPLEMENT) 	# load code record 188
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 189
    INSTEPCODE.append(iDirectThreadedVM.STEP_DECIMAL) 	# load code record 190
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (34,))) 	# load code record 191
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 192
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (20,))) 	# load code record 193
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (1,))) 	# load code record 194
    INSTEPCODE.append(iDirectThreadedVM.STEP_LOGAND) 	# load code record 195
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 196
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (35,))) 	# load code record 197
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 198
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (20,))) 	# load code record 199
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (0,))) 	# load code record 200
    INSTEPCODE.append(iDirectThreadedVM.STEP_LOGAND) 	# load code record 201
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 202
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (36,))) 	# load code record 203
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 204
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (20,))) 	# load code record 205
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (1,))) 	# load code record 206
    INSTEPCODE.append(iDirectThreadedVM.STEP_LOGOR) 	# load code record 207
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 208
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (37,))) 	# load code record 209
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 210
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (20,))) 	# load code record 211
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (0,))) 	# load code record 212
    INSTEPCODE.append(iDirectThreadedVM.STEP_LOGOR) 	# load code record 213
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 214
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (38,))) 	# load code record 215
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 216
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (20,))) 	# load code record 217
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (1,))) 	# load code record 218
    INSTEPCODE.append(iDirectThreadedVM.STEP_GT) 	# load code record 219
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 220
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (39,))) 	# load code record 221
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 222
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (20,))) 	# load code record 223
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (-11,))) 	# load code record 224
    INSTEPCODE.append(iDirectThreadedVM.STEP_LT) 	# load code record 225
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 226
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (40,))) 	# load code record 227
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 228
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (20,))) 	# load code record 229
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (20,))) 	# load code record 230
    INSTEPCODE.append(iDirectThreadedVM.STEP_EQ) 	# load code record 231
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 232
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (41,))) 	# load code record 233
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 234
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (20,))) 	# load code record 235
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (1,))) 	# load code record 236
    INSTEPCODE.append(iDirectThreadedVM.STEP_GE) 	# load code record 237
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 238
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (42,))) 	# load code record 239
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 240
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (20,))) 	# load code record 241
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (-11,))) 	# load code record 242
    INSTEPCODE.append(iDirectThreadedVM.STEP_LE) 	# load code record 243
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 244
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (43,))) 	# load code record 245
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 246
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (20,))) 	# load code record 247
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (20,))) 	# load code record 248
    INSTEPCODE.append(iDirectThreadedVM.STEP_GE) 	# load code record 249
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 250
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (44,))) 	# load code record 251
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 252
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (20,))) 	# load code record 253
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (20,))) 	# load code record 254
    INSTEPCODE.append(iDirectThreadedVM.STEP_LE) 	# load code record 255
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 256
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (45,))) 	# load code record 257
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 258
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (20,))) 	# load code record 259
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (20,))) 	# load code record 260
    INSTEPCODE.append(iDirectThreadedVM.STEP_NEQ) 	# load code record 261
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 262
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (46,))) 	# load code record 263
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 264
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (20,))) 	# load code record 265
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (21,))) 	# load code record 266
    INSTEPCODE.append(iDirectThreadedVM.STEP_NEQ) 	# load code record 267
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 268
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (47,))) 	# load code record 269
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 270
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (100,))) 	# load code record 271
    INSTEPCODE.append(iDirectThreadedVM.STEP_MINUS) 	# load code record 272
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 273
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (48,))) 	# load code record 274
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 275
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (-100,))) 	# load code record 276
    INSTEPCODE.append(iDirectThreadedVM.STEP_MINUS) 	# load code record 277
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 278
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (49,))) 	# load code record 279
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 280
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (100,))) 	# load code record 281
    INSTEPCODE.append(iDirectThreadedVM.STEP_SIGN) 	# load code record 282
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 283
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (50,))) 	# load code record 284
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 285
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (-100,))) 	# load code record 286
    INSTEPCODE.append(iDirectThreadedVM.STEP_SIGN) 	# load code record 287
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 288
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (51,))) 	# load code record 289
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 290
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (0,))) 	# load code record 291
    INSTEPCODE.append(iDirectThreadedVM.STEP_SIGN) 	# load code record 292
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 293
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (52,))) 	# load code record 294
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 295
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (100,))) 	# load code record 296
    INSTEPCODE.append(iDirectThreadedVM.STEP_ABS) 	# load code record 297
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 298
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (53,))) 	# load code record 299
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 300
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (-100,))) 	# load code record 301
    INSTEPCODE.append(iDirectThreadedVM.STEP_ABS) 	# load code record 302
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 303
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (54,))) 	# load code record 304
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 305
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (0,))) 	# load code record 306
    INSTEPCODE.append(iDirectThreadedVM.STEP_ABS) 	# load code record 307
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 308
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (55,))) 	# load code record 309
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 310
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (1,))) 	# load code record 311
    INSTEPCODE.append(iDirectThreadedVM.STEP_ZEQ) 	# load code record 312
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 313
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (56,))) 	# load code record 314
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 315
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (0,))) 	# load code record 316
    INSTEPCODE.append(iDirectThreadedVM.STEP_ZEQ) 	# load code record 317
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 318
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (57,))) 	# load code record 319
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 320
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (-1,))) 	# load code record 321
    INSTEPCODE.append(iDirectThreadedVM.STEP_ZEQ) 	# load code record 322
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 323
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (58,))) 	# load code record 324
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 325
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (1,))) 	# load code record 326
    INSTEPCODE.append(iDirectThreadedVM.STEP_ZNEQ) 	# load code record 327
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 328
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (59,))) 	# load code record 329
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 330
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (0,))) 	# load code record 331
    INSTEPCODE.append(iDirectThreadedVM.STEP_ZNEQ) 	# load code record 332
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 333
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (60,))) 	# load code record 334
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 335
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (-1,))) 	# load code record 336
    INSTEPCODE.append(iDirectThreadedVM.STEP_ZNEQ) 	# load code record 337
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 338
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (61,))) 	# load code record 339
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 340
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (1,))) 	# load code record 341
    INSTEPCODE.append(iDirectThreadedVM.STEP_ZLT) 	# load code record 342
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 343
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (62,))) 	# load code record 344
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 345
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (0,))) 	# load code record 346
    INSTEPCODE.append(iDirectThreadedVM.STEP_ZLT) 	# load code record 347
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 348
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (63,))) 	# load code record 349
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 350
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (-1,))) 	# load code record 351
    INSTEPCODE.append(iDirectThreadedVM.STEP_ZLT) 	# load code record 352
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 353
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (64,))) 	# load code record 354
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 355
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (1,))) 	# load code record 356
    INSTEPCODE.append(iDirectThreadedVM.STEP_ZGT) 	# load code record 357
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 358
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (65,))) 	# load code record 359
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 360
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (0,))) 	# load code record 361
    INSTEPCODE.append(iDirectThreadedVM.STEP_ZGT) 	# load code record 362
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 363
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (66,))) 	# load code record 364
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 365
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (-1,))) 	# load code record 366
    INSTEPCODE.append(iDirectThreadedVM.STEP_ZGT) 	# load code record 367
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 368
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (67,))) 	# load code record 369
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 370
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (1,))) 	# load code record 371
    INSTEPCODE.append(iDirectThreadedVM.STEP_ZGE) 	# load code record 372
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 373
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (68,))) 	# load code record 374
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 375
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (0,))) 	# load code record 376
    INSTEPCODE.append(iDirectThreadedVM.STEP_ZGE) 	# load code record 377
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 378
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (69,))) 	# load code record 379
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 380
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (-1,))) 	# load code record 381
    INSTEPCODE.append(iDirectThreadedVM.STEP_ZGE) 	# load code record 382
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 383
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (70,))) 	# load code record 384
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 385
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (1,))) 	# load code record 386
    INSTEPCODE.append(iDirectThreadedVM.STEP_ZLE) 	# load code record 387
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 388
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (71,))) 	# load code record 389
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 390
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (0,))) 	# load code record 391
    INSTEPCODE.append(iDirectThreadedVM.STEP_ZLE) 	# load code record 392
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 393
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (72,))) 	# load code record 394
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 395
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (-1,))) 	# load code record 396
    INSTEPCODE.append(iDirectThreadedVM.STEP_ZLE) 	# load code record 397
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 398
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (73,))) 	# load code record 399
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 400
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (-1,))) 	# load code record 401
    INSTEPCODE.append(iDirectThreadedVM.STEP_ADD1) 	# load code record 402
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 403
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (74,))) 	# load code record 404
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 405
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (-1,))) 	# load code record 406
    INSTEPCODE.append(iDirectThreadedVM.STEP_SUB1) 	# load code record 407
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 408
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (75,))) 	# load code record 409
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 410
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (-1,))) 	# load code record 411
    INSTEPCODE.append(iDirectThreadedVM.STEP_ADD2) 	# load code record 412
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 413
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (76,))) 	# load code record 414
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 415
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (-1,))) 	# load code record 416
    INSTEPCODE.append(iDirectThreadedVM.STEP_SUB2) 	# load code record 417
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 418
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (77,))) 	# load code record 419
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 420
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (-1,))) 	# load code record 421
    INSTEPCODE.append(iDirectThreadedVM.STEP_MULT2) 	# load code record 422
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 423
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (78,))) 	# load code record 424
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 425
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (-1,))) 	# load code record 426
    INSTEPCODE.append(iDirectThreadedVM.STEP_DIV2) 	# load code record 427
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 428
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (79,))) 	# load code record 429
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 430
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (9,))) 	# load code record 431
    INSTEPCODE.append(iDirectThreadedVM.STEP_SHL1) 	# load code record 432
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 433
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (80,))) 	# load code record 434
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 435
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (9,))) 	# load code record 436
    INSTEPCODE.append(iDirectThreadedVM.STEP_SHR1) 	# load code record 437
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 438
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (81,))) 	# load code record 439
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 440
    INSTEPCODE.append(iDirectThreadedVM.STEP_SIZEOF) 	# load code record 441
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 442
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (82,))) 	# load code record 443
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 444
    INSTEPCODE.append(iDirectThreadedVM.STEP_DS_DEPTH) 	# load code record 445
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 446
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (83,))) 	# load code record 447
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 448
    INSTEPCODE.append(iDirectThreadedVM.STEP_TS_DEPTH) 	# load code record 449
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 450
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (84,))) 	# load code record 451
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 452
    INSTEPCODE.append(iDirectThreadedVM.STEP_CODE_DICT_LEN) 	# load code record 453
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 454
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (85,))) 	# load code record 455
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 456
    INSTEPCODE.append(iDirectThreadedVM.STEP_DATA_DICT_LEN) 	# load code record 457
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (2,))) 	# load code record 458
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (86,))) 	# load code record 459
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 460
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (0,))) 	# load code record 461
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (10,))) 	# load code record 462
    INSTEPCODE.append(iDirectThreadedVM.STEP_DUP) 	# load code record 463
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (5,))) 	# load code record 464
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (87,))) 	# load code record 465
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 466
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (0,))) 	# load code record 467
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (10,))) 	# load code record 468
    INSTEPCODE.append(iDirectThreadedVM.STEP_DUP2) 	# load code record 469
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (5,))) 	# load code record 470
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (88,))) 	# load code record 471
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 472
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (0,))) 	# load code record 473
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (10,))) 	# load code record 474
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (20,))) 	# load code record 475
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (30,))) 	# load code record 476
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (40,))) 	# load code record 477
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (50,))) 	# load code record 478
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (2,))) 	# load code record 479
    INSTEPCODE.append(iDirectThreadedVM.STEP_DUP_I) 	# load code record 480
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (5,))) 	# load code record 481
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (89,))) 	# load code record 482
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 483
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (0,))) 	# load code record 484
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (10,))) 	# load code record 485
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (20,))) 	# load code record 486
    INSTEPCODE.append(iDirectThreadedVM.STEP_SWAP) 	# load code record 487
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (5,))) 	# load code record 488
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (90,))) 	# load code record 489
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 490
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (0,))) 	# load code record 491
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (10,))) 	# load code record 492
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (20,))) 	# load code record 493
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (30,))) 	# load code record 494
    INSTEPCODE.append(iDirectThreadedVM.STEP_OVER) 	# load code record 495
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (5,))) 	# load code record 496
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (91,))) 	# load code record 497
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 498
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (0,))) 	# load code record 499
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (10,))) 	# load code record 500
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (20,))) 	# load code record 501
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (30,))) 	# load code record 502
    INSTEPCODE.append(iDirectThreadedVM.STEP_OVER2) 	# load code record 503
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (5,))) 	# load code record 504
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (92,))) 	# load code record 505
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 506
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (0,))) 	# load code record 507
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (10,))) 	# load code record 508
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (20,))) 	# load code record 509
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (30,))) 	# load code record 510
    INSTEPCODE.append(iDirectThreadedVM.STEP_DROP) 	# load code record 511
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (5,))) 	# load code record 512
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (93,))) 	# load code record 513
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 514
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (0,))) 	# load code record 515
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (10,))) 	# load code record 516
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (20,))) 	# load code record 517
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (30,))) 	# load code record 518
    INSTEPCODE.append(iDirectThreadedVM.STEP_DROP2) 	# load code record 519
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (5,))) 	# load code record 520
    INSTEPCODE.append(iDirectThreadedVM.STEP_RETURN) 	# load code record 521
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (94,))) 	# load code record 522
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 523
    INSTEPCODE.append(iDirectThreadedVM.STEP_DUP) 	# load code record 524
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTI) 	# load code record 525
    INSTEPCODE.append(iDirectThreadedVM.STEP_CRLF) 	# load code record 526
    INSTEPCODE.append(iDirectThreadedVM.STEP_RETURN) 	# load code record 527
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (95,))) 	# load code record 528
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 529
    INSTEPCODE.append(iDirectThreadedVM.STEP_DUP) 	# load code record 530
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTI) 	# load code record 531
    INSTEPCODE.append(iDirectThreadedVM.STEP_CRLF) 	# load code record 532
    INSTEPCODE.append(iDirectThreadedVM.STEP_RETURN) 	# load code record 533
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (96,))) 	# load code record 534
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 535
    INSTEPCODE.append(iDirectThreadedVM.STEP_DUP) 	# load code record 536
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTI) 	# load code record 537
    INSTEPCODE.append(iDirectThreadedVM.STEP_CRLF) 	# load code record 538
    INSTEPCODE.append(iDirectThreadedVM.STEP_RETURN) 	# load code record 539
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_VAR, (97,))) 	# load code record 540
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTS) 	# load code record 541
    INSTEPCODE.append(iDirectThreadedVM.STEP_DUP) 	# load code record 542
    INSTEPCODE.append(iDirectThreadedVM.STEP_PRINTI) 	# load code record 543
    INSTEPCODE.append(iDirectThreadedVM.STEP_CRLF) 	# load code record 544
    INSTEPCODE.append(iDirectThreadedVM.STEP_RETURN) 	# load code record 545
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (-1,))) 	# load code record 546
    INSTEPCODE.append(iDirectThreadedVM.STEP_DUP) 	# load code record 547
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (7,))) 	# load code record 548
    INSTEPCODE.append(iDirectThreadedVM.STEP_LT) 	# load code record 549
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_GOTO0, (562,))) 	# load code record 550
    INSTEPCODE.append(iDirectThreadedVM.STEP_DUP) 	# load code record 551
    INSTEPCODE.append(DirectThreadedVM.STEP_GOTOX) 	# load code record 552
    INSTEPCODE.append(4) 	# load code record 553
    INSTEPCODE.append(522) 	# load code record 554
    INSTEPCODE.append(528) 	# load code record 555
    INSTEPCODE.append(534) 	# load code record 556
    INSTEPCODE.append(540) 	# load code record 557
    INSTEPCODE.append(DirectThreadedVM.STEP_CALL_SECONDARY) 	# load code record 558
    INSTEPCODE.append(0) 	# load code record 559
    INSTEPCODE.append(iDirectThreadedVM.STEP_ADD1) 	# load code record 560
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_GOTO, (547,))) 	# load code record 561
    INSTEPCODE.append(iDirectThreadedVM.STEP_DROP) 	# load code record 562
    INSTEPCODE.append(iDirectThreadedVM.STEP_RETURN) 	# load code record 563
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (18,))) 	# load code record 564
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CALL_SECONDARY, (546,))) 	# load code record 565
    INSTEPCODE.append(ivm.intern(ivm.incomplete_STEP_CONST, (0,))) 	# load code record 566
    INSTEPCODE.append(iDirectThreadedVM.STEP_RETURN) 	# load code record 567
    INSTEPDATA.append(' ') 	# load data record 0
    INSTEPDATA.append(', stack at ') 	# load data record 1
    INSTEPDATA.append('constant -1 as decimal yields ') 	# load data record 2
    INSTEPDATA.append('constant 1 as decimal yields ') 	# load data record 3
    INSTEPDATA.append('constant 0xa as decimal yields ') 	# load data record 4
    INSTEPDATA.append('constant 010 as decimal yields ') 	# load data record 5
    INSTEPDATA.append('constant -1 as hex yields ') 	# load data record 6
    INSTEPDATA.append('constant 1 as hex yields ') 	# load data record 7
    INSTEPDATA.append('constant 0xa as hex yields ') 	# load data record 8
    INSTEPDATA.append('constant 010 as hex yields ') 	# load data record 9
    INSTEPDATA.append('constant -1 as octal yields ') 	# load data record 10
    INSTEPDATA.append('constant 1 as octal yields ') 	# load data record 11
    INSTEPDATA.append('constant 010 as octal yields ') 	# load data record 12
    INSTEPDATA.append('constant 0xa as octal yields ') 	# load data record 13
    INSTEPDATA.append('20 5 + yields ') 	# load data record 14
    INSTEPDATA.append('20 -5 + yields ') 	# load data record 15
    INSTEPDATA.append('20 5 - yields ') 	# load data record 16
    INSTEPDATA.append('20 -5 - yields ') 	# load data record 17
    INSTEPDATA.append('20 5 * yields ') 	# load data record 18
    INSTEPDATA.append('20 -5 * yields ') 	# load data record 19
    INSTEPDATA.append('20 5 / yields ') 	# load data record 20
    INSTEPDATA.append('20 -5 / yields ') 	# load data record 21
    INSTEPDATA.append('20 5 % yields ') 	# load data record 22
    INSTEPDATA.append('20 3 % yields ') 	# load data record 23
    INSTEPDATA.append('0xffff0000 0xf0f0f0f0 & yields ') 	# load data record 24
    INSTEPDATA.append('0xffff0000 0xf0f0f0f0 | yields ') 	# load data record 25
    INSTEPDATA.append('0xffff0000 0xf0f0f0f0 ^ yields ') 	# load data record 26
    INSTEPDATA.append('0xffff0000 3 << yields ') 	# load data record 27
    INSTEPDATA.append('0xffff0000 5 >> yields ') 	# load data record 28
    INSTEPDATA.append('0xf0f0f0f0 3 lrot yields ') 	# load data record 29
    INSTEPDATA.append('0xf0f0f0f0 3 rrot yields ') 	# load data record 30
    INSTEPDATA.append('0xf0f0f0f0 3 lrot16 yields ') 	# load data record 31
    INSTEPDATA.append('0xf0f0f0f0 3 rrot16 yields ') 	# load data record 32
    INSTEPDATA.append('0xf0f0f0f0 ~ yields ') 	# load data record 33
    INSTEPDATA.append('20 1 && yields ') 	# load data record 34
    INSTEPDATA.append('20 0 && yields ') 	# load data record 35
    INSTEPDATA.append('20 1 || yields ') 	# load data record 36
    INSTEPDATA.append('20 0 || yields ') 	# load data record 37
    INSTEPDATA.append('20 1 > yields ') 	# load data record 38
    INSTEPDATA.append('20 -11 < yields ') 	# load data record 39
    INSTEPDATA.append('20 20 == yields ') 	# load data record 40
    INSTEPDATA.append('20 1 >= yields ') 	# load data record 41
    INSTEPDATA.append('20 -11 <= yields ') 	# load data record 42
    INSTEPDATA.append('20 20 >= yields ') 	# load data record 43
    INSTEPDATA.append('20 20 <= yields ') 	# load data record 44
    INSTEPDATA.append('20 20 != yields ') 	# load data record 45
    INSTEPDATA.append('20 21 != yields ') 	# load data record 46
    INSTEPDATA.append('100 minus yields ') 	# load data record 47
    INSTEPDATA.append('-100 minus yields ') 	# load data record 48
    INSTEPDATA.append('100 sign yields ') 	# load data record 49
    INSTEPDATA.append('-100 sign yields ') 	# load data record 50
    INSTEPDATA.append('0 sign yields ') 	# load data record 51
    INSTEPDATA.append('100 abs yields ') 	# load data record 52
    INSTEPDATA.append('-100 abs yields ') 	# load data record 53
    INSTEPDATA.append('0 abs yields ') 	# load data record 54
    INSTEPDATA.append('1 0== yields ') 	# load data record 55
    INSTEPDATA.append('0 0== yields ') 	# load data record 56
    INSTEPDATA.append('-1 0== yields ') 	# load data record 57
    INSTEPDATA.append('1 0!= yields ') 	# load data record 58
    INSTEPDATA.append('0 0!= yields ') 	# load data record 59
    INSTEPDATA.append('-1 0!= yields ') 	# load data record 60
    INSTEPDATA.append('1 0< yields ') 	# load data record 61
    INSTEPDATA.append('0 0< yields ') 	# load data record 62
    INSTEPDATA.append('-1 0< yields ') 	# load data record 63
    INSTEPDATA.append('1 0> yields ') 	# load data record 64
    INSTEPDATA.append('0 0> yields ') 	# load data record 65
    INSTEPDATA.append('-1 0> yields ') 	# load data record 66
    INSTEPDATA.append('1 0>= yields ') 	# load data record 67
    INSTEPDATA.append('0 0>= yields ') 	# load data record 68
    INSTEPDATA.append('-1 0>= yields ') 	# load data record 69
    INSTEPDATA.append('1 0<= yields ') 	# load data record 70
    INSTEPDATA.append('0 0<= yields ') 	# load data record 71
    INSTEPDATA.append('-1 0<= yields ') 	# load data record 72
    INSTEPDATA.append('-1 1+ yields ') 	# load data record 73
    INSTEPDATA.append('-1 1- yields ') 	# load data record 74
    INSTEPDATA.append('-1 2+ yields ') 	# load data record 75
    INSTEPDATA.append('-1 2- yields ') 	# load data record 76
    INSTEPDATA.append('-1 2* yields ') 	# load data record 77
    INSTEPDATA.append('-1 2/ yields ') 	# load data record 78
    INSTEPDATA.append('9 1<< yields ') 	# load data record 79
    INSTEPDATA.append('9 1>> yields ') 	# load data record 80
    INSTEPDATA.append('sizeof_word is ') 	# load data record 81
    INSTEPDATA.append('ds_depth is ') 	# load data record 82
    INSTEPDATA.append('ts_depth is ') 	# load data record 83
    INSTEPDATA.append('code_dict_len is ') 	# load data record 84
    INSTEPDATA.append('data_dict_len is ') 	# load data record 85
    INSTEPDATA.append('0 10 dup yields ') 	# load data record 86
    INSTEPDATA.append('0 10 dup2 yields ') 	# load data record 87
    INSTEPDATA.append('0 10 20 30 40 50 2 dupi yields ') 	# load data record 88
    INSTEPDATA.append('0 10 20 swap yields ') 	# load data record 89
    INSTEPDATA.append('0 10 20 30 over yields ') 	# load data record 90
    INSTEPDATA.append('0 10 20 30 over2 yields ') 	# load data record 91
    INSTEPDATA.append('0 10 20 30 drop yields ') 	# load data record 92
    INSTEPDATA.append('0 10 20 30 drop2 yields ') 	# load data record 93
    INSTEPDATA.append('inside s_proc0 on index ') 	# load data record 94
    INSTEPDATA.append('inside s_proc1 on index ') 	# load data record 95
    INSTEPDATA.append('inside s_proc2 on index ') 	# load data record 96
    INSTEPDATA.append('inside s_proc3 on index ') 	# load data record 97
    INSTEPPROCDBG.append(('.',2))
    INSTEPPROCDBG.append(('dumpds',5))
    INSTEPPROCDBG.append(('testmath',18))
    INSTEPPROCDBG.append(('s_proc0',522))
    INSTEPPROCDBG.append(('s_proc1',528))
    INSTEPPROCDBG.append(('s_proc2',534))
    INSTEPPROCDBG.append(('s_proc3',540))
    INSTEPPROCDBG.append(('testswitch',546))
    INSTEPPROCDBG.append(('main',564))
    INSTEPPCDBG.append('/export/home/faculty/parson/private/csc526/solutions/vectors2/vm_in_python/testlib.stp')
    return((INSTEPCODE,INSTEPDATA,INSTEPPROCDBG,INSTEPDATDBG,INSTEPPCDBG))
