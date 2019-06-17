# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

class RecipesPipeline(object):
    # Initialise of the class
    def __init__ (self):
        
        # Connecting to Server with Name and Port
        self.conn = pymongo.MongoClient(
            'localhost',
            27017
        )
        
        # Choosing Database and Collection
        db = self.conn["test"]
        self.collection = db["recipes"]

    # Processing
    def process_item(self, item, spider):
        
        # Inserting Scraped item into MongoDB
        self.collection.insert(dict(item))
        return item