from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import requests
import urllib
import time
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager, rc
from tqdm.notebook import tqdm
import nltk
from konlpy.tag import Okt; t = Okt()
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image


class NaverWordCloud:

    def __init__(self, keyword, page):
        self.keyword = keyword
        self.page = page
        self.links = []
        self.present_candi_text = []
        self.html = 'http://kin.naver.com/search/list.nhn?query={key_word}&page={num}'
        
    def crawling(self):
        for n in tqdm(range(1,self.page+1)):
            req = Request(self.html.format(num=n, 
                                      key_word=urllib.parse.quote(self.keyword)));
            req.add_header('Referer', 'http://www.naver.com/')

            response = urlopen(req)
            soup = BeautifulSoup(response, 'html.parser')

            self.links.extend(soup.find_all('dt'))
            
        for each_link in tqdm(self.links):
            r = requests.get(each_link.a['href'])
            soup_tmp = BeautifulSoup(r.text, 'html.parser')

            search_result = soup_tmp.find_all('div','_endContentsText')

            time.sleep(0.5)

            for each in search_result:
                self.present_candi_text.append(each.get_text())
        
        return self.present_candi_text

    def preprocessing(self):    
        present_text = " ".join(self.present_candi_text)
        tokens_ko = t.nouns(present_text)

        stop_words = ['한','수','은','들','!','도','이','\u200b','을','에',',','.','[',']','~',
                      '는','것','요','제','수','것','뼘','제','요','해','분','때문','더','줄']

        tokens_ko = [each_word for each_word in tokens_ko if each_word not in stop_words]

        self.ko = nltk.Text(tokens_ko, name=self.keyword)
        
    def wordcloud(self):
        f_path = "C:\Windows\Fonts\Malgun.ttf"
        font_name = font_manager.FontProperties(fname=f_path).get_name()
        rc('font', family=font_name)
        plt.rcParams['axes.unicode_minus'] = False

        data = self.ko.vocab().most_common(200)
        mask = np.array(Image.open('heart.jpg'))
        image_colors = ImageColorGenerator(mask)
        wordcloud = WordCloud(font_path=f_path,
                             relative_scaling=0.1,
                              mask=mask,
                             background_color='white',
                             min_font_size=1, max_font_size=100).generate_from_frequencies(dict(data))

        default_colors = wordcloud.to_array()
        plt.figure(figsize=(12,12))
        plt.imshow(wordcloud.recolor(color_func=image_colors),
                  interpolation='bilinear')
        plt.axis('off')
        plt.savefig('word_cloud.png', dpi=300)
        plt.show()
        
if __name__ == "__main__":
    naver = NaverWordCloud("크리스마스 선물", 1)
    naver.crawling()
    naver.preprocessing()
    naver.wordcloud()