import ctypes
import struct
import sys

# Windows API Constants
DEBUG_PROCESS = 0x00000001
INFINITE = 0xFFFFFFFF
EXCEPTION_DEBUG_EVENT = 1
EXCEPTION_ACCESS_VIOLATION = 0xC0000005

# Define Win32 Structures for 64-bit Windows
class EXCEPTION_RECORD(ctypes.Structure):
    pass
EXCEPTION_RECORD._fields_ = [
    ("ExceptionCode", ctypes.c_uint32),
    ("ExceptionFlags", ctypes.c_uint32),
    ("ExceptionRecord", ctypes.POINTER(EXCEPTION_RECORD)),
    ("ExceptionAddress", ctypes.c_void_p),
    ("NumberParameters", ctypes.c_uint32),
    ("ExceptionInformation", ctypes.c_uint64 * 15)
]

class EXCEPTION_DEBUG_INFO(ctypes.Structure):
    _fields_ = [
        ("ExceptionRecord", EXCEPTION_RECORD),
        ("dwFirstChance", ctypes.c_uint32)
    ]

class DEBUG_EVENT_U(ctypes.Union):
    _fields_ = [("Exception", EXCEPTION_DEBUG_INFO)]

class DEBUG_EVENT(ctypes.Structure):
    _fields_ = [
        ("dwDebugEventCode", ctypes.c_uint32),
        ("dwProcessId", ctypes.c_uint32),
        ("dwThreadId", ctypes.c_uint32),
        ("u", DEBUG_EVENT_U)
    ]

class STARTUPINFO(ctypes.Structure):
    _fields_ = [
        ("cb", ctypes.c_uint32), ("lpReserved", ctypes.c_char_p),
        ("lpDesktop", ctypes.c_char_p), ("lpTitle", ctypes.c_char_p),
        ("dwX", ctypes.c_uint32), ("dwY", ctypes.c_uint32),
        ("dwXSize", ctypes.c_uint32), ("dwYSize", ctypes.c_uint32),
        ("dwXCountChars", ctypes.c_uint32), ("dwYCountChars", ctypes.c_uint32),
        ("dwFillAttribute", ctypes.c_uint32), ("dwFlags", ctypes.c_uint32),
        ("wShowWindow", ctypes.c_uint16), ("cbReserved2", ctypes.c_uint16),
        ("lpReserved2", ctypes.c_void_p), ("hStdInput", ctypes.c_void_p),
        ("hStdOutput", ctypes.c_void_p), ("hStdError", ctypes.c_void_p)
    ]

class PROCESS_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("hProcess", ctypes.c_void_p), ("hThread", ctypes.c_void_p),
        ("dwProcessId", ctypes.c_uint32), ("dwThreadId", ctypes.c_uint32)
    ]

# Setup Win32 Function Signatures
kernel32 = ctypes.windll.kernel32
kernel32.CreateProcessA.argtypes = [
    ctypes.c_char_p, ctypes.c_char_p, ctypes.c_void_p, ctypes.c_void_p,
    ctypes.c_bool, ctypes.c_uint32, ctypes.c_void_p, ctypes.c_char_p,
    ctypes.POINTER(STARTUPINFO), ctypes.POINTER(PROCESS_INFORMATION)
]

def debug_binary(exe_path):
    si = STARTUPINFO()
    si.cb = ctypes.sizeof(STARTUPINFO)
    pi = PROCESS_INFORMATION()
    
    # Spawn the process in suspended debugging mode
    success = kernel32.CreateProcessA(
        None, exe_path.encode('utf-8'), None, None,
        False, DEBUG_PROCESS, None, None, ctypes.byref(si), ctypes.byref(pi)
    )
    
    if not success:
        print(f"[-] Failed to launch {exe_path}. Error Code: {kernel32.GetLastError()}")
        return

    print(f"[+] Attached to process {pi.dwProcessId}. Running execution track...")
    
    debug_event = DEBUG_EVENT()
    while kernel32.WaitForDebugEvent(ctypes.byref(debug_event), INFINITE):
        if debug_event.dwDebugEventCode == EXCEPTION_DEBUG_EVENT:
            exception = debug_event.u.Exception.ExceptionRecord
            code = exception.ExceptionCode
            address = exception.ExceptionAddress
            
            if code == EXCEPTION_ACCESS_VIOLATION:
                # Calculate relative offset from the standard 0x400000 image base
                # Code section lands at +0x1000 Virtual Address
                offset_from_entry = (address - 0x401000) if address else 0
                
                print("\n" + "!" * 50)
                print(f" CRASH DETECTED: ACCESS VIOLATION (0xC0000005)")
                print(f" Absolute Memory Address: 0x{address:016X}")
                print(f" Relative Offset in .text: +0x{offset_from_entry:X}")
                
                # Check what type of violation it was (Read/Write vs Target address)
                type_flag = exception.ExceptionInformation[0]
                fault_addr = exception.ExceptionInformation[1]
                access_type = "Write" if type_flag == 1 else "Read" if type_flag == 0 else "Execute"
                
                print(f" Hardware Operation: Attempted {access_type} on Address 0x{fault_addr:016X}")
                print("!" * 50 + "\n")
                
                kernel32.TerminateProcess(pi.hProcess, 1)
                break
                
        kernel32.ContinueDebugEvent(debug_event.dwProcessId, debug_event.dwThreadId, 0x00010002) # DBG_CONTINUE

if __name__ == "__main__":
    debug_binary(r".\a.exe")