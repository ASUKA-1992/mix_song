from urllib import request
from bs4 import BeautifulSoup
from mix_song.models import Artists

class ArtistsDao:
  def __init__(self, name):
    self.name = name

  def insert_artist(self, insert_type):

    i = 0
    #あいうえお順にループ
    while i < 45:
      print("ループ:" + str(i) + "/46")
      # 対象URLのHTMLソース取得
      html = request.urlopen("https://www.uta-net.com/name_list/" + str(i) + "/")
      soup = BeautifulSoup(html, "html.parser")

      #ページ全体からアーティスト一覧取得
      artist_list = soup.find_all("p", class_="name")

      #アーティスト一覧でループ
      for artist_info in artist_list:
        #アーティスト名抽出
        artist = artist_info.get_text().rstrip()
        print("アーティスト名:" + artist)

        #既に該当アーティスト名がDBに登録されているか確認
        count = Artists.objects.filter(artist=artist).count()

        #既に登録されている場合、次のループへ
        if 0 < count:
          print("登録済/スキップ")
          continue

        # DB更新用にモデル作成
        model = Artists()
        model.artist = artist
        model.page_index = i
        # モデル更新
        model.save()
        print("登録完了")

      #ループカウント増加
      i += 1