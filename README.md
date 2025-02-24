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
✅ Execute  
✏️ Edit  - Direct JSON edit  
💬 Provide feedback - Can provide feedback in our natural language  
❌ Cancel  

Need to set your Open API Key & Install required dependencies.  
This may be the requirements -  
langchain>=0.1.0  
langchain-openai>=0.0.7  
langchain-community>=0.0.1  
openai>=1.0.0  
python-dotenv>=1.0.0  
tavily-search>=0.1.3  
Feel free to fork and contribute! ✨
