from pprint import pprint

from src.api_hh import HeadHunterAPI

if __name__ == '__main__':
    vacan = HeadHunterAPI()
    a = vacan.get_employers('hh')
    vac = vacan.get_json_list('hh')

    pprint(vac)
