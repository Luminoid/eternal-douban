# Eternal Douban
一个针对豆瓣用户喜好记录的爬虫。保存用户的读书、电影、电视剧、音乐喜好以及相应作者、影人和音乐人信息。

## Features
1. 用户可以将喜好记录本地保存
2. 已标记的条目不会由于豆瓣网站原因消失
3. 更方便的条目查看

## Usages
将用户豆瓣 id 当作参数，传入 scheduler/scheduler.py 的 main 函数中的 scrape() 即可。

## Details
### Book
- 作者部分可能有以下两种代码结构
```
<span class="pl">作者:</span>
```
```
<span class="pl"> 作者</span>
": "
```
- 作者和译者可能有多个
- 内容简介、作者简介和目录部分可能有展开全部按钮，但无需操作js，缩略和详细简介都可以在html中找到
- 目录部分代码结构不统一，需要按换行符 `\n` 重新组织文本

### Movie
- 国外电影的标题包含中文标题和原标题
- 条目的展开全部以 `<span style="display: none;">` 的方式实现
- value1 / value2 / ... 形式的列表有三种实现方式
    1. 如导演信息：封装在 `<span class="attrs">` 中
    2. 如类型信息：以同级的一或多个 `<span property="v:genre">` 展示
    3. 如语言信息：已经直接按照 ` / ` 划分好的字符串

### Music
- 部分条目名没有用 `<span>` 标签包装，直接以 String 的形式显示
- 曲目内容可能分别用 `<div>` 标签包转，也可能直接以 String 的形式显示，需要格式化换行符 `re.sub(r'\s*?\n+\s*', '\n', track_list)`
