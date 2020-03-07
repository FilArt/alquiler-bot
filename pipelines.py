# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2

from alquiler.bot import send_message


def filtr(item):
    return item['price'] < 500


class AlquilerPipeline:
    # noinspection PyMethodMayBeStatic, PyAttributeOutsideInit,PyUnusedLocal
    def open_spider(self, spider):
        self.conn = psycopg2.connect('dbname=alquiler user=postgres password=1')
        self.cur = self.conn.cursor()
        self.count = 0

    # noinspection PyUnusedLocal
    def process_item(self, item, spider):
        self.count += 1
        if not filtr(item):
            return
        url = item['url']
        self.cur.execute(
            'select url from alquiler where url = %s',
            [url]
        )
        exist = self.cur.fetchone()
        if not exist:
            self.cur.execute(
                'insert into alquiler (url) values (%s)',
                [url]
            )
            self.conn.commit()
            msg = url
            send_message(msg)
        return item

    # noinspection PyUnusedLocal
    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
        print(f'\n\t{spider} count:{self.count}\n')
