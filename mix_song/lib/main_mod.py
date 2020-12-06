import random
from urllib import request
from bs4 import BeautifulSoup
from mix_song.models import Artists

class MainMod:
  def __init__(self, name):
    self.name = name
    self.ret_map = {}

  def get_song(self, prm_artist, prm_title):
    try:
      i = -1 #ループ用変数兼ページNo
      artist_link = ""

      #アーティスト名からページNo取得
      record = Artists.objects.filter(artist=prm_artist).order_by('id')
      if 0 < len(record):
        #アーティスト名がDBと完全一致した場合
        i = record[0].page_index
        print("完全一致/ページNo:" + str(i))
      else:
        #完全一致しなかった場合、部分一致検索実施。ランダム検索の場合もココに入る
        record = Artists.objects.filter(artist__icontains=prm_artist).order_by('id')
        if 0 < len(record):
          #ここで取得した値をMAXとしてランダムインデックスを生成
          random_redord_idx = random.randint(0, len(record) - 1)
          #アーティスト名とページNo取得
          prm_artist = record[random_redord_idx].artist
          i = record[random_redord_idx].page_index
          print("部分一致/ページNo:" + str(i))

      while -1 < i and i < 45:
        # 対象URLのHTMLソース取得
        html = request.urlopen("https://www.uta-net.com/name_list/" + str(i) + "/")
        soup = BeautifulSoup(html, "html.parser")

        #ページ全体からアーティスト一覧取得
        artist_list = soup.find_all("p", class_="name")

        #アーティスト一覧でループ
        for artist_info in artist_list:
          #アーティスト名抽出
          artist_name = artist_info.get_text()
          #返却用マップにアーティスト名格納
          self.ret_map["artist"] = artist_name

          if prm_artist.strip() == artist_name.strip():
            #入力されたアーティストと名前が一致した場合
            wk_link = artist_info.find('a')
            artist_link = wk_link.get('href')
            #ループを抜ける
            break

        #該当アーティストが見つかった場合、ループを抜ける
        if artist_link != "":
          break
        i += 1  # i に1を足す

      #フラグが立っていない場合、処理終了
      if artist_link == "":
        return ""

      #アーティスト情報のリンクURL抽出
      artist_html = request.urlopen("https://www.uta-net.com" + artist_link)
      artist_soup = BeautifulSoup(artist_html, "html.parser")

      #曲リスト取得
      song_list = artist_soup.find_all("td", class_="side td1")
      song_row = ''
      if prm_title != "":
        # 曲名から曲情報取得
        for wk_song in song_list:
          if prm_title == wk_song.get_text():
            #タイトルが見つかった場合、ループを抜ける
            song_row = wk_song
            break

      if prm_title == '' or song_row == '':
        #タイトルパラメーターが存在しないor合致するタイトルが見つからなかった場合、ランダムに曲取得
        target_index = random.randint(0, len(song_list)-1)
        song_row = song_list[target_index]

      #曲名取得
      title = song_row.get_text()
      # 返却用マップに曲名格納
      self.ret_map["title"] = title

      #該当曲URL取得
      wk_song_link = song_row.find('a')
      song_link = wk_song_link.get('href')

      song_info_map = self.get_song_info("https://www.uta-net.com" + song_link)

      #返却用配列作成
      self.ret_map["lyricist"] = song_info_map["lyricist"]
      self.ret_map["composer"] = song_info_map["composer"]
      self.ret_map["lyrics"] = song_info_map["lyrics"]

      #曲情報出力
      print('-------------------------')
      print("アーティスト:" + self.ret_map["artist"])
      print("曲名:" + self.ret_map["title"])
      print("作詞:" + self.ret_map["lyricist"])
      print("作曲:" + self.ret_map["composer"])
      print('-------------------------')

      #該当曲のページへ
      return self.ret_map

    except:
      print('-------------------------')
      print('エラーが発生しました')
      print('-------------------------')
      return ""

  #曲情報取得メソッド
  def get_song_info(self, url):

    #対象URLのHTMLソース取得
    html = request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")

    # 作詞作曲者抽出
    lyricist = soup.find("h4", itemprop="lyricist").get_text()
    composer = soup.find("h4", itemprop="composer").get_text()

    #歌詞部分抽出
    wk_lyrics = str(soup.select('#kashi_area')[0])
    #不要タグ削除
    wk_lyrics = wk_lyrics.replace('<div id="kashi_area" itemprop="text">', "")
    wk_lyrics = wk_lyrics.replace('</br>', "")
    wk_lyrics = wk_lyrics.replace('</div>', "")

    #配列化
    wk_lyrics_arr = wk_lyrics.split('<br/>')

    lyrics_arr = []
    # 返却用配列に文字列を加える
    for lyric in wk_lyrics_arr:
      if '<br>' in lyric:
        wk_lyrics_arr2 = lyric.split('<br>')
        for lyric2 in wk_lyrics_arr2:
          lyrics_arr.append(lyric2)
      else:
        lyrics_arr.append(lyric)

    #曲情報を配列に格納
    ret_map = {"lyricist":lyricist,"composer":composer,"lyrics":lyrics_arr}

    return ret_map