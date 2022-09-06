from requests_oauthlib import OAuth1Session
import json
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import MeCab
import re
from os import environ
from dotenv import load_dotenv
from flask import Flask
from markupsafe import escape


load_dotenv()
CK = environ['CK']  # API Key
CS = environ['CS']  # API Key Secret
AT = environ['AT']  # Access token
ATS = environ['ATS']  # Access Secret
twitter = OAuth1Session(CK, CS, AT, ATS)  # 認証処理


def get_related_texts(keyword):
    url = 'https://api.twitter.com/1.1/search/tweets.json'
    params = {'q': keyword, 'count': 100}
    re = twitter.get(url, params=params)
    if re.status_code != 200:
        return ''

    re_json = json.loads(re.text)
    ret = ''
    for tweet in re_json['statuses']:
        ret += tweet['text']
    return ret


def generate_word_cloud_from(text):
    fpath = "../Noto_Sans_JP/NotoSansJP-Light.otf"
    wordcloud = WordCloud(width=800, height=800,
                          background_color='white',
                          font_path=fpath,
                          stopwords=STOPWORDS,
                          min_font_size=10).generate(text)
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis('off')

    plt.show()


def filter_wakati(text):
    tagger = MeCab.Tagger('-Owakati')
    return tagger.parse(text)


def generate_twitter_wordcloud(keyword):
    text = get_related_texts(keyword)
    filtered_text = filter_wakati(text)
    generate_word_cloud_from(filtered_text)


def filter_wakati_limited_class(text):
    selected_conditions = ['名詞', '動詞', '形容詞', '形容動詞', '副詞']
    tagger = MeCab.Tagger('')

    text = text.replace(' ', '')
    text = text.replace('\n', '')
    text = text.replace('\u2028', '')

    node = tagger.parseToNode(text)
    terms = []

    while node:
        term = node.surface
        pos = node.feature.split(',')[0]

        if pos in selected_conditions:
            terms.append(term)

        node = node.next

    text_result = ' '.join(terms)
    return text_result


def generate_twitter_wordcloud(keyword):
    text = get_related_texts(keyword)
    filtered_text = filter_wakati_limited_class(text)
    generate_word_cloud_from(filtered_text)


def filtered_unimport_words(text, keyword):
    ban_words = ['https', 't', 't co', 'co', 'RT', keyword]

    # ひらがなのみの文字列にマッチする正規表現
    kana_re = re.compile("^[ぁ-ゖ]+$")

    src = text.split(' ')
    src = [t for t in src if not kana_re.match(t)]
    src = [t for t in src if t not in ban_words]
    dest = ' '.join(src)
    return dest


def generate_twitter_wordcloud(keyword):
    text = get_related_texts(keyword)
    filtered_text = filtered_unimport_words(filter_wakati_limited_class(text))
    generate_word_cloud_from(filtered_text)


def generate_word_cloud_html_from(text, width=800, height=800):
    fpath = "./ipaexg00401/ipaexg.ttf"

    wc = WordCloud(
        width=width,
        height=height,
        background_color='white',
        font_path=fpath,
        stopwords=STOPWORDS,
        min_font_size=10).generate(text)

    return wc.to_svg()


def generate_twitter_wordcloud(keyword):
    text = get_related_texts(keyword)
    wakati_text = filter_wakati_limited_class(text)
    filtered_text = filtered_unimport_words(wakati_text, keyword)
    svg = generate_word_cloud_html_from(filtered_text)

    link_script = '''
    <script>
        svg = document.getElementsByTagName("svg")[0];
        text_tags =  svg.getElementsByTagName("text")
        for(var i=0; i<text_tags.length; i++){
            text_tags[i].addEventListener(
                "click",
                function(){
                    word = this.textContent;
                    word_uri = encodeURI(word);
                    url = "https://twitter.com/search?q="''' + f' +encodeURI("{keyword}") + " " ' + ''' + word_uri ;
                    window.open(url, "_blank");
                }
            )
        }
    </script>'''

    res_html = "<!DOCTYPE HTML>\n"
    res_html += svg
    res_html += link_script

    return res_html


app = Flask(__name__)


@app.route("/<keyword>")
def generate_wordcloud_page(keyword):
    res = generate_twitter_wordcloud(escape(keyword))
    return res
