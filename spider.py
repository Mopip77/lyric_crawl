#!/usr/bin/env python3
import requests
import json
import re
import os
import sys

from getch import _Getch
import font_color as FC

getch = _Getch()

tmp_file = "/tmp/lyric.tmp"
url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&remoteplace=txt.yqq.lyric&searchid=101537613984919113&aggr=0&catZhida=1&lossless=0&sem=1&t=7&p={}&n=7&w={}&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0'
cur_page = 1
total_page = 0

def get_lyrics(song_name, page=1, auto_select_first=False):
    os.system("clear")
    cur_page = page
    r = requests.get(url.format(page, song_name))
    doc = json.loads(r.text)

    if doc['data']['lyric']['curnum'] <= 0:
        return
    elif auto_select_first:
        save_lyric(doc['data']['lyric']['list'][0]['content'])
        return

    total_page = int((doc['data']['lyric']['totalnum'] + 6) / 7)
    print(FC.w(str(cur_page)+" of "+str(total_page)+"页", 'c'))

    song_infos = doc['data']['lyric']['list']
    cur_page_lyric_num = len(song_infos)
    for idx, song_info in enumerate(song_infos):
        # like <em>身骑白马</em> - 徐佳莹 (LALA Xu)\n 词：徐佳莹\n 曲：徐佳莹/苏通达\n
        # 就是关键词会使用em标签, 然后歌曲名和演唱者用 - 相连
        try:
            title = song_info['lyric'].split('\\n')[0]
            title = title.replace('<em>', '').replace('</em>', '')
            name = re.findall('^(\w+) ', title)[0]
            singer = re.findall('.*?- (.*?)$', title)[0]
            print(FC.g("[{}]".format(idx+1)), name, FC.c(singer))
        except:
            print(FC.g("[{}]".format(idx+1)), title, "[DEBUG]")

    navigator = ""
    if cur_page != 1:
        navigator += FC.y("[9] 上一页  ")
    if cur_page < total_page:
        navigator += FC.y("[0] 下一页")
    print("\n" + navigator)

    i = int(getch())
    if 1 <= i <= cur_page_lyric_num:
        save_lyric(song_infos[i-1]['content'])
    elif i == 9:
        get_lyrics(song_name, cur_page-1)
    elif i == 0:
        get_lyrics(song_name, cur_page+1)

def save_lyric(lyric):
    os.system("clear")
    lyric = lyric.replace('<em>', '').replace('</em>', '')
    lines = lyric.split('\\n')
    with open(tmp_file, "w") as f:
        f.write('\n'.join(lines))


if __name__ == '__main__':
    if sys.argv.__len__() > 2 and sys.argv[2] == '-f':
        get_lyrics(sys.argv[1], auto_select_first=True)
    else:
        get_lyrics(sys.argv[1], auto_select_first=False)