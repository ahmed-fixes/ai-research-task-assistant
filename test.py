from app.agent.routing import select_tool


result = select_tool("Calculate 25 * 8")

print("Tool Name:", result.tool_name)
print("Tool Input:", result.tool_input)