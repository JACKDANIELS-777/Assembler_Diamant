rax=0
while rax<=9 rax+=1
;Disassembly:
;0:  48 b8 00 00 00 00 00    movabs rax,0x0
;7:  00 00 00 
;a:  48 83 f8 09             cmp    rax,0x9
;e:  7f 06                   jg     0x16
;10: 48 83 c0 01             add    rax,0x1
;14: eb f4                   jmp    0xa
