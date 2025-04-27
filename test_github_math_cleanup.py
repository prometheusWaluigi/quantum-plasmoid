import os
import shutil
import difflib
from github_math_cleanup import process_math_blocks

def test_process_math_blocks():
    # Test LaTeX block
    input1 = r"""
This is a formula:
\[ S_{t+1} = \mathcal{C}[\Psi_{ext}(S_{t+1}) \oplus \Psi_{int}(S_{t+1}); Q] \]
"""
    expected1 = """
This is a formula:
Sₜ₊₁ = ℂ[ Ψₑₓₜ(Sₜ₊₁) ⊕ Ψᵢₙₜ(Sₜ₊₁) ; Q ]
"""
    assert process_math_blocks(input1).strip() == expected1.strip()

    # Test inline math
    input2 = r"Here is inline math: $a_{ext} + b_{int}$ and $\Psi_{tot}$"
    expected2 = "Here is inline math: `aₑₓₜ + bᵢₙₜ` and `Ψₜₒₜ`"
    assert process_math_blocks(input2).strip() == expected2.strip()

    # Test block math with $$
    input3 = """
$$
A_{tot} = B_{ext} + C_{int}
$$
"""
    expected3 = """

Aₜₒₜ = Bₑₓₜ + Cᵢₙₜ

"""
    assert process_math_blocks(input3).strip() == expected3.strip()

    print("All tests passed.")

def compare_backup_and_new(mdfile):
    bakfile = mdfile + '.bak'
    if not os.path.exists(bakfile):
        print(f"No backup for {mdfile}")
        return
    with open(bakfile, encoding='utf-8') as f:
        old = f.readlines()
    with open(mdfile, encoding='utf-8') as f:
        new = f.readlines()
    diff = list(difflib.unified_diff(old, new, fromfile=bakfile, tofile=mdfile))
    if diff:
        diff_file = mdfile + '.diff'
        with open(diff_file, 'w', encoding='utf-8') as f:
            f.writelines(diff)
        print(f"Diff written to {diff_file}")
    else:
        print(f"No changes between backup and new for {mdfile}")

def compare_all_backups(repo_root):
    for dirpath, _, filenames in os.walk(repo_root):
        for fn in filenames:
            if fn.endswith('.md') and os.path.exists(os.path.join(dirpath, fn + '.bak')):
                compare_backup_and_new(os.path.join(dirpath, fn))

if __name__ == '__main__':
    test_process_math_blocks()
    repo_root = os.path.dirname(os.path.abspath(__file__))
    compare_all_backups(repo_root)
