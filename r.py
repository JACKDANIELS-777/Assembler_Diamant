import ctypes

def execute_compiler_bytes():
    # Your exact 93 bytes of raw machine code
    code_bytes = bytes([
        0xE8, 0x48, 0x00, 0x00, 0x00, 0x53, 0x48, 0x83, 0xC0, 0x01, 0x48, 0xB8, 0x01, 0x00, 0x00, 0x00, 
        0x00, 0x00, 0x00, 0x00, 0x48, 0x83, 0xF8, 0x01, 0x0F, 0x8D, 0x1D, 0x00, 0x00, 0x00, 0x48, 0xB8, 
        0x0A, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x48, 0xB8, 0x0A, 0x00, 0x00, 0x00, 0x00, 0x00, 
        0x00, 0x00, 0x48, 0x83, 0xC0, 0x01, 0xE9, 0xDD, 0xFF, 0xFF, 0xFF, 0x48, 0x01, 0xC3, 0x53, 0x48, 
        0x8B, 0x1B, 0x48, 0x83, 0xC3, 0x01, 0x48, 0x83, 0xC3, 0x02, 0x48, 0x89, 0xD8, 0x55, 0x48, 0x89, 
        0xE5, 0x48, 0xB8, 0x0A, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x5D, 0xC3
    ])

    print(f"[+] Allocating staging memory space...")

    # Step 1: Allocate as standard READWRITE (0x04) so memmove is safe from DEP
    ptr = ctypes.windll.kernel32.VirtualAlloc(
        None, len(code_bytes), 0x1000, 0x04
    )
    
    if not ptr:
        print("[-] Memory allocation failed.")
        return

    # Step 2: Copy your compiled instructions safely into the data page
    ctypes.memmove(ptr, code_bytes, len(code_bytes))
    print("[+] Machine code bytes safely staged in memory.")

    # Step 3: Use VirtualProtect to switch flags to EXECUTE_READ (0x20)
    # This keeps Windows happy and satisfies DEP constraints perfectly
    old_protect = ctypes.c_uint32()
    protect_success = ctypes.windll.kernel32.VirtualProtect(
        ptr, len(code_bytes), 0x20, ctypes.byref(old_protect)
    )

    if not protect_success:
        print("[-] Failed to flip memory page execution flags.")
        ctypes.windll.kernel32.VirtualFree(ptr, 0, 0x8000)
        return

    # Step 4: Cast raw address to an executable function signature block
    func = ctypes.CFUNCTYPE(ctypes.c_uint64)(ptr)

    print("[+] Executing track directly on the iron...")
    try:
        result = func()
        print(f"\n" + "="*40)
        print(f" SUCCESS! Main line completed execution.")
        print(f" Final RAX State (Returned Value): {result}")
        print("="*40)
    except Exception as e:
        print(f"\n[-] Hardware branch crash caught inside memory track: {e}")
    finally:
        # Clean up allocation page cleanly
        ctypes.windll.kernel32.VirtualFree(ptr, 0, 0x8000)

if __name__ == "__main__":
    execute_compiler_bytes()