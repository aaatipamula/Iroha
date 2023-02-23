def main():
    while True:
        token = input("Please input your bot token here: ")

        if token != '':
            break
        else: print('\nPlease enter your bot token!')

    while True:
        dump_channel = input("Please input the channel id here: ")

        if dump_channel != '' and dump_channel.isdigit():
            break
        else: print('\nPlease enter your bot token!')

    while True:
        command_prefix = input("Please input the command prefix you would like here: ")

        if command_prefix != '':
            break
        else: print('\nPlease enter your bot token!')

    while True:
        about_me = input("Please input the about me you would like here: ")

        if about_me != '':
            break
        else: print('\nPlease enter your bot token!')

    with open('./src/.env', 'w') as f:
        dump_string = """
            TOKEN="{token}"
            DUMP_CHANNEL={dump_channel}
            COMMAND_PREFIX=\"{command_prefix}\"
            ABOUT_ME=\"{about_me}\""""

        f.write(dump_string)

    print('\nYour data is saved in ./src/.env and can be edited if any of the previously input information is incorrect or needs to be updated!')

if __name__ == '__main__':
    main()
