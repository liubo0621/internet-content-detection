import sys
sys.path.append('../../')

import base.base_parser as base_parser
import init
import utils.tools as tools
from utils.log import log
import base.constance as Constance
import re

# 必须定义 网站id
SITE_ID = 9
# 必须定义 网站名
NAME = 'sichuanhuagong'


# 必须定义 添加网站信息
@tools.run_safe_model(__name__)
def add_site_info():
    log.debug('添加网站信息')
    site_id = SITE_ID
    name = NAME
    table = 'op_site_info'
    url = "http://www.sccc.edu.cn/new/"

    base_parser.add_website_info(table, site_id, url, name)

# 必须定义 添加根url
@tools.run_safe_model(__name__)
def add_root_url(parser_params = {}):
    log.debug('''
        添加根url
        parser_params : %s
        '''%str(parser_params))

    url = "http://www.sccc.edu.cn/new/"
    base_parser.add_url('op_urls', SITE_ID, url)

# 必须定义 解析网址
def parser(url_info):
    url_info['_id'] = str(url_info['_id'])
    log.debug('处理 \n' + tools.dumps_json(url_info))

    source_url = url_info['url']
    depth = url_info['depth']
    website_id = url_info['site_id']
    description = url_info['remark']

    html, request = tools.get_html_by_requests(source_url, code='gb2312')
    if html == None:
        base_parser.update_url('op_urls', source_url, Constance.EXCEPTION)
        return

    urls = tools.get_urls(html)
    for url in urls:
        if re.match("http", url):
            new_url = url
        elif re.match('/', url):
            new_url = 'http://www.sccc.edu.cn/new' + url
        else:
            new_url = 'http://www.sccc.edu.cn/new/' + url
        base_parser.add_url('op_urls', website_id, new_url, depth + 1)
    regexs = '<script type="text/javascript" language="JavaScript" src="(.*?)"'
    urls = tools.get_info(html, regexs)
    for url in urls:
        new_url = 'http://www.sccc.edu.cn/new/'+url
        base_parser.add_url('op_urls', website_id, new_url, depth + 1)

    # 取当前页的文章信息
    # 标题

    regexs = 'td height="60" align="center" valign="bottom" class="nrbt">(.*?)</td>'
    title = tools.get_info(html, regexs)
    title = title and title[0] or ''
    title = tools.del_html_tag(title)

    #时间
    regexs = '<td height="3" align="center" valign="top">(.*?)</td>'
    release_time = tools.get_info(html, regexs)
    release_time = release_time and release_time[1] or ''

    # #作者
    regexs = '<td width="250">(.*?)</td>'
    author = tools.get_info(html, regexs)
    author = author and author[0] or ''
    #author = tools.del_html_tag(author)

    #文章来源
    regexs = '<td width="300">(.*?)</td>'
    origin = tools.get_info(html, regexs)
    origin = origin and origin[0] or ''
    origin = tools.del_html_tag(origin)

    # #点击数
    regexs = ' <td>阅读(\d*?)次</td>'
    watched_count = tools.get_info(html, regexs)
    watched_count = watched_count and watched_count[0] or ''
    watched_count = tools.del_html_tag(watched_count)

    # 内容
    regexs = ['<td class="nr">(.*?)</td>']
    content = tools.get_info(html, regexs)
    content = content and content[0] or ''
    content = tools.del_html_tag(content)

    log.debug('''
                    depth               = %s
                    url                 = %s
                    title               = %s
                    release_time        = %s
                    author              = %s
                    origin              = %s
                    watched_count       = %s
                    content             = %s
                 ''' % (depth+1, source_url, title, release_time, author, origin, watched_count, content))

    if content and title:
        base_parser.add_op_info('op_content_info', website_id, source_url, title=title, release_time=release_time, author=author,
                                origin=origin, watched_count=watched_count, content=content)
    # 更新source_url为done
    base_parser.update_url('op_urls', source_url, Constance.DONE)

if __name__ == '__main__':
    url = "http://www.sccc.edu.cn/new/"
    html, request = tools.get_html_by_requests(url, code='gb2312')
    urls = tools.get_urls(html)
    #print(html)
    for url in urls:
        for url in urls:
            if re.match("http", url):
                new_url = url
            elif re.match('/', url):
                new_url = 'http://www.sccc.edu.cn/new' + url
            else:
                new_url = 'http://www.sccc.edu.cn/new/' + url
            # base_parser.add_url('op_urls', website_id, new_url, depth + 1)
    regexs = '<script type="text/javascript" language="JavaScript" src="(.*?)"'
    urls = tools.get_info(html, regexs)
    for url in urls:
        new_url = 'http://www.sccc.edu.cn/new/'+url
        # base_parser.add_url('op_urls', website_id, new_url, depth + 1)
    # regexs = ['<td class="nr">(.*?)</td>']
    # content = tools.get_info(html, regexs)
    # content = content and content[0] or ''
    # content = tools.del_html_tag(content)
    # print(content)
    #urls = tools.get_urls(html)
    #print(urls)
    # for url in urls:
    #     print(url)
        #base_parser.add_url('article_urls', SITE_ID, url)





