def login_required(f):
    def decorated(username, password, **kwargs):
        if username == 'asd' and password == 1234:
            f(username, password)
            print('You are logged in')
            return

        print('Login is required')

    return decorated


@login_required
def my_func(username, password):
    print(f'You provided username as {username} and password as {password}')


my_func('asd', 1234)
