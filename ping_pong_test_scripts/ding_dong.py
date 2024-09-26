import sys

def main(param):
    if param == "ding":
        return "dong"
    else:
        return f"Ungültiger Parameter: {param}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        param = sys.argv[1]
        print(main(param))
    else:
        print("Fehler: Kein Parameter übergeben.")
