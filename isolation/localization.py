import locale

from .menu_names import *
from . import resources

lang, _ = locale.getdefaultlocale()
translation = {
    "It's a draw!": "Ничья!",
    "Player %s has won!": "Игрок %s победил!",
    "Draw!": "Ничья!",
    "Ann won!": "Победа Анны!",
    "Bob won!": "Боб победил!",
    "Host: ": "Имя хоста: ",
    "Port: ": "Порт подключения: ",
    "Waiting for the second player to join the game...": "Ожидаем подключения второго игрока...",
    "Player 2 has joined: ": "Второй игрок присоединился",
    "Enter the desired port number: ": "Введите номер порта для начала игры: ",
    " or ": " или ",
    "Your move": "Ваш ход",
    "Player %s! %s": "Игрок %s! %s",
    "Enter your move (ex. A3):": "Введите клетку для перемещения (напр. A3):",
    "Wait": "Подождите...",
    WELCOME_HEADER: "Добро пожаловать в Isolation!",
    CHOOSE_DIFFICULTY_HEADER: "Выберите уровень сложности",
    CHOOSE_PVP_TYPE_HEADER: "Выберите тип схватки",
    CHOOSE_ROLE_HEADER: "Выберите роль",
    CHOOSE_PORT_HEADER: "Выберите порт",
    JOIN_GAME_HEADER: "Присоединиться к игре",
    PVE_BUTTON: "Сыграть с компьютером",
    PVP_BUTTON: "Сыграть с другом",
    QUIT_BUTTON: "Выйти",
    EASY_BUTTON: "Лёгкий",
    NORMAL_BUTTON: "Нормальный",
    HARD_BUTTON: "Сложный",
    BACK_BUTTON: "< Назад",
    THIS_COMPUTER_BUTTON: "Этот компьютер",
    TWO_COMPUTERS_BUTTON: "Два компьютера",
    START_GAME_BUTTON: "Начать игру",
    CREATE_AND_WAIT: "Создать игру и ожидать",
    JOIN_BUTTON: "Присоединиться",
    HOST_BUTTON: "Создать",
    PORT_INPUT: "Порт:  ",
    HOST_INPUT: "Хост:  "
}

translation[resources.rules] = """
Правила:
Шаг 1) Переместить
игрока в соседнюю
свободную позицию

Шаг 2) Удалить любую
клетку на поле, на
которой нет фигурок
игроков

Проигрывет игрок,
который не может
сдвинуться
"""

def translate(phrase):
    if lang == "ru_RU":
        return translation.get(phrase, phrase)
    return phrase