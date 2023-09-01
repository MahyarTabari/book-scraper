# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        
        # Note: each item is passed to this pipeline separately

        adapter = ItemAdapter(item)


        # make "category" and "product_type" lowercase
        keys = ["category", "product_type"]
        for key in keys:
            value = adapter.get(key)
            adapter[key] = value.lower()


        # remove leading and trailing white spaces
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != "description":
                value = adapter.get(field_name)
                adapter[field_name] = value.strip()


        # remove pound sign and cast the prices float
        prices = ["price_excl_tax", "price_incl_tax", "tax"]
        for price in prices:
            value = adapter.get(price)
            value = value.replace("£", "")
            adapter[price] = float(value)


        # extract the availability number
        value = adapter.get("availability")
        value = value.split("(")
        value = value[1].split(" ")
        
        adapter["availability"] = int(value[0])


        # convert n_reviews to integer
        value = adapter.get("n_reviews")
        adapter["n_reviews"] = int(value)


        return item