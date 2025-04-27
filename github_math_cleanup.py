import os
import re
import shutil

# Unicode replacements for common symbols
import re

# Use re.escape on all keys to avoid regex errors
UNICODE_MAP = {
    re.escape(r"\mathcal{C}"): "ℂ",
    re.escape(r"\Psi"): "Ψ",
    re.escape(r"_{ext}"): "ₑₓₜ",
    re.escape(r"_{int}"): "ᵢₙₜ",
    re.escape(r"_{tot}"): "ₜₒₜ",
    re.escape(r"_{t+1}"): "ₜ₊₁",
    re.escape(r"_{s}"): "ₛ",
    re.escape(r"_{Q}"): "_Q",
    re.escape(r"\oplus"): "⊕",
    re.escape(r"\cdot"): "·",
    re.escape(r"\text{select max}_{s}"): "select maxₛ",
    re.escape(r"\text{max}_{s}"): "maxₛ",
    re.escape(r"\text{min}_{s}"): "minₛ",
    re.escape(r"\Big"): "",
    re.escape(r"\left"): "",
    re.escape(r"\right"): "",
    re.escape(r"\,"): " ",
    re.escape(r"\;"): " ",
    re.escape(r"\!"): "",
    re.escape(r"\["): "",
    re.escape(r"\]"): "",
    re.escape(r"\("): "",
    re.escape(r"\)"): "",
    re.escape(r"\{"): "{",
    re.escape(r"\}"): "}",
}


# Regex patterns for math environments
INLINE_MATH = re.compile(r"\$(.+?)\$", re.DOTALL)
BLOCK_MATH = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)
LATEX_BLOCK = re.compile(r"\\\[(.+?)\\\]", re.DOTALL)
LATEX_INLINE = re.compile(r"\\\((.+?)\\\)", re.DOTALL)

# Apply Unicode replacements to a math string
def latex_to_unicode(expr):
    for pat, rep in UNICODE_MAP.items():
        expr = re.sub(pat, rep, expr)
    # Remove remaining LaTeX escapes
    expr = re.sub(r"\\([a-zA-Z]+)", r"", expr)
    # Remove curly braces
    expr = expr.replace('{', '').replace('}', '')
    # Add space after [ if not present
    expr = re.sub(r'\[([^ ])', r'[ \1', expr)
    # Add space before ; if not present
    expr = re.sub(r'([^ ])(;)', r'\1 \2', expr)
    # Add space before ] if not present
    expr = re.sub(r'([^ ])(\])', r'\1 \2', expr)
    # Remove double spaces
    expr = re.sub(r" +", " ", expr)
    return expr.strip()

def process_math_blocks(text):
    # Block math first
    def block_repl(match):
    # Remove extra newline before output
        return latex_to_unicode(match.group(1))
    text = BLOCK_MATH.sub(block_repl, text)
    text = LATEX_BLOCK.sub(block_repl, text)
    # Inline math
    def inline_repl(match):
        return '`' + latex_to_unicode(match.group(1)) + '`'
    text = INLINE_MATH.sub(inline_repl, text)
    text = LATEX_INLINE.sub(inline_repl, text)
    return text

def process_file(path):
    with open(path, encoding='utf-8') as f:
        content = f.read()
    new_content = process_math_blocks(content)
    if new_content != content:
        # Backup original
        shutil.copy2(path, path + '.bak')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated: {path}")
    else:
        print(f"No changes: {path}")

def find_markdown_files(root):
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if fn.lower().endswith('.md'):
                yield os.path.join(dirpath, fn)

def main():
    repo_root = os.path.dirname(os.path.abspath(__file__))
    for mdfile in find_markdown_files(repo_root):
        process_file(mdfile)

if __name__ == '__main__':
    main()

# Export for testing
__all__ = ['process_math_blocks']
