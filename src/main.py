
"""
Written by Seedorfe
"""



import init
import databace
import bot


def main():
    init.find_root_path()
    init.make_needed_dir()
    databace.creat_databace()
    bot.run_bot()








if __name__ == "__main__":
    main()