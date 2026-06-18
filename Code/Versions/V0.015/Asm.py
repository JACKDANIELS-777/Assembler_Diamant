class Asm:
    registers  = {
    # 64-bit Registers
    "rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp",
    "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15",

    # 32-bit Registers (Lower halves)
    "eax", "ebx", "ecx", "edx", "esi", "edi", "ebp", "esp",
    "r8d", "r9d", "r10d", "r11d", "r12d", "r13d", "r14d", "r15d",

    # 16-bit Registers (Lower quarters)
    "ax", "bx", "cx", "dx", "si", "di", "bp", "sp",
    "r8w", "r9w", "r10w", "r11w", "r12w", "r13w", "r14w", "r15w",

    # 8-bit Low Registers
    "al", "bl", "cl", "dl", "sil", "dil", "bpl", "spl",
    "r8b", "r9b", "r10b", "r11b", "r12b", "r13b", "r14b", "r15b",

    # 8-bit High Registers (Legacy)
    "ah", "bh", "ch", "dh"
}
    def __init__(self):
        self.code=bytearray()

    def emit_mov_imm(self, reg_name, value):
        """
        Encodes a 'mov register, immediate' instruction for any x64 GPR size.
        Automatically handles REX prefixes, opcodes, ModR/M, and byte lengths.
        Appends the raw bytes to self.code and returns them.
        """
        reg = reg_name.lower().strip()

        # -------------------------------------------------------------------------
        # 1. ARCHITECTURE DEFINITIONS MAP
        # Format: (size_in_bytes, is_extension_r8_r15, opcode, fixed_rex, [prefix])
        # -------------------------------------------------------------------------
        reg_table = {
            # --- 64-BIT REGISTERS (mov reg64, imm64) ---
            "rax": (8, False, 0xB8, 0x48), "rcx": (8, False, 0xB9, 0x48),
            "rdx": (8, False, 0xBA, 0x48), "rbx": (8, False, 0xBB, 0x48),
            "rsp": (8, False, 0xBC, 0x48), "rbp": (8, False, 0xBD, 0x48),
            "rsi": (8, False, 0xBE, 0x48), "rdi": (8, False, 0xBF, 0x48),
            "r8": (8, True, 0xB8, 0x49), "r9": (8, True, 0xB9, 0x49),
            "r10": (8, True, 0xBA, 0x49), "r11": (8, True, 0xBB, 0x49),
            "r12": (8, True, 0xBC, 0x49), "r13": (8, True, 0xBD, 0x49),
            "r14": (8, True, 0xBE, 0x49), "r15": (8, True, 0xBF, 0x49),

            # --- 32-BIT REGISTERS (mov reg32, imm32) ---
            "eax": (4, False, 0xB8, None), "ecx": (4, False, 0xB9, None),
            "edx": (4, False, 0xBA, None), "ebx": (4, False, 0xBB, None),
            "esp": (4, False, 0xBC, None), "ebp": (4, False, 0xBD, None),
            "esi": (4, False, 0xBE, None), "edi": (4, False, 0xBF, None),
            "r8d": (4, True, 0xB8, 0x41), "r9d": (4, True, 0xB9, 0x41),
            "r10d": (4, True, 0xBA, 0x41), "r11d": (4, True, 0xBB, 0x41),
            "r12d": (4, True, 0xBC, 0x41), "r13d": (4, True, 0xBD, 0x41),
            "r14d": (4, True, 0xBE, 0x41), "r15d": (4, True, 0xBF, 0x41),

            # --- 16-BIT REGISTERS (mov reg16, imm16) requires 0x66 operand prefix ---
            "ax": (2, False, 0xB8, None, 0x66), "cx": (2, False, 0xB9, None, 0x66),
            "dx": (2, False, 0xBA, None, 0x66), "bx": (2, False, 0xBB, None, 0x66),
            "sp": (2, False, 0xBC, None, 0x66), "bp": (2, False, 0xBD, None, 0x66),
            "si": (2, False, 0xBE, None, 0x66), "di": (2, False, 0xBF, None, 0x66),
            "r8w": (2, True, 0xB8, 0x41, 0x66), "r9w": (2, True, 0xB9, 0x41, 0x66),
            "r10w": (2, True, 0xBA, 0x41, 0x66), "r11w": (2, True, 0xBB, 0x41, 0x66),
            "r12w": (2, True, 0xBC, 0x41, 0x66), "r13w": (2, True, 0xBD, 0x41, 0x66),
            "r14w": (2, True, 0xBE, 0x41, 0x66), "r15w": (2, True, 0xBF, 0x41, 0x66),

            # --- 8-BIT LOW REGISTERS (mov reg8, imm8) ---
            "al": (1, False, 0xB0, None), "cl": (1, False, 0xB1, None),
            "dl": (1, False, 0xB2, None), "bl": (1, False, 0xB3, None),
            # Uniform 8-bit low regs (spl, bpl, sil, dil) require an empty REX prefix (0x40)
            "spl": (1, False, 0xB4, 0x40), "bpl": (1, False, 0xB5, 0x40),
            "sil": (1, False, 0xB6, 0x40), "dil": (1, False, 0xB7, 0x40),
            "r8b": (1, True, 0xB0, 0x41), "r9b": (1, True, 0xB1, 0x41),
            "r10b": (1, True, 0xB2, 0x41), "r11b": (1, True, 0xB3, 0x41),
            "r12b": (1, True, 0xB4, 0x41), "r13b": (1, True, 0xB5, 0x41),
            "r14b": (1, True, 0xB6, 0x41), "r15b": (1, True, 0xB7, 0x41),

            # --- 8-BIT HIGH REGISTERS (Legacy) ---
            "ah": (1, False, 0xB4, None), "ch": (1, False, 0xB5, None),
            "bh": (1, False, 0xB6, None), "dh": (1, False, 0xB7, None)
        }

        if reg not in reg_table:
            raise ValueError(f"Unknown register target: {reg_name}")

        # Extract encoding properties
        entry = reg_table[reg]
        byte_size = entry[0]
        opcode = entry[2]
        rex_prefix = entry[3]
        operand_prefix = entry[4] if len(entry) > 4 else None

        # -------------------------------------------------------------------------
        # 2. INSTRUCTION CONSTRUCT
        # -------------------------------------------------------------------------
        instruction = bytearray()

        # Apply 16-bit operand override size prefix if required (0x66)
        if operand_prefix:
            instruction.append(operand_prefix)

        # Apply REX extension prefix if required (0x40, 0x41, 0x48, 0x49)
        if rex_prefix:
            instruction.append(rex_prefix)

        # Add core opcode byte
        instruction.append(opcode)

        # Pack the immediate value to the matching size (Little-Endian)
        mask = (1 << (byte_size * 8)) - 1
        value_bytes = (value & mask).to_bytes(byte_size, byteorder='little')
        instruction.extend(value_bytes)

        # -------------------------------------------------------------------------
        # 3. COMMIT AND RETURN
        # -------------------------------------------------------------------------
        self.code.extend(instruction)
        return instruction

    def emit_mov_reg_reg(self, dest_reg, src_reg):
        """
        Encodes a 'mov dest_reg, src_reg' instruction for matching x64 GPR sizes.
        Handles REX prefixes, opcodes, and ModR/M encoding automatically.
        Appends the raw bytes to self.code and returns them.
        """
        dest = dest_reg.lower().strip()
        src = src_reg.lower().strip()

        # -------------------------------------------------------------------------
        # 1. ARCHITECTURE DEFINITIONS MAP
        # Format: (size_in_bytes, register_index, is_extension_r8_r15, [prefix])
        # -------------------------------------------------------------------------
        reg_table = {
            # --- 64-BIT ---
            "rax": (8, 0, False), "rcx": (8, 1, False), "rdx": (8, 2, False), "rbx": (8, 3, False),
            "rsp": (8, 4, False), "rbp": (8, 5, False), "rsi": (8, 6, False), "rdi": (8, 7, False),
            "r8": (8, 0, True), "r9": (8, 1, True), "r10": (8, 2, True), "r11": (8, 3, True),
            "r12": (8, 4, True), "r13": (8, 5, True), "r14": (8, 6, True), "r15": (8, 7, True),

            # --- 32-BIT ---
            "eax": (4, 0, False), "ecx": (4, 1, False), "edx": (4, 2, False), "ebx": (4, 3, False),
            "esp": (4, 4, False), "ebp": (4, 5, False), "esi": (4, 6, False), "edi": (4, 7, False),
            "r8d": (4, 0, True), "r9d": (4, 1, True), "r10d": (4, 2, True), "r11d": (4, 3, True),
            "r12d": (4, 4, True), "r13d": (4, 5, True), "r14d": (4, 6, True), "r15d": (4, 7, True),

            # --- 16-BIT ---
            "ax": (2, 0, False, 0x66), "cx": (2, 1, False, 0x66), "dx": (2, 2, False, 0x66), "bx": (2, 3, False, 0x66),
            "sp": (2, 4, False, 0x66), "bp": (2, 5, False, 0x66), "si": (2, 6, False, 0x66), "di": (2, 7, False, 0x66),
            "r8w": (2, 0, True, 0x66), "r9w": (2, 1, True, 0x66), "r10w": (2, 2, True, 0x66),
            "r11w": (2, 3, True, 0x66),
            "r12w": (2, 4, True, 0x66), "r13w": (2, 5, True, 0x66), "r14w": (2, 6, True, 0x66),
            "r15w": (2, 7, True, 0x66),

            # --- 8-BIT LOW ---
            "al": (1, 0, False), "cl": (1, 1, False), "dl": (1, 2, False), "bl": (1, 3, False),
            "spl": (1, 4, False), "bpl": (1, 5, False), "sil": (1, 6, False), "dil": (1, 7, False),
            "r8b": (1, 0, True), "r9b": (1, 1, True), "r10b": (1, 2, True), "r11b": (1, 3, True),
            "r12b": (1, 4, True), "r13b": (1, 5, True), "r14b": (1, 6, True), "r15b": (1, 7, True),

            # --- 8-BIT HIGH ---
            "ah": (1, 4, False), "ch": (1, 5, False), "bh": (1, 6, False), "dh": (1, 7, False)
        }

        if dest not in reg_table or src not in reg_table:
            raise ValueError(f"Invalid register pair: mov {dest_reg}, {src_reg}")

        dest_size, dest_idx, dest_ext, *dest_pref = reg_table[dest]
        src_size, src_idx, src_ext, *src_pref = reg_table[src]

        if dest_size != src_size:
            raise TypeError(f"Size mismatch: Cannot move {src_size * 8}-bit register to {dest_size * 8}-bit register")

        # Prevent mixing legacy high-8 bits (AH/BH/CH/DH) with extended uniform byte registers
        legacy_8bit = {"ah", "bh", "ch", "dh"}
        uniform_8bit_ext = {"spl", "bpl", "sil", "dil", "r8b", "r9b", "r10b", "r11b", "r12b", "r13b", "r14b", "r15b"}
        if dest_size == 1:
            if (dest in legacy_8bit and src in uniform_8bit_ext) or (src in legacy_8bit and dest in uniform_8bit_ext):
                raise TypeError(
                    "Architecture restriction: Cannot mix high-8 registers with uniform x64 byte extensions.")

        # -------------------------------------------------------------------------
        # 2. CALC OPCODES & PREFIXES
        # -------------------------------------------------------------------------
        instruction = bytearray()

        # 16-bit size override prefix
        if dest_size == 2:
            instruction.append(0x66)

        # Determine core Opcode (0x88 for 8-bit registers, 0x89 for 16/32/64-bit)
        opcode = 0x88 if dest_size == 1 else 0x89

        # Build REX Prefix (0x40-0x4F base)
        # REX.W (bit 3 = 1) -> 64-bit operand size
        # REX.R (bit 2 = 1) -> Extension bit for ModR/M 'reg' field (src)
        # REX.B (bit 0 = 1) -> Extension bit for ModR/M 'r/m' field (dest)
        rex = 0x40
        if dest_size == 8:  rex |= 0x08  # REX.W
        if src_ext:        rex |= 0x04  # REX.R
        if dest_ext:       rex |= 0x01  # REX.B

        # Force a base REX prefix (0x40) if using uniform 8-bit registers (spl, bpl, sil, dil)
        requires_rex_base = (
                    dest_size == 1 and (dest in {"spl", "bpl", "sil", "dil"} or src in {"spl", "bpl", "sil", "dil"}))

        if rex > 0x40 or requires_rex_base:
            instruction.append(rex)

        instruction.append(opcode)

        # -------------------------------------------------------------------------
        # 3. CONSTRUCT MODR/M BYTE
        # Format: [ Mode: 2 bits (11) ] [ Source Reg: 3 bits ] [ Dest Reg: 3 bits ]
        # Mode 11 (0xC0) represents standard register-to-register operation
        # -------------------------------------------------------------------------
        modrm = 0xC0 | (src_idx << 3) | dest_idx
        instruction.append(modrm)

        # -------------------------------------------------------------------------
        # 4. COMMIT AND RETURN
        # -------------------------------------------------------------------------
        self.code.extend(instruction)
        return instruction

    def emit_add_reg_reg(self, dest_reg, src_reg):
        """
        Encodes an 'add dest_reg, src_reg' instruction for matching x64 GPR sizes.
        Modifies dest_reg in-place: dest_reg = dest_reg + src_reg.
        Appends the raw bytes to self.code and returns them.
        """
        dest = dest_reg.lower().strip()
        src = src_reg.lower().strip()

        # -------------------------------------------------------------------------
        # 1. ARCHITECTURE DEFINITIONS MAP
        # Format: (size_in_bytes, register_index, is_extension_r8_r15)
        # -------------------------------------------------------------------------
        reg_table = {
            # --- 64-BIT ---
            "rax": (8, 0, False), "rcx": (8, 1, False), "rdx": (8, 2, False), "rbx": (8, 3, False),
            "rsp": (8, 4, False), "rbp": (8, 5, False), "rsi": (8, 6, False), "rdi": (8, 7, False),
            "r8": (8, 0, True), "r9": (8, 1, True), "r10": (8, 2, True), "r11": (8, 3, True),
            "r12": (8, 4, True), "r13": (8, 5, True), "r14": (8, 6, True), "r15": (8, 7, True),

            # --- 32-BIT ---
            "eax": (4, 0, False), "ecx": (4, 1, False), "edx": (4, 2, False), "ebx": (4, 3, False),
            "esp": (4, 4, False), "ebp": (4, 5, False), "esi": (4, 6, False), "edi": (4, 7, False),
            "r8d": (4, 0, True), "r9d": (4, 1, True), "r10d": (4, 2, True), "r11d": (4, 3, True),
            "r12d": (4, 4, True), "r13d": (4, 5, True), "r14d": (4, 6, True), "r15d": (4, 7, True),

            # --- 16-BIT ---
            "ax": (2, 0, False), "cx": (2, 1, False), "dx": (2, 2, False), "bx": (2, 3, False),
            "sp": (2, 4, False), "bp": (2, 5, False), "si": (2, 6, False), "di": (2, 7, False),
            "r8w": (2, 0, True), "r9w": (2, 1, True), "r10w": (2, 2, True), "r11w": (2, 3, True),
            "r12w": (2, 4, True), "r13w": (2, 5, True), "r14w": (2, 6, True), "r15w": (2, 7, True),

            # --- 8-BIT LOW ---
            "al": (1, 0, False), "cl": (1, 1, False), "dl": (1, 2, False), "bl": (1, 3, False),
            "spl": (1, 4, False), "bpl": (1, 5, False), "sil": (1, 6, False), "dil": (1, 7, False),
            "r8b": (1, 0, True), "r9b": (1, 1, True), "r10b": (1, 2, True), "r11b": (1, 3, True),
            "r12b": (1, 4, True), "r13b": (1, 5, True), "r14b": (1, 6, True), "r15b": (1, 7, True),

            # --- 8-BIT HIGH ---
            "ah": (1, 4, False), "ch": (1, 5, False), "bh": (1, 6, False), "dh": (1, 7, False)
        }

        if dest not in reg_table or src not in reg_table:
            raise ValueError(f"Invalid register pair: add {dest_reg}, {src_reg}")

        dest_size, dest_idx, dest_ext = reg_table[dest]
        src_size, src_idx, src_ext = reg_table[src]

        if dest_size != src_size:
            raise TypeError(f"Size mismatch: Cannot add {src_size * 8}-bit register to {dest_size * 8}-bit register")

        # Guard against illegal 8-bit hybrid mixing (x86-64 hardware restriction)
        legacy_8bit = {"ah", "bh", "ch", "dh"}
        uniform_8bit_ext = {"spl", "bpl", "sil", "dil", "r8b", "r9b", "r10b", "r11b", "r12b", "r13b", "r14b", "r15b"}
        if dest_size == 1:
            if (dest in legacy_8bit and src in uniform_8bit_ext) or (src in legacy_8bit and dest in uniform_8bit_ext):
                raise TypeError(
                    "Architecture restriction: Cannot mix high-8 registers with uniform x64 byte extensions.")

        # -------------------------------------------------------------------------
        # 2. CONSTRUCT PREFIXES & OPCODES
        # -------------------------------------------------------------------------
        instruction = bytearray()

        # 16-bit size override operand prefix
        if dest_size == 2:
            instruction.append(0x66)

        # Core Opcode: 0x00 for 8-bit registers, 0x01 for 16/32/64-bit registers
        opcode = 0x00 if dest_size == 1 else 0x01

        # Calculate the REX prefix byte
        # REX.W (bit 3) = 1 for 64-bit width
        # REX.R (bit 2) = Extension for ModR/M 'reg' field (src register)
        # REX.B (bit 0) = Extension for ModR/M 'r/m' field (dest register)
        rex = 0x40
        if dest_size == 8: rex |= 0x08
        if src_ext:       rex |= 0x04
        if dest_ext:      rex |= 0x01

        # Force a base REX prefix (0x40) if using uniform 8-bit base extensions (spl, bpl, sil, dil)
        requires_rex_base = (
                    dest_size == 1 and (dest in {"spl", "bpl", "sil", "dil"} or src in {"spl", "bpl", "sil", "dil"}))

        if rex > 0x40 or requires_rex_base:
            instruction.append(rex)

        instruction.append(opcode)

        # -------------------------------------------------------------------------
        # 3. CONSTRUCT MODR/M BYTE
        # Format: [ Mode: 11 (Register-to-register) ] [ Source Reg (3 bits) ] [ Dest Reg (3 bits) ]
        # -------------------------------------------------------------------------
        modrm = 0xC0 | (src_idx << 3) | dest_idx
        instruction.append(modrm)

        # -------------------------------------------------------------------------
        # 4. COMMIT AND RETURN
        # -------------------------------------------------------------------------
        self.code.extend(instruction)
        return instruction

    def emit_add_reg_imm(self, dest_reg, immediate):
        """
        Emits x64 machine code bytes for: add dest_reg, immediate
        Supports standard 64-bit architectural registers.
        """
        # 1. Register mapping dictionary for standard x64 registers
        # (The binary code used inside the ModR/M byte)
        reg_map = {
            'rax': 0, 'rcx': 1, 'rdx': 2, 'rbx': 3,
            'rsp': 4, 'rbp': 5, 'rsi': 6, 'rdi': 7
        }

        if dest_reg not in reg_map:
            raise ValueError(f"Unsupported or unmapped register: {dest_reg}")

        reg_code = reg_map[dest_reg]
        out_bytes = bytearray()

        # 2. Check if the immediate can fit into a single signed byte (-128 to 127)
        # This lets us use the optimized 0x83 opcode (Saves 3 bytes of code space!)
        if -128 <= immediate <= 127:
            # REX.W prefix (0x48) + Opcode (0x83)
            out_bytes.extend(b'\x48\x83')

            # ModR/M Byte: Mod=11 (registers), Opcode Extension=000 (for ADD), R/M=reg_code
            # Binary: 11 000000 | reg_code -> 0xC0 | reg_code
            modrm = 0xC0 | reg_code
            out_bytes.append(modrm)

            # Append the single byte immediate (handling negative numbers with two's complement)
            out_bytes.append(immediate & 0xFF)

        else:
            # Fallback for large numbers: Use 0x81 opcode with a full 4-byte (32-bit) immediate
            out_bytes.extend(b'\x48\x81')

            # ModR/M Byte is configured the exact same way for ADD
            modrm = 0xC0 | reg_code
            out_bytes.append(modrm)

            # Append the 32-bit immediate in Little-Endian byte order
            out_bytes.append((immediate >> 0) & 0xFF)
            out_bytes.append((immediate >> 8) & 0xFF)
            out_bytes.append((immediate >> 16) & 0xFF)
            out_bytes.append((immediate >> 24) & 0xFF)

        # Append these generated bytes straight into your compiler's main binary stream
        self.code.extend(out_bytes)
        return out_bytes
