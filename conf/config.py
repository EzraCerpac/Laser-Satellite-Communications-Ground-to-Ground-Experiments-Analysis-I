from dataclasses import dataclass


class DataDF:
    def __init__(self, data_set: int, mode: bool, number: int):
        dir = {
            11: 'data11/'
        }
        mode_dict = {
            True: {
                'number': [2, 4, 8, 16, 28],
                'filename': f'{number} modes.pickle'
            },
            False: {
                'number': [1, 2, 3, 4, 5],
                'filename': f'off{number}.pickle'
            }
        }
        rootdir: str = 'Data/DFs/'
        self.file = rootdir + dir[data_set] + mode_dict[mode]['filename'] \
            if number in mode_dict[mode]['number'] else None


@dataclass
class UserInterface:
    title: str = "My app"
    width: int = 1024
    height: int = 768


@dataclass
class FileConfig:
    default: DataDF = DataDF(11, False, 1)
    ui: UserInterface = UserInterface()
