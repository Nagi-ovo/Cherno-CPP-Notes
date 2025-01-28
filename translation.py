import os
import asyncio
import openai
import dotenv
import aiofiles
import logging
from asyncio import Queue
from openai import AsyncOpenAI

dotenv.load_dotenv()
openai.api_key = dotenv.get_key(".env", "API_KEY")
en_dir = "docs/en/51-100"

async def log_message(queue: Queue, message: str):
    await queue.put(message)

async def log_worker(queue: Queue):
    while True:
        message = await queue.get()
        if message is None:
            queue.task_done()
            break
        logging.info(message)
        queue.task_done()

class OpenAITranslator:
    def __init__(self, api_key: str, en_dir: str, max_concurrent: int = 5):
        self.client = AsyncOpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.en_dir = en_dir

    async def translate_file(self, filename: str, log_queue: Queue, max_retries: int = 3):
        file_path = os.path.join(self.en_dir, filename)
        
        async with self.semaphore:
            async with aiofiles.open(file_path, "r", encoding="utf-8") as file:
                await log_message(log_queue, file_path)
                content = await file.read()

            for attempt in range(max_retries):
                try:
                    response = await self.client.chat.completions.create(
                        model="deepseek-chat",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant"},
                            {"role": "user", "content": "你是一个充满人格魅力的编程科普专家，下面是一篇作者对游戏引擎工程师Cherno的C++教程的学习笔记，请你将其文字部分翻译为地道的英语，你的要求是能使用正确的技术术语，并严格保持原文的Markdown、图片、引用等格式和结构不变，请不要漏掉原文中的任何内容！直接输出Markdown内容即可，不需要从```开始。\n笔记正文：\n" + content}
                        ],
                        temperature=1.3
                    )
                    translated_content = response.choices[0].message.content
                    
                    async with aiofiles.open(file_path, "w", encoding="utf-8") as output_file:
                        await output_file.write(translated_content)
                        await log_message(log_queue, f"{filename} translated")
                    
                    return f"Translated: {filename}"
                except Exception as e:
                    if attempt < max_retries - 1:
                        await log_message(log_queue, f"Attempt {attempt + 1} failed for {filename}: {str(e)}, retrying...")
                        await asyncio.sleep(1)
                    else:
                        await log_message(log_queue, f"Error translating {filename} after {max_retries} attempts: {str(e)}")
                        return f"Failed to translate: {filename}"

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    log_queue = Queue()
    
    log_worker_task = asyncio.create_task(log_worker(log_queue))
    
    translator = OpenAITranslator(api_key=openai.api_key, en_dir=en_dir, max_concurrent=5)
    
    files = [f for f in os.listdir(en_dir) if f.endswith(".md")]
    tasks = [translator.translate_file(filename, log_queue) for filename in files]
    results = await asyncio.gather(*tasks)
    
    await log_queue.put(None)
    await log_worker_task
    
    for result in results:
        logging.info(result)

if __name__ == "__main__":
    asyncio.run(main())