def write_log(error):
    with open('app/log/error_log.txt', 'a') as file:
        file.write(str(error))

    return 0