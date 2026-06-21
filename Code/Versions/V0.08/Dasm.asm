FOR (rax+1,1,1) {rax=10,rax=10}
;Disassembly:
;0:  48 83 c0 01             add    rax,0x1
;4:  48 b8 01 00 00 00 00    movabs rax,0x1
;b:  00 00 00 
;e:  48 83 f8 01             cmp    rax,0x1
;12: 0f 8d 1d 00 00 00       jge    0x35
;18: 48 b8 0a 00 00 00 00    movabs rax,0xa
;1f: 00 00 00 
;22: 48 b8 0a 00 00 00 00    movabs rax,0xa
;29: 00 00 00 
;2c: 48 83 c0 01             add    rax,0x1
;30: e9 dd ff ff ff          jmp    0x12
;35: 48 bb 0a 00 00 00 00    movabs rbx,0xa
;3c: 00 00 00
FOR (%FOR (rax+1,1,1) {rax=10,rax=10}%,1,1) {rax=10,rax=10}
;Disassembly:
;0:  48 83 c0 01             add    rax,0x1
;4:  48 b8 01 00 00 00 00    movabs rax,0x1
;b:  00 00 00 
;e:  48 83 f8 01             cmp    rax,0x1
;12: 0f 8d 1d 00 00 00       jge    0x35
;18: 48 b8 0a 00 00 00 00    movabs rax,0xa
;1f: 00 00 00 
;22: 48 b8 0a 00 00 00 00    movabs rax,0xa
;29: 00 00 00 
;2c: 48 83 c0 01             add    rax,0x1
;30: e9 dd ff ff ff          jmp    0x12
;35: 48 b8 01 00 00 00 00    movabs rax,0x1
;3c: 00 00 00 
;3f: 48 83 f8 01             cmp    rax,0x1
;43: 0f 8d 1d 00 00 00       jge    0x66
;49: 48 b8 0a 00 00 00 00    movabs rax,0xa
;50: 00 00 00 
;53: 48 b8 0a 00 00 00 00    movabs rax,0xa
;5a: 00 00 00 
;5d: 48 83 c0 01             add    rax,0x1
;61: e9 dd ff ff ff          jmp    0x43
;66: 48 bb 0a 00 00 00 00    movabs rbx,0xa
;6d: 00 00 00
