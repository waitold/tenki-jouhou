from datetime import datetime
from datetime import timedelta
import tweepy
import os
import config
import kakasi
import weather
import img_edit

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
WK = config.WEATHER_KEY
auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, ATS)
api = tweepy.API(auth)
WEATHER = {"clear sky": "めっちゃ晴れ", "few clouds": "ちょい雲ある", "scattered clouds": "まぁくもり",
           "broken clouds": "だいぶ曇ってる", "overcast clouds": "曇ってる", "shower rain": "くそ雨降ってる",
           "rain": "まぁふつうの雨", "thunderstorm": "荒れすぎてヤバイ", "snow": "珍しく雪", "mist": "霧かかってる"}
# やった　メンションされたらリプで天気（場所は後で）をリプする
#       　メンションされた地名をローマ字変換しその場所の天気を返す
#         最低、最高気温取得
#         次の日の天気予報ツイート
# やる　 日時の指定　例　明日の千葉＝＞　明日の千葉の天候をリプライ（画像付きで出来たら神）
# やりたい 　フォロバ機能　


def get_mention():  # 前回取得したツイートIDより後のメンション取ってIDリスト返してそのIDはどっか保存しとく
    if not os.path.exists("log/config.txt"):  # ファイルがないとき
        with open("log/config.txt", 'w'):
            pass
    with open("log/config.txt", 'r') as f:
        last_id = f.read()
    id_list = []
    if last_id == "":  # 初期状態でファイルに何も書かれていないとき
        mention = api.mentions_timeline()
        id_list.append(mention[0].id)
        with open("log/config.txt", 'w')as f:
            f.write(str(id_list[0]))
    else:
        mention = api.mentions_timeline(since_id=last_id)
        if len(mention) == 0:
            return []
        for status in mention:
            id_list.append(status.id)
        with open("log/config.txt", 'w')as f:
            f.write(str(id_list[0]))
    return id_list


def get_timeline():
    public_tweet = api.home_timeline()
    for tweet in public_tweet:
        print(tweet)


def reply_weather():  # メンション送られたツイートに天気情報をリプする
    id_list = get_mention()  # メンションされたツイートのidを取得
    if len(id_list) == 0:  # 前回からメンションされてないとき用
        return 0
    for status_id in id_list:
        tweet = api.get_status(id=status_id)
        user_id = tweet.user.screen_name
        text = tweet.text
        city_kanji = text.split()[1]
        city_name = kakasi.to_english(city_kanji)
        if weather.confirm_exists_city(city_name) == "404":
            reply_text = "@"+user_id+"ちょっとわからないですね…"
            api.update_status(status=reply_text, in_reply_to_status_id=status_id)
            with open("log/errorlog.txt", 'w') as file:
                file.write(status_id+text)
        else:
            info = weather.get_current_weather(city_name)
            reply_text = "@"+user_id+"今の"+city_kanji+info[0]+"らしいっすよ\n"\
                         + "最高気温： "+str(info[1])+"\n最低気温: "+str(info[2])
            api.update_status(status=reply_text, in_reply_to_status_id=status_id)


def tweet_word(word):
    api.update_status(word)


def tweet_forecast():
    img_edit.create_forecast_img()
    img_edit.write_text()
    temp = weather.get_days_forecast("chiba")
    date = (datetime.now() + timedelta(days=1))
    text = "明日"+str(date.month)+"/"+str(date.day)+"の千葉の天気"+"\n予想最高気温:"+str(temp[-2]) + \
           "\n予想最低気温:"+str(temp[-1])
    img = "img/today_weather.png"
    api.update_with_media(filename=img, status=text)


if __name__ == '__main__':
    with open("log/activatelog.txt", 'w') as f:
        f.write("activate"+datetime.now().strftime("%m/%d %H:%M:%S"))
    reply_weather()
    time = datetime.now()
    print(type(weather.confirm_exists_city("asakusa")))
    if time.hour == 22 and time.minute == 0:
        tweet_forecast()
    elif time.hour == 8 and time.minute == 0:
        api.update_with_media(filename="img/today_weather.png", status="今日"+time.strftime("%m/%d")+"の千葉の天気")
