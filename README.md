# Assembler_Diamant

A compiler from a small register-level language straight to **raw x86-64 machine code**, written from scratch in
Python (about **1,900 lines** in V0.12). There's no NASM and no external assembler: it parses the source with
[SLY](https://github.com/dabeaz/sly), walks the syntax tree, and writes the instruction bytes itself, including REX
prefixes and ModR/M bytes.

```
rax=100 rbx=20
rbx += 5
```

becomes

```
48 B8 64 00 00 00 00 00 00 00    mov rax, 100
48 BB 14 00 00 00 00 00 00 00    mov rbx, 20
48 83 C3 05                      add rbx, 5
```

## Functions and calls

This is the sample program in `Code/Versions/V0.12/Dasm.asm`:

```
FUN a (): rbx+10 rax=10
rax=1+%a()%
```

Output, disassembled with `objdump`:

```
0:  e8 0b 00 00 00          call   0x10
5:  48 83 c3 0a             add    rbx, 0xa
9:  48 83 c3 01             add    rbx, 0x1
d:  48 89 d8                mov    rax, rbx
10: 55                      push   rbp          ; function a
11: 48 89 e5                mov    rbp, rsp
14: 48 b8 0a 00 00 00 00    mov    rax, 0xa
    00 00 00
1e: 5d                      pop    rbp
1f: c3                      ret
```

The function gets a proper stack frame (`push rbp` / `mov rbp, rsp` / `pop rbp` / `ret`), and the `call` offset is
worked out from where the function ends up in the output.

## How it works

1. **Lexer and parser** (`script.py`, built with SLY): turns the source into a tree of tuples.
2. **Tree walker** (`script.py`): decides which instructions each node needs.
3. **Encoder** (`Asm.py`): writes the bytes for each instruction, building the REX prefix, opcode and ModR/M byte
   by hand.
4. **`finalize_program()`**: puts the main code and the functions together and fixes up the call offsets.

## What it can emit

| Area | Instructions |
|---|---|
| Moves | `mov reg, imm`, `mov reg, reg`, loads through a pointer |
| Arithmetic | `add`, `sub`, `imul` (with a register or an immediate) |
| Compare | `cmp` with a register or an immediate |
| Stack | `push`, `pop`, reading and writing stack slots by offset |
| Control flow | `for` and `while` loops, `if … then … else` |
| Functions | `FUN name (): …`, calls with `%name()%`, prologue and epilogue |

## Running it

```sh
pip install sly
cd Code/Versions/V0.12
python script.py          # compiles Dasm.asm and prints the machine code in hex
```

To see the instructions, save the bytes to a file and disassemble them:

```sh
objdump -D -b binary -m i386:x86-64 -M intel out.bin
```

## Versions

Every version is kept in `Code/Versions/`, from V0.01 (about 650 lines) to V0.12 (about 1,900).

---

### AI training notice

This repository is opted out of AI scraping, data mining and model training. It's distributed under the MIT License
(see `LICENSE`).
