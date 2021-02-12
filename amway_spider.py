import requests
import re
import json
from bs4 import BeautifulSoup
from lxml import html
import pyotp
import requests
import json
import sys

from splinter import Browser
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


def get_catalog(soup):
    catalog_list = soup.find(class_='col-sm-9 tab-content').find_all('a')
    catalog_list = list(filter(lambda x: '%' in x.attrs["href"], catalog_list))
    for item in catalog_list:
        if(item.attrs["title"] == 'カタログ・Amagram'):
            break
        # 类目进入后数据
        html_catalog = request_dandan(home_url + item.attrs["href"])
        catalog_soup = BeautifulSoup(html_catalog, 'lxml')
        get_page(catalog_soup)


def get_page(soup):
    page_list = soup.find(class_='product__listing product__list row js-query-result new-product__listing ditto-changeTo-sop').find_all(
        lambda tag: tag.name == "a" and tag.has_attr('target'))
    for item in page_list:
        # 拿到商品信息
        get_product(home_url + item.attrs["href"])


def get_product(url):
    browser.visit(url)
    title = browser.find_by_xpath(
        '//*[@id="product-details-page"]/div[1]/div/div/div/div[1]').html
    id_prefix = hash('amway') % ((sys.maxsize + 1) * 2)
    order_number = int(url.split('/')[-1])
    product_id = id_prefix + order_number
    sku = 'amway' + str(order_number)
    price_text = browser.find_by_xpath(
        '//*[@id="product-details-page"]/div[6]/div/div/div[2]/div[3]/p[2]').text
    first_index = price_text.find(' ')
    second_index = price_text.find(' ', first_index + 1)
    price = int(price_text[first_index + 1:second_index].replace(',', ''))

    # 然后登陆到magento去
    global token
    headers = {'content-type': 'application/json',
               'Authorization': 'Bearer ' + token}
    response_from_magento = requests.post(magento_url + '/index.php/rest/default/V1/products',
                  data=json.dumps({
                      "product": {
                                  "id": product_id,
                                  "sku": sku,
                                  "name": title,
                                  "price": price,
                                  "status": 1,
                                  "visibility": 1,
                                  "type_id": "amway",
                                  "weight": 1,
                                  "extension_attributes": {
                                      "website_ids": [
                                          0
                                      ],
                                      "category_links": [
                                          {
                                              "position": 0,
                                              "category_id": "string",
                                              "extension_attributes": {}
                                          }
                                      ],
                                      "stock_item": {
                                          "item_id": 0,
                                          "product_id": 0,
                                          "stock_id": 0,
                                          "qty": 0,
                                          "is_in_stock": True,
                                          "is_qty_decimal": True,
                                          "use_config_min_qty": True,
                                          "min_qty": 0,
                                          "use_config_min_sale_qty": 0,
                                          "min_sale_qty": 0,
                                          "use_config_max_sale_qty": True,
                                          "max_sale_qty": 0,
                                          "use_config_backorders": True,
                                          "backorders": 0,
                                          "use_config_notify_stock_qty": True,
                                          "notify_stock_qty": 0,
                                          "use_config_qty_increments": True,
                                          "qty_increments": 0,
                                          "use_config_enable_qty_inc": True,
                                          "enable_qty_increments": True,
                                          "use_config_manage_stock": True,
                                          "manage_stock": True,
                                          "low_stock_date": "string",
                                          "is_decimal_divided": True,
                                          "stock_status_changed_auto": 0,
                                          "extension_attributes": {}
                                      },
                                      "bundle_product_options": [
                                          {
                                              "option_id": 0,
                                              "title": "string",
                                              "required": True,
                                              "type": "string",
                                              "position": 0,
                                              "sku": "string",
                                              "product_links": [
                                                  {
                                                      "id": "string",
                                                      "sku": "string",
                                                      "option_id": 0,
                                                      "qty": 0,
                                                      "position": 0,
                                                      "is_default": True,
                                                      "price": 0,
                                                      "price_type": 0,
                                                      "can_change_quantity": 0,
                                                      "extension_attributes": {}
                                                  }
                                              ],
                                              "extension_attributes": {}
                                          }
                                      ],
                                      "configurable_product_options": [
                                          {
                                              "id": 0,
                                              "attribute_id": "string",
                                              "label": "string",
                                              "position": 0,
                                              "is_use_default": True,
                                              "values": [
                                                  {
                                                      "value_index": 0,
                                                      "extension_attributes": {}
                                                  }
                                              ],
                                              "extension_attributes": {},
                                              "product_id": 0
                                          }
                                      ],
                                      "configurable_product_links": [
                                          0
                                      ]
                                  },
                                  "product_links": [
                                      {
                                          "sku": "string",
                                          "link_type": "string",
                                          "linked_product_sku": "string",
                                          "linked_product_type": "string",
                                          "position": 0,
                                          "extension_attributes": {
                                              "qty": 0
                                          }
                                      }
                                  ],
                                  "options": [
                                      {
                                          "product_sku": "string",
                                          "option_id": 0,
                                          "title": "string",
                                          "type": "string",
                                          "sort_order": 0,
                                          "is_require": True,
                                          "price": 0,
                                          "price_type": "string",
                                          "sku": "string",
                                          "file_extension": "string",
                                          "max_characters": 0,
                                          "image_size_x": 0,
                                          "image_size_y": 0,
                                          "values": [
                                              {
                                                  "title": "string",
                                                  "sort_order": 0,
                                                  "price": 0,
                                                  "price_type": "string",
                                                  "sku": "string",
                                                  "option_type_id": 0
                                              }
                                          ],
                                          "extension_attributes": {
                                              "vertex_flex_field": "string"
                                          }
                                      }
                                  ],
                                  "tier_prices": [
                                      {
                                          "customer_group_id": 0,
                                          "qty": 0,
                                          "value": 0,
                                          "extension_attributes": {
                                              "percentage_value": 0,
                                              "website_id": 0
                                          }
                                      }
                                  ],
                                  "custom_attributes": [
                                      {
                                          "attribute_code": "string",
                                          "value": "string"
                                      }
                                  ]
                                  },
                      "saveOptions": True
                  }),
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
    get_catalog(soup)
