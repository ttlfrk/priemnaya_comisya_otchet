import os
import json


class ConfigFile():
    __data = list()

    def __init__(self, path: str = '.config.json'):
        self.__path = path
        self.__read_file()

    def __read_file(self) -> None:
        ''' Прочитать файл '''
        if not os.path.exists(self.__path):
            self.save_file()
        # Проверка, файл может быть поврежден
        try:
            with open(self.__path, 'r') as f:
                self.data = json.load(f)
        except Exception:
            self.data = dict()
            self.save_file()

    @property
    def data(self) -> list:
        ''' list -> dict[user_id, user_name, ...] '''
        return self.__data

    @data.setter
    def data(self, value: list) -> None:
        error_msg = 'Данные должны быть вида list->dict'
        if not isinstance(value, list):
            raise ValueError(error_msg)
        for item in value:
            if not isinstance(item, dict):
                raise ValueError(error_msg)
        self.__data = value

    def save_file(self) -> None:
        ''' Сохранить файл '''
        with open(self.__path, 'w', encoding='utf-8') as f:
            json.dump(self.__data, f, indent=4, ensure_ascii=True)

    def repair_data(self, repair_data: dict) -> dict:
        '''
        Исправляет значения из repair_data

        Параметры
        ---------
        repair_data: dict - данные для исправления (список студентов)

        Пример
        ------
        repair_data = dict(
            all=[
                dict(user_id=1, user_name=Test1, status=Ok),
                dict(user_id=2, user_name=Test2, status=something),
            ],
            green=[
                dict(user_id=1, user_name=Test1, status=Ok),
            ]
            red=[
                dict(user_id=2, user_name=Test2, status=something),
            ]
        )
        self.data = [
            dict(user_id=123, status=green),
        ]
        self.repair_data(repair_data, 'spo') ->
        dict(
            all=[
                dict(user_id=1, user_name=Test1, status=Ok),
                dict(user_id=2, user_name=Test2, status=something),
            ],
            green=[
                dict(user_id=1, user_name=Test1, status=Ok),
                dict(user_id=2, user_name=Test2, status=something),
            ]
        )
        '''
        # Выбираем ID пользователей
        ids = {str(user.get('user_id')): user for user in self.data
               if user.get('user_id', '')}
        if not ids:
            return repair_data
        for key in repair_data.keys():
            if key == 'all':
                continue
            # Поиск пользователей с совпадающими ID, и сортируем
            # в обратном порядке, что бы list.pop() не сломал нумерацию
            found_user_indexes = [index for index, user in enumerate(repair_data[key])
                                  if str(user.get('user_id', '')) in ids]
            if not found_user_indexes:
                continue
            found_user_indexes.reverse()
            for user_index in found_user_indexes:
                # Получаем данные пользователя
                user = repair_data[key][user_index]
                user_id = str(user.get('user_id', None))
                if not user_id:
                    continue
                # Получаем статус, который он должен иметь
                new_status = ids[user_id]['status']
                if user.get('status', None) == new_status:
                    continue
                # Удаляем пользователя из списка, где он сейчас находится
                repair_data[key].pop(user_index)
                if new_status == 'remove':
                    if 'all' not in repair_data:
                        continue
                    repair_data['all'] = [user for user in repair_data['all']
                                          if user.get('user_id', '') != user_id]
                else:
                    repair_data[new_status].append(user)
        return repair_data


if __name__ == '__main__':
    x = ConfigFile()
    before = dict()

    import json
    with open('data.json', 'r') as f:
        before = json.load(f)
    after = x.repair_data(repair_data=before)

    def print_result(data):
        print('Data: green={} blue={} red={} all={}'.format(
            len(data['green']),
            len(data['blue']),
            len(data['red']),
            len(data['all']),
        ))

    print_result(before)
    print_result(after)
