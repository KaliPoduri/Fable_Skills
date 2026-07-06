"""Phase 0 canary: proves Python script invocation works in this environment.

Stdlib-only. Non-interactive. No network. Prints a bounded report and exits 0.
"""

import platform
import sys


def main() -> int:
    print("FABLE-SCRIPT-OK")
    print(f"python={sys.version.split()[0]}")
    print(f"executable={sys.executable}")
    print(f"platform={platform.platform()}")
    # Phase 0 flow 3 also asks whether python-pptx / python-docx are usable.
    for module, package in (("pptx", "python-pptx"), ("docx", "python-docx")):
        try:
            __import__(module)
            print(f"{package}=importable")
        except ImportError:
            print(f"{package}=not-installed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
