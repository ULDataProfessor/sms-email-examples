---
---

# 🐾 Pet Store AI Pipeline Example

The pet store demo shows how adoption records can flow through a simple pipeline. The script `pipeline.py` accepts adoption data as JSON objects typed into the console. It identifies any animals under one year old that need a first vet visit and prints reminders.

## Running
```bash
python pipeline.py
```
Provide JSON objects like:
```json
{"name": "Fluffy", "species": "cat", "age": 0.5}
```
Finish with a blank line to see the generated messages.
