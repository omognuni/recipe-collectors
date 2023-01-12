import aiohttp
import asyncio


URL =  'https://www.10000recipe.com/'

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()
        
        
async def search():
    url = URL
    async with aiohttp.ClientSession() as session:
        result = await fetch(session, url)
        print(result)


if __name__ == '__main__':
    asyncio.run(search())