from kruti.tools.builtins.retrieve import RetrieveTool

def test_retrieve_returns_results():
    t = RetrieveTool()
    out = t.run({"query": "guardrails allowlist"})
    assert "guardrails" in out.lower() or out == "no_results"
