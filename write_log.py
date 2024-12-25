def write_log(error):
    with open('log/error_log.txt', 'a') as file:
        file.write(error)

    return 0