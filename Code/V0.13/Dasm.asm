;rax=v:([0,v:([18*10]->^:(rax*rbx+1*9)+2)]->rax)
;rax=%rbx=10%+%rax=10%
;eax=(10*8)+(10)+9
;FOR (rax+1,%rbx=^:([10]<-%rdx=%FOR (rax+1,1,1) {rax=10,rax=10}%*9%)%,1)rax=10rbx=10
;rax=0
;while rax<=9 {rax+=1,rbx=10}
FUN a ():rbx rax=10
a()
a()