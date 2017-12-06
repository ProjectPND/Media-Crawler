from dateutil import parser
import unicodedata
import re
from scrapy import Request
from datetime import datetime, timedelta

# from scrapy.http.request import Request
# import scrapy


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
		if m == 'viva' or m == 'bisnis' or m == 'liputan6' or m == 'beritasatu' or m == 'sindonews'\
		 	or m == 'cnnindonesia' or m == 'bbc' or m == 'sinarharapan' or m == 'teropongsenayan'\
		 	or m == 'katadata' or m == 'fajar' or m == 'pikiran' or m == 'merdeka' or m == 'inilah'\
		 	or m == 'suara' or m == 'beritajateng' or m == 'tirto' or m == 'rappler' or m == 'beritagar' or m == 'solopos'\
		 	or m == 'tribratanews' or m == 'faktualnews' or m == 'lensaindonesia' or m == 'maduracorner' or m == 'riauonline'\
		 	or m == 'harianrakyatbengkulu' or m == 'rakyatpos' or m == 'krjogja' or m == 'hargo' or m == 'suarakarya' \
		 	or m == 'jalandamai' or m == 'damailahindonesiaku' or m == 'theconversation' or m == 'dutadamai' or m == 'lombokpost'\
		 	or m == 'radarposo' or m == 'rakyatsultra.fajar' or m == 'radarsulbar' or m == 'ambonekspres' or m == 'utamanews' \
		 	or m == 'australiaplus' or m == 'bareksa' or m == 'dailysocial' or m == 'goal' or m == 'hipwee' or m == 'hukumonline' or m == 'news.idntimes':
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
		if m == 'tribunnews' or m == 'surabaya.tribunnews':
			try:
				return e[0].split(':')[1].replace('\t','').strip()
			except IndexError:
				return '-'
		if m == 'indopos' or m == 'batamtoday' or m == 'bloktuban' or m == 'gatra' or m == 'hidayatullah':
			try:
				return e[0].split(':')[1].strip()
			except IndexError:
				return '-'
		if m == 'harnas' or m == 'nukita':
			try:
				return e[1].split(':')[1].strip()
			except IndexError:
				return '-'
		# if m == 'harianterbit':
		# 	return re.sub('[()]','',e[-1])
		if m == 'kricom':
			i = self.f_index(e,'Redaktur:')[0]+1
			return e[i].strip()
		# if m == 'theconversation':
		# 	return e[0].strip()
		if m == 'jurnas':
			return e[0].split('|')[0]
		if m == 'rri':
			return e[5].replace('by','').strip()
		if m == 'kontan':
			return e[0].split('Editor')[1].strip()
		if m == 'okezone':
			return e[0].replace(',','').strip()
		if m == 'fajaronline' or m == 'republika':
			return e[-1].split(':')[-1].strip()
		if m == 'nu':
			e = e[1].replace('Red:','')
			return re.sub('[()]','',e)
		if m == 'berdikari' or m == 'kahaba' or m == 'ahad':
			return e[-1].strip()
		if m == 'covesia':
			return e[1].strip()
		if m == 'kabarpas' or m == 'kini':
			return e[0].split(':')[1].strip()
		if m == 'beritajatim' or m == 'voaindonesia':
			try:
				e = re.sub('[[\]]','',e[1])
			except IndexError:
				try:
					e = re.sub('[[\]]','',e[0])
				except IndexError:
					e = '-'
			return e
		if m == 'lampungpro':
			return e[3].split(':')[1].replace('&nbsp','').strip()
		if m == 'josstoday' or m == 'bimakini' or m == 'siwalimanews' or m == 'harianterbit':
			e = e[-1].strip()
			return re.sub('[(\)]','',e)
		if m == 'damai':
			return e
		if m == 'antaranews':
			try:
				e = self.m_replacer(e[0],['Editor',':'],'')
			except IndexError:
				e = "-"
			return e.strip()
		if m == 'palembang.tribunnews' or m == 'kupang.tribunnews' or m == 'makassar.tribunnews':
			try:
				e = e[0].split(',')[1]
			except IndexError:
				e = '-'
			return e.strip()
		if m == 'jambiekspres':
			try:
				e = re.sub('[(\)]','',e[1])
			except IndexError:
				e = '-'
			return e.strip()
		if m == 'timesindonesia':
			return e[5].strip()
		if m == 'bantenraya' or m == 'manado.tribunnews' or m == 'harianpilar' or m == 'kalsel.prokal':
			try:
				e = e[-1].split()[-1]
				return re.sub('[(\)]','',e).strip()
			except IndexError:
				return "-"
		if m == 'equator':
			e = e[-1].split(':')[-1]
			return e.strip()
		if m == 'kalteng.prokal':
			e = ' '.join(e).split('(')[1].replace(')','')
			return e.strip()
		if m == 'suaramerdeka':
			e = re.sub('[()]','',e[0]).split()
			e = ''.join(e)
			return e
		if  m == 'wartabromo':
			e = e[-2].split()[-1]
			e = re.sub('[()]','',e)
			return e
		if  m == 'jabarnews':
			e = e[-3]#.split()[-1]
			if "(" not in e and ")" not in e:
				e = "-"
			e = re.sub('[()]','',e)
			return e
		if  m == 'batamnews':
			i = self.f_index(e,'Editor')
			e = e[i[0]].split(':')[1]
			return e.strip()
		if  m == 'kbr':
			try:
				return e[1].strip()
			except IndexError:
				return e[0].strip()
		if  m == 'kumparan':
			try:
				i = self.f_index(e,'Editor :')[0]+1
				return e[i]
			except IndexError:
				return "-"
		if  m == 'bnpt':
			e = e[-1].split()[-1]
			e = re.sub('[\[\]]','',e)
			return e
		if  m == 'padek':
			i = self.f_index(e,'Editor')
			e = e[i[0]+1].split('-')[0]
			return e.strip()
		if  m == 'malang-post':
			for x in reversed(e):
				if "(" in x and")" in x:
					e = x
					break
			e = e.split()[-1]
			e = re.sub('[()]','',e)
			return e
		if m == 'kaltim.prokal':
			e = ' '.join(e).split()#.strip()
			e = ' '.join(e).split()[-1]
			e = re.sub('[()]','',e)
			return e
		if m == 'tabloidjubi':
			i = self.f_index(e,'Editor')
			e = e[i[0]].split(':')[1]
			return e.strip()
		if m == 'papuapos':
			e = e[0].split()[-1]
			return e
		if m == 'radarsultengonline':
			e = e[-1]
			try:
				e = e.split('.')[-1]
			except IndexError:
				pass
			e = re.sub('[()]','',e)
			return e.strip()
		if m == 'waspada':
			try:
				e = e[-1]
			except IndexError:
				e = "-"
			if ":" in e:
				e = e.split(":")[-1]
			else:
				if "(" in e and ")" in e:
					e = re.sub('[()]','',e)
				else:
					pass
			return e.strip()
		if m == 'jpnn': #Content must be load by paging
			# for x in reversed(e):
				# if ")" in x:
				# if "(" in x and ")" in x:
					# e = x
					# break
			# e = e.split()[-1]
			# e = re.sub('[()]','',e)
			return "-"
		if m == 'dw' or m == 'elshinta': 
			return "-"
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
		if m == "desember" or m == "dec" or m == "des":
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
			try:
				t = self.m_replacer(d[0].split('-')[1], [',','WIB'],'')
				return self.f_date(t)
			except IndexError:
				t = self.d_now()
			return self.f_date(t)

		if m == 'dream':
			try:
				parse_date = d[2].split(', ')[1].split(' ')
				bulan = self.month_name(parse_date[1])
				t = parse_date[0] + ' ' + bulan + ' ' + \
					parse_date[2] + ' ' + parse_date[3]
			except IndexError:
				t = self.d_now()
			return self.f_date(t)
		if m == 'viva' or m == 'suara' or m == 'skalanews' or m == 'analisadaily':
			try:
				parse_date = d[0].replace('WIB', '').replace('| ', '').split(', ')[1].strip().split(' ')
				bulan = self.month_name(parse_date[1])
				t = parse_date[0] + ' ' + bulan + ' ' + \
					parse_date[2] + ' ' + parse_date[3]
			except IndexError:
				t = self.d_now()
			return self.f_date(t)
		if m == 'kontan':
			parse_date = d[0].replace('WIB', '').replace('/ ', '').split(', ')[1].strip().split(' ')
			bulan = self.month_name(parse_date[1])
			t = parse_date[0] + ' ' + bulan + ' ' + \
				parse_date[2] + ' ' + parse_date[3]
			return self.f_date(t)
		if m == 'tribunnews' or m == 'surabaya.tribunnews' or m == 'merdeka' or m == 'bloktuban' or m == 'palembang.tribunnews' or m == 'kupang.tribunnews'\
			or m == 'makassar.tribunnews' or m == 'manado.tribunnews':
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
			except IndexError:
				t = self.d_now() # different position '.wp-caption-text' example : http://rmol.co/dpr/read/2017/10/26/312606/Semoga,-Implementasi-APBN-2018-Bukan-Sekadar-Pencitraan-
			return self.f_date(t)
		if m == 'sindonews' or m == 'hidayatullah':
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
		# if m == 'sinarharapan':
		# 	parse_date = d[0].split()
		# 	bulan = self.month_name(parse_date[1])
		# 	t = parse_date[0] + ' ' + bulan + ' ' + parse_date[2] + ' ' + parse_date[3]
		# 	return self.f_date(t)
		if m == 'kricom': #fix
			i = self.f_index(d,'WIB')
			t = d[i[0]].split(',')[1].split()
			bulan = self.month_name(t[1])
			t = t[0] + ' ' + bulan + ' ' + t[3] + ' ' + t[4]
			return self.f_date(t)
			# return t
		if m == 'teropongsenayan':
			parse_date = d[0].split()
			bulan = self.month_name(parse_date[3])
			t = parse_date[2] + ' ' + bulan + ' ' + parse_date[4] + ' ' + parse_date[6]
			return self.f_date(t)
		if m == 'katadata':
			parse_date = d[0].split()
			t = parse_date[1].replace(',','')+' '+parse_date[2].replace('.',':')
			return self.f_date(t)
		if m == 'fajar' or m == 'beritajateng' or m == 'rakyatsultra.fajar' or m == 'radarsulbar' or m == 'ambonekspres':
			parse_date = d[0]
			t = parse_date.replace(',','').replace('@','')
			return self.f_date(t)
		if m == 'pikiran-rakyat':
			parse_date = d[0].replace(',','').replace('-','').split()
			bulan = self.month_name(parse_date[1])
			t = parse_date[0] + ' ' + bulan + ' ' + parse_date[2] + ' ' + parse_date[3]
			return self.f_date(t)
		if m == 'theconversation':
			try:
				parse_date = d[0].replace(',','').replace('.',':').split()
				bulan = self.month_name(parse_date[0])
				t = parse_date[1] + ' ' + bulan + ' ' + parse_date[2] + ' ' + parse_date[3]
			except IndexError:
				t = self.d_now()
			return self.f_date(t)
		if m == 'jurnas':
			t = d[0].split('|')[1].split(',')[1].replace('WIB','')
			return self.f_date(t)
		if m == 'batamtoday':
			parse_date = d[0].split('|')
			t = parse_date[1]+' '+parse_date[2]
			t = t.replace('WIB','')
			return self.f_date(t)
		if m == 'rri':
			t = ' '.join(d)
			t = re.sub('\s+', ' ', t).split()
			b = self.month_name(t[1])
			t = t[0] + ' ' + b + ' ' + t[3] + ' ' + t[2]
			return self.f_date(t)
			# return t
		# if m == 'bbc':
		# 	t = d[0].split()
		# 	bulan = self.month_name(t[1])
		# 	t = t[0] + ' ' + bulan + ' ' + t[2]
			# return t
			return self.f_date(t)
		if m == 'independen':
			t = d[0].split()
			bulan = self.month_name(t[1])
			t = t[0] + ' ' + bulan + ' ' + t[2] + ' ' + t[3]
			return self.f_date(t)
		if m == 'tirto' or m == 'bnpt':
			try:
				t = d[0].replace(',','').split()
				bulan = self.month_name(t[1])
				t = t[0] + ' ' + bulan + ' ' + t[2]
			except IndexError:
				t = self.d_now()
			return self.f_date(t)
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
			return self.f_date(t)
		if m == 'tribratanews':
			t = d[0].replace('pm','')
			return self.f_date(t)
		if m == 'nu' or m == 'kalteng.prokal' or m == 'malang-post' or m == 'kaltim.prokal' or m == 'papuapos' or m == 'bareksa' \
			or m == 'elshinta' or m == 'utamanews':
			t = d[0].split(',')[1].split()
			b = self.month_name(t[1])
			t = t = t[0] + ' ' + b + ' ' + t[2] + ' ' + t[3]
			return self.f_date(t)
		if m == 'berdikarionline':
			t = d[0].replace('|','').split()
			b = self.month_name(t[1])
			t = t = t[0] + ' ' + b + ' ' + t[2] + ' ' + t[3]
			return self.f_date(t)
		if m == 'wartabromo':
			t = d[0].split(',')[1].replace('|','').split()
			b = self.month_name(t[1])
			t = t = t[0] + ' ' + b + ' ' + t[2] + ' ' + t[3]
			return self.f_date(t)
		if m == 'covesia':
			t = d[0].replace('WIB','').split(',')[1]
			return self.f_date(t)
		if m == 'kabarpas' or m == 'lensaindonesia' or m == 'radarsultengonline':
			t = d[0]
			return self.f_date(t)
		if m == 'kini':
			try:
				t = d[2].split(',')
			except IndexError:
				t = d[0].split(',')
			t = self.m_replacer(t[1],['-','WIB'],'').split()
			b = self.month_name(t[1])
			t = t = t[0] + ' ' + b + ' ' + t[2] + ' ' + t[3]
			return self.f_date(t)
		if m == 'beritajatim':
			t = d[0].split(',')[1].split()
			b = self.month_name(t[1])
			j = d[1].replace('WIB','').strip()
			t = t = t[0] + ' ' + b + ' ' + t[2] + ' ' + j
			return self.f_date(t)
		if m == 'jabarnews' or m == 'bimakini':
			try:
				t = d[0].replace(',','').split()
				b = self.month_name(t[0])
				t = t = t[1] + ' ' + b + ' ' + t[2]
			except TypeError:
				t = self.d_now()
			return self.f_date(t)
		if m == 'lampungpro':
			t = d[2].split(',')
			t = self.m_replacer(t[1],['|','PM','&nbsp'],'').split()
			b = self.month_name(t[1])
			t = t = t[0] + ' ' + b + ' ' + t[2] + ' ' + t[3]
			return self.f_date(t)
		if m == 'faktualnews':
			t = d[0].split(',')[1]
			t = self.m_replacer(t,['|','WIB'],'').split()
			b = self.month_name(t[1])
			t = t = t[0] + ' ' + b + ' ' + t[2] + ' ' + t[3]
			return self.f_date(t)
		if m == 'maduracorner':
			t = d[0].replace('|','').split()
			b = self.month_name(t[1])
			t = t = t[0] + ' ' + b + ' ' + t[2] + ' ' + t[3]
			return self.f_date(t)
		if m == 'josstoday' or m == 'sinarharapan':
			t = d[0].split()
			b = self.month_name(t[1])
			t = t = t[0] + ' ' + b + ' ' + t[2] + ' ' + t[3]
			return self.f_date(t)
		if m == 'riauonline' or m == 'kbr':
			t = d[0].split(',')[1].replace('WIB','').split()
			b = self.month_name(t[1])
			t = t = t[0] + ' ' + b + ' ' + t[2] + ' ' + t[3]
			return self.f_date(t)
		if m == 'jambiekspres':
			d = d[0].split('|')
			t = d[0].split(',')[1].split()
			b = self.month_name(t[1])
			j = d[1].replace('WIB','')
			t = t = t[0] + ' ' + b + ' ' + t[2] + ' ' + j
			return self.f_date(t)
		if m == 'timesindonesia' or m == 'nukita':
			t = d[0].replace('-','').split(',')[1].split()
			b = self.month_name(t[1])
			t = t = t[0] + ' ' + b + ' ' + t[2] + ' ' + t[3]
			return self.f_date(t)
		if m == 'harianrakyatbengkulu' or m == 'equator' or m == 'harianpilar' or m == 'jalandamai' \
			or m =='bbc' or m == 'damailahindonesiaku' or m == 'dutadamai' or m == 'lombokpost'or m == 'kahaba' or m == 'radarposo' \
			or m == 'ahad' or m == 'news.idntimes' :
			try:
				try:
					t = d[0].split()
					b = self.month_name(t[1])
					t = t = t[0] + ' ' + b + ' ' + t[2]
				except IndexError:
					t = self.d_now()
			except TypeError:
				t = self.d_now()
			return self.f_date(t)
		if m == 'rakyatpos':
			t = self.m_replacer(d[0],['th,',',','pm','am'],'')
			return self.f_date(t)
		if m == 'krjogja':
			t = d[0].split(',')[1].split()
			j = d[1]
			b = self.month_name(t[1])
			t = t[0] + ' ' + b + ' ' + t[2] + ' ' + j
			return self.f_date(t)
		if m == 'bantenraya':
			t = d[0].replace('|','').split(',')[1].split()
			b = self.month_name(t[1])
			t = t[0] + ' ' + b + ' ' + t[2] + ' ' + t[3]
			return self.f_date(t)
		if m == 'hargo' or m == 'kalsel.prokal' or m == 'siwalimanews' or m == 'hukumonline':
			t = d[0].split(',')[1].split()
			b = self.month_name(t[1])
			t = t[0] + ' ' + b + ' ' + t[2]
			return self.f_date(t)
		if m == 'republika':
			t = d[0].split(',')
			j = t[2].replace('WIB','')
			t = t[1].split()
			b = self.month_name(t[1])
			t = t[0] + ' ' + b + ' ' + t[2] + ' ' + j
			return self.f_date(t)
		if m == 'suaramerdeka':
			t = d[0].replace('|','').split()
			b = self.month_name(t[1])
			t = t[0] + ' ' + b + ' ' + t[2] + ' ' + t[3]
			return self.f_date(t)
		if m == 'batamnews':
			t = d[1].replace(',','').split()
			b = self.month_name(t[2])
			t = t[1] + ' ' + b + ' ' + t[3] + ' ' + t[4]
			return self.f_date(t)
		if m == 'damai' or m == 'suarakarya':
			t = self.d_now()
			return self.f_date(t)
		if m == 'gatra':
			t = d[1].split(',')[1].split()
			b = self.month_name(t[1])
			t = t[0] + ' ' + b + ' ' + t[2] + ' ' + t[3]
			return self.f_date(t)
		if m == 'kumparan':
			t = d[0].replace('-','').split()
			b = self.month_name(t[1])
			t = t[0] + ' ' + b + ' ' + t[2] + ' ' + t[3]
			return self.f_date(t)
		if  m == 'padek':
			i = self.f_index(d,'Editor')
			t = d[i[0]+1].split('-')[1]
			t = t.split()
			b = self.month_name(t[1])
			t = t[0] + ' ' + b + ' ' + t[2] + ' ' + t[3]
			return self.f_date(t)
		if m == 'tabloidjubi':
			t = d[0].split(',')[1].split()
			b = self.month_name(t[1])
			t = t[0] + ' ' + b + ' ' + t[2] + ' ' + t[4]
			return self.f_date(t)
		if m == 'waspada' or m == 'voaindonesia' or m == 'hipwee':
			t = d[0].split()
			t = str(self.t_ago(t))
			return self.f_date(t)
		if m == 'australiaplus':
			t = d[2].split()
			if 'ago' in t:
				# t = d[0].split()
				t = str(self.t_ago(t))
			else:
				b = self.month_name(t[1])
				t = t[0] + ' ' + b + ' ' + t[2]
			return self.f_date(t)
		if m == 'dailysocial' or m == 'dw':
			t = d[-1].strip()
			return self.f_date(t)
		if m == 'goal':
			t = d[0]
			if ":" in t :
				t = str(datetime.now())
				t = t.split()
				t[-1] = d[0].strip()
				t = ' '.join(t)
			return self.f_date(t)
			# return t
		else:
			# if not d:
			# 	return self.d_now()
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
	def d_now(self):
		return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	# a is array [number, string about hours, days, or months]
	def t_ago(self,a):
		n = a[0]
		s = a[1]
		if s == 'min' or s == 'mins' or s == 'menit':
			return datetime.now() - timedelta(minutes=int(n))
		if s == 'hour' or s == 'hours' or s == 'jam':
			return datetime.now() - timedelta(hours=int(n))
		if s == 'day' or s == 'days' or s == 'hari':
			return datetime.now() - timedelta(days=int(n))
		if s == 'month' or s == 'months' or s == 'bulan':
			return datetime.now() - timedelta(month=int(n))
		else :
			return datetime.now()

	def r_index(self,a,k):
		try:
			i = self.f_index(a,k)[0]
			del a[i]
		except IndexError:
			pass
		return a

	def temp(self,f,t):
		file = open('temp/'+f+'.txt', 'a')
		t = self.s_undecode(t)
		file.write(t)
		file.close()
		
	# delete file
	# def e_temp(self):
	# 	return open("temp.txt","w").close()

	def p_content(self,response,c,f):
		r = response.css(c).extract()
		return self.temp(f,r)

