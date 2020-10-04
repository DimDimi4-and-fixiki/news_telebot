from my_tele_bot import MyTeleBot

def main():
    bot = MyTeleBot(token_path="secure_codes/token.txt")
    bot.polling()

if __name__ == "__main__":
    main()