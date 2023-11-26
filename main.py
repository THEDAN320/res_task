import asyncio
import os
from time import sleep

from ui import MainInterface

#Константа для текста меню
MENU_TEXT = (
        "Выберите действие:\n"
        "1. Добавить игру\n"
        "2. Найти игру\n"
        "3. Изменить информацию о игре\n"
        "4. Удалить игру\n"
        "5. Вывести список игр\n"
        "6. Выход\n>>"
    )
    
async def start() -> None:
    """
    
    Главная функция программы.
    В ней вызываються методы из объекта класса MainInterface в зависимости от ввода пользователя.
    
    """
    main = MainInterface()
    await main.run_script()
    
    try:
        while True:
            user_input = input(MENU_TEXT)
            #проверяем корректность выбора.
            if user_input not in ["1", "2", "3", "4", "5", "6"]:
                await main.clear_console()
                print("Неверный ввод!\n")
                continue

            match user_input:
                case "1":
                    await main.add_game()
                case "2":
                    await main.find_game()
                case "3":
                    await main.select_game_for_update()
                case "4":
                    await main.select_game_for_deleting()
                case "5":
                    await main.get_list()
                case "6":
                    await main.close_script()
                    return
    except EOFError:
        await main.close_script()
        
    except:
        print("Произошла ошибка! скрипт будет перезапущен.")
        sleep(2)
        await main.close_script()
        os.system("run.bat")
        

if __name__ == "__main__":
    asyncio.run(start())
