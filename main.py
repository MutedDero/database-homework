#
#   - ТИПИЧНЫЙ ПРИМЕР ДАТАБАЗЫ (с урезанным функционалом)
#   сделано за час +-, очень редко пишу на питоне что-либо
#
#   работает на локал хосте, тк было лень ставить сервер :))
#   посылаете запрос на локалку в виде /get/?type=тип&index=индекс
#
#   типов всего два - once и all.
#   all - возвращает все содержимое json файла (индекс не нужен)
#   once - вернет ток таблицу под определенным индексом (он тут нужен)
#
#   > 06.02.23 - 07.02.23
#

# БИБЛИОТЕКИ

from flask import *
import json

# КЛАСС

class Database:

    # ИНИЦИАЛИЗАЦИЯ
    def __init__(self):
        self._app = Flask(__name__) # фласк приложение дада

        self._file = open("data.json", "r+", encoding = "utf8") # файл с датой
        self._data = json.load(self._file) # читаемая дата

        @self._app.route("/", methods = ["GET"]) # регаем новый "ивент" с приветствием
        def _welcome():
            return json.dumps({"Status": True, "Content": "Hello!"})
        
        @self._app.route("/get/", methods = ["GET"]) # регаем уже "ивент" связанный с получением
        def _function():
            type = str(request.args.get("type"))
            index = str(request.args.get("index"))

            return self.get_data(type, index)

        self._app.run(host = "0.0.0.0", port = 5000)

    # ПОДТВЕРЖДЕНИЕ ТИПА ЗАПРОСА
    def validate_type(self, type):
        if not type: return False
        if type != "all" and type != "once": return False

        return True
    
    # ОДИНОЧНЫЙ СПОСОБ ПОЛУЧЕНИЯ
    def get_once_data(self, index):
        if not index in self._data: return json.dumps({"Status": False, "Error": "Invalid index"})
        return json.dumps(self._data[index], ensure_ascii = False).encode("utf8")
    
    # МАССОВЫЙ СПОСОБ ПОЛУЧЕНИЯ
    def get_all_data(self):
        return json.dumps(self._data, ensure_ascii = False).encode("utf8")

    # ОБРАБОТКА ЗАПРОСА
    def get_data(self, type, index):
        type_validated = self.validate_type(type) # валидация типа
        if not type_validated: return json.dumps({"Status": False, "Error": "Invalid type"})

        if type == "all": # тип "all" - получение всей инфы
            return self.get_all_data()
        elif type == "once": # тип "once" - ток определенный индекс
            index = str(request.args.get("index"))
            if not index: return json.dumps({"Status": False, "Error": "Invalid index"})

            return self.get_once_data(index)

# ИСПОЛЬЗОВАНИЕ

if __name__ == "__main__":
    Database()