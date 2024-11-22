import pytest
import requests
from requests import *
import pytest
from methods.highest import HighestSuperhero
from .config import Constants
from pytest_mock import MockerFixture

class TestGetHighest:
    """
            Класс для теста метода get_highest_superkotleta()
            """
    @pytest.fixture
    def get_api_response(self):
        """
            Фикстура для получения ответа от API.
            """
        def _get_api_response(url):
            return get(url)

        return _get_api_response

    @pytest.mark.parametrize("gender, employed, expected_code_response, expected_id", [
        ('Male', True, 200, 273),
        ('Male', False, 200, 256),
        ('Female', False, 200, 42),
        ('Female', True, 200, 716),
    ])
    def test_correct_hero(self, get_api_response, gender: str, employed: bool, expected_id: int, expected_code_response: int):
        """
            Тестирует корректные случаи работы метода и соответствующего ответа API. Репрезентирует пункты 1,2,3,4 из cases.txt

            Аргументы:
                get_api_response: Метод из фикстуры. Нужен, чтобы получить ответ от АПИ для сравнения.
                gender: Валидный пол супергероя.
                employed: Имеет работу или нет.
                expected_id: Ожидаемый герой.
                expected_code_response: ожидаемый код ответа API.
            """
        method_class = HighestSuperhero(gender, employed, Constants().MAIN_URL)
        hero_got = method_class.get_highest_superkotleta()
        height = float(hero_got['id'])
        response = get_api_response(Constants().MAIN_URL)
        assert response.status_code == Constants().HTTP_OK_RESPONSE
        assert height == expected_id

    @pytest.mark.parametrize("gender, employed", [
        ([1],False),
        ('Male', 246218.0),
        ('Female', ([1], False)),
        (None, True),
        (1,10),
    ])
    def test_invalid_types(self, gender: str, employed: bool):
        """
            Тестирует случаи подачи данных неверного типа в метод. Репрезентирует пункты 5,6 из cases.txt

            Аргументы:
                gender: Любое не строчное значение.
                employed: Любое не строковое значение.
            """
        method_class = HighestSuperhero(gender, employed, Constants().MAIN_URL)
        with pytest.raises(ValueError) as ex:
            method_class.get_highest_superkotleta()
        assert type(ex.value) is ValueError

    @pytest.mark.parametrize("gender", [
        ('Trans'),
        ('Genderfluid'),
        ('Attack-helicopter'),
        ('Adron collider'),
        ('Mechanic'),
    ])
    def test_empty_response(self, get_api_response, gender: str):
        """
            Тестирует случай, когда API возвращает пустой ответ. Репрезентирует пункт 7 из cases.txt

            Аргументы:
                get_api_response: Метод из фикстуры. Нужен, чтобы получить ответ от АПИ для сравнения.
                gender: Любая строка, не являющаяся Male или Female
            """
        method_class = HighestSuperhero(gender, True, Constants().MAIN_URL)
        response = get_api_response(Constants().MAIN_URL)
        assert response.status_code == Constants().HTTP_OK_RESPONSE
        with pytest.raises(requests.exceptions.RequestException) as ex:
            method_class.get_highest_superkotleta()
        assert type(ex.value) is requests.exceptions.RequestException


    def test_not_found_response(self, get_api_response):
        """
            Тестирует случай, когда API возвращает ошибку 404. Репрезентирует пункт 8 из cases.txt
            Можно параметризировать и добавить больше ссылок, но я ограничился 1 ссылкой в константах.
            Аргументы:
                get_api_response: Метод из фикстуры. Нужен, чтобы получить ответ от АПИ для сравнения.
            """
        method_class = HighestSuperhero('Male', True, Constants().INCORRECT_URL)
        response = get_api_response(Constants().INCORRECT_URL)
        with pytest.raises(requests.exceptions.HTTPError) as ex:
            method_class.get_highest_superkotleta()
        assert type(ex.value) is requests.exceptions.HTTPError
        assert response.status_code == Constants().HTTP_NOT_FOUND_RESPONSE

    def test_server_internal_error(self, mocker: MockerFixture):
        """
            Тестирует случай, когда API возвращает ошибку 500. Репрезентирует пункт 9 из cases.txt
            Единственный случай, который сложно воспроизвести, поэтому был мокирован.
            Аргументы:
                mocker: класс для создания имитации ответа API.
            """
        highest_superkotleta = HighestSuperhero('Male', True, Constants().MAIN_URL)
        mocker.patch(
            'requests.get',
            side_effect=[
                mocker.Mock(
                    status_code=500
                )
        ])
        with pytest.raises(requests.exceptions.HTTPError) as ex:
            highest_superkotleta.get_highest_superkotleta()
        assert ex.value.response.status_code == Constants().HTTP_INTERNAL_SERVER_ERROR_RESPONSE






