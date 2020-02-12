#必要なもージュールのインポート
import json # json解析モジュールのインポート
from ibm_watson import PersonalityInsightsV3 # PersonalityInsights
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from os.path import join, dirname


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
  with open('C:/Users/Masafumi/PycharmProjects/kasahara/lemon.txt', 'r',encoding="utf-8") as profile_text:  #解析したいtxtファイルを絶対パスで指定
      profile = service.profile(
          profile_text.read(),
          'application/json',
          content_language='ja',
          accept_language='ja').get_result()

      # ファイルに書き込み
      with open('C:/Users/Masafumi/PycharmProjects/kasahara/result.json', 'w',encoding="utf-8") as resultFile:
          json.dump(profile, resultFile, ensure_ascii=False, indent=2)

analyze_personality() #関数を実行