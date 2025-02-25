# Human-In-Loop-Single-Agent
A Human-in-the-Loop (HITL) single-agent system built with LangChain and OpenAI, designed for booking travel tickets. This workflow allows users to interactively review, edit, or cancel tool actions before execution, ensuring human oversight and accuracy.

🚀 Features  
✅ Human-in-the-Loop (HITL) integration for real-time action validation.  
🎯 Single-agent architecture using LangChain StateGraph.  
💬 Dynamic user feedback for tool invocation.  
✈️ Travel ticket booking with customizable parameters (date, location, class, passengers).  
🔗 OpenAI GPT integration with streaming support.  
⚡ Robust input validation and error handling.  

💡 Example Input:  
I need to book a ticket on 12th March 2025 for 2 passengers from Mumbai to Dubai in economy class.  
🔄 The agent will:  
Parse user input  
Propose tool actions  
Allow you to:  
✅ Execute  - Proceed with execution  
✏️ Edit  - Update the tool call before execution  
💬 Provide feedback -  Ask LLM to refine the tool call    
❌ Cancel  - Can cancel the execution  

**The Flow can be as**  
**1. APPROVE**  
**Query 👤 : “I need to book a ticket on 12th March 2025 for 2 passengers from mumbai to dubai in economy class”**  
Proposed action: tool='book_ticket' tool_input={'date': '2025-03-12', 'from_location': 'Mumbai', 'to_location': 'Dubai', 'passengers': 2, 'class_type': 'economy'}
Choose an option:
1. Execute action [y]
2. Edit action [e]
3. Provide feedback [f]
4. Cancel [n]  
**Your choice: y**  
**Output 🤖 : “I have successfully booked 2 economy class tickets from Mumbai to Dubai for 12th March 2025. The total price for the tickets is $600. Your booking reference is BOK-9223014.”**

**2. MODIFY - Direct Human Edits IN JSON**

**Query 👤 : “I need to book a ticket on 12th March 2025 for 2 passengers from mumbai to dubai in economy class”**  
Proposed action: tool='book_ticket' tool_input={'date': '2025-03-12', 'from_location': 'Mumbai', 'to_location': 'Dubai', 'passengers': 2, 'class_type': 'economy'}
Choose an option:
1. Execute action [y]
2. Edit action [e]
3. Provide feedback [f]
4. Cancel [n]
**Your choice: e**
Current tool input: {'date': '2025-03-12', 'from_location': 'Mumbai', 'to_location': 'Dubai', 'passengers': 2, 'class_type': 'economy'}  
**Enter new tool input (as JSON string): {"date": "2024-03-20","from_location": "new york","to_location": "london","passengers": 2,"class_type": "business"}**

**Output 🤖:”I have successfully booked the flight tickets for 2 passengers from Mumbai to Dubai on 12th March 2025 in the economy class. The total price for the tickets is $4000.”**



**3.Provide Feedback 💬 — LLM Fixes It**

**Query 👤: “I need to book a ticket on 12th March 2025 for 2 passengers from mumbai to dubai in economy class”**  
Proposed action: tool='book_ticket' tool_input={ 'date': '2025-03-12', 'from_location': 'Mumbai', 'to_location': 'Dubai', 'passengers': 2, 'class_type': 'economy'}

Choose an option:
1. Execute action [y]
2. Edit action [e]
3. Provide feedback [f]
4. Cancel [n]
**Your choice: f**

**Provide your feedback about the tool call 👤: I need only single ticket**

Proposed action: tool='book_ticket' tool_input={'query': 'Book a ticket from Mumbai to Dubai', 'date': '2025-03-12', 'from_location': 'Mumbai', 'to_location': 'Dubai', 'passengers': 1, 'class_type': 'economy'}

Choose an option:
1. Execute action [y]
2. Edit action [e]
3. Provide feedback [f]
4. Cancel [n]
**Your choice: y**  

**Output 🤖:”The ticket from Mumbai to Dubai for 1 passenger on 12th March 2025 in economy class has been successfully booked. The total price is $300. Booking reference: BOK-7904400.”**


Need to set your Open API Key & Install required dependencies.  
This may be the requirements -  
langchain>=0.1.0  
langchain-openai>=0.0.7  
langchain-community>=0.0.1  
openai>=1.0.0  
python-dotenv>=1.0.0  
tavily-search>=0.1.3  
Feel free to fork and contribute! ✨
