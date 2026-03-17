import re
from pathlib import Path
from datetime import datetime

README_PATH = Path("README.md")

ARCH_BLOCK = """## Architecture Overview

CNX is structured as a layered control system:

- **Gateway** — receives requests from users or applications  
- **Wrapper** — applies enforcement, refusal, and control logic  
- **CCF** — validates outputs against defined constraints  
- **Model Execution Layer** — executes the underlying LLM or agent  

In simplified form:

`Client → CNX Gateway → Wrapper → CCF → Model`

The separation between these layers allows control to remain independent from model behavior.

CNX is designed so that intelligence and control do not collapse into the same layer.
"""

def backup_readme():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = README_PATH.with_name(f"README.backup_{timestamp}.md")
    backup_path.write_text(README_PATH.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"[backup] Created: {backup_path}")

def fix_sentence(content: str) -> str:
    return content.replace(
        "Intelligence can scale — but control must remain invariant.",
        "Intelligence can scale, but control must remain invariant."
    )

def replace_architecture_section(content: str) -> str:
    pattern = r"## Architecture Overview[\s\S]*?(?=\n## |\Z)"

    if re.search(pattern, content):
        updated = re.sub(pattern, ARCH_BLOCK, content)
        print("[update] Architecture section replaced")
        return updated
    else:
        print("[warning] Architecture section not found, appending at end")
        return content.rstrip() + "\n\n" + ARCH_BLOCK + "\n"

def update_readme():
    if not README_PATH.exists():
        print("[error] README.md not found")
        return

    original = README_PATH.read_text(encoding="utf-8")

    # Backup first (safety)
    backup_readme()

    updated = fix_sentence(original)
    updated = replace_architecture_section(updated)

    if updated == original:
        print("[info] No changes detected")
        return

    README_PATH.write_text(updated, encoding="utf-8")
    print("[success] README updated safely")

if __name__ == "__main__":
    update_readme()