"""
Module localization provides translation for
different languages
"""

import locale
import enum

@enum.unique
class Msg(enum.Enum):
    DRAW = enum.auto()
    PLAYER_X_WON = enum.auto()
    ANN_WON = enum.auto()
    BOB_WON = enum.auto()
    YOUR_MOVE = enum.auto()
    ENTER_YOUR_MOVE = enum.auto()
    ENTER_YOUR_REMOVE = enum.auto()
    WITH_PLAYER_IDENT = enum.auto()
    WAIT = enum.auto()
    RULES = enum.auto()

    WELCOME_HEADER = enum.auto()
    CHOOSE_DIFFICULTY_HEADER = enum.auto()
    CHOOSE_PVP_TYPE_HEADER = enum.auto()
    CHOOSE_ROLE_HEADER = enum.auto()
    CREATE_GAME_HEADER = enum.auto()
    JOIN_GAME_HEADER = enum.auto()

    PVE_BUTTON = enum.auto()
    PVP_BUTTON = enum.auto()
    QUIT_BUTTON = enum.auto()
    EASY_BUTTON = enum.auto()
    NORMAL_BUTTON = enum.auto()
    HARD_BUTTON = enum.auto()
    BACK_BUTTON = enum.auto()
    THIS_COMPUTER_BUTTON = enum.auto()
    TWO_COMPUTERS_BUTTON = enum.auto()
    CONNECT_BUTTON = enum.auto()
    CREATE_AND_WAIT = enum.auto()
    JOIN_BUTTON = enum.auto()
    HOST_BUTTON = enum.auto()

    PORT_INPUT = enum.auto()
    HOST_INPUT = enum.auto()

lang = locale.getdefaultlocale()[0]

english = {
    Msg.DRAW: "Draw!",
    Msg.PLAYER_X_WON: "Player %s has won!",
    Msg.ANN_WON: "Ann won!",
    Msg.BOB_WON: "Bob won!",
    Msg.WITH_PLAYER_IDENT: "Player %s! %s",
    Msg.YOUR_MOVE: "Your move",
    Msg.ENTER_YOUR_MOVE: "Enter a cell to move (e.g. A3):",
    Msg.ENTER_YOUR_REMOVE: "Enter a cell to remove (e.g. B3):",
    Msg.WELCOME_HEADER: "Welcome to Isolation!",
    Msg.CHOOSE_DIFFICULTY_HEADER: "Choose difficulty",
    Msg.CHOOSE_PVP_TYPE_HEADER: "Choose PvP type",
    Msg.CHOOSE_ROLE_HEADER: "Choose role",
    Msg.CREATE_GAME_HEADER: "Create a game",
    Msg.JOIN_GAME_HEADER: "Join a game",

    Msg.PVE_BUTTON: "Play with computer",
    Msg.PVP_BUTTON: "Play with a friend",
    Msg.QUIT_BUTTON: "Quit",
    Msg.EASY_BUTTON: "Easy",
    Msg.NORMAL_BUTTON: "Normal",
    Msg.HARD_BUTTON: "Hard",
    Msg.BACK_BUTTON: "< Back",
    Msg.THIS_COMPUTER_BUTTON: "This computer",
    Msg.TWO_COMPUTERS_BUTTON: "Two computers",
    Msg.CONNECT_BUTTON: "Connect",
    Msg.CREATE_AND_WAIT: "Create and wait",
    Msg.JOIN_BUTTON: "Join",
    Msg.HOST_BUTTON: "Host",
    Msg.PORT_INPUT: "Port:  ",
    Msg.HOST_INPUT: "Host:  ",
    Msg.RULES: """
Rules:

1) Moving one's piece to 
a neighboring position 
that contains a square 
but not the opponent's
piece

2) Removing any square 
with no piece on it

The player who
cannot make any move 
loses the game

""",
}

russian = {
    Msg.DRAW: "Ничья!",
    Msg.PLAYER_X_WON: "Игрок %s победил!",
    Msg.ANN_WON: "Победа Анны!",
    Msg.BOB_WON: "Боб победил!",
    Msg.YOUR_MOVE: "Ваш ход",
    Msg.ENTER_YOUR_MOVE: "Введите клетку для перемещения (напр. A3):",
    Msg.ENTER_YOUR_REMOVE: "Введите клетку для удаления (напр. B3):",
    Msg.WITH_PLAYER_IDENT: "Игрок %s! %s",
    Msg.WELCOME_HEADER: "Добро пожаловать в Isolation!",
    Msg.CHOOSE_DIFFICULTY_HEADER: "Выберите уровень сложности",
    Msg.CHOOSE_PVP_TYPE_HEADER: "Выберите тип схватки",
    Msg.CHOOSE_ROLE_HEADER: "Выберите роль",
    Msg.CREATE_GAME_HEADER: "Создание игры",
    Msg.JOIN_GAME_HEADER: "Присоединиться к игре",
    Msg.PVE_BUTTON: "Сыграть с компьютером",
    Msg.PVP_BUTTON: "Сыграть с другом",
    Msg.QUIT_BUTTON: "Выйти",
    Msg.EASY_BUTTON: "Лёгкий",
    Msg.NORMAL_BUTTON: "Нормальный",
    Msg.HARD_BUTTON: "Сложный",
    Msg.BACK_BUTTON: "< Назад",
    Msg.THIS_COMPUTER_BUTTON: "Этот компьютер",
    Msg.TWO_COMPUTERS_BUTTON: "Два компьютера",
    Msg.CONNECT_BUTTON: "Подключиться",
    Msg.CREATE_AND_WAIT: "Создать игру и ожидать",
    Msg.JOIN_BUTTON: "Присоединиться",
    Msg.HOST_BUTTON: "Создать",
    Msg.PORT_INPUT: "Порт:  ",
    Msg.HOST_INPUT: "Хост:  ",
    Msg.RULES: """
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
""",
}

def _(msg):
    en = english.get(msg, "")
    if lang == "ru_RU":
        return russian.get(msg, "" or en)
    return en
