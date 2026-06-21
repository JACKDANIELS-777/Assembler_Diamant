;Simple moves into each register
;Keep in mind you can also do rax=1\nrbx=1 ie
;rax=1
;rbx=1 etc 
rax=1rcx=1rdx=1rbx=1rsi=1rdi=1rsp=1rbp=1r8=1r9=1r10=1r11=1r12=1r13=1r14=1r15=1eax=1ecx=1edx=1ebx=1esi=1edi=1esp=1ebp=1r8d=1r9d=1r10d=1r11d=1r12d=1r13d=1r14d=1r15d=1ax=1cx=1dx=1bx=1si=1di=1sp=1bp=1r8w=1r9w=1r10w=1r11w=1r12w=1r13w=1r14w=1r15w=1al=1cl=1dl=1bl=1sil=1dil=1spl=1bpl=1r8b=1r9b=1r10b=1r11b=1r12b=1r13b=1r14b=1r15b=1ah=1ch=1dh=1bh=1
;48 B8 01 00 00 00 00 00 00 00 48 B9 01 00 00 00 00 00 00 00 48 BA 01 00 00 00 00 00 00 00 48 BB 01 00 00 00 00 00 00 00 48 BE 01 00 00 00 00 00 00 00 48 BF 01 00 00 00 00 00 00 00 48 BC 01 00 00 00 00 00 00 00 48 BD 01 00 00 00 00 00 00 00 49 B8 01 00 00 00 00 00 00 00 49 B9 01 00 00 00 00 00 00 00 49 BA 01 00 00 00 00 00 00 00 49 BB 01 00 00 00 00 00 00 00 49 BC 01 00 00 00 00 00 00 00 49 BD 01 00 00 00 00 00 00 00 49 BE 01 00 00 00 00 00 00 00 49 BF 01 00 00 00 00 00 00 00 B8 01 00 00 00 B9 01 00 00 00 BA 01 00 00 00 BB 01 00 00 00 BE 01 00 00 00 BF 01 00 00 00 BC 01 00 00 00 BD 01 00 00 00 41 B8 01 00 00 00 41 B9 01 00 00 00 41 BA 01 00 00 00 41 BB 01 00 00 00 41 BC 01 00 00 00 41 BD 01 00 00 00 41 BE 01 00 00 00 41 BF 01 00 00 00 66 B8 01 00 66 B9 01 00 66 BA 01 00 66 BB 01 00 66 BE 01 00 66 BF 01 00 66 BC 01 00 66 BD 01 00 66 41 B8 01 00 66 41 B9 01 00 66 41 BA 01 00 66 41 BB 01 00 66 41 BC 01 00 66 41 BD 01 00 66 41 BE 01 00 66 41 BF 01 00 B0 01 B1 01 B2 01 B3 01 40 B6 01 40 B7 01 40 B4 01 40 B5 01 41 B0 01 41 B1 01 41 B2 01 41 B3 01 41 B4 01 41 B5 01 41 B6 01 41 B7 01 B4 01 B5 01 B7 01 B6 01
;Disassembly
;0:   48 b8 01 00 00 00 00     movabs rax,0x1
;7:   00 00 00 
;a:   48 b9 01 00 00 00 00     movabs rcx,0x1
;11: 00 00 00 
;14: 48 ba 01 00 00 00 00     movabs rdx,0x1
;1b: 00 00 00 
;1e: 48 bb 01 00 00 00 00     movabs rbx,0x1
;25: 00 00 00 
;28: 48 be 01 00 00 00 00     movabs rsi,0x1
;2f: 00 00 00 
;32: 48 bf 01 00 00 00 00     movabs rdi,0x1
;39: 00 00 00 
;3c: 48 bc 01 00 00 00 00     movabs rsp,0x1
;43: 00 00 00 
;46: 48 bd 01 00 00 00 00     movabs rbp,0x1
;4d: 00 00 00 
;50: 49 b8 01 00 00 00 00     movabs r8,0x1
;57: 00 00 00 
;5a: 49 b9 01 00 00 00 00     movabs r9,0x1
;61: 00 00 00 
;64: 49 ba 01 00 00 00 00     movabs r10,0x1
;6b: 00 00 00 
;6e: 49 bb 01 00 00 00 00     movabs r11,0x1
;75: 00 00 00 
;78: 49 bc 01 00 00 00 00     movabs r12,0x1
;7f: 00 00 00 
;82: 49 bd 01 00 00 00 00     movabs r13,0x1
;89: 00 00 00 
;8c: 49 be 01 00 00 00 00     movabs r14,0x1
;93: 00 00 00 
;96: 49 bf 01 00 00 00 00     movabs r15,0x1
;9d: 00 00 00 
;a0: b8 01 00 00 00           mov    eax,0x1
;a5: b9 01 00 00 00           mov    ecx,0x1
;aa: ba 01 00 00 00           mov    edx,0x1
;af: bb 01 00 00 00           mov    ebx,0x1
;b4: be 01 00 00 00           mov    esi,0x1
;b9: bf 01 00 00 00           mov    edi,0x1
;be: bc 01 00 00 00           mov    esp,0x1
;c3: bd 01 00 00 00           mov    ebp,0x1
;c8: 41 b8 01 00 00 00        mov    r8d,0x1
;ce: 41 b9 01 00 00 00        mov    r9d,0x1
;d4: 41 ba 01 00 00 00        mov    r10d,0x1
;da: 41 bb 01 00 00 00        mov    r11d,0x1
;e0: 41 bc 01 00 00 00        mov    r12d,0x1
;e6: 41 bd 01 00 00 00        mov    r13d,0x1
;ec: 41 be 01 00 00 00        mov    r14d,0x1
;f2: 41 bf 01 00 00 00        mov    r15d,0x1
;f8: 66 b8 01 00              mov    ax,0x1
;fc: 66 b9 01 00              mov    cx,0x1
;100:    66 ba 01 00             mov    dx,0x1
;104:    66 bb 01 00             mov    bx,0x1
;108:    66 be 01 00             mov    si,0x1
;10c:    66 bf 01 00             mov    di,0x1
;110:    66 bc 01 00             mov    sp,0x1
;114:    66 bd 01 00             mov    bp,0x1
;118:    66 41 b8 01 00          mov    r8w,0x1
;11d:    66 41 b9 01 00          mov    r9w,0x1
;122:    66 41 ba 01 00          mov    r10w,0x1
;127:    66 41 bb 01 00          mov    r11w,0x1
;12c:    66 41 bc 01 00          mov    r12w,0x1
;131:    66 41 bd 01 00          mov    r13w,0x1
;136:    66 41 be 01 00          mov    r14w,0x1
;13b:    66 41 bf 01 00          mov    r15w,0x1
;140:    b0 01                   mov    al,0x1
;142:    b1 01                   mov    cl,0x1
;144:    b2 01                   mov    dl,0x1
;146:    b3 01                   mov    bl,0x1
;148:    40 b6 01                mov    sil,0x1
;14b:    40 b7 01                mov    dil,0x1
;14e:    40 b4 01                mov    spl,0x1
;151:    40 b5 01                mov    bpl,0x1
;154:    41 b0 01                mov    r8b,0x1
;157:    41 b1 01                mov    r9b,0x1
;15a:    41 b2 01                mov    r10b,0x1
;15d:    41 b3 01                mov    r11b,0x1
;160:    41 b4 01                mov    r12b,0x1
;163:    41 b5 01                mov    r13b,0x1
;166:    41 b6 01                mov    r14b,0x1
;169:    41 b7 01                mov    r15b,0x1
;16c:    b4 01                   mov    ah,0x1
;16e:    b5 01                   mov    ch,0x1
;170:    b7 01                   mov    bh,0x1
;172:    b6 01                   mov    dh,0x1
