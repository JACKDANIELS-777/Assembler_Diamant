FUN a (): rbx+10 rax=10
rax=1+%a()%
;Disassembly:
;0:  e8 0b 00 00 00          call   0x10
;5:  48 83 c3 0a             add    rbx,0xa
;9:  48 83 c3 01             add    rbx,0x1
;d:  48 89 d8                mov    rax,rbx
;10: 55                      push   rbp
;11: 48 89 e5                mov    rbp,rsp
;14: 48 b8 0a 00 00 00 00    movabs rax,0xa
;1b: 00 00 00 
;1e: 5d                      pop    rbp
;1f: c3                      ret
