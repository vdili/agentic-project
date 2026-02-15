# Agentic Assistant

This project implements a multi-agent AI system using LangGraph and Streamlit.
The system follows a Planner → Research → Writer → Verifier workflow and produces
grounded answers based on uploaded documents.

---

## Architecture

The system is composed of four agents:

1. **Planner**
   - Analyzes the user task
   - Creates a step-by-step plan

2. **Research**
   - Retrieves relevant information from uploaded documents
   - Uses TF-IDF vector search with cosine similarity
   - Returns evidence snippets with source metadata

3. **Writer**
   - Generates a draft answer using only the retrieved evidence
   - Attaches citations to the answer

4. **Verifier**
   - Checks whether the answer is supported by evidence
   - Returns "Not found in sources" if no reliable evidence is available

The agents are orchestrated using **LangGraph** with a shared state.

---

## Retrieval Method

The system uses a baseline vector search approach:

- TF-IDF vectorization
- Cosine similarity
- Top-k relevant text chunks are selected as evidence

This satisfies the project requirement for document-based retrieval.

---

## User Interface

The application is built with **Streamlit** and provides:

- Text input for user tasks
- File upload for PDF and TXT documents
- Configurable limit on PDF pages
- Display of:
  - Final answer
  - Citations / sources
  - Agent trace logs

---

## Setup

Install dependencies:

```bash
py -m pip install -r requirements.txt
```

---

## Run

Start the application:

```bash
py -m streamlit run main.py
```

Then open the local URL shown in the terminal.

---

## Project Structure

```
.
├── agents/
│   ├── planner.py
│   ├── research.py
│   ├── writer.py
│   └── verifier.py
├── core/
│   ├── graph.py
│   ├── state.py
│   └── retrieval.py
├── eval/
│   └── tests.json
├── main.py
└── README.md
```

---

## Evaluation

An evaluation dataset is provided in the `eval/tests.json` file.
It contains sample tasks, expected outputs, and associated documents
used to manually validate the system behavior.

Evaluation is currently performed manually by running the application
with the provided test cases.

---

## Limitations

- The system reads only the first N pages of PDF files
- TF-IDF is used as a baseline retrieval method
- No persistent vector database is used
- Evaluation is manual

---

## Future Improvements

- Replace TF-IDF with embedding-based retrieval (FAISS / Chroma)
- Add automated evaluation scripts
- Improve citation granularity
- Deploy the application
