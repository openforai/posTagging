#!/usr/bin/python
#-*-coding:Utf-8-*

'''
Created on Dec 21, 2013

@author: Paulin AMOUGOU
@contact:  <adiks007@gmail.com>
'''

mixture = ['nns+md', 'ppss+bez', 'ppss+bez*', 'rbr+cs', 'np+md', 'to+vb', 'in+ppo', 'in+in', 
           'do+ppss', 'vb+at', 'wrb+doz', 'dts+bez', 'wdt+do+pps', 'rb+cs', 'wrb+dod*', 'wdt+ber', 
           'pn+hvd', 'pn+bez', 'wps+hvd', 'nn+hvd', 'wdt+dod', 'wrb+do', 'wrb+in', 'wrb+dod', 'wrb+md',
           'ex+hvz', 'ppss+vb', 'wrb+ber', 'ex+hvd', 'wps+hvz', 'pn+md', 'vb+to', 'dt+md', 'hv+to', 
           'md+to', 'md+ppss', 'nr+md', 'nn+in', 'rp+in', 'np+hvz', 'nn+nn', 'jj+jj', 'ap+ap', 'vb+jj', 
           'vb+vb', 'vb+in', 'wdt+ber+pp', 'vbg+to', 'nn+hvz', 'vbn+to', 'nn+bez', 'wdt+hvz', 'wps+md', 
           'nn+md', 'jjr+cs', 'pps+hvd', 'vb+rp', 'ex+md', 'wrb+bez', 'wdt+bez', 'rb+bez', 'vb+ppo', 
           'wps+bez', 'np+bez', 'pn+hvz', 'md+hv', 'dt+bez', 'ex+bez', 'ppss+hv', 'pps+md', 'ppss+hvd', 
           'ppss+ber', 'ppss+bem', 'pps+hvz', 'ppss+md', 'pps+bez', 'fw']

alias = {'pn$':'pn', 'cd$':'cd', 'rb$':'rb', 'ap$':'ap', 'qlp':'ql', 'ppls':'ppl', 'rbt':'rb', 'nr$':'nr', 
         'nrs':'nr', 'ppss':'pps', 'jjr':'jj', 'jjt':'jj', 'jjs':'jj', 'jj$':'jj', 'np$':'np', 'nps':'np', 
         'nps$':'np', 'dti': 'dt', 'dt$':'dt', 'dts':'dt', 'dtx':'dt', 'nns':'nm', 'nn$':'nn', 'nns$':'nn', 
         'rbr':'rb', 'hvd':'hv', 'hvz':'hv', 'hvn':'hv', 'hvg':'hv', 'hvd*':'hv*', 'hvz*':'hv*', 'bedz':'be', 
         'bez':'be', 'ber':'be', 'ben':'be', 'bed':'be', 'beg':'be', 'bem':'be', 'bem*':'be', 'bedz*':'be*', 
         'bez*':'be', 'ber*':'be*', 'bed*':'be*', 'dod':'do', 'doz':'do', 'dod*':'do*', 'doz*':'do*', 
         'vbg':'vb', 'vbn':'vb', 'vbz':'vb', 'vbd':'vb'}

dummy = ['cd-tl', 'day', 'l', 'destination', '2-story', '8', '2%', '4', 'or', '20th', '8', '4', '2', '64', '16', '32', 'under', '50th', '3', '2-foot', '16-inch', '8-inch', '8-inch-thick', '29', 'destination', '3%', 'm.', '16', 'sec', 'active', '', 'g', 'cell', 'chamber', '7074', 'Output', 'output', 'lBOD', 'day', 'coating', 'sq.', 'hr.', 'watt', '4-inch']

numberMarquee = '0'