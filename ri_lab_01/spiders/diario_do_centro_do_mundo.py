# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.loader import ItemLoader
import csv

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem


class DiarioDoCentroDoMundoSpider(scrapy.Spider):
    name = 'diario_do_centro_do_mundo'
    allowed_domains = ['diariodocentrodomundo.com.br']
    start_urls = []
    

    def __init__(self, *a, **kw):
        super(DiarioDoCentroDoMundoSpider, self).__init__(*a, **kw)
        with open('seeds/diario_do_centro_do_mundo.json') as json_file:
                data = json.load(json_file)
        self.start_urls = list(data.values())

    def parse(self, response):
        links = response.xpath('//a/@href').getall()
        for link in links:
            if(link != '#' and link != "/"):
                print('Scrapping: ')
                print(link)
                yield scrapy.Request(link, self.parseNoticia)
            
  
    # Funcao que recebe pagina de noticia e extrai as informacoes necessarias
    def parseNoticia(self, response):
        if(self.permitsCrawl(response.url)):
            links = response.xpath('//a/@href').getall() # Links que ja estao 'dentro' da pagina de noticias:
            titulo_noticia = response.xpath('//h1/text()').get()
            with open('frontier/diariodocentrodomundo.json', 'r') as frontier:
                frontier_data = json.load(frontier) # Pega para gerar o id da noticia -> Ordem em que foi add no frontier
            noticia_loader = ItemLoader(item=RiLab01Item(), response=response)
            noticia_loader.add_value('_id', len(frontier_data) + 1)
            noticia_loader.add_xpath('title', '//h1/text()')
            noticia_loader.add_value('sub_title', 'Noticias não tem subtitle no Diario do Centro do Mundo')
            noticia_loader.add_xpath('author', '//div[@class="td-post-author-name"]/a/text()')
            date = response.xpath('//time/@datetime').get()
            noticia_loader.add_value('date', date)
            noticia_loader.add_value('section', 'Not specified on page!')
            noticia_loader.add_xpath('text', '//div[@class="td-post-content td-pb-padding-side"]/p/text()')
            noticia_loader.add_value('url', response.url)
            item = noticia_loader.load_item()

            yield item

            with open('frontier/diariodocentrodomundo.json', 'r') as frontier:
                frontier_data = json.load(frontier)
            frontier_data[titulo_noticia] = response.url
            with open('frontier/diariodocentrodomundo.json', 'w') as frontier:
                json.dump(frontier_data, frontier)

            for link in links:
                if(self.permitsCrawl(link)): 
                    yield scrapy.Request(link, self.parseNoticia)

    # Funcao que verifica se uma url ja nao foi acessada anteriormente, verificando no frontier, etc...
    def permitsCrawl(self, url):
        blacklist = ['sobre', 'tag', 'author', 'midia', '', 'especiais-dcm']
        url_components = url.split('/')
        if(len(url_components) >= 4 and url_components[2] == 'www.diariodocentrodomundo.com.br' and (url_components[3] not in blacklist)):
            with open('frontier/diariodocentrodomundo.json', 'r') as f:
                frontier_data = json.load(f)
                if(len(frontier_data) < 250):  #Impoe um limit de urls para o crawling buscar - Optional 
                    for key, value in frontier_data.items():
                        if(value == url):
                            return False
                    return True
                else:
                    print("Limite de noticias atingido: %d" % (len(frontier_data)))
                    
                    return False
        return False

    




#Run on command line:
# scrapy crawl diario_do_centro_do_mundo -o output/results.csv	