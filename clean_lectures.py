import os
import re

for i in range(15, 31):
    tex_path = f"lecture_{i}.tex"
    if not os.path.exists(tex_path):
        continue
    
    with open(tex_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # We want to remove everything from "\noindent\rule{\textwidth}{0.5pt}\n\section*{4. UNIVERSITY EXAMINATION QUESTIONS \& MARKING RUBRIC}"
    # up to just before "\end{document}"
    
    # Regex to match Section 4 and Section 5 until \end{document}
    pattern = r"\\noindent\\rule\{\\textwidth\}\{0\.5pt\}\s*\\section\*\{4\. UNIVERSITY EXAMINATION QUESTIONS.*?(?=\\end\{document\})"
    
    new_content = re.sub(pattern, "", content, flags=re.DOTALL)
    
    # Wait, some might have \noindent\rule just before Section 4. 
    # Let's do a simpler split
    if "4. UNIVERSITY EXAMINATION" in new_content:
        parts = new_content.split(r"\section*{4. UNIVERSITY EXAMINATION")
        part1 = parts[0]
        # remove the \noindent\rule before it if it exists
        part1 = re.sub(r"\\noindent\\rule\{\\textwidth\}\{0\.5pt\}\s*$", "", part1.rstrip())
        
        # Keep \end{document}
        new_content = part1 + "\n\n\\end{document}\n"
    
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Cleaned {tex_path}")
