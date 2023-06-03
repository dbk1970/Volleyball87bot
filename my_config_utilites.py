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
DICT_MENU = {'team_log':'Представьтесь! (напишите имя под которым вас будут узнавать в списке игроков)',
             'team_unlog': 'Вы удалены из списка голосования',
             ' ': ' '
            }

DAY_OF_THE_WEEK_DEFAULT = 2
VOTING_TIME_DEFAULT = "12:00:00"
TEAM_DICT_DEFAULT = {'5h2COTj83ZE6IAsIcTEVGw==': 'DK'}
VOTING_MEMBERS = {}
CONFIG_DEFAULT = {"day_of_the_week": DAY_OF_THE_WEEK_DEFAULT,
                      "voting_time": VOTING_TIME_DEFAULT,
                      "team_members": TEAM_DICT_DEFAULT,
                      'voting_members': VOTING_MEMBERS
                      }

@dataclass
class MyConfig:
    day_of_the_week: int = 0
    voting_time: datetime.time = ()
    team_members: dict = field(default_factory=dict)
    voting_members: dict = field(default_factory=dict)

    def __post_init__(self):
        my_config_json = get_config(PATH_SET)
        self.day_of_the_week = my_config_json['day_of_the_week']
        self.voting_time = my_config_json['voting_time']
        self.team_members = my_config_json['team_members']
        self.voting_members = my_config_json['voting_members']


def create_config(path):
    """
    Create a config file
    """

    config_default = CONFIG_DEFAULT

    with open(path, "w") as settings_file:
        json.dump(config_default, settings_file)


def get_config(path):
    """
    Returns the config object
    """
    if not os.path.exists(path):
        create_config(path)

    try:
        with open(PATH_SET) as settings_file:
            config = json.load(settings_file)

        # проверяем файл на исправность данных, если нет - создаем снова по дефолту
    except ValueError:
        create_config(path)
        with open(PATH_SET) as settings_file:
            config = json.load(settings_file)
    finally:
            g = config['voting_time'].split(':')
            #  переводим "время голосования" в формат datetime
            config['voting_time'] = time(int(g[0]), int(g[1]), int(g[2]))
            #  переводим "время голосования" в формат datetime

    return config


def update_config(path, config: MyConfig):
    """
    Update a settings config
    """
    my_config = CONFIG_DEFAULT
    my_config["day_of_the_week"] = config.day_of_the_week
    my_config["voting_time"] = strftime(config.voting_time, '%H:%M:%S') # переводим в строку, а то json не увидит
    my_config["voting_members"] = config.voting_members
    my_config["team_members"] = config.team_members
    with open(path, "w") as settings_file:
        json.dump(my_config, settings_file)


def delete_setting(path, section, setting):
    """
    Delete a setting НЕ РАБОТАЕТ
    """
    config = get_config(path)
    config.remove_option(section, setting)
    with open(path, "w") as config_file:
        config.write(config_file)


def incoming_parsing(incoming_id, incoming_text):
    if not myconfig["team_members"].keys(incoming_id):
        myconfig["team_members"][incoming_id] = ''
        update_config(myconfig)
        incoming_text = DICT_MENU['team_log']
        return incoming_id, incoming_text, myconfig
    return incoming_id, incoming_text

if __name__ == "__main__":
    a = MyConfig()
    print(a, type(a.voting_time))
    print(a.voting_members)
    a.voting_members["06:06:23"].append('xxxxxxxxxxxxxxxxxxxxxxxx')
    update_config(PATH_SET,a)
    print(a, type(a.voting_time))

