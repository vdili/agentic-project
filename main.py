import streamlit as st
from pypdf import PdfReader

from core.graph import build_graph


# read pdf text
def read_pdf_text(uploaded_file, max_pages=3):
    reader = PdfReader(uploaded_file)
    text_parts = []
    pages = reader.pages[:max_pages]

    for i, page in enumerate(pages, start=1):
        page_text = page.extract_text() or ""
        text_parts.append(f"--- PAGE {i} ---\n{page_text}")

    return "\n".join(text_parts)


# page setup
st.set_page_config(page_title="Agentic Assistant", layout="centered")
st.title("Agentic Assistant")

# build graph once
graph = build_graph()

# task input
task = st.text_area("Write your task:")

st.subheader("Upload documents (optional)")
uploaded_files = st.file_uploader(
    "Upload PDF/TXT files",
    type=["pdf", "txt"],
    accept_multiple_files=True
)

# pdf page limit
max_pages = st.slider("Max PDF pages to read (faster)", 1, 10, 3)

run_btn = st.button("Run")


# split text into chunks
def make_chunks(text, doc_id, filename, size=500):
    chunks = []
    start = 0
    idx = 1

    while start < len(text):
        part = text[start:start + size]

        chunks.append({
            "doc_id": doc_id,
            "filename": filename,
            "locator": f"chunk {idx}",
            "text": part
        })

        start += size
        idx += 1

    return chunks


# run app logic
if run_btn:
    # validate task
    if not task.strip():
        st.warning("Please write a task first.")
        st.stop()

    all_chunks = []
    doc_id = 1

    # read uploaded files
    if uploaded_files:
        for f in uploaded_files:
            filename = f.name
            did = f"doc{doc_id}"
            doc_id += 1

            # txt file
            if filename.lower().endswith(".txt"):
                text = f.read().decode("utf-8", errors="ignore")

            # pdf file
            elif filename.lower().endswith(".pdf"):
                with st.spinner(f"Reading {filename}..."):
                    text = read_pdf_text(f, max_pages)

            else:
                continue

            # create chunks
            chunks = make_chunks(text, did, filename)
            all_chunks.extend(chunks)

    # initial state
    state = {
        "task": task,
        "chunks": all_chunks,
        "trace": []
    }

    # run agents
    with st.spinner("Running agents..."):
        result = graph.invoke(state)

    st.divider()

    # final answer
    st.subheader("Final Answer")
    st.write(result.get("final_answer", "No answer generated."))

    # sources output
    st.subheader("Citations / Sources")

    if result.get("sources"):
        for s in result["sources"]:
            if isinstance(s, dict):
                pid = s.get("id", "?")
                title = s.get("title", "unknown")
                loc = s.get("locator", "")

                st.markdown(f"- [{pid}] {title} ({loc})")
            else:
                st.markdown(f"- {s}")
    else:
        st.markdown("- (none)")

    # trace output
    st.subheader("Agent Trace")

    if result.get("trace"):
        st.table(result["trace"])
    else:
        st.write("(no trace)")