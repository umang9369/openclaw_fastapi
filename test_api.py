import asyncio
from services.gemini_client import call_llm

async def main():
    try:
        res = await call_llm([{"role": "user", "content": "Hello!"}])
        print("Success:", res)
    except Exception as e:
        print("Error:", e)

asyncio.run(main())
