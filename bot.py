import subprocess

from telegram.ext import Updater, Job


def send_message(text):
    import telegram
    user_id = '339020478'
    token = '1034132424:AAHmTbYhFwILefcRUIthWzvUCG_Rt3AVLoU'
    bot = telegram.Bot(token)
    bot.send_message(user_id, text)


# noinspection PyUnusedLocal
# @run_async
def run_spiders(job: Job):
    subprocess.run(['scrapy list | xargs -n 1 -P 0 scrapy crawl -L INFO'], shell=True)


def main():
    updater = Updater("1090727386:AAE0CDKMsCPiqfT5mausVh3N3EWJIaA_OKY", use_context=True)
    updater.job_queue.run_once(run_spiders, 1)
    updater.job_queue.run_repeating(run_spiders, interval=1200)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
