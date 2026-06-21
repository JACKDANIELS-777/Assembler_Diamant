FUN a (): rbx rax=10
rax=1+%a()%
;Disassembly:
;0:  e8 07 00 00 00          call   0xc
;5:  48 83 c3 01             add    rbx,0x1
;9:  48 89 d8                mov    rax,rbx
;c:  55                      push   rbp
;d:  48 89 e5                mov    rbp,rsp
;10: 48 b8 0a 00 00 00 00    movabs rax,0xa
;17: 00 00 00 
;1a: 5d                      pop    rbp
;1b: c3                      ret
