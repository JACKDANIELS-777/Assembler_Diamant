rax=^:rbx
rax=^:([0]<-rbx)
rax=v:([0]->rbx)

;Intended Disassembly
;Disassembly:
;0:  53                      push   rbx
;1:  48 89 d8                mov    rax,rbx
;4:  48 89 5c 24 00          mov    QWORD PTR [rsp+0x0],rbx
;9:  48 89 d8                mov    rax,rbx
;c:  48 8b 5c 24 00          mov    rbx,QWORD PTR [rsp+0x0]
;11: 48 89 d8                mov    rax,rbx
