from nevara.agent.interface import Interface
import asyncio

interface = Interface()

async def main():
    while True:
        userInput = input("user: ")
        if userInput == '/exit':  break
        await interface.astream_audioSupport(userInput=userInput)

if __name__ == "__main__":
    asyncio.run(main())
