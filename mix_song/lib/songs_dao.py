from urllib import request
from bs4 import BeautifulSoup
from mix_song.models import Songs

class SongsDao:
  def __init__(self, name):
    self.name = name

  def insert_song(self, insert_type):

    i = 0
    i2 = 1
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
        artist = artist_info.get_text()
        print("アーティスト名:" + artist)

        #アーティスト情報のリンクURL抽出
        wk_link = artist_info.find('a')
        link = "https://www.uta-net.com" + wk_link.get('href')

        #アーティスト情報のHTMLソース取得
        artist_html = request.urlopen(link)
        artist_soup = BeautifulSoup(artist_html, "html.parser")

        #曲リスト取得
        song_list = artist_soup.find_all("td", class_="side td1")

        #曲一覧でループ
        for song_info in song_list:
          #曲名取得
          title = song_info.get_text()

          #曲情報のリンクURL抽出
          wk_song_link = song_info.find('a')
          song_link = "https://www.uta-net.com" + wk_song_link.get('href')

          # 対象URLのHTMLソース取得
          song_html = request.urlopen(song_link)
          song_soup = BeautifulSoup(song_html, "html.parser")

          #歌詞抽出
          wk_lyrics = str(song_soup.select('#kashi_area')[0])
          #不要タグ削除
          wk_lyrics = wk_lyrics.replace('<div id="kashi_area" itemprop="text">', "")
          wk_lyrics = wk_lyrics.replace('</br>', "")
          lyrics = wk_lyrics.replace('</div>', "")

          # 作詞家抽出
          if song_soup.find("h4", itemprop="lyricist") != None:
            lyricist = song_soup.find("h4", itemprop="lyricist").get_text()
          else:
            lyricist = ''

          # 作曲家抽出
          if song_soup.find("h4", itemprop="composer") != None:
            composer = song_soup.find("h4", itemprop="composer").get_text()
          else:
            composer = ''

          # DB更新用にモデル作成
          model = Songs()
          model.artist = artist
          model.lyricist = lyricist
          model.composer = composer
          model.title = title
          model.lyrics = lyrics
          # モデル更新
          model.save()

          print("DB更新件数:" + str(i2))
          i2 += 1

      #ループカウント増加
      i += 1