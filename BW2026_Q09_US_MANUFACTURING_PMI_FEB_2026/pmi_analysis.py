import os
import subprocess
import sys


def main():
    folder = os.path.dirname(__file__)
    subprocess.check_call([sys.executable, os.path.join(folder, "base_rate_calc.py")])
    subprocess.check_call([sys.executable, os.path.join(folder, "quant_model.py")])


if __name__ == "__main__":
    main()
