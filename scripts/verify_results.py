import random
import sys
import argparse
import os

TEST_FILE = "tests.txt"

OPS = {
    "ADD": lambda a, b: a + b,
    "SUB": lambda a, b: a - b,
    "AND": lambda a, b: a & b,
    "OR":  lambda a, b: a | b
}

def generate_tests(num_tests=35):
    with open(TEST_FILE, "w") as f:
        for _ in range(num_tests):
            a = random.randint(0, 255)
            b = random.randint(0, 255)
            op = random.choice(list(OPS.keys()))
            f.write(f"{a} {b} {op}\n")

    print(f"[PYTHON] Generated {num_tests} test cases -> {TEST_FILE}")

def golden_model(a, b, op):
    return OPS[op](a, b) & 0xFF 

def verify_results(log_file):
    if not os.path.exists(TEST_FILE):
        print("[ERROR] tests.txt not found")
        sys.exit(1)

    if not os.path.exists(log_file):
        print("[ERROR] simulation log not found")
        sys.exit(1)

    tests = []
    with open(TEST_FILE) as f:
        for line in f:
            a, b, op = line.strip().split()
            tests.append((int(a), int(b), op))

    total = passed = failed = 0

    with open(log_file) as log:
        for line, (a, b, op) in zip(log, tests):
            total += 1

            expected = golden_model(a, b, op)

            # Expected log format:
            # A=10 B=5 OP=ADD RESULT=15
            try:
                actual = int(line.strip().split("RESULT=")[1])
            except Exception:
                print(f"[ERROR] Bad log format: {line.strip()}")
                sys.exit(1)

            if actual == expected:
                passed += 1
            else:
                failed += 1
                print(
                    f"[FAIL] A={a} B={b} OP={op} "
                    f"EXPECTED={expected} GOT={actual}"
                )

    print("\n[PYTHON] Verification Summary")
    print(f"Total  : {total}")
    print(f"Passed : {passed}")
    print(f"Failed : {failed}")

    if failed > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HDL Verification Script")
    parser.add_argument("--generate", action="store_true", help="Generate test vectors")
    parser.add_argument("--check", metavar="LOG", help="Verify simulation output")

    args = parser.parse_args()

    if args.generate:
        generate_tests()
    elif args.check:
        verify_results(args.check)
    else:
        parser.print_help()
        sys.exit(1)
