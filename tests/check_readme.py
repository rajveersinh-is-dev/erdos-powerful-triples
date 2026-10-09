"""Static check of README.md: link resolution, math-delimiter balance, headings."""
import os
import re

s = open("README.md", encoding="utf-8").read()
print("lines:", s.count("\n") + 1, " chars:", len(s))

# math delimiter balance: count of "$" outside fenced code blocks
in_fence = False
math = 0
for line in s.split("\n"):
    if line.strip().startswith("```"):
        in_fence = not in_fence
        continue
    if not in_fence:
        math += line.count("$")
print("inline math '$' outside code fences:", math, "-> balanced:", math % 2 == 0)

# fenced code blocks balanced
print("code fences balanced:", s.count("```") % 2 == 0)

# relative links resolve
bad = []
for link in sorted(set(re.findall(r"\]\((?!https?:)([^)#]+)", s))):
    if not os.path.exists(link):
        bad.append(link)
    print(("OK   " if os.path.exists(link) else "MISS "), link)
print("broken relative links:", bad if bad else "none")

print("--- headings ---")
for line in s.split("\n"):
    if line.startswith("#"):
        print("  " + line[:72])