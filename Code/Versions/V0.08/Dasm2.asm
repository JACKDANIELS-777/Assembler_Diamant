FOR (rax+1,%rbx=^:([10]<-rdx)%,1)rax=10rbx=10
;Disassembly:
;0:  48 89 54 24 0a          mov    QWORD PTR [rsp+0xa],rdx
;5:  48 89 d3                mov    rbx,rdx
;8:  48 83 c0 01             add    rax,0x1
;c:  48 89 d8                mov    rax,rbx
;f:  48 83 f8 01             cmp    rax,0x1
;13: 0f 8d 09 00 00 00       jge    0x22
;19: 48 83 c0 01             add    rax,0x1
;1d: e9 f1 ff ff ff          jmp    0x13
;22: 48 bb 0a 00 00 00 00    movabs rbx,0xa
;29: 00 00 00
