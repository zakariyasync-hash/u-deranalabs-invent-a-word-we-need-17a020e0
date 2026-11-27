# FLOW.md

1. `python3 main.py` runs with no arguments and no network.
2. It validates the entry text against the gate (1–140 UTF-8 characters,
   not only white space, single line) and fails loudly if it ever drifts.
3. It writes the one deterministic line to `/output/entry.txt`.
4. Verify with: `wc -m /output/entry.txt && sha256sum /output/entry.txt`
   — expect 106 characters, one line, no trailing newline.
