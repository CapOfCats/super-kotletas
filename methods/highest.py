from tests.config import Constants
import requests
import pprint

class HighestSuperhero:
    """
        Класс для поиска супергероя с самым высоким ростом, исходя из входящих критериев.

        Атрибуты:
            gender: Пол супергероя.
            employed: Флаг наличия работы.
            url: URL для запроса данных от API.
        """
    def __init__(self, _gender: str, _employed: bool, _url: str):
        """
            Конструктор
            """
        self.gender = _gender
        self.employed = _employed
        self.url = _url

    # TODO: Добавить проверку наличия данных в ответе от API
    def get_highest_superkotleta(self) -> dict:
        """
                Находит всех супергероев по заданным критериям, а затем - самого высокого из них.

                Возвращает:
                    dict: Все данные о самом высоком герое.

                Вызывает исключения:
                    ValueError: Если какой-то из критериев не соответствует нужному типу: employed не является булевым
                    или gender не является строкой.
                    RequestException: В случае, если API ответил пустым сообщением.
                    HTTPError: Если ответ от API содержит ошибку HTTP.
                """
        if type(self.employed) is not bool or type(self.gender) is not str:
            raise ValueError("employed должен быть булевым, gender принимается, как строка") #В противном случае - нарушает логику лямбда-выражения
        constants = Constants()
        response = requests.get(self.url)
        match response.status_code:
            case constants.HTTP_OK_RESPONSE: #Когда ответ от АПИ успешный
                kotletas_data = response.json()
                work_condition = lambda x: x == "-" if not self.employed else x!= "-"
                superkotletas = [kotleta for kotleta in kotletas_data if
                                 kotleta["appearance"]["gender"] == f"{self.gender}" and
                                 work_condition(kotleta["work"]["occupation"])]

                if len(superkotletas) == 0:
                    raise requests.exceptions.RequestException("Пустой ответ от API")
                highest_kotleta = max(
                    superkotletas,
                    key=lambda kotleta: float(
                        kotleta["appearance"]["height"][1].replace(" cm", "")
                        .replace(" meters", "").replace(" kg", "")) if
                        kotleta["appearance"]["height"][1] != '-' else 0
                )
                pprint.pprint(highest_kotleta)
                return highest_kotleta
            case constants.HTTP_NOT_FOUND_RESPONSE:
                raise requests.exceptions.HTTPError(response=response)  #Ошибка 404
            case constants.HTTP_INTERNAL_SERVER_ERROR_RESPONSE:
                raise requests.exceptions.HTTPError(response=response) #Ошибка 500
            case _:
                raise requests.exceptions.RequestException(
                    f"К таким кодам меня жизнь не готовила. Код ответа API: {response.status_code} ")
                    #Ну тут когда полномочия - "всё"


