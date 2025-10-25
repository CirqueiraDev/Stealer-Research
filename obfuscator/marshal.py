import argparse
import base64
import marshal
import zlib
import sys
from pathlib import Path

LOADER_TEMPLATE = '''import base64 as b, marshal as m{decompress_import};a={b64!s};b=b.b64decode(a){maybe_decompress};c=m.loads(b);exec(c)'''

def obfuscate_file(input_path: Path, output_path: Path, compress: bool = False):
    src = input_path.read_text(encoding="utf-8")
    code_obj = compile(src, str(input_path), "exec")

    data = marshal.dumps(code_obj)

    if compress:
        data = zlib.compress(data)
    b64 = base64.b64encode(data).decode("ascii")
    loader = LOADER_TEMPLATE.format(
        b64=repr(b64),
        decompress_import=";import zlib as z" if compress else "",
        maybe_decompress=";b=z.decompress(b)" if compress else ""
    )
    output_path.write_text(loader, encoding="utf-8")
    print(f"Obfuscated file generated: {output_path} (compress={compress})")

def main():
    p = argparse.ArgumentParser(description="Obfuscates a .py file using marshal+base64 (optional zlib compression).")
    p.add_argument("input", help="Input .py file")
    p.add_argument("-o", "--output", help="Output .py file (default: obfuscated_<input>)")
    p.add_argument("--compress", action="store_true", help="Apply zlib.compress before base64 (recommended)")
    args = p.parse_args()

    inp = Path(args.input)
    if not inp.exists():
        print("Input file not found:", inp, file=sys.stderr)
        sys.exit(2)
    out = Path(args.output) if args.output else inp.with_name(f"obfuscated_{inp.name}")
    obfuscate_file(inp, out, compress=args.compress)

if __name__ == "__main__":
    main()