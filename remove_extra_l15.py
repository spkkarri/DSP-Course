import os
import re

tex_path = "lecture_15.tex"
with open(tex_path, "r", encoding="utf-8") as f:
    content = f.read()

# Remove subsection 2.2 and its contents
pattern = r"\\subsection\*\{2\.2 Transposed Direct Form \(Flow Graph Reversal\)\}.*?(?=\\subsection\*\{2\.3 Cascade Realization\}|\\section)"
content = re.sub(pattern, "", content, flags=re.DOTALL)

with open(tex_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Removed 2.2 from lecture 15")
