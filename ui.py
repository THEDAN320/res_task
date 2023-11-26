import os
import platform

from DB.database import Database

class MainInterface:
    """
    
    Данный класс является интерфейсом между действиями пользователя и интерфейсом для базы данных.
    Его главная задача обрабатывать ввод пользователя и проверять корректность ввода перед вызывом методов из класса Database.
    
    """

    def __init__(self):
        """
        
        В конструкторе записываем операционную систему пользователя и создаем композицию класса Database.
        
        """
        self.__user_platform = platform.system()
        self.__db = Database()
    
    async def close_script(self) -> None:
        """
        
        Метод для завершения скрипта.
        
        """
        await self.__db.close_connect()
        
    async def run_script(self) -> None:
        """
        
        Метод для начала работы скрипта.
        
        """
        await self.clear_console()
        await self.__db.open_connect()
    
    async def clear_console(self) -> None:
        """
        
        Метод, который в зависимости от операционной системы пользователя выполняет команду для очистки консоли.
        
        """
        if self.__user_platform == "Windows":
            os.system("cls")
        else:
            os.system("clear")

    async def add_game(self) -> None:
        """
        
        Данный метод проверяет корректность ввода и передает аргументы для регистрации игры в бд.
        
        """
        await self.clear_console()
        name = None
        publisher = None
        date = None

        #запрашиваем и проверяем корректность ввода названия игры.
        while (name is None) or (len(name) < 1):
            if name is not None:
                print("Неверный ввод!\n")
            name = input("Введите название игры\n>>")
        
        #запрашиваем и проверяем корректность ввода издателя игры.
        while (publisher is None) or (len(publisher) < 1):
            if publisher is not None:
                print("Неверный ввод!\n")
            publisher = input("Введите издателя игры\n>>")
        
        #запрашиваем и проверяем корректность ввода даты.
        while (date is None) or (len(date) < 1):
            if date is not None:
                print("Неверный ввод!\n")
            date = input("Введите дату игры\n>>")

        await self.__db.register_game(name, publisher, date)
        await self.clear_console()
        print("Готово!")

    async def select_game_for_update(self) -> None:
        """
        
        Метод для выбора игры для редактирования ее информации.
        
        """

        await self.clear_console()
        #получем список игр
        games = await self.__db.get_list_games()
        game_index = None
        counter = 0

        if games == []:
            print("Нет игр для редактирования\n")
            return
            
        #создаем массив строк. строки имеют формат 'Номер_игры. Название игры'.
        games_list = [f"{(counter := counter + 1)}. {game[1]}" for game in games]
        #Выводим игры на экран
        print("\n".join(games_list) + "\n")
        #Запрашиваем и проверяем корректность ввода номера игры.
        while True:
            if game_index is not None:
                print("Неверный ввод!\n")
            game_index = input("Введите номер игры\n>>")

            if (
                not game_index.isnumeric()
                or int(game_index) > len(games)
                or int(game_index) < 1
            ):  continue
            else:
                break
        #вызываем метод для обновления информации игры, передавая ее айди.
        await self.__update_game_info(games[int(game_index) - 1][0])
        await self.clear_console()

    async def __update_game_info(self, id: int) -> None:
        """
        
        В этом методе выберается поле для редактирования и вводится новая информация для
        обновления информации по переданному айди игры.
        
        """
        await self.clear_console()
        user_input = None
            
        while True:
            #получаем информацию о выбранной игре.
            game_info = await self.__db.get_game_info(id)
            #создаем текст с информацией..
            menu_text = (
                f"{game_info}\n"
                f"Выберите поле для редактирования:\n"
                f"1. Название\n"
                f"2. Издатель\n"
                f"3. Дата выпуска\n"
                f"4. Назад\n"
                f">>"
            )
            user_input = input(menu_text)
            #завершаем цикл если пользователь ввел 4 для выхода.
            if user_input == "4":
                break
            if user_input not in ["1", "2", "3"]:
                print("Неверный ввод!")
                continue

            new_data = None
            #просим ввести новые данные и проверяем их корректность.
            while (new_data is None) or (len(new_data) < 1):
                if new_data is not None:
                    print("Неверный ввод!\n")
                new_data = input("Введите новые данные\n>>")
            
            #обновляем информации в зависимости от выбора пользователя.
            match user_input:
                case "1":
                    await self.__db.update_game_name(id, new_data)
                case "2":
                    await self.__db.update_game_publisher(id, new_data)
                case "3":
                    await self.__db.update_game_date(id, new_data)

            await self.clear_console()
            print("Готово!\n")

    async def select_game_for_deleting(self) -> None:
        """
        
        Метод для выбора игры для удаления с обработкой вводимых данных.
        Когда пользователь выбирает номер игры, мы получаем из кортежа со всеми играми
        кортеж, содеражащий айди выбранной игры, затем передаем его в метов delete_game.
        
        """

        await self.clear_console()
        #получем список игр
        games = await self.__db.get_list_games()
        game_index = None
        counter = 0
        #создаем массив строк. строки имеют формат 'Номер_игры. Название игры'.
        games_list = [f"{(counter := counter + 1)}. {game[1]}" for game in games]

        if games == []:
            print("Нет игр для удаления!\n")
            return
        #выводим игры на экран.
        print("\n".join(games_list) + "\n")
        
        #проверяем корректность выбора игры.
        while True:
            if game_index is not None:
                print("Неверный ввод!\n")
            game_index = input("Введите номер игры\n>>")

            if (
                not game_index.isnumeric()
                or int(game_index) > len(games)
                or int(game_index) < 1
            ):
                continue
            else:
                break
        
        #вызываем метод для удаления игры и передаем ее айди.
        await self.__db.delete_game(games[int(game_index) - 1][0])
        await self.clear_console()
        print("Игра удалена!")

    async def get_list(self) -> None:
    
        """
        Метод для вывода списка игр из бд.
            
        """
        await self.clear_console()
        #получаем список игр
        games = await self.__db.get_list_games()
        #проверка на существование игр в базе данных.
        if len(games) == 0:
            print("Вы еще не добавили ни одной игры!\n")
            return
        
        counter = 0        
        #создаем массив строк. строки имеют формат 'Номер_игры. Название игры'.
        games_list = [f"{(counter := counter + 1)}. {game[1]}" for game in games]
        #выводим игры на экран.
        print("\n".join(games_list) + "\n")
    
    @staticmethod
    async def __comparison_of_search_with_a_game(user_input: list, game_data: dict) -> bool:
        """
        
        метод для проверки совпадений в вводе пользователя и в информации о игре.
        
        """
        count_coincidences = 0
        for i in user_input:
            if any(i in data for data in game_data[1].split()): count_coincidences += 1
            if any(i in data for data in game_data[2].split()): count_coincidences += 1
            if any(i in data for data in game_data[3].split()): count_coincidences += 1
            
        return count_coincidences
        
    async def find_game(self) -> None:
        """
        
        метод для поиска игры.
        
        """
        await self.clear_console()
        user_input = input("введите название, издателя или год выпуска игры\n>>").split()
        #получаем список игр.
        games_data = await self.__db.get_all_games_data()
        resault_list = []
        
        #перебираем список игр.
        for game_data in games_data:
            if await self.__comparison_of_search_with_a_game(user_input, game_data):
                resault_list.append(game_data)
        
        await self.clear_console()
        #проверка на наличие совпадений.
        if len(resault_list) == 0:
            print("по вашему запросу ничего не найдено!")
            return
        
        print("по вашему запросу найдено:")
        #создаем массив строк. строки имеют формат 'Номер_игры. Название игры'.
        game_data = [f"{index + 1}. {resault_list[index][1]}" for index in range(len(resault_list))]
        #выводим результат поиска на экран.
        print("\n".join(game_data) + "\n")