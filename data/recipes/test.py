path = "Zinger_Burger.txt"

# Read as Windows-1252, Write as UTF-8
with open(path, "r", encoding="cp1252") as f:
    text = f.read()

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("Conversion complete!")
