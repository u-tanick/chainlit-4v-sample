import os
import base64
import chainlit as cl
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

@cl.on_message
async def on_message(message: cl.Message):
    if not message.elements:
        await cl.Message(content="画像が存在しません").send()
        return

    # 画像を取得して、base64エンコーディング    
    images = [file for file in message.elements if "image" in file.mime]
    encoded = base64.b64encode(images[0].content).decode()
    
    # テキストと画像を送信
    messages=[
            # {"role": "user", "content": message.content},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": message.content},
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64, {encoded}"
                    },
                ]
            }
        ]
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=messages,
        max_tokens=1000
    )

    # 受け取った結果をチャットに送信
    await cl.Message(
        content=response.choices[0].message.content,
    ).send()
