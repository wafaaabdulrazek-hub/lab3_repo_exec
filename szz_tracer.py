import subprocess
import sys

from pydriller import Repository


repo_path = sys.argv[1]
fix_hash = sys.argv[2]

candidate_bics = set()

for commit in Repository(repo_path, single=fix_hash).traverse_commits():
    print(f"Bug-fixing commit: {commit.hash[:7]} ({commit.msg})")

   
    if not commit.parents:
        print("No parent revision: nothing to blame.")
        break
    parent_hash = commit.parents[0]

    for modified_file in commit.modified_files:
       
        old_path = modified_file.old_path
        if old_path is None:
            print(f"{modified_file.new_path}: new file, skipped.")
            continue

        # Read deleted lines
        deleted_lines = modified_file.diff_parsed["deleted"]
        if not deleted_lines:
            print(f"{old_path}: no deleted lines (addition-only fix), nothing to trace.")
            continue

        for line_number, line_text in deleted_lines:
            if not line_text.strip():
                continue  # skip blank lines

            # 2. For each deleted line blame the parent revision
            try:
                result = subprocess.run(
                    ["git", "blame", parent_hash,
                     "-L", f"{line_number},{line_number}",
                     "--", old_path],
                    cwd=repo_path, capture_output=True,
                    text=True, check=True
                )
            except subprocess.CalledProcessError:
                print(f"{old_path}:{line_number}: blame failed, skipped.")
                continue

           
            bic_hash = result.stdout.split()[0].lstrip("^")
            candidate_bics.add(bic_hash)
            print(f"{old_path} line {line_number}: '{line_text.strip()}' -> {bic_hash[:7]}")

print("Candidate bug-inducing commits:", ", ".join(h[:7] for h in candidate_bics) or "none")
