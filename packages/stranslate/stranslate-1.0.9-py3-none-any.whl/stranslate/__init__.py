# -*- coding: utf-8 -*-
'''
Created on 31-Jan-2019

@author: Surya ST
'''
import re,requests
import html.parser
parser = html.parser.HTMLParser()

class strans:
    def translate(to_trans,hl):
        try:
            #https://translate.google.com/?hl=ta
            base = 'http://translate.google.com/m?sl=auto&hl='+hl+'&q=' + to_trans
            html = requests.get(base).text
            re_tran_result = re.search(r'</a></div><br><div\s*dir="ltr"\s*class="t0">(.*?)</div', html)
            if re_tran_result:
                translated = re_tran_result.group(1).strip()
                result=parser.unescape(translated)
                return result
            else:
                return to_trans
        except:
            return to_trans

if __name__ == '__main__':
    ob = strans()
    ob.translate()