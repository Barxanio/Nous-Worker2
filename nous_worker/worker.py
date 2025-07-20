import asyncio
from nous_client import NousClient

class Worker:
    def __init__(self, client: NousClient, queue: asyncio.Queue, name: str):
        self.client = client
        self.queue = queue
        self.name = name

    async def run(self):
        while True:
            job = await self.queue.get()
            if job is None:
                print(f"[{self.name}] Завершение работы.")
                break

            messages, callback = job
            try:
                print(f"[{self.name}] Обработка запроса...")
                result = await self.client.chat(messages)
                await callback(result)
            except Exception as e:
                print(f"[{self.name}] Ошибка: {e}")
                await callback({"error": str(e)})
            finally:
                self.queue.task_done()