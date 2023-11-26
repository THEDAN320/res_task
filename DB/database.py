import aiosqlite
import os


class Database:
    """
    
    Создаем интерфейс для взаимодействия с базой данных.
    Крайне не рекомендуется создавать инстансы от этого класса,
    рекомендуется использовать MainInterface для взаимодействия.
    В ином случае, уделите внимание обработке передаваемых аргументов перед передачей их в методы класса
    
    """

    def __init__(self):
        """
        
        В конструкторе устанавливаем путь до нашей бд.
        
        """
        self.__path_to_db = os.path.dirname(__file__) + r"\data.db"
        self.conn = None
    
    async def close_connect(self) -> None:
        """
        
        Метод для закрытия соединения с бд.
        
        """
        await self.conn.close()
        
    async def open_connect(self) -> None:
        """
        
        Метод для открытия соединения с бд.
        
        """
        self.conn = await aiosqlite.connect(self.__path_to_db)

    async def register_game(self, name: str, publisher: str, date: str) -> None:
        """
        
        Добавляем в базу данных новую игру, по переданным названию, издателю и дате издания.
        
        """
        try:
            await self.conn.execute(
                "INSERT INTO games(name, publisher, date) VALUES(?, ?, ?);",
                (name, publisher, date),
            )

            await self.conn.commit()

        except aiosqlite.Error as error:
            print("Ошибка при добавлении новой игры: ", error)

    async def get_all_games_data(self) -> list[dict]:
        """
        
        Метод возвращает список из кортежей, в которых храниться айди, название, издатель и дата выпуска игры из бд.
        
        """
        try:
            cur = await self.conn.execute("SELECT id, name, publisher, date FROM games")
            resaults = await cur.fetchall()

            await cur.close()
            return resaults

        except aiosqlite.Error as error:
            print("Ошибка при получении данных игр: ", error)
            
    async def get_list_games(self) -> list[dict]:
        """
        
        Метод возвращает список из кортежей, в которых храниться название игры и ее айди в бд.
        
        """
        try:
            cur = await self.conn.execute("SELECT id, name FROM games")
            resaults = await cur.fetchall()

            await cur.close()
            return resaults

        except aiosqlite.Error as error:
            print("Ошибка при получении списка игр: ", error)

    async def get_game_info(self, id: int) -> str:
        """
        
        Метод возвращает строку со всей информацией об игре.
        Формат строки:
            'Название - Имя_игры\n'
            'Издатель - Издатель_игры\n'
            'Дата выпуска - Дата_выпуска_игры\n'
            
        """
        try:
            cur = await self.conn.execute("SELECT name, publisher, date FROM games WHERE id = ?", (id,))
            resault = await cur.fetchone()

            await cur.close()
            game_info = (
                f"Название - {resault[0]}\n"
                f"Издатель - {resault[1]}\n"
                f"Дата выпуска - {resault[2]}\n"
            )
            return game_info

        except aiosqlite.Error as error:
            print("Ошибка при получении информации об игре: ", error)

    async def delete_game(self, id: int) -> None:
        """
        
        Метод удаляет игру из бд по айди.
        
        """
        try:
            await self.conn.execute("DELETE FROM games WHERE id = ?", (id,))
            await self.conn.commit()

        except aiosqlite.Error as error:
            print("Ошибка при удалении игры: ", error)

    async def update_game_name(self, id: int, name: str) -> None:
        """
        
        Обновляем в базе данных название игры по айди.
        
        """
        try:
            await self.conn.execute("UPDATE games SET name = ? WHERE id = ?", (name, id))
            await self.conn.commit()

        except aiosqlite.Error as error:
            print("Ошибка при обновлении названия игры: ", error)

    async def update_game_publisher(self, id: int, publisher: str) -> None:
        """
        
        Обновляем в базе данных издателя игры по айди.
        
        """
        try:
            await self.conn.execute("UPDATE games SET publisher = ? WHERE id = ?", (publisher, id))
            await self.conn.commit()

        except aiosqlite.Error as error:
            print("Ошибка при обновлении издателя игры: ", error)

    async def update_game_date(self, id: int, date: str) -> None:
        """
        
        Обновляем в базе данных дату издания игры по айди.
        
        """
        try:
            await self.conn.execute("UPDATE games SET date = ? WHERE id = ?", (date, id))
            await self.conn.commit()

        except aiosqlite.Error as error:
            print("Ошибка при обновлении даты игры: ", error)
