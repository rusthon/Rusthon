'''
ffi
'''
# ABI types: stdcall, aapcs, cdecl, fastcall, Rust, rust-intrinsic, system, C, win64
import libc
from libc import c_int

with extern(link="readline", abi="C"):
	let rl_readline_version : c_int

def main():
	print rl_readline_version

