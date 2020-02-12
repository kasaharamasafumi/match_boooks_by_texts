import json # json解析モジュールのインポート
from ibm_watson import PersonalityInsightsV3 # PersonalityInsights
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from os.path import join, dirname

import json
from requests_oauthlib import OAuth1Session
from twitter import Twitter, OAuth
from janome.tokenizer import Tokenizer
import collections
import re
from collections import Counter, defaultdict
import sys, json, time, calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json
from watson_developer_cloud import PersonalityInsightsV3
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN
from collections import OrderedDict
import pprint
import itertools
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from os.path import join, dirname
from ibm_watson import PersonalityInsightsV3
import random

def analyze_personality():
  #------------------------------入力----------------------------------
  authenticator = IAMAuthenticator('tt0Ul73SdE0aOXsfeeAV55XHrBASyZs1ukRIZD3WWdYn') #APIkeyを入力
  #---------------------------------------------------------------------

  service = PersonalityInsightsV3(
      version='2018-10-30',
      authenticator= authenticator)
  #------------------------------入力----------------------------------
  service.set_service_url('https://api.jp-tok.personality-insights.watson.cloud.ibm.com/instances/591407d0-781f-49cf-a85e-2315151d4f61') #URLを入力
  #--------------------------------------------------------------------
  # 性格を分析
  with open('C:/Users/Masafumi/PycharmProjects/kasahara/meros.txt', 'r',encoding="utf-8") as profile_text:  #解析したいtxtファイルを絶対パスで指定
      profile = service.profile(
          profile_text.read(),
          content_type="text/plain",
          accept='application/json',
          content_language='ja',
          accept_language='ja').get_result()

      return profile



def sort_personality(tweet_result):
    return sorted(tweet_result.items(), key=lambda x: x[1], reverse=True)

def main(my_user_name):
    user_personality_dict = OrderedDict()
    tweet_personality_dict = analyze_personality()  # ツイートを結合したデータをAPIに入力


    # ツイートから分析した性格の名前
    personality_name = [big5["name"] for big5 in tweet_personality_dict["personality"]]
    # 性格の値。小数点第2位で四捨五入した後、decimal.Decimalからfloatに変換している。
    # 参考サイト(四捨五入)：https://note.nkmk.me/python-round-dec\imal-quantize/
    personality_percentile = [float(Decimal(str(big5["percentile"])).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)) \
                              for big5 in tweet_personality_dict["personality"]]

    # ユーザのツイートの分析結果
    all_tweets_big5 = OrderedDict(zip(personality_name, personality_percentile))

    # { my_user_id: { personality_name1: percentile1, personality2: percentile2, ... } }
    user_personality_dict[my_user_name] = all_tweets_big5
    # print("finished analyzing all({}) tweets.".format(len(tweets)))

    # Agreeableness: 協調性, Conscientiousness: 真面目さ, Emotional range: 精神的安定性, Extraversion: 外向性, Openness: 開放性
    # 参考サイト：https://note.nkmk.me/python-math-factorial-permutations-combinations/
    big5_list = ["Agreeableness", "Conscientiousness", "Emotional range", "Extraversion", "Openness"]

    # big5から2つの性格を選ぶ組み合わせを列挙する
    category_patterns = [set(pat) for pat in itertools.combinations(big5_list, 2)]

    # ユーザのツイートのカテゴリ分けを記録する辞書
    user_tweet_category_table = OrderedDict()

    # ユーザのツイートの分析結果を、値の大きい順にソートする
    sorted_result = sort_personality(user_personality_dict[my_user_name])

    # big5のうち大きい順から2番目までの値の性格名のみを取得し、その本のカテゴリとする(例：{Openness, Extraversion})
    # この時、複数の性格の順番を考慮させないために、setで用意する
    # 2つを組み合わせているため、1つだけの場合よりも幅広くカテゴリ分けできそう
    tweet_category = {big5_elm[0] for big5_elm in sorted_result[0:2]}
    user_tweet_category_table[my_user_name] = tweet_category

    user_personality = user_tweet_category_table[my_user_name]

    suggest_book = ""
    img_path = "./static/images/nothing.jpg"  # templates/index.htmlを基準にしたパス
    if user_personality == {'Openness', 'Extraversion'}:
        candidates = ['chumonno_oi_ryoriten', 'hashire_merosu']
        suggest_book = random.choice(candidates)
        img_path = "./static/images/" + suggest_book + ".jpg"
    elif user_personality == {'Openness', 'Emotional range'}:
        suggest_book = 'bocchan'
        img_path = "./static/images/" + suggest_book + ".jpg"
    elif user_personality == {'Openness', 'Agreeableness'}:
        candidates = ['kaijin_nijumenso', 'ningen_shikkaku']
        suggest_book = random.choice(candidates)
        img_path = "./static/images/" + suggest_book + ".jpg"
    else:
        suggest_book = "not found a suggested book..."

    return suggest_book, img_path