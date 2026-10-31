import os
from fastapi import FastAPI, Request
import uvicorn
from openai import OpenAI

app = FastAPI()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

RASAQ_SYSTEM_PROMPT = """
أنت اسمك "رَسَق"، موظف استقبال ذكي لعيادة تجميل فخمة.
- أسلوبك بالكلام: باللهجة السعودية الطبيعية، الذربة، العفوية، وبدون تكلف أو كلام زايد.
- قاعدتك الأساسية: كن مختصراً ومباشراً، لا تكتب فقرات طويلة، ورد كأنك شخص حقيقي قاعد يرد من جواله.
- مهمتك: تجاوب الزباين عن الأسعار الخدمات والمواعيد بكل دقة، وإذا ما عندك معلومة واضحة، لا تألف من راسك.
"""

@app.post("/webhook")
async def receive_whatsapp_message(request: Request):
    data = await request.json()
    user_message = data.get("message", "السلام عليكم")
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": RASAQ_SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ]
    )
    
    rasaq_reply = response.choices[0].message.content
    print("رد رَسَق:", rasaq_reply)
    
    return {"status": "success", "reply": rasaq_reply}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
  
