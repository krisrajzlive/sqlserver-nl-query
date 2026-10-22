import streamlit as st

from nlquery import lc, li

EXAMPLES = [
    "Which hotels under 150 dollars include parking?",
    "Top 3 highest rated hotels and their prices",
    "Average price per night by country",
    "Somewhere quiet and romantic with good food",
    "Family-friendly beach resort with activities for kids",
    "Traditional place with hot spring baths",
]

st.set_page_config(page_title="Hotels NL Query", page_icon="🏨", layout="centered")
st.title("🏨 Ask your SQL Server in plain English")
st.caption("Local SQL Server · Azure AI Foundry · LangChain / LlamaIndex")

with st.sidebar:
    engine = st.radio("Framework", ["LangChain", "LlamaIndex"])
    mode = st.radio("Retrieval path", ["Auto (router)", "SQL only", "Vector only"],
                    disabled=engine == "LlamaIndex",
                    help="LlamaIndex always routes automatically.")
    st.divider()
    st.write("**Examples**")
    for ex in EXAMPLES:
        if st.button(ex, use_container_width=True):
            st.session_state["q"] = ex

question = st.text_input("Your question", key="q", placeholder="e.g. cheapest hotel in Japan")


def run(q: str):
    if engine == "LlamaIndex":
        return li.ask(q)
    return {"Auto (router)": lc.ask, "SQL only": lc.ask_sql, "Vector only": lc.ask_vector}[mode](q)


if st.button("Ask", type="primary") and question.strip():
    with st.spinner("Thinking..."):
        try:
            ans = run(question.strip())
        except Exception as e:  # surface model/SQL errors in the UI
            st.error(f"{type(e).__name__}: {e}")
        else:
            st.markdown(ans.text)
            st.caption(f"Path used: **{ans.route}**")
            if ans.sql:
                with st.expander("Generated SQL"):
                    st.code(ans.sql, language="sql")
