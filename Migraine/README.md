# MIGRAINE 🧠💥
**Migration Guidance & Refactor Assistant with Intentional, Guided Navigation & Execution**

MIGRAINE is a vibe compiler for experienced developers tackling high-stakes migrations and refactors. It doesn't teach you to code—it helps you *not lose your mind* while migrating that ancient PHP monolith into something clean, testable, and futureproof.

---

## 🔍 What It Does

MIGRAINE walks you through the steps of a refactor using `.jmp` prompt files, one decision at a time. It helps you:

- Extract context from legacy systems (or ask smart fallback questions)
- Plan new architectures
- Handle database and schema transitions
- Define auth, service boundaries, and file structure
- Build a TDD-driven refactor plan
- Execute changes (with temp file scaffolding)
- Verify success and perform cleanup
- Capture everything as `.mig` files in `/migraine/`

---

## 📁 Files & Structure

- `migraine.vw`: The manifest and table of contents
- `*.jmp`: Prompt modules that guide each stage
- `/migraine/`: Stores all `.mig` context files generated during the process

---

## 🧭 Navigation Flow

Each step can be:
- Run sequentially
- Skipped based on natural-language prompts
- Jumped to directly via user input or context clues

The `.vw` manifest contains structured metadata for all steps, including descriptions and triggering prompts.

---

## 🚦 Steps

1. `00_intro.jmp` – Context gathering from file paths or fallback questions  
2. `01_architecture.jmp` – Stack design, boundaries, and intent  
3. `02_databases.jmp` – DB migrations, schemas, storage decisions  
4. `03_authentication.jmp` – Auth and permission model transitions  
5. `04_file_structure.jmp` – Service and route layout redesign  
6. `05_tdd_plan.jmp` – Test planning before and during refactor  
7. `06_execution.jmp` – File scaffolding and refactor order  
8. `07_verification.jmp` – Post-refactor testing and sanity checks  
9. `08_cleanup.jmp` – Legacy removal and rollback plan  

---

## ✨ Philosophy

MIGRAINE doesn’t assume you’re lost—it assumes you’re overloaded.  
Its job is to bring order, structure, and a little wit to your chaos.

---

## 🧵 Need to Customize?

Fork it. Add more `.jmp` modules. Adjust the tone. Swap out storage targets. MIGRAINE is modular by design and works well with other vibe compilers.

---

## 🧑‍🚀 Made by Squibs & Rizzo

Tested under pressure. Powered by caffeine and context windows.

---
