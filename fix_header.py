import json

NOTEBOOK_PATH = "main.ipynb"

with open(NOTEBOOK_PATH, "r", encoding="utf-8") as f:
    nb = json.load(f)

old_header = "Medical Insurance Cost Prediction :: Pabitra Banerjee\n"
new_header = "# Medical Insurance Cost Prediction\n### By Yajat Deshpande\n"

fixed = False
for cell in nb["cells"]:
    if cell["cell_type"] == "markdown" and cell["source"] and cell["source"][0] == old_header:
        cell["source"][0] = new_header
        fixed = True
        break

if not fixed:
    print("Header line not found — no changes made. Check the notebook manually.")
else:
    with open(NOTEBOOK_PATH, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1)
    print("Header fixed successfully.")