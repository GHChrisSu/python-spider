from splinter import Browser
import base64
import requests
import re
import json
from bs4 import BeautifulSoup
from lxml import html
import pyotp
import requests
import json
import sys
import json
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="magento",
    database="magento"
)

mycursor = mydb.cursor()

sql = "SET FOREIGN_KEY_CHECKS = 0;"
mycursor.execute(sql)
sql = "TRUNCATE TABLE catalog_category_entity;"
mycursor.execute(sql)
sql = "TRUNCATE TABLE catalog_category_entity_decimal;"
mycursor.execute(sql)
sql = "TRUNCATE TABLE catalog_category_entity_datetime;"
mycursor.execute(sql)
sql = "TRUNCATE TABLE catalog_category_entity_int; "
mycursor.execute(sql)
sql = "TRUNCATE TABLE catalog_category_entity_text; "
mycursor.execute(sql)
sql = "TRUNCATE TABLE catalog_category_entity_varchar; "
mycursor.execute(sql)
sql = "TRUNCATE TABLE catalog_category_product; "
mycursor.execute(sql)
sql = "TRUNCATE TABLE catalog_category_product_index;"
mycursor.execute(sql)
sql = "INSERT INTO `catalog_category_entity` (`entity_id`, `attribute_set_id`, `parent_id`, `created_at`, `updated_at`, `path`, `position`, `level`, `children_count`) VALUES ('1', '0', '0', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, '1', '0', '0', '1'),('2', '3', '1', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, '1/2', '1', '1', '0');"
mycursor.execute(sql)
sql = "INSERT INTO `catalog_category_entity_int` (`value_id`, `attribute_id`, `store_id`, `entity_id`, `value`) VALUES ('1', '69', '0', '1', '1'),('2', '46', '0', '2', '1'),('3', '69', '0', '2', '1');"
mycursor.execute(sql)
sql = "INSERT INTO `catalog_category_entity_varchar` (`value_id`, `attribute_id`, `store_id`, `entity_id`, `value`) VALUES ('1', '45', '0', '1', 'Root Catalog'),('2', '45', '0', '2', 'Default Category');"
mycursor.execute(sql)
sql = "SET FOREIGN_KEY_CHECKS = 1;"
mycursor.execute(sql)
sql = "DELETE FROM url_rewrite WHERE entity_type = 'category';"
mycursor.execute(sql)
sql = "DELETE FROM `catalog_product_entity`;"
mycursor.execute(sql)
sql = "ALTER TABLE `catalog_product_entity` AUTO_INCREMENT =1;"
mycursor.execute(sql)

mydb.commit()

executable_path = {'executable_path': '/usr/local/bin/chromedriver'}

browser = Browser('chrome', **executable_path)

admin = """curl -X POST "https://magento2.test/index.php/rest/V1/tfa/provider/google/authenticate"      -H "Content-Type:application/json"      -d '{"username":"suhao", "password":"suhao520", "otp":"982222"}'"""
factor = """curl -X POST "https://magento2.test/index.php/rest/V1/tfa/provider/google/authenticate"      -H "Content-Type:application/json"      -d '{"username":"suhao", "password":"suhao520"}'"""

home_url = 'https://www.amwaylive.com'
magento_url = 'https://magento2.test'
token = 'token'


def request_dandan(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None


def get_catalog_level_3(soup, i, parent_id):
    catalog_3_list = soup.find(id='navMenuTab' + str(i)).find_all('a')
    catalog_3_list = list(
        filter(lambda x: '%' in x.attrs["href"], catalog_3_list))

    headers = {'content-type': 'application/json',
               'Authorization': 'Bearer ' + token}

    for item in catalog_3_list:
        if(item.attrs["title"] == 'カタログ・Amagram'):
            break
        category_3 = {
            "category": {
                "parent_id": parent_id,
                "name": item.attrs["title"],
                "custom_attributes": [
                    {
                        "attribute_code": "url_key",
                        "value": item.attrs["href"].split('/')[-1],
                    },
                ],
                "is_active": True,
                "position": 1,
                "level": 3,
                "include_in_menu": True
            }
        }
        category_3_magento = requests.post(magento_url + '/index.php/rest/default/V1/categories',
                                           data=json.dumps(category_3),
                                           verify=False, headers=headers)

        category_3_response_json_object = json.loads(category_3_magento.text)

        # 类目进入后数据
        html_catalog = request_dandan(home_url + item.attrs["href"])
        catalog_soup = BeautifulSoup(html_catalog, 'lxml')
        get_page(catalog_soup, category_3_response_json_object['id'])


def get_catalog_level_1_2(soup):
    headers = {'content-type': 'application/json',
               'Authorization': 'Bearer ' + token}
    # amway category
    category_1 = {
        "category": {
            "parent_id": 1,
            "name": "アムウェイ",
            "custom_attributes": [
                {
                    "attribute_code": "url_key",
                    "value": "amway"
                },
            ],
            "is_active": True,
            "position": 1,
            "level": 1,
            "include_in_menu": True
        }
    }

    response_from_magento = requests.post(magento_url + '/index.php/rest/default/V1/categories',
                                          data=json.dumps(category_1),
                                          verify=False, headers=headers)

    catalog_2_list = soup.select(
        '#overlay-menu-wrapper > div > div > div.col-sm-3.overlay-menu-headers > div > div > ul')[0].find_all('li')

    for i in range(len(catalog_2_list)):
        if i > 3:
            break
        # 更新magento的category
        category_2 = {
            "category": {
                "parent_id": 3,
                "name": catalog_2_list[i].text.strip(),
                "custom_attributes": [
                    {
                        "attribute_code": "url_key",
                        "value": str(101+i)
                    },
                ],
                "is_active": True,
                "position": 1,
                "level": 2,
                "include_in_menu": True
            }
        }
        # response_from_magento = requests.get(magento_url + '/index.php/rest/default/V1/categories',
        #                                       verify=False, headers=headers)
        # print(response_from_magento.text)

        category_2_response = requests.post(magento_url + '/index.php/rest/default/V1/categories',
                                            data=json.dumps(category_2),
                                            verify=False, headers=headers)
        print(category_2_response.text)

        category_2_response_json_object = json.loads(category_2_response.text)
        get_catalog_level_3(soup, i, category_2_response_json_object['id'])


def get_page(soup, category_id):
    page_list = soup.find(class_='product__listing product__list row js-query-result new-product__listing ditto-changeTo-sop').find_all(
        lambda tag: tag.name == "a" and tag.has_attr('target'))
    for item in page_list:
        # 拿到商品信息
        get_product(home_url + item.attrs["href"], category_id)


def get_product(url, category_id):
    browser.visit(url)
    title = browser.find_by_xpath(
        '//*[@id="product-details-page"]/div[1]/div/div/div/div[1]').html
    order_number = int(url.split('/')[-1])
    product_id = int('100' + str(order_number))
    sku = 'amway-' + str(order_number)
    price_text = browser.find_by_css(
        '#product-details-page > div.col-sm-12.col-md-6.pdp-info.new-pdp-info > div > div > div:nth-child(2) > div.product-details > p.mob-top-border.price.retail-price-discount').text
    first_index = price_text.find(' ')
    second_index = price_text.find(' ', first_index + 1)
    price = int(price_text[first_index + 1:second_index].replace(',', ''))
    description = browser.find_by_css(
        '#product-details-page > div.col-sm-12.col-md-6.pdp-info.new-pdp-info > div > div > div:nth-child(2) > div.description > p').text

    media_gallery_entry = []
    image_tags = BeautifulSoup(browser.find_by_id(
        'thumbnailSlider').html, 'lxml').find_all('img')
    for i in range(len(image_tags)):
        media_gallery_entry.append(
            {
                "media_type": 'image',
                "label": "amway",
                "position": i,
                "disabled": False,
                "types": ['thumbnail', 'small_image', 'image'],
                "content": {
                    "base64_encoded_data": base64.b64encode(requests.get(image_tags[i].attrs["data-zoom-url"]).content).decode('utf-8'),
                    "type": "image/png",
                    "name": sku + "-" + str(i) + ".png"
                }
            }
        )

    product_json = {
        "product": {
            "id": product_id,
            "sku": sku,
            "attribute_set_id": 9,
            "name": title,
            "price": price,
            "status": 1,
            "visibility": 1,
            "type_id": "simple",
            "weight": "0.8",
            "extension_attributes": {
                "category_links": [
                    {
                        "position": 0,
                        "category_id": category_id
                    }
                ],
                "stock_item": {
                    "qty": "10",
                    "is_in_stock": True
                }
            },
            "custom_attributes": [
                {
                    "attribute_code": "description",
                    "value": description
                }
            ],
            "media_gallery_entries": media_gallery_entry
        }
    }

    # 然后登陆到magento去
    global token
    headers = {'content-type': 'application/json',
               'Authorization': 'Bearer ' + token}
    response_from_magento = requests.post(magento_url + '/index.php/rest/default/V1/products',
                                          data=json.dumps(product_json),
                                          verify=False, headers=headers)
    response_from_magento


def get_admin_token():
    totp = pyotp.TOTP('75PUAPQ3UIKIR2AXS4PXM3AMLHAULJAXET6EK4GZ7BPGACYWU74VEJO3V63IAU4YW2BLOAMULX4UGZ3LFYITF24KAB5CYOCLYCBSHUGU6BJZWEKWGOBNNSVZXAADSBOJF2LIPQU6MB4CJGLXYZABTURHS3RIFONFDIMQ32RLDNTM66TVO7HHPDDJDCWXBCXYNE4QO4U2HJ43E')  # サーバー側であらかじめ指定する一意の値
    global token
    headers = {'content-type': 'application/json'}
    authenticate_response = requests.post(magento_url + '/index.php/rest/V1/tfa/provider/google/authenticate',
                                          data=json.dumps(
                                              {"username": "suhao1", "password": "suhao520", "otp": totp.now()}),
                                          verify=False, headers=headers)
    token = authenticate_response.json()


if __name__ == "__main__":
    get_admin_token()
    html_home = request_dandan(home_url)
    soup = BeautifulSoup(html_home, 'lxml')
    get_catalog_level_1_2(soup)
