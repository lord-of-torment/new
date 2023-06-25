import scrapy


class GovermentSpider(scrapy.Spider):
    name = "goverment"
    allowed_domains = ["www.gd.gov.cn"]


    def start_requests(self):
        date_str = input('输入日期范围形如20230101-20230301:')
        date_list1 = date_str.split('-')
        date_list1 = [int(i) for i in date_list1]
        self.date_list=date_list1
        start_url = "https://www.gd.gov.cn/gkmlpt/policy"
        self.tmp=1
        yield scrapy.Request(start_url, self.parse,dont_filter=True, meta={'date_list':self.date_list,
            'tmp':self.tmp,
        })
    def parse(self, response):
        tr_list=response.css('tbody tr')
        print('parseparseparseparseparseparseparse')
        for tr_one in tr_list:
            print('tr_onetr_onetr_onetr_onetr_one')
            date1=tr_one.css('td::text').extract()[2]
            date1=int(date1.replace('-',''))
            print(date1)
            if date1 in range(self.date_list[0],self.date_list[1]+1):
                detail_url=tr_list.css('.first-td a::attr(href)').extract_first()
                print('movie_urlmovie_urlmovie_urlmovie_url',"https:"+detail_url)
                yield scrapy.Request("https:"+detail_url, callback=self.movie_detail_page,
                                     dont_filter=True)
        start_url = 'https://www.gd.gov.cn/gkmlpt/policy'
        self.tmp += 1
        if self.tmp < 237:
            yield scrapy.Request(start_url, self.parse, dont_filter=True, meta={
                'tmp': self.tmp,
            })
    def movie_detail_page(self, response):
        try:
            final_dict={}
            detail_head=response.css('tbody tr')
            indexhao=detail_head[0].css('.td-value-xl span::text').extract()
            publish_gov=detail_head[1].css('.td-value-xl span::text').extract()
            done_time=detail_head[1].css('.td-value span::text').extract()
            title=detail_head[2].css('.td-value span::text').extract()

            detail_content=response.css('.article-content p::text').extract()
            addlink=response.css('.nfw-cms-attachment::attr(href)').extract()
            final_dict['indexhao']=indexhao
            final_dict['publish_gov']=publish_gov
            final_dict['done_time']=done_time
            final_dict['title']=title
            final_dict['addlink']=addlink
            final_dict['detail_content']=detail_content
            yield final_dict
        except Exception as e:
            print(e)

