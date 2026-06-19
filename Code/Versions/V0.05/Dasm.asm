rax=v:([18*10]->^:(rbx+1)+2)+3 
;Disassembly:
;0:  48 83 c3 01             add    rbx,0x1
;4:  53                      push   rbx
;5:  48 83 c3 02             add    rbx,0x2
;9:  48 8b 9c 24 b4 00 00    mov    rbx,QWORD PTR [rsp+0xb4]
;10: 00 
;11: 48 83 c3 03             add    rbx,0x3
;15: 48 89 d8                mov    rax,rbx
