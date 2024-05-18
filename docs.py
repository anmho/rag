

import asyncio
from pathlib import Path
import httpx



async def get_doc(client: httpx.AsyncClient, name: str):
    print("making request")
    url = f"https://raw.githubusercontent.com/awsdocs/aws-lambda-developer-guide/0c9e6e431d01a8160cec3d5734150f5d92f9fe7d/doc_source/{name}"

    r = await client.get(url)
    file = Path(f"docs/{name}")
    if not file.exists():
        file.parent.mkdir(parents=True, exist_ok=True)
    with open(file, "w+") as f:
        f.write(r.text)

async def get_docs(docnames):
    promises = []
    async with httpx.AsyncClient() as client:
        for name in docnames:

            promise = get_doc(client, name)
            promises.append(promise)
            if len(promises) >= 50:
                docs = await asyncio.gather(*promises)
                promises.clear()

        await asyncio.gather(*promises)
        promises.clear()
            
                

async def main():
    docnames = []
    with open("docs.txt", "r") as f:
        for line in f:
            parts = line.split(" ")

            for part in parts:
                part = part.strip()
                # print(bytes(part, encoding='ascii'), sep="")
                if part.endswith(".md"):
                    docnames.append(part)
    await get_docs(docnames=docnames)
asyncio.run(main())
                


