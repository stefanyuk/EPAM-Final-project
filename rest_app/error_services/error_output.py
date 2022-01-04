from flask import make_response


def generate_error_message(message, error_code=404):
    """
    Generates error message in case of wrong request

    :param message: message to be returned
    :param error_code: status code that needs to be presented to user
    :return: message to be displayed to the user
    """

    return make_response(message, error_code)
