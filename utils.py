import shelve
import config


def set_user_game(chat_id, estimated_answer):
    with shelve.open(config.shelve_name) as sh_storage:
        sh_storage[str(chat_id)] = estimated_answer


def finish_user_game(chat_id):
    with shelve.open(config.shelve_name) as sh_storage:
        del sh_storage[str(chat_id)]


def get_answer_for_user(chat_id):
    with shelve.open(config.shelve_name) as sh_storage:
        try:
            answer = sh_storage[str(chat_id)]
            return answer
        except KeyError:
            return None
