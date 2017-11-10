from dateutil import parser
import unicodedata
import re
from scrapy import Request


class deteksi(object):


# ================= START EDITOR CONVERT ========= #

	def c_editor(self, e, m):
		if m == 'detik':
			try:
				return e[0].split(" - ")[0].strip()
			except IndexError:
				return '-'
		if m == 'kompas' or m == 'dream' or m == 'tempo' or m == 'mediaindonesia' or m == 'skalanews':
			try:
				return e[1].strip()
			except IndexError:
				return '-'
		if m == 'metrotvnews':
			try:
				e = unicodedata.normalize('NFKD', unicode(e[0].strip())).split(u'\u2022') # remove all whitespace with normalize
				return e[0].strip()
			except IndexError:
				return e
		if m == 'jawapos':
			try:
				return e[3]
			except IndexError:
				return e[1].split(u'\u00a0')[1]
		if m == 'viva' or m == 'antaranews' or m == 'bisnis' or m == 'liputan6' or m == 'beritasatu' or m == 'sindonews'\
		 	or m == 'cnnindonesia' or m == 'bbc' or m == 'sinarharapan' or m == 'teropongsenayan'\
		 	or m == 'katadata' or m == 'fajar' or m == 'pikiran' or m == 'merdeka' or m == 'inilah'\
		 	or m == 'suara' or m == 'beritajateng' or m == 'tirto' or m == 'rappler' or m == 'beritagar' or m == 'solopos':
			try:
				return e[0].strip()
			except IndexError:
				return '-'
		if m == 'aktual' or m == 'analisadaily':
			try:
				return re.sub('[()]','',e[0]).strip()
			except IndexError:
				return '-'
		if m == 'rmol':
			try:
				return e[5].replace(':','').replace('\t','').strip()
			except IndexError:
				return '-'
		if m == 'tribunnews' or m == 's_tribunnews':
			try:
				return e[0].split(':')[1].replace('\t','').strip()
			except IndexError:
				return '-'
		if m == 'indopos' or m == 'batamtoday' or m == 'bloktuban':
			try:
				return e[0].split(':')[1].strip()
			except IndexError:
				return '-'
		if m == 'harnas':
			try:
				return e[1].split(':')[1].strip()
			except IndexError:
				return '-'
		if m == 'harianterbit':
			return re.sub('[()]','',e[-1])
		if m == 'kricom':
			return e[11].strip()
		if m == 'theconversation':
			return e[0].strip()
		if m == 'jurnas':
			return e[0].split('|')[0]
		if m == 'rri':
			return e[5].replace('by','').strip()
		if m == 'kontan':
			return e[0].split('Editor')[1].strip()
		if m == 'okezone':
			return e[0].replace(',','').strip()
		if m == 'fajaronline':
			return e[-1].split(':')[-1].strip()
		else:
			# if not e:
			# 	return '-'
			# else:
			# 	return e
			return e
			

# ================= END ========= #
	def day(self, d):
		d = d.lower()
		if d == 'senin':
			return "monday"
		if d == 'selasa':
			return "tuesday"
		if d == 'rabu':
			return "wednesday"
		if d == 'kamis':
			return "thursday"
		if d == 'jumat':
			return "friday"
		if d == 'sabtu':
			return "saturday"
		else:
			return 'sunday'

	# ====== START CONVERT DATE ================== #
	# m is media
	def month_name(self, m):
		m = m.lower()
		if m == "januari" or m == "jan":
			return "jan"
		if m == "februari" or m == "feb":
			return "feb"
		if m == "maret" or m == "mar":
			return "mar"
		if m == "april" or m == "apr":
			return "apr"
		if m == "mei" or m == "may":
			return "may"
		if m == "juni" or m == "jun":
			return "jun"
		if m == "juli" or m == "jul":
			return "jul"
		if m == "agustus" or m == "aug":
			return "aug"
		if m == "september" or m == "sep":
			return "sep"
		if m == "oktober" or m == "oct" or m == "okt":
			return "oct"
		if m == "november" or m == "nov" or m == 'nopember':
			return "nov"
		if m == "desember" or m == "dec":
			return "dec"
	# d is date, m is media
	def c_date(self, d, m):
		if m == 'detik':
			try:
				# parse_date = d[0].replace('WIB', '').replace(',', '').strip().split(' ')
				parse_date = self.m_replacer(d[0],['WIB',','],'').strip().split(' ')
				bulan = self.month_name(parse_date[2])
				t = parse_date[1] + ' ' + bulan + ' ' + \
					parse_date[3] + ' ' + parse_date[4]
			except IndexError:
				t = d.replace('WIB','')
			return self.f_date(t)
		if m == 'kompas':
			# t = d[0].split('-')[1].replace(',','').replace('WIB','')
			t = self.m_replacer(d[0].split('-')[1], [',','WIB'],'')
			return self.f_date(t)
		if m == 'dream':
			try:
				parse_date = d[2].split(', ')[1].split(' ')
				bulan = self.month_name(parse_date[1])
				t = parse_date[0] + ' ' + bulan + ' ' + \
					parse_date[2] + ' ' + parse_date[3]
				return self.f_date(t)
			except IndexError:
				return '-'
		if m == 'viva' or m == 'suara' or m == 'skalanews' or m == 'analisadaily':
			try:
				parse_date = d[0].replace('WIB', '').replace('| ', '').split(', ')[1].strip().split(' ')
				bulan = self.month_name(parse_date[1])
				t = parse_date[0] + ' ' + bulan + ' ' + \
					parse_date[2] + ' ' + parse_date[3]
				return self.f_date(t)
			except IndexError:
				return '-'
			
		if m == 'kontan':
			parse_date = d[0].replace('WIB', '').replace('/ ', '').split(', ')[1].strip().split(' ')
			bulan = self.month_name(parse_date[1])
			t = parse_date[0] + ' ' + bulan + ' ' + \
				parse_date[2] + ' ' + parse_date[3]
			return self.f_date(t)
		if m == 'tribunnews' or m == 's_tribunnews' or m == 'merdeka' or m == 'bloktuban':
			parse_date = d[0].split(', ')[1].split(' ')
			bulan = self.month_name(parse_date[1])
			t = parse_date[0] + ' ' + bulan + ' ' + \
				parse_date[2] + ' ' + parse_date[3]
			return self.f_date(t)
		if m == 'inilah':
			parse_date = d[2].replace('|', '').replace('WIB', '').strip().split(', ')[1].split(' ')
			bulan = self.month_name(parse_date[1])
			t = parse_date[0] + ' ' + bulan + ' ' + \
				parse_date[2] + ' ' + parse_date[3]
			return self.f_date(t)
		if m == 'okezone' or m == 'antaranews' or m == 'tempo' or m == 'harnas' or m == 'solopos':
			parse_date = d[0].replace(',', '').replace('WIB', '').strip().split(' ')
			bulan = self.month_name(parse_date[2])
			t = parse_date[1] + ' ' + bulan + ' ' + \
				parse_date[3] + ' ' + parse_date[4]
			return self.f_date(t)
		if m == 'metrotvnews':
			t = d[0].split(',')[1].replace('WIB','')
			return self.f_date(t)
		if m == 'jpnn':
			# parse_date = unicodedata.normalize('NFKD', unicode(d[0].strip())).encode('ascii','ignore').replace('WIB','').split(',')[1].split()
			parse_date = self.s_undecode(d[0]).replace('WIB','').split(',')[1].split()
			bulan = self.month_name(parse_date[1])
			t = parse_date[0] + ' ' + bulan + ' ' + parse_date[2] + ' ' + parse_date[3]
			return self.f_date(t)
		if m == 'jawapos':
			t = d[1].split('|')[0].split(',')[1]
			return self.f_date(t)
		if m == 'bisnis':
			try:
				bulan = self.month_name(d[0].strip())
				t = d[1] + ' ' + bulan + ' ' + d[3] + ' ' + d[4].replace('WIB','')
				return self.f_date(t)
			except IndexError:
				return d
		if m == 'liputan6':
			parse_date = d[0].replace(',','').replace('WIB','').split()
			bulan = self.month_name(parse_date[1])
			t = parse_date[0] + ' ' + bulan + ' ' + parse_date[2] + ' ' + parse_date[3]
			return self.f_date(t)
		if m == 'beritasatu':
			parse_date = d[3].replace('|','').replace('WIB','').replace('\t','').split()
			bulan = self.month_name(parse_date[2])
			t = parse_date[1] + ' ' + bulan + ' ' + parse_date[3] + ' ' + parse_date[4]
			return self.f_date(t)
		if m == 'rmol':
			try:
				parse_date = d[3].replace(',','').replace('|','').replace('WIB','').split()
				bulan = self.month_name(parse_date[2])
				t = parse_date[1] + ' ' + bulan + ' ' + parse_date[3] + ' ' + parse_date[4]
				return self.f_date(t)
			except IndexError:
				return '-' # different position '.wp-caption-text' example : http://rmol.co/dpr/read/2017/10/26/312606/Semoga,-Implementasi-APBN-2018-Bukan-Sekadar-Pencitraan-
		if m == 'sindonews':
			parse_date = d[0].replace(',','').replace('-','').replace('WIB','').split()
			bulan = self.month_name(parse_date[2])
			t = parse_date[1] + ' ' + bulan + ' ' + parse_date[3] + ' ' + parse_date[4]
			return self.f_date(t)
		if m == 'cnnindonesia':
			parse_date = d[2].split('|')[1].split()
			t = parse_date[1] + ' ' + parse_date[2]
			return self.f_date(t)
		if m == 'aktual':
			parse_date = d[0].replace(',','').split()
			bulan = self.month_name(parse_date[0])
			t = parse_date[1] + ' ' + bulan + ' ' + parse_date[2] + ' ' + parse_date[3]
			return self.f_date(t)
		if m == 'indopos':
			parse_date = d[0].replace(',','').replace('|','').split()
			bulan = self.month_name(parse_date[2])
			t = parse_date[1] + ' ' + bulan + ' ' + parse_date[3] + ' ' + parse_date[4]
			return self.f_date(t)
		if m == 'mediaindonesia':
			t = d[0].split(',')[1].replace('WIB','')
			return self.f_date(t)
		if m == 'poskotanews':
			parse_date = d[0].split(',')[1].replace('WIB','').split()
			bulan = self.month_name(parse_date[1])
			t = parse_date[0] + ' ' + bulan + ' ' + parse_date[2] + ' ' + parse_date[4]
			return self.f_date(t)
		if m == 'harianterbit':
			parse_date = d[1].split(',')[1].replace('WIB','').split()
			bulan = self.month_name(parse_date[1])
			t = parse_date[0] + ' ' + bulan + ' ' + parse_date[2] + ' ' + parse_date[3]
			return self.f_date(t)
		if m == 'sinarharapan':
			parse_date = d[0].split()
			bulan = self.month_name(parse_date[1])
			t = parse_date[0] + ' ' + bulan + ' ' + parse_date[2] + ' ' + parse_date[3]
			return self.f_date(t)
		if m == 'kricom':
			i = self.f_index(d,'WIB')
			t = d[i].split()
			bulan = self.month_name(t[2])
			t = t[1] + ' ' + bulan + ' ' + t[3] + ' ' + t[4]
			return self.f_date(t)
		if m == 'teropongsenayan':
			parse_date = d[0].split()
			bulan = self.month_name(parse_date[3])
			t = parse_date[2] + ' ' + bulan + ' ' + parse_date[4] + ' ' + parse_date[6]
			return self.f_date(t)
		if m == 'katadata':
			parse_date = d[0].split()
			t = parse_date[1].replace(',','')+' '+parse_date[2].replace('.',':')
			return self.f_date(t)
		if m == 'fajar' or m == 'beritajateng':
			parse_date = d[0]
			t = parse_date.replace(',','').replace('@','')
			return self.f_date(t)
		if m == 'pikiran':
			parse_date = d[0].replace(',','').replace('-','').split()
			bulan = self.month_name(parse_date[1])
			t = parse_date[0] + ' ' + bulan + ' ' + parse_date[2] + ' ' + parse_date[3]
			return self.f_date(t)
		if m == 'theconversation':
			parse_date = d[0].replace(',','').replace('.',':').split()
			bulan = self.month_name(parse_date[0])
			t = parse_date[1] + ' ' + bulan + ' ' + parse_date[2] + ' ' + parse_date[3]
			try:
				return self.f_date(t)
			except IndexError:
				return '-'
		if m == 'jurnas':
			t = d[0].split('|')[1].split(',')[1].replace('WIB','')
			return self.f_date(t)
		if m == 'batamtoday':
			parse_date = d[0].split('|')
			t = parse_date[1]+' '+parse_date[2]
			t = t.replace('WIB','')
			return self.f_date(t)
		if m == 'rri':
			t = d[1]
			return t
		if m == 'bbc':
			t = d[0].split()
			bulan = self.month_name(t[1])
			t = t[0] + ' ' + bulan + ' ' + t[2]
			# return t
			return self.f_date(t)
		if m == 'independen':
			t = d[0].split()
			bulan = self.month_name(t[1])
			t = t[0] + ' ' + bulan + ' ' + t[2] + ' ' + t[3]
			return self.f_date(t)
		if m == 'tirto':
			try:
				t = d[0].replace(',','').split()
				bulan = self.month_name(t[1])
				t = t[0] + ' ' + bulan + ' ' + t[2]
				return self.f_date(t)
			except IndexError:
				return "-"
		if m == 'fajaronline':
			parse_date = d[1].replace(',','').replace('-','').split()
			bulan = self.month_name(parse_date[1])
			t = parse_date[0] + ' ' + bulan + ' ' + parse_date[2] + ' ' + parse_date[3]
			return self.f_date(t)
		if m == 'rappler':
			t = d[0].replace(',','').split()
			t = t[3]+' '+t[4]+' '+t[5]+' '+t[1]
			return self.f_date(t)
		if m == 'beritagar':
			t = d[0].replace('WIB','').replace('-','').replace(',','').split()
			t = t = t[2] + ' ' + self.month_name(t[3]) + ' ' + t[4] + ' ' + t[0]
			# return self.f_date(t)
			return self.f_date(t)
		else:
			# if not d:
			# 	return '-'
			# else:
			# 	return d
			return d
		# return self.f_date(t) # Finding format

# ====== END ================== #
# ========== START m_replacer ============= #
# s is string, a is array, r is replacer
	def m_replacer(self,s,a,r):
		for x in a:
			s = s.replace(x,r)
		return s
# ========== END m_replacer ============= #
# ========== START Content Paging ============= #
	def p_content(self,response):
		# return response.meta.get('t_target')
		return "ok"
# ========== END Content Paging ============= #
	def f_date(self,d):
		return parser.parse(d).strftime('%Y/%m/%d %H:%M:%S')
	def f_index(self,a,k):
		# Maybe can use re.search()
		return [idx for idx, s in enumerate(a) if k in s]
	def s_undecode(self,s):
		return unicodedata.normalize('NFKD', unicode(s)).encode('ascii','ignore')
