#!/usr/bin/env sh
# 搜索歌词app
# 查找qq音乐的曲库
# 接受一个或者没有参数, 一个则是歌曲名

# 没有参数默认读取正在播放的音乐app rhthymbox > audacious

if [ $# -eq 0 ]
then
  # rhthymbox
  song_name=$(rhythmbox-client --no-start --print-playing)
  if [ -z "$song_name" ]
  then
    # audacious
    song_name=$(audtool current-song)
    if [ -z "$song_name" ]
    then
      echo "当前没有正在播放的Rhthymbox或Audacious"
      exit
    fi
  fi
else
  song_name=$1
fi

curPath=$(cd `dirname $0`; pwd)
if [ -L "$0" ]
then
	curPath=$(cd `dirname $(ls -l "$0" | awk '{print $NF}')`; pwd)
fi
${curPath}/spider.py "$song_name"
if [ $? -eq 0 ]
then
  less "/tmp/lyric.tmp"
fi