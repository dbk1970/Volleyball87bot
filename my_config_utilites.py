from datetime import datetime, time
from time import strftime
from typing import Any, List
from dataclasses import dataclass, field
import os
import json


PATH_SET = "settings.json"
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
                                   '? - получить список сегодняшней команды',
             'team_member_allready_exist': 'Вы уже записаны на игру ',
             'out_of_time': 'Сегодня нет игры',
             'team_exist': 'Комплект!',
             'team_already_exist': 'Команда сформирована! На сегодня вы - в запасе.',
             'team_welcome': 'Вы зарегистрированы! Добро пожаловать на игру!',
             'remove_from_team': 'Вы отписаны от игры сегодня!',
             'in_reserve': 'В запасе:',
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
CONFIG_DEFAULT = {"day_of_the_week": DAY_OF_THE_WEEK_DEFAULT,
                  "voting_time": VOTING_TIME_DEFAULT,
                  "team_members": TEAM_DICT_DEFAULT,
                  'voting_members': VOTING_MEMBERS,
                  'number_team_members': NUMBERS_TEAM_MEMBERS,
                  'vip_team_members': VIP_TEAM_MEMBERS,
                  }
END_COUNTDOWN = False


@dataclass
class MyConfig:
    day_of_the_week: List[int] = field(default_factory=list)
    voting_time: str = ''
    team_members: dict = field(default_factory=dict)
    voting_members: dict = field(default_factory=dict)
    number_team_members: int = 14
    vip_team_members: List[str] = field(default_factory=list)

    def __post_init__(self):
        my_config_json = get_config_dict(PATH_SET)
        self.day_of_the_week = my_config_json['day_of_the_week']
        self.voting_time = my_config_json['voting_time']
        self.team_members = my_config_json['team_members']
        self.voting_members = my_config_json['voting_members']
        self.number_team_members = my_config_json['number_team_members']
        self.vip_team_members = my_config_json['vip_team_members']


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
    if not os.path.exists(path):
        create_config(path)
    try:
        with open(PATH_SET, encoding='utf8') as settings_file:
            config = json.load(settings_file)
        # проверяем файл на исправность данных, если нет - создаем снова по дефолту
    except ValueError:
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
    # my_config = MyConfig()
    my_config.day_of_the_week = config["day_of_the_week"]
    my_config.voting_time = config["voting_time"]
    my_config.voting_members = config["voting_members"]
    my_config.team_members = config["team_members"]
    my_config.number_team_members = int(config['number_team_members'])
    my_config.vip_team_members = config['vip_team_members']


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
    with open(path, "w", encoding='utf8') as settings_file:
        json.dump(my_config_str, settings_file, ensure_ascii=False)


def incoming_parsing(incoming_id: str, incoming_text: str):
    """
    Incoming message processing
    """
    global END_COUNTDOWN
    outcoming_ids: List = [incoming_id]
    outcoming_text = 'ошибочная команда'
    date_now = datetime.strftime(datetime.now(), '%d-%m-%y')
    if incoming_text[0] == '@':
        outcoming_ids, outcoming_text = admin_utilites(incoming_id, incoming_text)
    else:
        if END_COUNTDOWN:
            outcoming_ids = table_id_team(date_now)
            if len(my_config.voting_members[date_now]) == my_config.number_team_members:
                outcoming_text = table_game_team(date_now) + '\n' + DICT_MENU['team_exist']
            else:
                outcoming_text = table_game_team(date_now)

        # проверяем на наличие id в списке команды
        if incoming_id not in my_config.team_members and not END_COUNTDOWN:
            my_config.team_members[incoming_id] = ''
            outcoming_text = DICT_MENU['team_log']
        else:
            # проверяем на наличие имени в списке команды
            if my_config.team_members[incoming_id] == '':
                my_config.team_members[incoming_id] = incoming_text
                outcoming_text = DICT_MENU['team_login'] + incoming_text + '\n' + DICT_MENU['brief_instructions']
            else:
                # все выше пройдено - читаем меседж
                if weekday_is_true() and time_is_true():
                    if date_now not in my_config.voting_members:
                        # при первом обращении в нужное время - создаем запись голосующих с внесением первыми VIP
                        my_config.voting_members[date_now] = []
                        for vip_members in my_config.vip_team_members:
                            my_config.voting_members[date_now].append(vip_members)
                    if '+' in incoming_text:
                        if incoming_id not in my_config.voting_members[date_now]:
                            my_config.voting_members[date_now].append(incoming_id)
                            if len(my_config.voting_members[date_now]) > my_config.number_team_members:
                                outcoming_text = DICT_MENU['team_allready_exist']
                            else:
                                outcoming_text = DICT_MENU['team_welcome']
                        else:
                            outcoming_text = DICT_MENU['team_member_allready_exist']
                    if incoming_text == '-' and incoming_id in my_config.voting_members[date_now]:
                        my_config.voting_members[date_now].remove(incoming_id)
                        outcoming_text = DICT_MENU['remove_from_team']

                    if  incoming_text == '?':
                        outcoming_text = table_game_team(date_now)
                else:
                    outcoming_text = DICT_MENU['out_of_time']
        if (date_now in my_config.voting_members and len(my_config.voting_members[date_now]) == my_config.number_team_members and not END_COUNTDOWN
            and incoming_text != '?') or (not END_COUNTDOWN and incoming_text == '-'):
            END_COUNTDOWN = not END_COUNTDOWN
    update_config(PATH_SET, my_config)
    return outcoming_ids, outcoming_text


def admin_utilites(incoming_ids, incoming_text):
    """
    Processing an incoming service message
    """
    outcoming_ids = [incoming_ids]
    outcoming_text = 'Упс! Что-то пошло не так!!!'
    incoming_text = incoming_text.split('@@')

    if incoming_text[0] == '@change_list_day_of_week':
        try:
            a = my_config.day_of_the_week = [int(i) for i in incoming_text[1]]
            outcoming_text = 'Дни голосования изменены на ' + str(a)
        except ValueError:
            outcoming_text = 'Упс! Что-то пошло не так!!!'
    if incoming_text[0] == '@change_voting_time':
        outcoming_text = 'Время голосования изменено на '
    if incoming_text[0] == '@get_team_members':

        outcoming_text = 'Зарегистрированные члены команды: \n'
    if incoming_text[0] == '@delete_team_members':
        try:
            deleted = my_config.team_members.pop(incoming_text[1], 'Никто не')
            outcoming_text = str(deleted) + ' \n удален из членов команды'
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
    if incoming_text[0] == '@get_my_config':
        config = get_config_dict(PATH_SET)
        outcoming_text = json.dumps(config, ensure_ascii=False)
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
    return datetime.now().time() > time(int(t[0]), int(t[1]), int(t[2]))


def weekday_is_true():
    """
    Checking for condition compliance by weekday
    """
    return datetime.isoweekday(datetime.now()) in my_config.day_of_the_week


def table_game_team(date: str):
    """
    Formation of a list table
    """
    table_str = ''
    for i in range(len(my_config.voting_members[date])):
        if i == my_config.number_team_members:
            table_str += DICT_MENU['in_reserve'] + '\n '
        table_str += str(i + 1) + ' : ' + my_config.team_members[my_config.voting_members[date][i]] + '\n '
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

    b = '5h2COTj83ZE6IAsIcTEVGw=='
    c = '@change_list_day_of_week@@2'
    # e = incoming_parsing(b, c)
    # e = incoming_parsing(b, c)
    # b = '4444444444444-444-444='
    # c = 'Valera'
    # e = incoming_parsing(b, c)
    # e = incoming_parsing(b, c)
    #
    # b = '8230jakncdnac-657-342='
    # c = 'RL'
    # e = incoming_parsing(b, c)
    # e = incoming_parsing(b, c)
    # print(e, my_config.voting_members)
    # c = '+'
    # e = incoming_parsing(b, c)
    # print(e, my_config.voting_members)
    #
    # b = '4344289412118-248-353='
    # c = 'RK'
    # e = incoming_parsing(b, c)
    # e = incoming_parsing(b, c)
    # print(e, my_config.voting_members)
    # c = '+'
    # e = incoming_parsing(b, c)
    # print(e, my_config.voting_members)
    #
    #
    # b = '5h2COTj83ZE6IAsIcTEVGw=='
    # c = '+'
    # e = incoming_parsing(b, c)
    # print(e, my_config.voting_members, sep='\n')
    # b = '5h2COTj83ZE6IAsIcTEVGw=='
    # c = 'loh'
    # e = incoming_parsing(b, c)
    # e = incoming_parsing(b, c)
    # c = '+'
    # e = incoming_parsing(b, c)
    # print(e, my_config.voting_members, sep='\n')
    # c = ''
    e, ee = incoming_parsing(b, c)
    print(e, ee, type(ee), my_config, sep='\n')
    # input()
    # e, ee = incoming_parsing(' ', ' ')
    # print(e, ee, type(ee), my_config, sep='\n')

