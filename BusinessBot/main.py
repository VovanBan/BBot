from bots.memabot import main_memabot
from bots.memabotedit import main_memabotedit

async def main():
    await main_memabot()
    await main_memabotedit()

if __name__ == '__main__':
    main()
