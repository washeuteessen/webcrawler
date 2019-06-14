from ..items import RecipesItem
import re
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
import subprocess
import urllib

class ChefkochSpyder(CrawlSpider):
    """ 
    This class scrapes desired url by searching for recipe urls. 
    """
    # define name of spyder
    name = "essenundtrinken"

    # define start urls
    start_urls = ["https://www.essen-und-trinken.de"]

    # define rule to only parse links with "rezepte"
    rules = (Rule(LxmlLinkExtractor(allow="/rezepte/[0-9]{5}-*"), callback="parse_item", follow=True),)

    def parse_item(self, response):
        """
        Parse html reponse of scraper.

        Attributes:
            response (str): HTML source code of scraped page.

        Returns:
            items.json (dict): Json file with title and url of recipes as value.
        """
        # instantiate items
        items = RecipesItem()

        # get recipe title
        title = response.css(".headline-title::text").extract_first()

        # get title picture
        img_src = response.css(".recipe-img > img:nth-child(1)::attr(src)").extract_first()
        .recipe-img > img:nth-child(1)

        # get ingredients
        ingredients = response.css("ul.ingredients-list li::text").extract()

        # strip \n
        ingredients = [re.sub("\n", "", ingredient) for ingredient in ingredients]

        # strip whitespace
        ingredients = [re.sub(' +', " ", ingredient) for ingredient in ingredients]
        ingredients = [ingredient.strip() for ingredient in ingredients]

        # strip empty list elemens
        ingredients = [ingredient for ingredient in ingredients if len(ingredient)>0]

        # get text
        text = " ".join(response.css("ul.preparation li.preparation-step div.preparation-text p::text").extract())

        # sometimes text is not within paragraph
        if len(text)<1:
            text = " ".join(response.css("ul.preparation li.preparation-step div.preparation-text::text").extract())

        # store information as item
        items["title"] = title 
        items["domain"] = self.name
        items["img_src"] = img_src
        items["ingredients"] = ingredients
        items["url"] = response.url
        items["text"] = text

        return items

if __name__=="__main__":
    subprocess.call("scrapy", "crawl", "recipes", "-s", "JOBDIR=crawls/recipes-1")