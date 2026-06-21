FUN a () rax=10
a()
rax=10
;Disassembly:
;0:  e8 0a 00 00 00          call   0xf
;5:  48 b8 0a 00 00 00 00    movabs rax,0xa
;c:  00 00 00 
;f:  55                      push   rbp
;10: 48 89 e5                mov    rbp,rsp
;13: 48 b8 0a 00 00 00 00    movabs rax,0xa
;1a: 00 00 00 
;1d: 5d                      pop    rbp
;1e: c3                      ret
