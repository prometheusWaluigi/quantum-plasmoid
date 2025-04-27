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
    actual1 = process_math_blocks(input1).strip()
    if actual1 != expected1.strip():
        print('Test 1 failed:')
        print('Actual:')
        print(repr(actual1))
        print('Expected:')
        print(repr(expected1.strip()))
    assert actual1 == expected1.strip()

    # Test inline math
    input2 = r"Here is inline math: $a_{ext} + b_{int}$ and $\Psi_{tot}$"
    expected2 = "Here is inline math: `aₑₓₜ + bᵢₙₜ` and `Ψₜₒₜ`"
    actual2 = process_math_blocks(input2).strip()
    if actual2 != expected2.strip():
        print('Test 2 failed:')
        print('Actual:')
        print(repr(actual2))
        print('Expected:')
        print(repr(expected2.strip()))
    assert actual2 == expected2.strip()

    # Test block math with $$
    input3 = """
$$
A_{tot} = B_{ext} + C_{int}
$$
"""
    expected3 = """

Aₜₒₜ = Bₑₓₜ + Cᵢₙₜ

"""
    actual3 = process_math_blocks(input3).strip()
    if actual3 != expected3.strip():
        print('Test 3 failed:')
        print('Actual:')
        print(repr(actual3))
        print('Expected:')
        print(repr(expected3.strip()))
    assert actual3 == expected3.strip()

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
