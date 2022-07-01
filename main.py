from rdutilities.rdutilities import RDUtilities
from tools.tools import Settings

settings = Settings("private/settings.json")
rd = RDUtilities(api_key=settings.config.REALDEBRID.AUTH_TOKEN)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Simple loop to test functionality
    while True:
        magnet = input("Enter a magnet link or 'exit' to exit: ")
        if magnet == "exit":
            break
        result = rd.check_link(link=magnet)
        print("RESULT:", result)
        if bool(result):
            choice = input("Would you like to add this magnet to your library? (y/n): ")
            if choice.upper() == "Y":
                rd.add_magnet(magnet)
                print("Magnet added to library!")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
