import asyncio
from worker import Worker
from nous_client import NousClient

async def sample_callback(result):
    print("✅ Ответ получен:")
    print(result)

async def main():
    with open("keys.txt") as f:
        keys = [line.strip() for line in f if line.strip()]

    queue = asyncio.Queue()
    clients = [NousClient(key) for key in keys]
    workers = [Worker(c, queue, f"Worker-{i+1}") for i, c in enumerate(clients)]

    tasks = [asyncio.create_task(w.run()) for w in workers]

    system_prompt = {
        "role": "system",
        "content": (
            "You are a deep thinking AI. Use <think> tags for internal reasoning. "
            "Deliberate thoroughly before answering."
        )
    }
    user_message = {
        "role": "user",
        "content": "Describe the philosophical implications of AI teaching other AI."
    }
    messages = [system_prompt, user_message]

    await queue.put((messages, sample_callback))

    await queue.join()

    for _ in workers:
        await queue.put(None)
    await asyncio.gather(*tasks)

    for client in clients:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())