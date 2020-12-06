from django.views import generic
from django.http import JsonResponse
from .lib.main_mod import MainMod
from .lib.evaluate_mod import EvaluateMod
from django.shortcuts import redirect, render

import random
import math
import difflib

class IndexView(generic.TemplateView):
    template_name = "index.html"
    evaluate_mod = EvaluateMod('main')

    def get(self, request):
        if not 'login' in self.request.session:
            response = redirect('/login/')
            return response
        template_name = "index.html"
        return render(request, template_name)

    def check_login(request):
        #ログインセッション確認
        if 'login' in request.session:
            return "0"
        return "1"

    def ajax_get_lyrics(request):
        print('----BEGIN----------------')

        #画面で入力された文字列の取得
        input_artist = request.POST.get('input_artist')
        input_title = request.POST.get('input_title')

        # アーティスト名から曲を探す
        main_mod1 = MainMod('main1')
        song1_info = main_mod1.get_song(input_artist, input_title)

        # ランダムに曲を探す
        main_mod2 = MainMod('main2')
        song2_info = main_mod2.get_song('', '')

        #入力した曲が見つからなかった場合
        if song1_info == "" or song2_info == "":
            d = {
            }
            return JsonResponse(d)

        # 歌詞の生成
        random_num = random.randint(1, 100)
        if random_num <= 50:
            disp_lyrics = IndexView.make_lyric_type1(song1_info["lyrics"], song2_info["lyrics"], random_num)
        elif(random_num <= 100):
            disp_lyrics = IndexView.make_lyric_type2(song1_info["lyrics"], song2_info["lyrics"])
        else:
            disp_lyrics = IndexView.make_lyric_type3(song1_info["lyrics"], song2_info["lyrics"])

        # 画面返却用Json作成
        d = {
            'artist1': song1_info["artist"],
            'title1': song1_info["title"],
            'lyricist1': song1_info["lyricist"],
            'composer1': song1_info["composer"],

            'artist2': song2_info["artist"],
            'title2': song2_info["title"],
            'lyricist2': song2_info["lyricist"],
            'composer2': song2_info["composer"],

            'lyrics': disp_lyrics,
        }
        return JsonResponse(d)


    def make_lyric_type1(lyric1, lyric2, random_num):
        # 2曲の行数を取得し、短い方をベース、長い方をアディショナルとする
        base_lyrics = lyric1
        wk_add_lyrics = lyric2
        if len(lyric2) < len(lyric1):
            wk_add_lyrics = lyric1
            base_lyrics = lyric2

        # パート毎に分割し、多次元配列作成
        wk_disp_lyrics = []
        i1 = 1  # ループ用カウント
        i2 = 0  # パート終了有無を判定するカウント
        for row in base_lyrics:
            if i2 < 1:
                # 新規パート開始時
                wk_disp_lyrics_inner = []
            if i1 == len(base_lyrics) or row == '':
                if i1 == len(base_lyrics):
                    # 最終行の場合
                    wk_disp_lyrics_inner.append(row)
                #引数のランダム数字により、シャッフルするか決める
                if 40 < random_num:
                    random.shuffle(wk_disp_lyrics_inner)
                wk_disp_lyrics.append(wk_disp_lyrics_inner)
                i2 = 0  # カウントリセット
            else:
                wk_disp_lyrics_inner.append(row)
                i2 += 1  # i に1を足す
            i1 += 1

        # アディショナルから、空白を削除した配列を生成
        # ここで作った配列から要素を抜き出し、ベースに入れる
        add_lyrics = []
        for row in wk_add_lyrics:
            if row != '':
                add_lyrics.append(row)

        # 画面表示用文字列作成
        disp_lyrics = ''
        # 作成した多次元配列でループ
        for arr in wk_disp_lyrics:
            i = 0
            for row in arr:
                i += 1
                if i % 2 == 0:
                    # 追加曲の1行で置き換え
                    '''
                    # ■■■ランダム BEGIN■■■
                    # 配列シャッフル
                    random.shuffle(add_lyrics)
                    # 配列先頭を歌詞に加える
                    # ■■■テストコメントアウト　BEGIN■■■
                    disp_lyrics = disp_lyrics + add_lyrics[0] + "<br/>"
                    # ■■■テストコメントアウト　END■■■
                    # 先頭の要素を削除
                    add_lyrics.pop(0)
                    # ■■■ランダム END■■■
                    '''
                    after_lyric = IndexView.get_lyric_by_elastic_earch(arr[i-2], add_lyrics)
                    disp_lyrics = disp_lyrics + after_lyric + "<br/>"

                else:
                    disp_lyrics = disp_lyrics + row + "<br/>"
            # 次の部分へ
            disp_lyrics = disp_lyrics + "<br/>"
        return disp_lyrics


    def make_lyric_type2(lyric1, lyric2):
        #空白を削除した配列作成
        except_space_lyric1 = [a for a in lyric1 if a != '']
        except_space_lyric2 = [b for b in lyric2 if b != '']

        # 2曲の行数を取得し、長い方をベース、短い方をアディショナルとする
        base_lyrics = lyric1
        wk_add_lyrics = except_space_lyric2
        if len(except_space_lyric1) < len(except_space_lyric2):
            wk_add_lyrics = except_space_lyric1
            base_lyrics = lyric2

        #ベースの中で、置き換え可能な行のインデックスを取得
        add_able_index_list = []
        for i in range(len(base_lyrics)):
            if i != 0 and base_lyrics[i - 1] != "" and base_lyrics[i] != "":
                add_able_index_list.append(i)

        #アディショナルの1/2を行をベースに入れる
        loop_max = math.floor(len(wk_add_lyrics) / 2)
        for i in range(loop_max):
            #ベースの置き換え対象行をランダムに取得
            wk_i = random.randint(0, len(add_able_index_list) - 1)
            before_target = base_lyrics[add_able_index_list[wk_i - 1]]

            after_lyric = IndexView.get_lyric_by_elastic_earch(before_target, wk_add_lyrics)

            #置き換え対象行に選ばれた要素は配列から削除
            base_lyrics[add_able_index_list[wk_i]] = after_lyric
            del add_able_index_list[wk_i]

        #作成した配列を文字列に変換
        disp_lyrics = ''
        for row in base_lyrics:
            if row == '':
                disp_lyrics = disp_lyrics + "<br/>"
            else:
                disp_lyrics = disp_lyrics + row + "<br/>"

        return disp_lyrics


    def make_lyric_type3(lyric1, lyric2):
        #ベースから1行だけ除く

        # ベースの中で、置き換え可能な行のインデックスを取得
        add_able_index_list = []
        for i in range(len(lyric1)):
            if i != 0 and lyric1[i - 1] != "" and lyric1[i] != "":
                add_able_index_list.append(i)

        #万一、置き換え可能な行がなかった場合、別ロジック実行
        if len(add_able_index_list) < 1:
            disp_lyrics = IndexView.make_lyric_type2(lyric1, lyric2)
            return disp_lyrics

        #ランダムで置き換え行取得
        random_row = random.choice(add_able_index_list)
        #置き換え行の1つ前の行取得
        before_target = lyric1[random_row - 1]

        after_lyric = IndexView.get_lyric_by_elastic_earch(before_target, lyric2)

        # 置き換え実行
        lyric1[random_row] = after_lyric

        # 作成した配列を文字列に変換
        disp_lyrics = ''
        for row in lyric1:
            if row == '':
                disp_lyrics = disp_lyrics + "<br/>"
            else:
                disp_lyrics = disp_lyrics + row + "<br/>"

        return disp_lyrics

    def get_lyric_by_elastic_earch(before_lyric, additional_lyrics):
        # elasticSearchを用いて、サンプルの一節を取得
        print("-------------------------")
        print("target:" + before_lyric)
        after_lyric_sample = IndexView.evaluate_mod.get_after_lyric(before_lyric)
        print("sample:" + after_lyric_sample)

        score = 0  # 一節同士を比較したスコア
        after_lyric = ''  # 画面に表示する一節

        # 追加曲の中から、サンプルの一節に最も近しい行を取得
        for lyrics_for_diff in additional_lyrics:
            score_diff = difflib.SequenceMatcher(None, after_lyric_sample, lyrics_for_diff).ratio()
            print("candidate:" + lyrics_for_diff)
            print("score:" + str(score_diff))
            print("----")
            if score < score_diff:
                # スコアと一節を更新
                score = score_diff
                after_lyric = lyrics_for_diff

        if after_lyric != '':
            # 採用した一節を削除
            additional_lyrics.remove(after_lyric)
        else:
            # サンプルと合致する一節がなかった場合、ランダムに一節を取得
            random_index = random.randint(0, len(additional_lyrics) - 1)
            after_lyric = additional_lyrics[random_index]
            # 採用した一節を削除
            additional_lyrics.pop(random_index)

        return after_lyric

class LoginView(generic.TemplateView):
    template_name = "login.html"

    def check_password(request):
        request.session['login'] = 'true'
        response = redirect('../login/')
        if request.POST.get('password') == 'Password1!':
            response = redirect('../')
        return response
