# 技术报告

## 概要

本项目使用 Python 编写的轻量爬虫从维基百科（英文与中文站点）抓取文章文本样本，并对抓取得到的原始文本进行了基于规则的清洗以得到用于下游分析（例如熵/Zipf 分析）的语料。爬虫是单线程的、基于请求与解析的实现，支持会话恢复与重试机制。

------

## 使用的爬虫工具与库

-   语言：Python 3。
-   主要第三方库：
    -   `requests` — 发起 HTTP 请求、处理超时与异常。
    -   `BeautifulSoup` — HTML 解析与 DOM 提取。
-   主要标准库：argparse、time、re、urllib.parse、pathlib 等。
-   常量：USER_AGENT 在 constants.py 中定义，用于请求头（模拟常见浏览器 UA）。

------

## 爬虫脚本与入口

-   **快速开始**：
    -   中文爬虫：`bash scripts/zh_scrawler.sh`
    -   英文爬虫：`bash scripts/en_scrawler.sh`

-   **爬虫脚本**：wikipedia_crawler.py 为主爬虫脚本，接受参数 `--initial_url`、`--articles`（抓取数量上限）、`--interval`（请求间隔，秒）和 `--output`（输出目录）。
-   **爬虫入口**：
    -   英文维基百科：在 `scripts/en_scrawler.sh` 中使用 `--initial_url h ttps://en.wikipedia.org/wiki/Donald_Trump` 作为爬虫的开始页面。
    -   中文维基百科：在 `scripts/zh_scrawler.sh` 中使用 `--initial_url https://zh.wikipedia.org/wiki/唐纳·川普` 的 URL 编码形式 `https://zh.wikipedia.org/wiki/%E5%94%90%E7%B4%8D%C2%B7%E5%B7%9D%E6%99%AE` 作为爬虫的开始页面。

------

## 爬虫原理与数据清理

-   **抓取策略**：
    -   单线程**广度优先（BFS）**风格，使用列表作为队列 `pending_urls`，从初始文章开始，把页面中符合规则的 `/wiki/...` 链接加入队列并按顺序抓取，直到达到文章数上限或队列为空。
-   **链接过滤规则**：
    -   只接受以 `/wiki/` 开头的链接（排除非文章页）。
    -   忽略包含 `:` 的链接（例如 `Special:`、`File:` 等特殊命名空间）。
    -   忽略以图片后缀（`.png .jpg .jpeg .svg`）结尾的链接。
-   **会话与去重**：
    -   使用 `session_file` 记录已访问的完整 URL，脚本启动时尝试读取该文件以恢复会话。
    -   使用 `visited_urls` 集合缓存已访问 URL，避免重复抓取与重复写入输出文本。
-   **内容提取**：
    -   在返回页面中查找 `<div id="mw-content-text">`，并从该区域提取所有 `<p>` 标签文本（段落文本）。
    -   对每段进行简单正则去除括号内内容与引用标注后写入输出文件（每段之间以空行分隔）。
-   **稳健性**：
    -   支持重试机制：最多重试 10 次（包括请求异常和非预期状态码），失败时采取指数退避（backoff，最大 30s）。
    -   支持 `interval` 参数控制每次抓取前的睡眠时间（默认 5 秒），减少对目标站点压力。

>   [!note]
>
>   注意：直接对维基百科的中文界面爬虫会得到繁体中文，为了得到**简体中文**，需要在请求头增加字段 `"Accept-Language": "zh-CN,zh-Hans;q=0.9"`

------

## 爬虫输出

在本项目中，中文爬虫数据保存在 `data/zh` 文件夹下，英文爬虫数据保存在 `data/en` 文件夹下：
-   `text.txt ` — 原始抓取到的段落文本（按段落分行，段落之间空一行）。
-   `session.txt` — 已访问页面的完整 URL 列表，用于会话恢复。

------

## 实验结果

我们总共从维基百科中爬取了 172442252 字符的英文和 34390904 字符的中文文本，为了方便统计，我们只对 10000000 个字符进行统计，指标如下：

-   英文：
    -   英文单词的熵
    -   英文单词的概率分布（前 30 个）
    -   英文单词的 $f-r$ 图像、 $log(f)-log(r)$ 图像（其中 $f$ 表示 frequence；$r$ 表示 rank）
    -   英文字母的熵
    -   英文字母的概率分布
    -   英文字母的 $f-r$ 图像、 $log(f)-log(r)$ 图像（其中 $f$ 表示 frequence；$r$ 表示 rank）
-   中文：
    -   中文词语熵
    -   中文词语的概率分布（前 30 个）
    -   中文词语的 $f-r$ 图像、 $log(f)-log(r)$ 图像（其中 $f$ 表示 frequence；$r$ 表示 rank）
    -   中文汉字熵
    -   中文汉字的概率分布（前 30 个）
    -   中文汉字的 $f-r$ 图像、 $log(f)-log(r)$ 图像（其中 $f$ 表示 frequence；$r$ 表示 rank）

其中，英文分词使用空白字符，中文分词使用 jieba 第三方库。

### 熵

| size     | en-letter-entropy | en-word-entropy | zh-char-entropy | zh-word-entrop |
| -------- | ----------------- | --------------- | --------------- | -------------- |
| 1666666  | 4.1607            | 10.2674         | 9.1207          | 11.0052        |
| 3333333  | 4.1584            | 10.3194         | 9.2183          | 11.1632        |
| 4999998  | 4.1610            | 10.4583         | 9.3525          | 11.3928        |
| 6666664  | 4.1626            | 10.4923         | 9.4426          | 11.5958        |
| 8333330  | 4.1617            | 10.4690         | 9.4816          | 11.7033        |
| 10000000 | 4.1602            | 10.4706         | 9.5129          | 11.7882        |



### 英文：概率分布和齐夫定律

下面只展示英文前 1666666 字符的统计结果，其余样本规模的统计示意图请查看 `figures/en` 文件夹。从图中显然可以看出，英文单词符合齐夫定律。

-   **英文字母的 $f-r$ 图像、 $log(f)-log(r)$ 图像（其中 $f$ 表示 frequence；$r$ 表示 rank）**

    ![image-20251106120720418](https://tianchou.oss-cn-beijing.aliyuncs.com/img/20251106120720493.png)

-   **英文字母的概率分布**

    ![image-20251106120813358](https://tianchou.oss-cn-beijing.aliyuncs.com/img/20251106120813393.png)

-   **英文单词的 $f-r$ 图像、 $log(f)-log(r)$ 图像（其中 $f$ 表示 frequence；$r$ 表示 rank）**

    ![image-20251106121008533](https://tianchou.oss-cn-beijing.aliyuncs.com/img/20251106121008584.png)

-   **英文单词的概率分布（前 30 个）**

    ![image-20251106121126850](https://tianchou.oss-cn-beijing.aliyuncs.com/img/20251106121126891.png)



### 中文：概率分布和齐夫定律

同样地，下面只展示中文前 1666666 字符的统计结果，其余样本规模的统计示意图请查看 `figures/zh` 文件夹。从图中显然可以看出，中文词语符合齐夫定律。

-   **中文汉字的 $f-r$ 图像、 $log(f)-log(r)$ 图像（其中 $f$ 表示 frequence；$r$ 表示 rank）**

    ![image-20251106121607288](https://tianchou.oss-cn-beijing.aliyuncs.com/img/20251106121607330.png)

-   **中文汉字的概率分布（前 30 个）**

    ![image-20251106121742012](https://tianchou.oss-cn-beijing.aliyuncs.com/img/20251106121742061.png)

-   **中文词语的 $f-r$ 图像、 $log(f)-log(r)$ 图像（其中 $f$ 表示 frequence；$r$ 表示 rank）**

    ![image-20251106121816333](https://tianchou.oss-cn-beijing.aliyuncs.com/img/20251106121816367.png)

-   **中文词语的概率分布（前 30 个）**

    ![image-20251106121851419](https://tianchou.oss-cn-beijing.aliyuncs.com/img/20251106121851455.png)
