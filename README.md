# Character Generator (CharGen)

This was my bachelor's thesis project, completed in 2024 at the University of Calabria, Italy. <br>
A Python desktop application that creates and manages Non‑Player Characters (NPCs) endowed with coherent, Big‑Five‑based personalities and dynamic backstories. <br>
The system couples an easy‑to‑use Tkinter GUI with local Large Language Models (LLMs), allowing real‑time, memory‑aware dialogue generation for role‑playing games and narrative prototypes.

---

## Features

- **Big‑Five personality synthesis**: generate or edit the five traits numerically and preview them instantly.
- **Backstory & dialogue auto‑generation**: 3‑shot prompting crafts up‑to‑25‑line origin stories and in‑character replies.
- **Persistent conversational memory**: chat summaries are stored in SQLite and re‑injected into future prompts for long‑term coherence.
- **Model‑agnostic**: works with any LLM that exposes an OpenAI‑compatible API and supports ≥ 4 000 tokens context length.
- **Statistical evaluation**: built‑in IPIP‑50 test runner, CSV logging and Matplotlib/Seaborn plots to benchmark accuracy vs. inference time.

---
