# -*- coding: UTF-8 -*-
logger.info("Loading 15 objects to table cal_recurrentevent...")
# fields: id, start_date, start_time, end_date, end_time, name, user, every_unit, every, monday, tuesday, wednesday, thursday, friday, saturday, sunday, max_events, event_type, description
loader.save(create_cal_recurrentevent(1,date(2013,1,1),None,None,None,['Neujahr', "Jour de l'an", "New Year's Day"],None,u'Y',1,True,True,True,True,True,True,True,None,1,u''))
loader.save(create_cal_recurrentevent(2,date(2013,5,1),None,None,None,['Tag der Arbeit', 'Premier Mai', "International Workers' Day"],None,u'Y',1,True,True,True,True,True,True,True,None,1,u''))
loader.save(create_cal_recurrentevent(3,date(2013,7,21),None,None,None,['Nationalfeiertag', 'F\xeate nationale', 'National Day'],None,u'Y',1,True,True,True,True,True,True,True,None,1,u''))
loader.save(create_cal_recurrentevent(4,date(2013,8,15),None,None,None,['Mari\xe4 Himmelfahrt', 'Assomption de Marie', 'Assumption of Mary'],None,u'Y',1,True,True,True,True,True,True,True,None,1,u''))
loader.save(create_cal_recurrentevent(5,date(2013,10,31),None,None,None,['Allerseelen', 'Comm\xe9moration des fid\xe8les d\xe9funts', "All Souls' Day"],None,u'Y',1,True,True,True,True,True,True,True,None,1,u''))
loader.save(create_cal_recurrentevent(6,date(2013,11,1),None,None,None,['Allerheiligen', 'Toussaint', "All Saints' Day"],None,u'Y',1,True,True,True,True,True,True,True,None,1,u''))
loader.save(create_cal_recurrentevent(7,date(2013,11,11),None,None,None,['Waffenstillstand', 'Armistice', 'Armistice with Germany'],None,u'Y',1,True,True,True,True,True,True,True,None,1,u''))
loader.save(create_cal_recurrentevent(8,date(2013,12,25),None,None,None,['Weihnachten', 'No\xebl', 'Christmas'],None,u'Y',1,True,True,True,True,True,True,True,None,1,u''))
loader.save(create_cal_recurrentevent(9,date(2013,3,31),None,None,None,['Ostersonntag', 'P\xe2ques', 'Easter sunday'],None,u'E',1,False,False,False,False,False,False,False,None,1,u''))
loader.save(create_cal_recurrentevent(10,date(2013,4,1),None,None,None,['Ostermontag', 'Lundi de P\xe2ques', 'Easter monday'],None,u'E',1,False,False,False,False,False,False,False,None,1,u''))
loader.save(create_cal_recurrentevent(11,date(2013,5,9),None,None,None,['Christi Himmelfahrt', 'Ascension', 'Ascension of Jesus'],None,u'E',1,False,False,False,False,False,False,False,None,1,u''))
loader.save(create_cal_recurrentevent(12,date(2013,5,20),None,None,None,['Pfingsten', 'Pentec\xf4te', 'Pentecost'],None,u'E',1,False,False,False,False,False,False,False,None,1,u''))
loader.save(create_cal_recurrentevent(13,date(2013,3,29),None,None,None,['Karfreitag', 'Vendredi Saint', 'Good Friday'],None,u'E',1,False,False,False,False,False,False,False,None,1,u''))
loader.save(create_cal_recurrentevent(14,date(2013,2,13),None,None,None,['Aschermittwoch', 'Mercredi des Cendres', 'Ash Wednesday'],None,u'E',1,False,False,False,False,False,False,False,None,1,u''))
loader.save(create_cal_recurrentevent(15,date(2013,2,11),None,None,None,['Rosenmontag', 'Lundi de carnaval', 'Rosenmontag'],None,u'E',1,False,False,False,False,False,False,False,None,1,u''))

loader.flush_deferred_objects()
