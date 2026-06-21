FOR (rax+1,%rbx=^:([10]<-%rdx=%FOR (rax+1,1,1) {rax=10,rax=10}%%)%,1)rax=10rbx=10
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
;35: 48 89 c2                mov    rdx,rax
;38: 48 89 54 24 0a          mov    QWORD PTR [rsp+0xa],rdx
;3d: 48 89 d3                mov    rbx,rdx
;40: 48 83 c0 01             add    rax,0x1
;44: 48 89 d8                mov    rax,rbx
;47: 48 83 f8 01             cmp    rax,0x1
;4b: 0f 8d 09 00 00 00       jge    0x5a
;51: 48 83 c0 01             add    rax,0x1
;55: e9 f1 ff ff ff          jmp    0x4b
;5a: 48 bb 0a 00 00 00 00    movabs rbx,0xa
;61: 00 00 00
