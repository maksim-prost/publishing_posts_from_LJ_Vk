Botya = {
	'url':          'https://botya.livejournal.com/',
	'creator':      'botya',
	'list_date' : ('span',{'class':"entryHeaderDate"} ),
	'list_header' : ('a', {'class':"subj-link"}),
	'list_urls' : None,
	'soup':{'class':'b-singlepost-wrapper'},
	'post':{'class':'b-singlepost-body entry-content e-content'},
}

ONB = {
	'url':          'https://onb2017.livejournal.com/',
	'creator':      'ONB 2017',
	'list_date' : ('span',{'class':"date-entryunit__day"}),
	'list_header' : ('h3',{'class':'entryunit__title'}),
	'list_urls' : (lambda tag:tag.parent.name=='h3',),
	'soup':None,
	'post':{'class':'entry-content'},
}

Remi = {
	'url':'https://remi-meisner.livejournal.com/?skip=2',
	'creator':'Реми Майнсер',
	'list_header' : ('a', {'class':"subj-link"}),
	'list_date' :('abbr', {'class':"updated"} ),
	'list_urls':  None,
	'soup':None,
	'post':{'class':'entry-content'},
}

Ballaev = {
	'url':'https://p-balaev.livejournal.com/',
	'creator':'Петр Балаев',
	'list_header' : ('a',{'class':"subj-link"}),
	'list_date' :('abbr' ,{'class':"updated"}),
	'list_urls':  None,
	'soup':None,
	'post':{'class':'entry-content'},
}

Bulgat = {
	'url':'https://bulgat.livejournal.com/',
	'creator':'bulgat',
	'list_date' : ('abbr' ,{'class':"updated"}),
	'list_header' : ('dt', {'class':"entry-title"}),
	'list_urls' : ('a', {'class':"subj-link"}),
	'soup':None,
	'post':{'class':'entry-content'},
}

BlauKraeh = {
	'url':'https://blau-kraehe.livejournal.com/',
	'creator':'Яна Завацкая',
	'list_date' : ('abbr', {'class':"datetime"}),
	'list_header' : ('a', {'class':"subj-link"}),
	'list_urls' : None,
	'soup':{'class':'b-singlepost-wrapper'},
	'post':{'class':"b-singlepost-body entry-content e-content"},

}