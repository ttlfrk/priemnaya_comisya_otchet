import os
from typing import Union
from io import StringIO

from lxml import etree
from requests import Session


class PriemkaSite():
    '''
    Парсит с сайта списки студентов по заданным параметрам

    Параметры
    ---------
    login: str - логин от личного кабинета
    password: str - пароль от личного кабинета
    domain: str - адрес сайта с http:// (домен или ip)
    '''

    def __init__(self, login: str, password: str, domain: str):
        self.__session = Session()
        self.__login = login
        self.__password = password
        self.__domain = domain

    def __get_etree(self, part_url: str,
                    params: dict = dict()) -> etree._ElementTree:
        '''
        Скачивает страницу domain + part_url,
        и возвращает объект etree.

        Параметры:
        part_url: str - часть адреса после http://domain.com/
        params: dict - GET параметры запроса (?param=1&other=2)
        '''
        respopse = self.__session.get(
            url=self.__domain + part_url,
            params=params,
        )
        respopse.raise_for_status()
        parser = etree.HTMLParser(no_network=True)
        return etree.parse(StringIO(respopse.text), parser)

    def is_authentication(self, root: etree._ElementTree) -> bool:
        '''
        Проверяет аутентификацию, проверяя
        наличие логина на странице (вверху).

        Параметры
        ---------
        root: _ElementTree - объект страницы
        '''
        el_login = root.xpath('//div[@class="box_login"]/span')
        if el_login:
            return el_login[0].text == self.__login
        return False

    def authentication(self) -> bool:
        '''
        Пройти авторизацию, отправив POST ajax запрос.
        '''
        data = dict(
            email=self.__login,
            password=self.__password,
            auth='true',
        )
        r = self.__session.post(
            url=self.__domain + 'admin/ajax/login',
            data=data,
            verify=False,
        )
        r.raise_for_status()
        root = self.__get_etree('admin/main')
        if not self.is_authentication(root):
            raise PermissionError('Ошибка авторизации')

    def search_users(
            self,
            page: Union[int, None] = 1,
            user_id: Union[int, None] = None,
            ufamily: str = '',
            uname: str = '',
            uotchestvo: str = '',
            email: str = '',
            main_phone: str = '',
            status: Union[int, None] = None,
            form_pay: Union[int, None] = None,
            form_education: Union[int, None] = None,
            level_education: Union[int, None] = None,
            faculty: Union[int, None] = None,
            method_delivery: Union[int, None] = None,
            scenarios: Union[int, None] = None,
            sort: int = 1,
            addition: Union[int, None] = None,
            ) -> dict[list]:
        '''
        Поиск по запросу.

        Параметры
        ---------
        page: int or None - страница
        user_id: int or None - ID юзера
        ufamily: str - фамилия
        uname: str - имя
        uotchestvo: str - отчество
        email: str - электронная почта
        main_phone: str - мобильный телефон
        status: int or None - статус (подано, одобрено, отказано, ...)
        form_pay: int or None - источник финансирования (бюджет, целевое, ...)
        form_education: int or None - форма образования
        level_education: int or None - направление подготовки
                                       (бакалавр, магистратура, ...)
        faculty: int or None - подразделение (СПО/ВПО + филиал)
        method_delivery: int or None - способ подачи
        scenarios: int or None - сценарий (приемная компания)
        sort: int or None - сортировать по умолчанию. Является 1
                            по умолчанию, иначе фигня выходит
        addition: int or None - дополнительно (непрочитанные, особое право)
        '''

        def _get_user_id() -> str:
            ''' Получить ID пользователя '''
            return row.xpath('.//td')[id_index].text.strip()

        def _get_user_name() -> str:
            ''' Получить ФИО пользователя (+ очистка от мусора) '''
            user_name = row.xpath('.//td')[fio_index]
            return ' '.join(next(user_name.itertext()).split())[:-1]

        def _get_user_status() -> str:
            ''' Получить статус пользователя '''
            return row.xpath('.//td')[status_index].text.strip()

        def _is_last_page() -> bool:
            ''' Проверка, является ли текущая страница последней '''
            # Поиск предпоследнего элемента пагинации с классом "active"
            return bool(root.xpath('//ul[@class="pagination"]/li[last() - 1]'
                                   '[contains(@class, "active")]'))

        column_index_pattern = 'count(.//thead/tr/th[text()="{}"]' \
                               '/preceding-sibling::*)'
        params = dict(
            page=page,
            user_id=user_id,
            ufamily=ufamily,
            uname=uname,
            uotchestvo=uotchestvo,
            email=email,
            main_phone=main_phone,
            status=status,
            form_pay=form_pay,
            form_education=form_education,
            level_education=level_education,
            faculty=faculty,
            method_delivery=method_delivery,
            scenarios=scenarios,
            sort=sort,
            addition=addition,
        )
        root: etree._ElementTree = self.__get_etree(
            part_url='admin/main',
            params=params,
        )
        users = dict(
            all=list(),
            green=list(),
            blue=list(),
            red=list(),
            other=list(),
        )

        # Ищем на странице таблицу, индексы данных по таблице (фио, id),
        # затем построчно собираем из таблицы данные, проверяем,
        # является ли текущая страница последней, и, если нет,
        # тогда загружаем следущую, пока страница не станет последней.
        while True:
            table_root: etree._ElementTree = root.xpath('.//table')[0]
            # Ищем индексы столбцов в таблице
            id_index = int(table_root.xpath(
                column_index_pattern.format('id')))
            fio_index = int(table_root.xpath(
                column_index_pattern.format('ФИО')))
            status_index = int(table_root.xpath(
                column_index_pattern.format('Статус')))
            user_rows = table_root.xpath('.//tbody/tr')

            # Построчно проверяем пользователей
            for row in user_rows:
                row: etree._ElementTree
                user_data = dict(
                    user_id=_get_user_id(),
                    user_name=_get_user_name(),
                    user_status_checked=_get_user_status(),
                    error=False,
                )
                users['all'].append(user_data)

                if 'direct_status_color_2' in row.attrib['class']:
                    if user_data['user_status_checked'] != 'Одобрено':
                        user_data['error'] = True
                    users['green'].append(user_data)
                    continue
                if 'mark_delete' in row.attrib['class']:
                    users['red'].append(user_data)
                    continue
                if 'direct_status_color_4' in row.attrib['class']:
                    users['blue'].append(user_data)
                    continue
                users['other'].append(user_data)

            if _is_last_page():
                break
            else:
                params['page'] += 1
                root = self.__get_etree(
                    part_url='admin/main',
                    params=params,
                )
        return users


if __name__ == '__main__':
    #  Пример использования
    import os
    app = PriemkaSite(
        login=os.environ.get('LOGIN'),
        password=os.environ.get('PASSWORD'),
    )
    app.authentication()
    # СПО - 9, ВПО - 21
    data = app.search_users(faculty=9)
    import json
    with open('data.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(data)
