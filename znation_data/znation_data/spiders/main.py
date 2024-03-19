from pathlib import Path

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        url = "https://en.wikipedia.org/wiki/List_of_sovereign_states"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        tabledata=response.css("table.wikitable").css("tr")
        counter=0
        for x in tabledata:
            if len(x.css("td"))==0:
                continue
            tempStatus=''
            if len(x.css("td"))>3:
                for y in x.css("td")[3].css("::text"):
                    tempStatus+=y.get()
            tempMembershipWithinUN=''
            if len(x.css("td"))>1:
                for y in x.css("td")[1].css("td::text"):
                    tempMembershipWithinUN+=y.get()
            tempSovereigntyDispute=''
            if len(x.css("td"))>2:
                for y in x.css("td")[2].css("td::text"):
                    tempSovereigntyDispute+=y.get()
            imgUrl=''
            if x.css("td")[0].css("img::attr(src)").get() is not None:
                imgUrl='https:'+ x.css("td")[0].css("img::attr(src)").get()
            url="https://en.wikipedia.org"+ x.css("td")[0].css("a::attr(href)").get()
            yield {
                "id": counter,
                "name": x.css("td")[0].css("b::text").get(),
                "imgUrl": imgUrl,
                "url": url,
                "membershipWithinUN": tempMembershipWithinUN,
                "sovereigntyDispute": tempSovereigntyDispute,
                "status": tempStatus,
                #response.css("table.wikitable").css("tr")[1].css("td::text")[2].get()
            }
            counter+=1