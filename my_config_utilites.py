from datetime import datetime, time, timezone, timedelta
# from pytz import timezone
from time import strftime
from typing import Any, List
from dataclasses import dataclass, field
import os
import json


PATH_SET = "settings.json"
if __name__ == "__main__": PATH_SET = "settings_.json"  #для отладки
NAME_BOT = 'Volleyball78bot'
AVATAR_BOT = 'mikasa_or_molten.jpg'
AUTH_TOKEN = '50ee0ec538a7dc83-f5d7265684ea6499-2995774239081905'
DICT_MENU = {'team_log': 'Представьтесь! (напишите имя под которым вас будут узнавать в списке игроков. '
                         'К примеру - свое имя и первые 1-3 буквы фамилии)',
             'team_unlog': 'Вы удалены из списка голосования',
             'team_login': 'Вы записаны в команду под именем ',
             'brief_instructions': 'Краткие инструкции по общению с ботом: \n'
                                   '+ - запись на игру \n'
                                   '- - отказаться от игры (если записались ранее) \n'
                                   '? - получить список сегодняшней команды \n'
                                   '@- - отписаться от бота \n'
                                   'help - получить эту страничку',
             'team_member_allready_exist': 'Вы уже записаны на игру ',
             'out_of_time': 'Не сейчас!!! \n Начало переклички :',
             'team_exist': 'Комплект!',
             'team_already_exist': 'Команда сформирована! На сегодня вы - в запасе.',
             'team_welcome': 'Вы зарегистрированы! Добро пожаловать на игру!',
             'remove_from_team': 'Вы отписаны от игры сегодня!',
             'in_reserve': 'В запасе:',
             'wrong_command': 'ошибочная команда',
             }
ADMIN_DICT = {'@change_list_day_of_week': 'Дни голосования изменены на ',
              '@change_voting_time': 'Время голосования изменено на ',
              '@get_team_members': 'Зарегистрированные члены команды: \n',
              '@delete_team_members': ' \n удален из членов команды',
              '@save_team_members': ' \n внесен в члены команды',
              '@get_voting_members': ' записались : \n',
              '@delete_voting_members': ' \n удален из списка играющих ',
              '@save_voting_members': ' \n внесен в список играющих ',
              '@get_vip_team_members': 'В VIP списке: \n',
              '@delete_vip_team_members': ' \n удален из VIP списка',
              '@save_vip_team_members': ' \n внесен в VIP список',
              '@change_number_team_members': 'Максимальное количество игроков изменено на ',
              '@get_my_config': '***my_config***\n',
              '@save_my_config': 'OK',
              }
VIP_TEAM_MEMBERS = []
DAY_OF_THE_WEEK_DEFAULT = [2, ]
VOTING_TIME_DEFAULT = '12:00:00'
NUMBERS_TEAM_MEMBERS = 14
TEAM_DICT_DEFAULT = {'5h2COTj83ZE6IAsIcTEVGw==': 'DK'}
VOTING_MEMBERS = {}
END_COUNTDOWN = False # флаг окончания набора команды
RESERVE_SAVE = False # флаг создания резервной копии my_config (т.к. на сервере нельзя сохранить файл м\д деплоями)
CONFIG_DEFAULT = {"day_of_the_week": DAY_OF_THE_WEEK_DEFAULT,
                  "voting_time": VOTING_TIME_DEFAULT,
                  "team_members": TEAM_DICT_DEFAULT,
                  'voting_members': VOTING_MEMBERS,
                  'number_team_members': NUMBERS_TEAM_MEMBERS,
                  'vip_team_members': VIP_TEAM_MEMBERS,
                  'end_countdown': END_COUNTDOWN,
                  'reserve_save': RESERVE_SAVE,
                  }
WEEK = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']

@dataclass
class MyConfig:
    day_of_the_week: List[int] = field(default_factory=list)
    voting_time: str = ''
    team_members: dict = field(default_factory=dict)
    voting_members: dict = field(default_factory=dict)
    number_team_members: int = 14
    vip_team_members: List[str] = field(default_factory=list)
    end_countdown: bool = False
    reserve_save: bool = False

    def __post_init__(self):
        my_config_json = get_config_dict(PATH_SET)
        self.day_of_the_week = my_config_json['day_of_the_week']
        self.voting_time = my_config_json['voting_time']
        self.team_members = my_config_json['team_members']
        self.voting_members = my_config_json['voting_members']
        self.number_team_members = my_config_json['number_team_members']
        self.vip_team_members = my_config_json['vip_team_members']
        self.end_countdown = my_config_json['end_countdown']
        self.reserve_save = my_config_json['reserve_save']


def create_config(path: str):
    """
    Create a config file
    """
    config_default = CONFIG_DEFAULT
    with open(path, "w", encoding='utf8') as settings_file:
        json.dump(config_default, settings_file, ensure_ascii=False)


def get_config_dict(path: str) -> dict:
    """
    Returns the config dict
    """
    try:
        with open(PATH_SET, encoding='utf8') as settings_file:
            config = json.load(settings_file)
        # проверяем файл на исправность данных, если нет - создаем снова по дефолту
    except Exception:
        create_config(path)
        with open(PATH_SET, encoding='utf8') as settings_file:
            config = json.load(settings_file)
    return config


def get_config(path: str, str_config=None) -> None:
    """
    Returns the config object
    """
    if str_config:
        config = str_config
    else:
        config = get_config_dict(path)
    # переводим из dict в объект
    my_config.day_of_the_week = config["day_of_the_week"]
    my_config.voting_time = config["voting_time"]
    my_config.voting_members = config["voting_members"]
    my_config.team_members = config["team_members"]
    my_config.number_team_members = int(config['number_team_members'])
    my_config.vip_team_members = config['vip_team_members']
    my_config.end_countdown = config['end_countdown']
    my_config.reserve_save = config['reserve_save']


def update_config(path: str, config: MyConfig) -> None:
    """
    Update a settings config
    """
    my_config_str = CONFIG_DEFAULT
    my_config_str['day_of_the_week'] = config.day_of_the_week
    my_config_str['voting_time'] = config.voting_time
    my_config_str['voting_members'] = config.voting_members
    my_config_str['team_members'] = config.team_members
    my_config_str['number_team_members'] = config.number_team_members
    my_config_str['vip_team_members'] = config.vip_team_members
    my_config_str['end_countdown'] = config.end_countdown
    my_config_str['reserve_save'] = config.reserve_save
    with open(path, "w", encoding='utf8') as settings_file:
        json.dump(my_config_str, settings_file, ensure_ascii=False)


def incoming_parsing(incoming_id: str, incoming_text: str):
    """
    Incoming message processing
    """
    outcoming_ids: List = [incoming_id]
    outcoming_text = DICT_MENU['wrong_command']
    date_now = datetime.strftime(datetime.now(), '%d-%m-%y')
    # разделяем на два блока - служебные команд (с @ в заголовке) и блок с регистрацией и голосование(+,-)/регистрация
    if incoming_text[0] == '@' or incoming_text == 'help' or incoming_text == 'Help':
        outcoming_ids, outcoming_text = admin_utilites(incoming_id, incoming_text)
    else:
        # проверяем на наличие id в списке команды
        if incoming_id not in my_config.team_members:
            my_config.team_members[incoming_id] = ''
            outcoming_text = DICT_MENU['team_log']
            if (len(my_config.team_members) in [5, 10, 15, 20, 25]) or (len(my_config.team_members) > 25):
                my_config.reserve_save = True
        else:
            # проверяем на наличие имени в списке команды
            if my_config.team_members[incoming_id] == '':
                my_config.team_members[incoming_id] = incoming_text
                outcoming_text = DICT_MENU['team_login'] + incoming_text + '\n' + DICT_MENU['brief_instructions']
                if (len(my_config.team_members) in [10, 15, 20, 25]) or (len(my_config.team_members) > 25):
                    my_config.reserve_save = True
            else:
                # все выше пройдено - читаем меседж
                if weekday_is_true() and time_is_true():
                    if date_now not in my_config.voting_members:
                        # при первом обращении в нужное время - создаем запись голосующих с внесением первыми VIP
                        my_config.voting_members[date_now] = []
                        for vip_members in my_config.vip_team_members:
                            my_config.voting_members[date_now].append(vip_members)
                    if '+' in incoming_text and len(incoming_text) < 4:
                        if incoming_id not in my_config.voting_members[date_now]:
                            my_config.voting_members[date_now].append(incoming_id)
                            if len(my_config.voting_members[date_now]) > my_config.number_team_members:
                                outcoming_text = DICT_MENU['team_already_exist']
                            else:
                                outcoming_text = DICT_MENU['team_welcome']
                        else:
                            outcoming_text = DICT_MENU['team_member_allready_exist']

                    if incoming_text == '-' and incoming_id in my_config.voting_members[date_now]:
                        my_config.voting_members[date_now].remove(incoming_id)
                        if len(my_config.voting_members[date_now]) < 1:
                            my_config.voting_members.pop(date_now)
                        outcoming_text = DICT_MENU['remove_from_team']

                    if incoming_text == '?':
                        outcoming_text = table_game_team(date_now)
                        if my_config.end_countdown:
                            outcoming_ids = my_config.voting_members[date_now]
                            outcoming_text = table_game_team(date_now) + '\n' + DICT_MENU['team_exist']
                            my_config.end_countdown = False

                    if len(my_config.voting_members[date_now]) == my_config.number_team_members \
                            and incoming_text != '?' and not my_config.end_countdown:
                        my_config.end_countdown = not my_config.end_countdown
                        # при достжении нужного кол-ва игроков вызываем рассылку всем сообщения
                else:
                    outcoming_text = DICT_MENU['out_of_time'] + '\n'
                    for day_week in my_config.day_of_the_week:
                        outcoming_text += WEEK[day_week-1] + ' -  в ' + str(my_config.voting_time) + '\n'
    update_config(PATH_SET, my_config)
    return outcoming_ids, outcoming_text


def admin_utilites(incoming_ids, incoming_text):
    """
    Processing an incoming service message
    """
    outcoming_ids = [incoming_ids]
    outcoming_text = 'Упс! Что-то пошло не так!!!'
    incoming_text = incoming_text.split('@@')

    if incoming_text[0] == '@change_list_day_of_week' and len(incoming_text) != 1:
        try:
            a = my_config.day_of_the_week = [int(i) for i in incoming_text[1]]
            outcoming_text = 'Дни голосования изменены на ' + str(a)
        except ValueError:
            outcoming_text = 'Упс! Что-то пошло не так!!!'
    if incoming_text[0] == '@change_voting_time' and len(incoming_text) != 1:
        a = my_config.voting_time = incoming_text[1]
        outcoming_text = 'Время голосования изменено на ' + a
    if incoming_text[0] == '@get_team_members':
        outcoming_text = 'Зарегистрированные члены команды: \n'
        i = 0
        for key, item in my_config.team_members.items():
            i += 1
            outcoming_text += str(i) + ' - ' + item + '\n'
    if incoming_text[0] == '@-':
        # удаление из общего списка команды
        if len(incoming_text) == 1:
            try:
                deleted = my_config.team_members.pop(incoming_ids, 'Никто не')
                outcoming_text = str(deleted) + ' \n удален из членов команды'
            except IndexError:
                pass
        else:
            try:
                outcoming_text = ''
                for delete_id in incoming_ids:
                    deleted = my_config.team_members.pop(delete_id, 'Никто не')
                    outcoming_text += str(deleted) + ' \n удален из членов команды'
            except IndexError:
                pass
    if incoming_text[0] == '@save_team_members':
        outcoming_text = ' \n внесен в члены команды'
    if incoming_text[0] == '@get_voting_members':
        outcoming_text = ' записались : \n'
    if incoming_text[0] == '@delete_voting_members':
        outcoming_text = ' \n удален из списка играющих '
    if incoming_text[0] == '@save_voting_members':
        outcoming_text = ' \n внесен в список играющих '
    if incoming_text[0] == '@get_vip_team_members':
        outcoming_text = 'В VIP списке: \n'
    if incoming_text[0] == '@delete_vip_team_members':
        outcoming_text = ' \n удален из VIP списка'
    if incoming_text[0] == '@save_vip_team_members':
        outcoming_text = ' \n внесен в VIP список'
    if incoming_text[0] == '@change_number_team_members':
        outcoming_text = 'Максимальное количество игроков изменено на '
    if incoming_text[0] == 'help':
        outcoming_text = DICT_MENU['brief_instructions']
    if incoming_text[0] == '@get_my_config':
        config = get_config_dict(PATH_SET)
        outcoming_text = '@save_my_config@@' + json.dumps(config, ensure_ascii=False)
    if incoming_text[0] == '@save_my_config':
        try:
            json_config = incoming_text[1]
            config = json.loads(json_config)
            get_config(PATH_SET, str_config=config)
            outcoming_text = 'OK'
        except ValueError:
            pass
    update_config(PATH_SET, my_config)
    return outcoming_ids, outcoming_text


def time_is_true():
    """
    Checking for condition compliance by time
    """
    t = my_config.voting_time
    t = t.split(':')
    dt = timedelta(hours=3)
    return (datetime.now() + dt).time() > time(int(t[0])-3, int(t[1]), int(t[2]))
    # return datetime.now(timezone("Europe/Samara")).time() > time(int(t[0]), int(t[1]), int(t[2]))
    # пришлось делать костыли тк  ModuleNotFoundError: No module named 'pytz'
    # и  Pip - Fatal error in launcher: Unable to create process using
def weekday_is_true():
    """
    Checking for condition compliance by weekday
    """
    dt = timedelta(hours=3)
    return datetime.isoweekday(datetime.now() + dt) in my_config.day_of_the_week


def table_game_team(date: str):
    """
    Formation of a list table
    """
    table_str = ''
    for i in range(len(my_config.voting_members[date])):
        if i == my_config.number_team_members:
            #  проверка на полноту команды
            table_str += DICT_MENU['in_reserve'] + '\n '
        if my_config.voting_members[date][i] in my_config.team_members:
            # если участник игры не удалился из общего списка
            table_member = my_config.team_members[my_config.voting_members[date][i]]
        else:
            table_member = ''
        table_str += str(i + 1) + ' : ' + table_member + '\n '
    return table_str


def table_id_team(date: str) -> List:
    """
    Formation of a list table
    """
    table_list = []
    for i in range(len(my_config.voting_members[date])):
        table_list.append(my_config.voting_members[date][i])
    return table_list


my_config: Any = MyConfig()
get_config(PATH_SET)

if __name__ == "__main__":
    a = MyConfig()
    # b = '3333333333333-333-333='
    # c = 'Лёша'

    b = '4444444444444-444-444='
    # c = 'Valera'

    # b = '8230jakncdnac-657-342='
    # c = 'RL'

    # b = '00002852524234240000='
    # c = 'RK'

    # b = '5h2COTj83ZE6IAsIcTEVGw=='
    # b = '?'
    c = '+'
    e, ee = incoming_parsing(b, c)
    print(e, ee, type(ee), my_config, sep='\n')
    # input()
    # c = '?'
    # e, ee = incoming_parsing(b, c)
    # print(e, ee, type(ee), my_config, sep='\n')
    # input()
    # c = '-'
    # e, ee = incoming_parsing(b, c)
    # print(e, ee, type(ee), my_config, sep='\n')
    c = 'ghcq'
    # проверить рассылку всем достижении 14 и проверить рассылку запасным при минусовании гоглибо из основного
    # help прикрутить и в него допом добавить еще чего нить, облегчить ввод мембертим
