from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from agent import DoctorAppointmentAgent
from langchain_core.messages import HumanMessage
import os
from typing import List, Dict, Any 
import traceback

os.environ.pop("SSL_CERT_FILE", None)

app = FastAPI()

class UserQuery(BaseModel):
    id_number: int = Field(..., description="7 or 8 digit patient ID", ge=1_000_000, le=99_999_999)
    messages: str = Field(..., min_length=1, description="User query message")

agent = DoctorAppointmentAgent()

@app.post("/execute")
async def execute_agent(user_input: UserQuery) -> Dict[str, Any]:
    try:
        app_graph = agent.workflow()
        input_messages = [HumanMessage(content=user_input.messages)]
        query_data = {
            "messages": input_messages,
            "id_number": user_input.id_number,
            "next": "",
            "query": "",
            "current_reasoning": "",
        }
        response = await app_graph.ainvoke(query_data, config={"recursion_limit": 20})
        return {"messages": [msg.content for msg in response["messages"]]}
    
    except Exception as e:
        print("Exception occurred:", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Could not process the request: {str(e)}")
    

# uvicorn main:app --reload