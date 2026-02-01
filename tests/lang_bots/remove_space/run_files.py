"""

python3 I:/mdwiki/fix_refs_new_py/tests/lang_bots/remove_space/run_files.py

"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from fix_refs.lang_bots.remove_space import remove_spaces_between_last_word_and_beginning_of_ref as new_removes
base_path = Path(__file__).parent / "remove_space_texts"

for i in [1, 2]:
    base_path_sub = base_path / str(i)
    input_file = base_path_sub / "input.txt"
    if not input_file.exists():
        print(f"file not found: {input_file}")
        continue
    expected=(base_path_sub / "expected.txt").read_text(encoding="utf-8")
    input_text=(base_path_sub / "input.txt").read_text(encoding="utf-8")
    output_file=base_path_sub / "output.txt"

    result = new_removes(input_text, "hy")

    if result == expected:
        print("result === expected")
    elif result == input_text:
        print("result === input")
    else:
        print("result !== expected")

    # --- حفظ النتيجة
    output_file.write_text(result, encoding="utf-8")
    print(f"\n saved to: {output_file}")
