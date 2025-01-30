from fastapi import FastAPI, Request, Form
from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse

app = FastAPI()

# In-memory store for the shopping list
SHOPPING_LIST = []

@app.post("/whatsapp", response_class=PlainTextResponse)
async def whatsapp_webhook(
    request: Request,
    Body: str = Form(...)
):
    """
    This endpoint will be triggered by Twilio whenever a user sends a WhatsApp message
    to your Twilio sandbox number. We'll parse that message and add it to our shopping list.
    """
    incoming_msg = Body.strip().lower()
    
    # Create a Twilio MessagingResponse object to generate the reply
    resp = MessagingResponse()
    
    # If user wants to see the list
    if incoming_msg in ["list", "show", "show list"]:
        if SHOPPING_LIST:
            items_str = "\n".join(f"- {item}" for item in SHOPPING_LIST)
            reply_text = f"Your current shopping list:\n{items_str}"
        else:
            reply_text = "Your shopping list is empty."
        resp.message(reply_text)
        return str(resp)
    
    # If user wants to clear the list
    if incoming_msg in ["clear", "reset"]:
        SHOPPING_LIST.clear()
        resp.message("Your shopping list has been cleared.")
        return str(resp)
    
    # Otherwise, add the item to the list
    SHOPPING_LIST.append(Body.strip())
    reply_text = (
        f"Added '{Body.strip()}' to your shopping list!\n\n"
        "Send 'list' to see all items, or 'clear' to reset."
    )
    resp.message(reply_text)
    
    return str(resp)


@app.get("/")
def index():
    return {"message": "WhatsApp Shopping List Bot is running!"}
