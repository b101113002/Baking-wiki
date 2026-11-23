"""LangGraph workflow skeleton; illustrative, not a live-run record.
Install: pip install langgraph
Connect real search/fetch and persistence tools before production use.
"""
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END

class RecipeState(TypedDict, total=False):
    topic: str
    urls: list[str]
    fetched: list[dict]
    recipes: list[dict]
    issues: list[str]
    retry_count: int
    status: str

def plan(s): return {"retry_count": s.get("retry_count", 0), "issues": []}
def search(s):
    # TODO: connect a search provider; never fabricate URLs.
    return {"urls": s.get("urls", [])}
def fetch(s):
    # TODO: fetch URLs and retain source URL + retrieval status.
    return {"fetched": s.get("fetched", [])}
def parse(s):
    # TODO: parse only content actually present in fetched pages.
    return {"recipes": s.get("recipes", [])}
def validate(s):
    issues = list(s.get("issues", []))
    if not s.get("recipes"): issues.append("沒有解析到食譜資料")
    return {"issues": issues, "status": "PASS" if s.get("recipes") and not issues else "WARNING"}
def route(s) -> Literal["persist", "retry", "review"]:
    if s.get("status") == "PASS": return "persist"
    if s.get("retry_count", 0) < 2: return "retry"
    return "review"
def persist(s):
    # TODO: write validated pages to GitHub with provenance.
    return {"status": "READY_TO_PERSIST"}
def review(s): return {"status": "NEEDS_HUMAN_REVIEW"}

g=StateGraph(RecipeState)
for name, fn in [("plan",plan),("search",search),("fetch",fetch),("parse",parse),
                 ("validate",validate),("persist",persist),("review",review)]:
    g.add_node(name,fn)
g.add_edge(START,"plan"); g.add_edge("plan","search"); g.add_edge("search","fetch")
g.add_edge("fetch","parse"); g.add_edge("parse","validate")
g.add_conditional_edges("validate",route,{"persist":"persist","retry":"search","review":"review"})
g.add_edge("persist",END); g.add_edge("review",END)
app=g.compile()
if __name__=="__main__":
    print(app.invoke({"topic":"烘焙食譜","urls":[],"recipes":[]}))
