from config import Config


def record_not_found_by_id_error(id_of_the_searched_row: str) -> dict:
    error_record_not_found = {
        'status': 404,
        'message': f'{id_of_the_searched_row} with the provided id was not found'
    }

    return error_record_not_found


error_bad_api_version = {
    'status': 410,
    'message': 'You are using not the current version of api.' +
               f' Please use the newest version which is {Config.API_VERSION}',
    'correct_url': f'/api/v{Config.API_VERSION}/...'
}

error_resource_not_found = {
    'status': 404,
    'message': 'Resource not found',
    'correct_url': f'/api/v{Config.API_VERSION}/...'
}