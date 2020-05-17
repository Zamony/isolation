import locale

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
    "Enter a cell to remove (ex. B3): ": "Введите клетку для удаления (напр. A3):",
    "Wait": "Подождите...",

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