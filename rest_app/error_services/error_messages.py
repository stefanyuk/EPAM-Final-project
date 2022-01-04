from config import Config

error_employee_not_found = {
    'status': 404,
    'message': 'Employee with the provided id was not found'
}

error_department_not_found = {
    'status': 404,
    'message': 'Department with the provided name was not found'
}

error_bad_api_version = {
    'status': 410,
    'message': 'You are using not the current version of api.' +
               f' Please use the newest version which is {Config.API_VERSION}',
    'correct_url': f'/api/v{Config.API_VERSION}/...'
}

error_for_not_found = {
    'status': 404,
    'message': 'Resource not found',
    'correct_url': f'/api/v{Config.API_VERSION}/...'
}

error_order_not_found = {
    'status': 404,
    'message': 'order with the provided id was not found'
}

error_user_not_found = {
    'status': 404,
    'message': 'user with the provided id was not found'
}

error_vacation_not_found = {
    'status': 404,
    'message': 'vacation with the provided id was not found'
}
