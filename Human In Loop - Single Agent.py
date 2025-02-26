from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolExecutor
from langchain_openai import ChatOpenAI
from langchain.tools.render import format_tool_to_openai_function
from langchain_core.utils.function_calling import convert_to_openai_function
from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage
from langgraph.prebuilt import ToolInvocation
import json
from langchain_core.tools import tool
from langchain_core.messages import FunctionMessage
from langgraph.graph import StateGraph, END
import os
from langchain_core.messages import HumanMessage

os.environ["OPENAI_API_KEY"] = "sk...............You can enter your opeN API key here"

@tool
def book_ticket( date: str = None, from_location: str = None, to_location: str = None, passengers: int = 1, class_type: str = "economy"):
    """Book a travel ticket with the specified parameters.
    Args:
        date: Travel date in YYYY-MM-DD format
        from_location: Departure city/location
        to_location: Arrival city/location
        passengers: Number of passengers
        class_type: Class of travel (economy/business/first)
    """
    # This is a placeholder for actual ticket booking implementation
    
    # Sample ticket database
    available_routes = {
        ("new york", "london"): {
            "economy": 500,
            "business": 2000,
            "first": 5000
        },
        ("san francisco", "tokyo"): {
            "economy": 800,
            "business": 3000,
            "first": 7000
        },
        ("mumbai", "dubai"): {
            "economy": 300,
            "business": 1200,
            "first": 3000
        }
    }
    
    # Normalize inputs
    from_location = (from_location or "").lower()
    to_location = (to_location or "").lower()
    class_type = (class_type or "economy").lower()
    
    # Validate inputs
    if not all([date, from_location, to_location]):
        return "Please provide all required information: date, departure city, and arrival city"
    
    # Check if route exists
    route = (from_location, to_location)
    if route not in available_routes:
        return f"No flights available from {from_location} to {to_location}"
    
    # Check if class type is valid
    if class_type not in available_routes[route]:
        return f"Invalid class type. Available options: economy, business, first"
    
    # Calculate total price
    price_per_ticket = available_routes[route][class_type]
    total_price = price_per_ticket * passengers
    
    return {
        "status": "success",
        "message": f"Ticket(s) booked successfully!",
        "details": {
            "from": from_location,
            "to": to_location,
            "date": date,
            "passengers": passengers,
            "class": class_type,
            "price_per_ticket": price_per_ticket,
            "total_price": total_price,
            "booking_reference": "BOK" + str(hash(str(route) + date))[:8]
        }
    }

tools = [book_ticket]
tool_executor = ToolExecutor(tools)

# We will set streaming=True so that we can stream tokens
# See the streaming section for more information on this.
model = ChatOpenAI(temperature=0, streaming=True)

# functions = [format_tool_to_openai_function(t) for t in tools]
functions = [convert_to_openai_function(t) for t in tools]
model = model.bind_functions(functions)

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

# Define the function that determines whether to continue or not
def should_continue(state):
    messages = state["messages"]
    last_message = messages[-1]
    # If there is no function call, then we finish
    if "function_call" not in last_message.additional_kwargs:
        print(f"last_message: {last_message}")
        print("end case")
        return "end"
    # Otherwise if there is, we continue
    else:
        print(f"last_message: {last_message}")
        print("continue case")
        return "continue"


# Define the function that calls the model
def call_model(state):
    messages = state["messages"]
    response = model.invoke(messages)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}


# Define the function to execute tools
def call_tool(state):
    messages = state["messages"]
    last_message = messages[-1]
    action = ToolInvocation(
        tool=last_message.additional_kwargs["function_call"]["name"],
        tool_input=json.loads(
            last_message.additional_kwargs["function_call"]["arguments"]
        ),
    )
    print(f"\nProposed action: {action}")
    
    while True:
        response = input("\nChoose an option:\n1. Execute action [y]\n2. Edit action [e]\n3. Provide feedback [f]\n4. Cancel [n]\nYour choice: ")
        
        if response.lower() == 'y':
            break
        elif response.lower() == 'n':
            print("Operation cancelled")
            #print(f"last_message: {last_message}")
            return {"messages": [HumanMessage(content="Operation cancelled by user")]}
        elif response.lower() == 'e':
            # Direct editing feature
            print(f"\nCurrent tool input: {action.tool_input}")
            new_input = input("Enter new tool input (as JSON string): ")
            try:
                # Parse and update the action with new input
                new_tool_input = json.loads(new_input)
                action = ToolInvocation(
                    tool=action.tool,
                    tool_input=new_tool_input
                )
                print(f"Updated action: {action}")
                # Update the original message to reflect the edited query
                query = f"Book a ticket from {new_tool_input.get('from_location', '')} to {new_tool_input.get('to_location', '')} on {new_tool_input.get('date', '')}"
                if 'passengers' in new_tool_input:
                    query += f" for {new_tool_input['passengers']} passengers"
                if 'class_type' in new_tool_input:
                    query += f" in {new_tool_input['class_type']} class"
                print(query)
                # Update messages with constructed query
                state["messages"] = [HumanMessage(content=query)]
                
                # Execute the edited action
                response = tool_executor.invoke(action)
                function_message = FunctionMessage(content=str(response), name=action.tool)
                return {"messages": [HumanMessage(content = query),function_message]}
            except json.JSONDecodeError:
                print("Invalid JSON format. Please try again.")
                continue
        elif response.lower() == 'f':
            # Feedback feature
            feedback = input("\nProvide your feedback about the tool call: ")
            feedback_message = HumanMessage(content=f"Adjust the tool call based on this feedback: {feedback}")
            messages.append(feedback_message)
            # Return to the agent to process the feedback
            return {"messages": messages}
            
    # Execute the final action
    response = tool_executor.invoke(action)
    function_message = FunctionMessage(content=str(response), name=action.tool)
    return {"messages": [function_message]}



# Define a new graph
workflow = StateGraph(AgentState)

# Define the two nodes we will cycle between
workflow.add_node("agent", call_model)
workflow.add_node("action", call_tool)

# Set the entrypoint as `agent`
# This means that this node is the first one called
workflow.set_entry_point("agent")

# We now add a conditional edge
workflow.add_conditional_edges(
    # First, we define the start node. We use `agent`.
    # This means these are the edges taken after the `agent` node is called.
    "agent",
    # Next, we pass in the function that will determine which node is called next.
    should_continue,
    # Finally we pass in a mapping.
    # The keys are strings, and the values are other nodes.
    # END is a special node marking that the graph should finish.
    # What will happen is we will call `should_continue`, and then the output of that
    # will be matched against the keys in this mapping.
    # Based on which one it matches, that node will then be called.
    {
        # If `tools`, then we call the tool node.
        "continue": "action",
        # Otherwise we finish.
        "end": END,
    },
)

# We now add a normal edge from `tools` to `agent`.
# This means that after `tools` is called, `agent` node is called next.
workflow.add_edge("action", "agent")

# Finally, we compile it!
# This compiles it into a LangChain Runnable,
# meaning you can use it as you would any other runnable
app = workflow.compile()


inputs = {"messages": [HumanMessage(content="I need to book a ticket on 12th March 2025 for 2 passengers from mumbai to dubai in economy class")]}
for output in app.stream(inputs):
    # stream() yields dictionaries with output keyed by node name
    for key, value in output.items():
        print(f"Output from node '{key}':")
        print("---")
        print(value)
    print("\n---\n")
