# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os

import pymysql
from itemadapter import ItemAdapter

class MySQLPipeline:
    # Static variable to ensure SQL script is executed only once

    def open_spider(self, spider):
        self.connection = pymysql.connect(
            host=spider.settings.get('MYSQL_HOST'),
            user=spider.settings.get('MYSQL_USER'),
            password=spider.settings.get('MYSQL_PASSWORD'),
            port=spider.settings.get('MYSQL_PORT'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.connection.cursor()
          
        # Connect to the newly created database
        self.connection.select_db(spider.settings.get('MYSQL_DATABASE'))

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        sql = item.sql
        self.cursor.execute(sql, tuple((adapter.get(filed) for filed in item.fields_list)))
        self.connection.commit()
        return item
