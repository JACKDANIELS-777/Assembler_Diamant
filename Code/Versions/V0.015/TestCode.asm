rax=9+9+9+rax+rbx+1+rcx+rdx+9+10+11
--output
Disassembly:
0:  48 83 c0 1b             add    rax,0x1b
4:  48 01 c3                add    rbx,rax
7:  48 83 c3 01             add    rbx,0x1
b:  48 01 cb                add    rbx,rcx
e:  48 01 da                add    rdx,rbx
11: 48 83 c2 09             add    rdx,0x9
15: 48 83 c2 0a             add    rdx,0xa
19: 48 83 c2 0b             add    rdx,0xb
1d: 48 89 d0                mov    rax,rdx

