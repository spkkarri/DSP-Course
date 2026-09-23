import os
import re

tex_path = "lecture_15.tex"
with open(tex_path, "r", encoding="utf-8") as f:
    content = f.read()

# Remove part (b) from the worked example
pattern = r"\\textbf\{\(b\) Transposed Direct Form:\}.*?(?=\\textbf\{\(c\) Cascade Form:\})"
content = re.sub(pattern, "", content, flags=re.DOTALL)

with open(tex_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Removed part (b) from lecture 15 worked examples")
