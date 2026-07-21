import sys

if len(sys.argv) != 2:
    print("Usage:")
    print("python run_phase.py 3A")
    print("python run_phase.py 3B")
    print("python run_phase.py 3C")
    sys.exit()

phase = sys.argv[1].upper()

if phase not in ["3A", "3B", "3C"]:
    print("Invalid Phase.")
    sys.exit()

print(f"Current Phase : {phase}")