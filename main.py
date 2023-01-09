from parsel import Selector
import requests
from config import DEFAULT_HEADERS
from db.models import AutoRiaModel
from db.database import Database
from logs_mongo.mongo_database import Mongo_DB


class NewCarsScraper:
    MAIN_URL = "https://auto.ria.com/newauto/category-legkovie/?page={}"
    AUTO_URL_XPATH = '//a[@class="proposition_link"]/@href'
    TITLE_AUTO_XPATH = '//h1[@class="auto-head_title bold mb-15"]/text()'
    PRICE_AUTO_XPATH = '//div[@class="price_value"]/text()'
    PRICE_USD_EURO_XPATH = '//div[@class="price_value price_value--additional"]/text()'
    ACTUAL_COST_DATE_XPATH = '//div[@class="item_inner"]/text()'
    IN_STOCK_XPATH = '//b/text()|//span[@class="badge badge--red order--on"]/text()'
    CAR_RATING_XPATH = '//span[@class="score-rating-mark"]/text()'
    CREDIT_XPATH = '//li[@data-gaq="credit-competence-desk-text"]/b/text()'  # с кредитом выходят непонятные символы
    AUTOSALON_NAME_XPATH = '//h4[@class="seller_info_name"]/a/strong/text()'
    # AUTOSALON_PHONE_XPATH = '//div[@id="react-phones"]//span[@class="show-phone-btn dotted"][contains(text(),"показать")]//span[@class="bold load_phone__item"]/text()'
    # '//span[@class="phone bold pl-20"]/text()' #скрытый номер вытаскивает но нет
    AUTOSALON_RATING_XPATH = '//div[@class="item_inner"]/span[@class="bold"]/text()'
    LOCATION_XPATH = '//div[@class="sticky-15"]//li[2]//div[1]/text()'
    ENGINE_XPATH = '//dd[@class="defines_list_value"]/a[@data-gaq="link-fuel"]/text()'
    GEARBOX_XPATH = '//dl[@class="defines_list mb-15 unstyle"]/dd[2]/text()'  # 14
    PRIVOD_XPATH = '//dl[@class="defines_list mb-15 unstyle"]/dd[3]/text()'
    GENERATION_XPATH = '//a[@data-gaq="link-generation"]/text()'
    CAR_COLOR_XPATH = '//div[@class="body_color_name"]/text()'
    AVAILABLE_COLOR_XPATH = '//dd[@class="defines_list_value color"]//a/@title'
    IMAGE_XPATH = "//picture//img/@src"  # all images
    MAX_SPEED_XPATH = '//ul[@class="full-characteristics-list accordion-body unstyle size13"]//li[2]//ul//li[2]//strong/span[@class="el"]/text()'  # проверка
    VIN_CODE_XPATH = '//span[@class="checked_ad label-check"]/svg/@aria-label'

    def __init__(self):
        self.all_pages = []
        self.all_urls = []
        self.database = Database()
        self.mongo_database = Mongo_DB()

    def get_all_pages(self):
        for i in range(1, 5):
            self.all_pages.append(self.MAIN_URL.format(i))
        for one_page in self.all_pages:
            content = requests.get(one_page).text
            page_selector = Selector(text=content)
            self.all_urls.extend(page_selector.xpath(self.AUTO_URL_XPATH).extract())

    def get_car_data(self):
        for url in self.all_urls:
            response = requests.request(
                "GET",
                "https://auto.ria.com" + url,
                headers=DEFAULT_HEADERS,
            )
            content = response.text
            tree = Selector(text=content)
            title = tree.xpath(self.TITLE_AUTO_XPATH).extract_first()
            price = tree.xpath(self.PRICE_AUTO_XPATH).extract_first()
            price_usd_euro = tree.xpath(self.PRICE_USD_EURO_XPATH).extract_first()
            actual_cost_date = tree.xpath(self.ACTUAL_COST_DATE_XPATH).extract_first()
            in_stock = tree.xpath(self.IN_STOCK_XPATH).extract_first()
            car_rating = tree.xpath(self.CAR_RATING_XPATH).extract_first()
            credit = tree.xpath(self.CREDIT_XPATH).extract_first()
            autosalon_name = tree.xpath(self.AUTOSALON_NAME_XPATH).extract_first()
            autosalon_rating = tree.xpath(self.AUTOSALON_RATING_XPATH).extract_first()
            location = tree.xpath(self.LOCATION_XPATH).extract_first()
            engine = tree.xpath(self.ENGINE_XPATH).extract_first()
            gearbox = tree.xpath(self.GEARBOX_XPATH).extract_first()
            privod = tree.xpath(self.PRIVOD_XPATH).extract_first()
            generation = tree.xpath(self.GENERATION_XPATH).extract_first()
            car_color = tree.xpath(self.CAR_COLOR_XPATH).extract_first()
            available_color = tree.xpath(self.AVAILABLE_COLOR_XPATH).extract()
            image = tree.xpath(self.IMAGE_XPATH).extract()
            max_speed = tree.xpath(self.MAX_SPEED_XPATH).extract_first()
            vin_code = tree.xpath(self.VIN_CODE_XPATH).extract_first()
            if vin_code == None:
                vin_code = "Отсутствует"

            data = AutoRiaModel(
                current_url=response.request.url,
                title=title,
                price=price,
                price_usd_euro=price_usd_euro,
                actual_cost_date=actual_cost_date,
                in_stock=in_stock,
                car_rating=car_rating,
                credit=credit,
                autosalon_name=autosalon_name,
                autosalon_rating=autosalon_rating,
                location=location,
                engine=engine,
                gearbox=gearbox,
                privod=privod,
                generation=generation,
                car_color=car_color,
                available_color=available_color,
                image=image,
                max_speed=max_speed,
            )
            # print(title)
            # self.database.add_auto(objects=data)

            vin_code_data = Mongo_DB.log_collection = {
                "vin_code": vin_code,
                "url": response.request.url,
                "date": Mongo_DB.log_collection.get("date"),
            }
            auto_collection_data = Mongo_DB.auto_collection = {
                "current_url": response.request.url,
                "title": title,
                "price": price,
                "price_usd_euro": price_usd_euro,
                "actual_cost_date": actual_cost_date,
                "in_stock": in_stock,
                "car_rating": car_rating,
                "credit": credit,
                "autosalon_name": autosalon_name,
                "autosalon_rating": autosalon_rating,
                "location": location,
                "engine": engine,
                "gearbox": gearbox,
                "privod": privod,
                "generation": generation,
                "car_color": car_color,
                "available_color": available_color,
                "image": image,
                "max_speed": max_speed,
                "date": Mongo_DB.auto_collection.get("date"),
            }
            print(vin_code_data)
            print(auto_collection_data)
            self.mongo_database.add_to_log_collection(log_objects=vin_code_data)
            self.mongo_database.add_to_auto_collection(auto_objects=auto_collection_data)


    def main(self):
        self.get_all_pages()
        self.get_car_data()


if __name__ == "__main__":
    scraper = NewCarsScraper()
    scraper.main()
