from kruti.tools.builtins.calc import CalcTool

def test_calc_mult():
    t = CalcTool()
    assert t.run({"expression": "19*7"}) == "133"

def test_calc_reject_calls():
    t = CalcTool()
    out = t.run({"expression": "__import__('os').system('echo hi')"})
    assert out.startswith("error:")
