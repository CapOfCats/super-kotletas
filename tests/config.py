"""
Конфигурационный файл.

Содержит константы, используемые в тестах.
"""

class Constants:
    """
    Класс с константами.
    """

    @property
    def MAIN_URL(self) -> str:
        """
            URL со всеми суперкотлетами.
        """
        return "https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api/all.json"

    @property
    def INCORRECT_URL(self) -> str:
        """
            Попытка получить параметры work всех героев
        """
        return "https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api/work/all.json"

    @property
    def HTTP_OK_RESPONSE(self) -> int:
        """
            Код успешного ответа.
        """
        return 200

    @property
    def HTTP_NOT_FOUND_RESPONSE(self) -> int:
        """
             Код ответа: Запрошенные ресурсы не найдены.
        """
        return 404

    @property
    def HTTP_INTERNAL_SERVER_ERROR_RESPONSE(self) -> int:
        """
            Код ответа о внутренней ошибке на сервере.
        """
        return 500
