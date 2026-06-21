FOR (rax+1,%rbx=10%,rcx+1)rax=10rbx=10
;48 BB 0A 00 00 00 00 00 00 00 48 83 C1 01 48 83 C0 01 48 89 D8 48 39 C8 0F 8D 09 00 00 00 48 83 C0 01 E9 F1 FF FF FF 48 BB 0A 00 00 00 00 00 00 00
;Disassembly:
;0:  48 bb 0a 00 00 00 00    movabs rbx,0xa
;7:  00 00 00 
;a:  48 83 c1 01             add    rcx,0x1
;e:  48 83 c0 01             add    rax,0x1
;12: 48 89 d8                mov    rax,rbx
;15: 48 39 c8                cmp    rax,rcx
;18: 0f 8d 09 00 00 00       jge    0x27
;1e: 48 83 c0 01             add    rax,0x1
;22: e9 f1 ff ff ff          jmp    0x18
;27: 48 bb 0a 00 00 00 00    movabs rbx,0xa
;2e: 00 00 00
