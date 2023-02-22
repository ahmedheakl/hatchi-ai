pylint_errors = ""
with open("pylint.txt", "r", encoding="utf-8") as f:
    for line in f.readlines():
        pylint_errors += line
stat = ""
with open("pylint_status.txt", "r", encoding="utf-8") as f:
    stat = f.readline()

status = int(stat) == 0

if status:
    ans = "*   Pylint: ran :ok:"
else:
    ans = (
        "<details><summary>Pylint: problems :warning: (click for details)</summary>\n\n"
    )
    ans += f"```python\n{pylint_errors}```\n"
    ans += "</details>"

with open("pylint_data.txt", "w", encoding="utf-8") as f:
    f.write(ans)
