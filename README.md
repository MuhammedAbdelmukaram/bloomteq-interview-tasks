﻿# bloomteq-interview-tasks

> Two Python tasks:  
> 1. **Task 1** – Generate a new `{\"id\":…, \"value\":…}` entry based on repeat‐enabler rules.  
> 2. **Task 2** – Safely lookup a nested value in a dict via a dot‐separated path.

---

## Table of Contents

1. [Overview](#overview)  
2. [Features](#features)  
3. [Getting Started](#getting-started)  
   - [Prerequisites](#prerequisites)  
   - [Installation](#installation)  
   - [Directory Structure](#directory-structure)  
4. [Usage](#usage)  
   - [Task 1: `generate_new_entry`](#task-1-generatenewentry)  
   - [Task 2: `lookup`](#task-2-lookup)  
5. [Testing](#testing)    
6. [Contact](#contact)  

---

## Overview

This repository contains two standalone modules:

- **Task 1** (`task1/logic.py` + `task1/helpers.py`):  
  `generate_new_entry(existing: List[Dict[str,int]])`  
  • Extracts IDs and values, enforces repeat rules, optimized to **O(n)**.

- **Task 2** (`task2/logic.py`):  
  `lookup(obj: Dict, path: str) → Any`  
  • Traverses a nested dict by a dot‐separated string, returns `None` on invalid access in **O(k)** time (k = path depth).

Both modules come with full **unit-test coverage**, follow **PEP 8**, and include docstrings.

---

## Features

- **Modular code**: helpers separated into their own file  
- **Single-pass algorithms**: Task 1 in O(n), Task 2 in O(k)  
- **Robust error handling**: ignores invalid entries, returns `None` on bad lookups  
- **High-coverage tests**: edge cases, invalid inputs, large data sets  

---

## Getting Started

### Prerequisites

- Python 3.8 or newer  
- (Optional) Virtualenv/venv

### Installation

1. **Clone** the repo:  
   ```bash
   git clone https://github.com/MuhammedAbdelmukaram/bloomteq-interview-tasks.git
   cd bloomteq-interview-tasks
   ```
2. **(Optional) Create & activate** a virtualenv:  
   ```bash
   python -m venv .venv
   source .venv/bin/activate    # macOS/Linux
   .venv\Scripts\activate       # Windows
   ```

### Directory Structure

```text
.
├── README.md
├── task1
│   ├── __init__.py
│   ├── helpers.py      # extract_used_ids_and_values, find_valid_candidate_value
│   └── logic.py        # generate_new_entry
├── task2
│   ├── __init__.py
│   └── logic.py        # lookup
└── tests
    ├── __init__.py
    ├── test_task1.py
    └── test_task2.py
```

---

## Usage

### Task 1 – `generate_new_entry`

```python
from task1.logic import generate_new_entry

existing = [
    {"id": 1, "value": 3},
    {"id": 2, "value": 3},
    {"id": 3, "value": 7},
]
new_entry = generate_new_entry(existing)
# e.g. {"id": 4, "value": 4}
```

### Task 2 – `lookup`

```python
from task2.logic import lookup

obj = {"user": {"details": {"name": "Jane"}}}
print(lookup(obj, "user.details.name"))  # Jane
print(lookup(obj, "user.details.age"))   # None
```

---

## Testing

Run all tests with:

```bash
python -m unittest discover -v
```

Or target a single suite:

```bash
python -m unittest tests/test_task1.py
```

---

## Contact

Muhammed Abdelmukaram - [m.abdelmukaram@outlook.com](mailto:m.abdelmukaram@outlook.com) 
GitHub: https://github.com/MuhammedAbdelmukaram/bloomteq-interview-tasks
