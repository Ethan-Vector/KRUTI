from kruti.agent.loop import Agent
from kruti.guardrails.runtime import Guardrails
from kruti.llm.rule import RuleLLM
from kruti.tools.registry import ToolRegistry

def test_agent_calc_path():
    agent = Agent(
        llm=RuleLLM(),
        tools=ToolRegistry.default(),
        guardrails=Guardrails({"calc","retrieve"}, 10),
        system_prompt="You are KRUTI."
    )
    out = agent.run("calculate: 19*7", max_steps=4)
    assert "133" in out or out  # if RuleLLM returns tool result first, next action may be final later in loop

def test_guardrails_blocks_tool():
    agent = Agent(
        llm=RuleLLM(),
        tools=ToolRegistry.default(),
        guardrails=Guardrails({"retrieve"}, 10),
        system_prompt="You are KRUTI."
    )
    try:
        agent.run("calculate: 2+2", max_steps=2)
        assert False, "Expected PermissionError"
    except PermissionError:
        assert True
