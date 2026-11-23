"""LangGraph reference skeleton for Baking Wiki.

Not production-ready: connect real search, fetch, parsing, duplicate-check,
and GitHub persistence tools before treating a run as automated.

Install: pip install langgraph
"""
from typing import Any, TypedDict, Literal
from langgraph.graph import StateGraph, START, END

MAX_RETRIES = 2


class RecipeState(TypedDict, total=False):
    topic: str
    language: str
    candidate_urls: list[str]
    fetched_pages: list[dict[str, Any]]
    parsed_recipes: list[dict[str, Any]]
    normalized_recipes: list[dict[str, Any]]
    validation_issues: list[str]
    duplicate_matches: list[dict[str, Any]]
    duplicate_decision: str
    persisted_files: list[str]
    pending_review_files: list[str]
    retry_counts: dict[str, int]
    source_status: str
    schema_status: str
    quality_status: str
    doc_consistency_status: str
    persist_status: str
    report: dict[str, Any]


def retry_count(state: RecipeState, stage: str) -> int:
    return state.get("retry_counts", {}).get(stage, 0)


def bump_retry(state: RecipeState, stage: str) -> dict:
    counts = dict(state.get("retry_counts", {}))
    counts[stage] = counts.get(stage, 0) + 1
    return {"retry_counts": counts}


def plan(state: RecipeState) -> dict:
    return {
        "language": state.get("language", "zh-TW"),
        "candidate_urls": state.get("candidate_urls", []),
        "fetched_pages": [], "parsed_recipes": [], "normalized_recipes": [],
        "validation_issues": [], "duplicate_matches": [],
        "persisted_files": [], "pending_review_files": [],
        "retry_counts": state.get("retry_counts", {}),
    }


def search(state: RecipeState) -> dict:
    # TODO: connect a real search provider; never fabricate URLs.
    return {"candidate_urls": state.get("candidate_urls", [])}


def fetch(state: RecipeState) -> dict:
    # TODO: fetch candidate URLs; retain URL, timestamp, status and page text.
    return {"fetched_pages": state.get("fetched_pages", [])}


def source_gate(state: RecipeState) -> dict:
    pages = state.get("fetched_pages", [])
    valid = [p for p in pages if p.get("ok") and p.get("url") and p.get("content")]
    issues = [] if valid else ["沒有成功讀取且可追溯的食譜來源"]
    return {"fetched_pages": valid, "source_status": "PASS" if valid else "FAIL",
            "validation_issues": state.get("validation_issues", []) + issues}


def parse(state: RecipeState) -> dict:
    # TODO: parse only content actually present in fetched_pages.
    return {"parsed_recipes": state.get("parsed_recipes", [])}


def normalize(state: RecipeState) -> dict:
    # TODO: preserve source quantities/units alongside translations/conversions.
    return {"normalized_recipes": state.get("normalized_recipes", [])}


def schema_check(state: RecipeState) -> dict:
    recipes = state.get("normalized_recipes", [])
    required = {"title", "source_url", "ingredients", "steps"}
    issues = list(state.get("validation_issues", []))
    missing = []
    for i, recipe in enumerate(recipes):
        absent = sorted(required - set(recipe))
        if absent:
            missing.append(f"食譜 {i + 1} 缺少欄位：{', '.join(absent)}")
    issues.extend(missing)
    return {"schema_status": "PASS" if recipes and not missing else "FAIL",
            "validation_issues": issues}


def repair(state: RecipeState) -> dict:
    # TODO: repair only fields verifiable from source evidence.
    # Never invent missing ingredients, quantities, times or temperatures.
    return {}


def reasoning_check(state: RecipeState) -> dict:
    # TODO: check ingredient-step consistency, total time, temperatures,
    # equipment, allergens, safety and source evidence.
    # Until implemented, do not promote a recipe to PASS.
    issues = list(state.get("validation_issues", []))
    if not state.get("normalized_recipes"):
        issues.append("沒有可供內容檢查的標準化食譜")
    return {"quality_status": "WARNING", "validation_issues": issues}


def doc_consistency_check(state: RecipeState) -> dict:
    # TODO: load the paired Markdown Wiki and HTML deck, then compare source URL,
    # ingredient names/amounts, yield, pan, temperature, key method and status.
    # Never report PASS until a real file comparator has completed those checks.
    return {
        "doc_consistency_status": "WARNING",
        "validation_issues": state.get("validation_issues", []) +
            ["Markdown／HTML 自動一致性比較器尚未連接；需人工核對"],
    }


def repair_presentation(state: RecipeState) -> dict:
    # TODO: regenerate/update HTML only from the approved normalized Wiki record.
    # Do not invent values or silently replace manually curated content.
    return {"doc_consistency_status": "MISMATCH"}


def deduplicate(state: RecipeState) -> dict:
    # TODO: compare title, source URL, ingredients and method similarity.
    return {"duplicate_matches": state.get("duplicate_matches", [])}


def duplicate_review(state: RecipeState) -> dict:
    # Default to human review; never overwrite an existing recipe implicitly.
    return {"duplicate_decision": state.get("duplicate_decision", "NEEDS_HUMAN_REVIEW")}


def persist(state: RecipeState) -> dict:
    # TODO: write PASS records only; update index.md and log.md.
    # Return paths only after GitHub confirms successful writes.
    return {"persist_status": "NOT_CONNECTED", "persisted_files": []}


def quarantine(state: RecipeState) -> dict:
    # TODO: save WARNING records in a pending-review location only.
    return {"pending_review_files": state.get("pending_review_files", [])}


def human_review(state: RecipeState) -> dict:
    return {"quality_status": state.get("quality_status", "NEEDS_HUMAN_REVIEW")}


def report(state: RecipeState) -> dict:
    return {"report": {
        "source_count": len(state.get("fetched_pages", [])),
        "recipe_count": len(state.get("normalized_recipes", [])),
        "schema_status": state.get("schema_status", "UNSET"),
        "quality_status": state.get("quality_status", "UNSET"),
        "persist_status": state.get("persist_status", "NOT_ATTEMPTED"),
        "persisted_files": state.get("persisted_files", []),
        "pending_review_files": state.get("pending_review_files", []),
        "issues": state.get("validation_issues", []),
        "retry_counts": state.get("retry_counts", {}),
    }}


def route_source(state: RecipeState) -> Literal["parse", "retry_search", "human_review"]:
    if state.get("source_status") == "PASS":
        return "parse"
    return "retry_search" if retry_count(state, "source") < MAX_RETRIES else "human_review"


def route_schema(state: RecipeState) -> Literal["reasoning_check", "repair", "retry_fetch", "human_review"]:
    if state.get("schema_status") == "PASS":
        return "reasoning_check"
    if state.get("parsed_recipes") and retry_count(state, "repair") < MAX_RETRIES:
        return "repair"
    if retry_count(state, "schema_fetch") < MAX_RETRIES:
        return "retry_fetch"
    return "human_review"


def route_quality(state: RecipeState) -> Literal["doc_consistency", "quarantine", "retry_fetch", "human_review"]:
    status = state.get("quality_status")
    if status == "PASS":
        return "doc_consistency"
    if status == "WARNING":
        return "quarantine"
    if retry_count(state, "reasoning_fetch") < MAX_RETRIES:
        return "retry_fetch"
    return "human_review"


def route_doc_consistency(state: RecipeState) -> Literal["deduplicate", "repair_presentation", "quarantine", "human_review"]:
    status = state.get("doc_consistency_status")
    if status == "PASS":
        return "deduplicate"
    if status == "WARNING":
        return "quarantine"
    if retry_count(state, "presentation_repair") < MAX_RETRIES:
        return "repair_presentation"
    return "human_review"


def route_duplicate(state: RecipeState) -> Literal["persist", "duplicate_review"]:
    return "duplicate_review" if state.get("duplicate_matches") else "persist"


def route_duplicate_decision(state: RecipeState) -> Literal["persist", "report", "human_review"]:
    decision = state.get("duplicate_decision")
    if decision in ("APPROVED_NEW", "APPROVED_NEW_VERSION"):
        return "persist"
    if decision == "CONFIRMED_DUPLICATE":
        return "report"
    return "human_review"


def route_persist(state: RecipeState) -> Literal["report", "retry_persist", "human_review"]:
    if state.get("persist_status") == "SUCCESS":
        return "report"
    return "retry_persist" if retry_count(state, "persist") < MAX_RETRIES else "human_review"


graph = StateGraph(RecipeState)
for name, fn in [
    ("plan", plan), ("search", search), ("fetch", fetch),
    ("source_gate", source_gate), ("parse", parse), ("normalize", normalize),
    ("schema_check", schema_check), ("repair", repair),
    ("reasoning_check", reasoning_check), ("doc_consistency_check", doc_consistency_check),
    ("repair_presentation", repair_presentation), ("deduplicate", deduplicate),
    ("duplicate_review", duplicate_review), ("persist", persist),
    ("quarantine", quarantine), ("human_review", human_review), ("report", report),
]:
    graph.add_node(name, fn)

graph.add_node("retry_source", lambda s: bump_retry(s, "source"))
graph.add_node("retry_repair", lambda s: bump_retry(s, "repair"))
graph.add_node("retry_schema_fetch", lambda s: bump_retry(s, "schema_fetch"))
graph.add_node("retry_reasoning_fetch", lambda s: bump_retry(s, "reasoning_fetch"))
graph.add_node("retry_persist", lambda s: bump_retry(s, "persist"))

graph.add_edge(START, "plan")
graph.add_edge("plan", "search")
graph.add_edge("search", "fetch")
graph.add_edge("fetch", "source_gate")
graph.add_conditional_edges("source_gate", route_source, {
    "parse": "parse", "retry_search": "retry_source", "human_review": "human_review"})
graph.add_edge("retry_source", "search")
graph.add_edge("parse", "normalize")
graph.add_edge("normalize", "schema_check")
graph.add_conditional_edges("schema_check", route_schema, {
    "reasoning_check": "reasoning_check", "repair": "retry_repair",
    "retry_fetch": "retry_schema_fetch", "human_review": "human_review"})
graph.add_edge("retry_repair", "repair")
graph.add_edge("repair", "schema_check")
graph.add_edge("retry_schema_fetch", "fetch")
graph.add_conditional_edges("reasoning_check", route_quality, {
    "doc_consistency": "doc_consistency_check", "quarantine": "quarantine",
    "retry_fetch": "retry_reasoning_fetch", "human_review": "human_review"})
graph.add_edge("retry_reasoning_fetch", "fetch")
graph.add_conditional_edges("doc_consistency_check", route_doc_consistency, {
    "deduplicate": "deduplicate", "repair_presentation": "retry_presentation",
    "quarantine": "quarantine", "human_review": "human_review"})
graph.add_node("retry_presentation", lambda s: bump_retry(s, "presentation_repair"))
graph.add_edge("retry_presentation", "repair_presentation")
graph.add_edge("repair_presentation", "doc_consistency_check")
graph.add_conditional_edges("deduplicate", route_duplicate, {
    "persist": "persist", "duplicate_review": "duplicate_review"})
graph.add_conditional_edges("duplicate_review", route_duplicate_decision, {
    "persist": "persist", "report": "report", "human_review": "human_review"})
graph.add_conditional_edges("persist", route_persist, {
    "report": "report", "retry_persist": "retry_persist", "human_review": "human_review"})
graph.add_edge("retry_persist", "persist")
graph.add_edge("quarantine", "report")
graph.add_edge("human_review", "report")
graph.add_edge("report", END)

app = graph.compile()

if __name__ == "__main__":
    # No external tools/URLs are configured. This should not fabricate data
    # or claim persistence; connect integrations and tests before production.
    result = app.invoke({"topic": "烘焙食譜", "language": "zh-TW"})
    print(result.get("report", result))
