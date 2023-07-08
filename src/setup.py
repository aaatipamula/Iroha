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
        else: print('\nPlease a valid integer!')

    while True:
        command_prefix = input("Please input the command prefix you would like here: ")

        if command_prefix != '':
            break
        else: print('\nPlease a command prefix!')

    while True:
        about_me = input("Please input the about me you would like here: ")

        if about_me != '':
            break
        else: print('\nPlease enter an about me!')

    dump_string = f"TOKEN=\"{token}\"\nDUMP_CHANNEL={dump_channel}\nCOMMAND_PREFIX=\"{command_prefix}\"\nABOUT_ME=\"{about_me}\""

    with open('./src/data/.env', 'w') as f:

        f.write(dump_string)

    print('\nYour data is saved in ./src/.env and can be edited if any of the previously input information is incorrect or needs to be updated!')

if __name__ == '__main__':
    main()
