import json

with open('config.json') as data_file:
    config = json.load(data_file)

__doctors = config['search']['doctors']
__number_of_doctors = len(__doctors)
__last_selected_doctor_index = 0


def get_current_doctor():
    global __last_selected_doctor_index
    global __doctors
    global __number_of_doctors

    if not __doctors:
        return ""

    return __doctors[__last_selected_doctor_index]


def get_next_doctor():
    global __last_selected_doctor_index
    __last_selected_doctor_index = (__last_selected_doctor_index + 1) % __number_of_doctors
    return get_current_doctor()
