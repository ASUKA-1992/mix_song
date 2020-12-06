import datetime
import re
from urllib import request
from bs4 import BeautifulSoup

print('アルファベットを含む:0、含まない:1')
flg_alphabet = input('>> ')

#機械学習用ファイル作成
wk_now = datetime.datetime.now()
now = wk_now.strftime('%Y_%m_%d_%H_%M')
path = '../tmp/lyrics_' + now + '.txt'

with open(path, mode='w') as f:
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

        # 歌詞抽出
        wk_lyrics = str(song_soup.select('#kashi_area')[0])
        # 不要タグ削除
        wk_lyrics = wk_lyrics.replace('<div id="kashi_area" itemprop="text">', "")
        wk_lyrics = wk_lyrics.replace('</br>', "")
        lyrics = wk_lyrics.replace('</div>', "")

        #<br>または<br/>タグで分割して配列化する
        # 配列化
        wk_lyrics_arr = lyrics.split('<br/>')
        lyrics_arr = []
        # 返却用配列に文字列を加える
        for lyric in wk_lyrics_arr:
          if '<br>' in lyric:
            wk_lyrics_arr2 = lyric.split('<br>')
            for lyric2 in wk_lyrics_arr2:
              lyrics_arr.append(lyric2)
          else:
            lyrics_arr.append(lyric)

        #書き込み用配列作成
        write_lyrics_arr = []

        #機械学習用文字列作成
        i2 = 1
        for wk_lyric in lyrics_arr:
          if i2 == len(lyrics_arr):
            break
          if wk_lyric != '' and lyrics_arr[i2] != '':
            #アルファベット含むか確認
            if (bool(re.search(r'[a-zA-Z]', wk_lyric)) == False and bool(re.search(r'[a-zA-Z]', lyrics_arr[i2])) == False) \
                    or flg_alphabet == '0':
              print(wk_lyric + '\t' + lyrics_arr[i2])
              write_lyrics_arr.append(wk_lyric + '\t' + lyrics_arr[i2] + '\n')
          i2 += 1

        #書き込み用配列ソート
        if 0 < len(write_lyrics_arr):
          wk_write_lyrics_arr = set(write_lyrics_arr)
          for wk in wk_write_lyrics_arr:
            f.write(wk)

    #ループカウント増加
    i += 1

#ファイルクロ―ズ
f.close()