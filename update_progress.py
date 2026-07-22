import re
from pathlib import Path


def update_readme():
    readme_path = Path("README.md")
    if not readme_path.exists():
        print("README.md not found.")
        return

    content = readme_path.read_text(encoding="utf-8")

    # 1. Parse the phases and count checkboxes
    # We can split the document by phase headers to isolate each phase's content
    phase_pattern = re.compile(r"(### [^\n]*Phase (-?\d+)[^\n]*)")
    matches = list(phase_pattern.finditer(content))

    phase_counts = {}
    for i, match in enumerate(matches):
        phase_num = int(match.group(2))
        start_idx = match.end()
        # The phase content goes until the next phase header or the end of the file
        end_idx = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        phase_text = content[start_idx:end_idx]

        # Find checkboxes [ ] or [x]/[X]
        total_boxes = len(re.findall(r"-\s*\[[ xX]\]", phase_text))
        completed_boxes = len(re.findall(r"-\s*\[[xX]\]", phase_text))

        percent = 0
        if total_boxes > 0:
            percent = int((completed_boxes / total_boxes) * 100)

        phase_counts[phase_num] = {
            "total": total_boxes,
            "completed": completed_boxes,
            "percent": percent,
        }

    # 2. Update the Overview & Tracking table rows
    def replace_table_row(row_match):
        phase_str = row_match.group(1)
        phase_num = int(phase_str)
        focus_area = row_match.group(2)
        timeline = row_match.group(5)

        stats = phase_counts.get(phase_num, {"percent": 0, "completed": 0, "total": 0})
        percent = stats["percent"]

        # Calculate Status
        if percent == 0:
            status = "⏳ _Not Started_"
        elif percent == 100:
            status = "✅ _Completed_"
        else:
            status = "🏃 _In Progress_"

        # Build Progress Bar (10 steps)
        filled_blocks = percent // 10
        empty_blocks = 10 - filled_blocks
        progress_bar = f"`[{'█' * filled_blocks}{'░' * empty_blocks}] {percent}%`"

        return f"| **Phase {phase_num}**  | {focus_area} | {status} | {progress_bar} | {timeline} |"

    # Regex to match rows of the roadmap table:
    # e.g., | **Phase 0**  | [CS Fundamentals (DSA)](#-phase-0--computer-science-fundamentals)     | ⏳ _Not Started_ | `[░░░░░░░░░░] 0%` |    Week 1-3     |
    table_row_pattern = re.compile(
        r"^\|\s*\*\*Phase\s+(-?\d+)\*\*\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|",
        re.MULTILINE,
    )

    new_content = table_row_pattern.sub(replace_table_row, content)

    if new_content != content:
        readme_path.write_text(new_content, encoding="utf-8")
        print("README.md progress updated successfully!")
        for phase, stats in sorted(phase_counts.items()):
            print(
                f"  Phase {phase}: {stats['completed']}/{stats['total']} completed ({stats['percent']}%)"
            )
    else:
        print("No changes detected in progress levels.")


if __name__ == "__main__":
    update_readme()
