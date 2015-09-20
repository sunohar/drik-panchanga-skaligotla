#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.4 on Tue Jan 22 15:06:05 2013

# gui.py -- Displays a wxPython GUI for panchangam calculations
#
# Copyright (C) 2013 Satish BD  <bdsatish@gmail.com>
# Downloaded from https://github.com/bdsatish/drik-panchanga
#
# This file is part of the "drik-panchanga" Python library
# for computing Hindu luni-solar calendar based on the Swiss ephemeris
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import wx
import json
import re

from time import strptime
from pytz import timezone, utc
from datetime import datetime
from panchanga import *
import difflib

# begin wxGlade: extracode
# end wxGlade

format_time = lambda t: "%02d:%02d:%02d" % (t[0], t[1], t[2])

class Panchanga(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: Panchanga.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.dateTxt = wx.TextCtrl(self, wx.ID_ANY, "23/01/2013")
        self.searchBtn = wx.Button(self, wx.ID_ANY, "Search")
        self.placeTxt = wx.TextCtrl(self, wx.ID_ANY, "Bangalore")
        self.computeBtn = wx.Button(self, wx.ID_ANY, "Compute")
        self.latTxt = wx.TextCtrl(self, wx.ID_ANY, "12.97194", style=wx.TE_PROCESS_TAB)
        self.lonTxt = wx.TextCtrl(self, wx.ID_ANY, "77.59369", style=wx.TE_PROCESS_TAB)
        self.tzTxt = wx.TextCtrl(self, wx.ID_ANY, "+5.5")
        self.samvatTxt = wx.StaticText(self, wx.ID_ANY, "Nandana samvatsara")
        self.masaTxt = wx.StaticText(self, wx.ID_ANY, u"Pu\u1e63ya  m\u0101sa")
        self.rituTxt = wx.StaticText(self, wx.ID_ANY, u"Hemanta \u1e5btu")
        self.tithiTxt = wx.StaticText(self, wx.ID_ANY, u"\u015aukla pak\u1e63a dv\u0101da\u1e63\u012b   ")
        self.tithiTimeTxt = wx.StaticText(self, wx.ID_ANY, "28:43:28")
        self.nakTxt = wx.StaticText(self, wx.ID_ANY, u"Rohi\u1e47\u012b")
        self.nakTimeTxt = wx.StaticText(self, wx.ID_ANY, "06:57:56")
        self.yogaTxt = wx.StaticText(self, wx.ID_ANY, "Brahma")
        self.yogaTimeTxt = wx.StaticText(self, wx.ID_ANY, "08:32:02")
        self.karanaTxt = wx.StaticText(self, wx.ID_ANY, "Bhava")
        self.karanaTimeTxt = wx.StaticText(self, wx.ID_ANY, "15:27:47")
        self.varaTxt = wx.StaticText(self, wx.ID_ANY, u"Budhav\u0101ra  ")
        self.aharTxt = wx.StaticText(self, wx.ID_ANY, "KaliDay 1867850")
        self.sakaTxt = wx.StaticText(self, wx.ID_ANY, u"\u015a\u0101liv\u0101hana \u015baka 1934 ")
        self.kaliTxt = wx.StaticText(self, wx.ID_ANY, "GataKali 5113")
        self.sunriseTxt = wx.StaticText(self, wx.ID_ANY, "06:47:38")
        self.sunsetTxt = wx.StaticText(self, wx.ID_ANY, "18:15:31")
        self.duraTxt = wx.StaticText(self, wx.ID_ANY, "11:27:52")
        self.sizer_1_staticbox = wx.StaticBox(self, wx.ID_ANY, "")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_TEXT_ENTER, self.calculate_panchanga, self.dateTxt)
        self.Bind(wx.EVT_BUTTON, self.search_location, self.searchBtn)
        self.Bind(wx.EVT_TEXT_ENTER, self.search_location, self.placeTxt)
        self.Bind(wx.EVT_BUTTON, self.calculate_panchanga, self.computeBtn)
        self.Bind(wx.EVT_TEXT_ENTER, self.set_place, self.latTxt)
        self.Bind(wx.EVT_TEXT, self.set_place, self.latTxt)
        self.Bind(wx.EVT_TEXT_ENTER, self.set_place, self.lonTxt)
        self.Bind(wx.EVT_TEXT, self.set_place, self.lonTxt)
        self.Bind(wx.EVT_TEXT_ENTER, self.set_place, self.tzTxt)
        self.Bind(wx.EVT_TEXT, self.set_place, self.tzTxt)
        # end wxGlade

        now = datetime.now()
        self.dateTxt.SetValue("%d/%d/%d" % (now.day, now.month, now.year))
        self.init_db()

    def __set_properties(self):
        # begin wxGlade: Panchanga.__set_properties
        self.SetTitle("Indian Calendar")
        self.SetSize((625, 575))
        self.SetToolTip(wx.ToolTip("Can also be entered as: 77d 35' 37\""))
        self.dateTxt.SetToolTip(wx.ToolTip("Enter date and then Location below. Negative years are treated as per proleptic Gregorian calendar."))
        self.dateTxt.SetFocus()
        self.searchBtn.SetForegroundColour(wx.Colour(44, 44, 44))
        self.placeTxt.SetToolTip(wx.ToolTip("Type location, click Search. If the search fails, enter Latitude, Longitude and Time zone directly below. Lastly, \"Compute\". Enter ASCII names only."))
        self.latTxt.SetToolTip(wx.ToolTip("Can also be entered as: 12d 58' 19\""))
        self.tzTxt.SetToolTip(wx.ToolTip("In hours. Positive values are east of UTC and negative, west of UTC."))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: Panchanga.__do_layout
        self.sizer_1_staticbox.Lower()
        sizer_1 = wx.StaticBoxSizer(self.sizer_1_staticbox, wx.HORIZONTAL)
        grid_sizer_1 = wx.GridSizer(17, 3, 0, 0)
        label_1 = wx.StaticText(self, wx.ID_ANY, "")
        grid_sizer_1.Add(label_1, 0, 0, 0)
        label_2 = wx.StaticText(self, wx.ID_ANY, u"D\u1e5bg-ga\u1e47ita Pa\u00f1c\u0101\u1e45ga", style=wx.ALIGN_CENTER | wx.ALIGN_RIGHT)
        label_2.SetMinSize((319, 24))
        label_2.SetFont(wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        grid_sizer_1.Add(label_2, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        label_4 = wx.StaticText(self, wx.ID_ANY, "")
        grid_sizer_1.Add(label_4, 0, 0, 0)
        label_3 = wx.StaticText(self, wx.ID_ANY, "Date (DD/MM/YYYY)")
        grid_sizer_1.Add(label_3, 0, wx.ALIGN_CENTER, 0)
        grid_sizer_1.Add(self.dateTxt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 0)
        grid_sizer_1.Add(self.searchBtn, 0, 0, 0)
        label_6 = wx.StaticText(self, wx.ID_ANY, "Location")
        grid_sizer_1.Add(label_6, 0, wx.ALIGN_CENTER, 0)
        grid_sizer_1.Add(self.placeTxt, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
        grid_sizer_1.Add(self.computeBtn, 0, 0, 0)
        label_31 = wx.StaticText(self, wx.ID_ANY, "Latitude")
        grid_sizer_1.Add(label_31, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        label_32 = wx.StaticText(self, wx.ID_ANY, "Longitude")
        grid_sizer_1.Add(label_32, 0, wx.ALIGN_CENTER, 0)
        label_33 = wx.StaticText(self, wx.ID_ANY, "Time zone")
        grid_sizer_1.Add(label_33, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.latTxt, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT, 0)
        grid_sizer_1.Add(self.lonTxt, 0, wx.ALIGN_CENTER | wx.ALIGN_RIGHT, 0)
        grid_sizer_1.Add(self.tzTxt, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        static_line_1 = wx.StaticLine(self, wx.ID_ANY)
        grid_sizer_1.Add(static_line_1, 0, wx.EXPAND, 0)
        static_line_2 = wx.StaticLine(self, wx.ID_ANY)
        grid_sizer_1.Add(static_line_2, 0, wx.EXPAND, 0)
        static_line_3 = wx.StaticLine(self, wx.ID_ANY)
        grid_sizer_1.Add(static_line_3, 0, wx.EXPAND, 0)
        grid_sizer_1.Add(self.samvatTxt, 0, wx.ALIGN_CENTER, 0)
        grid_sizer_1.Add(self.masaTxt, 0, wx.ALIGN_CENTER, 0)
        grid_sizer_1.Add(self.rituTxt, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        label_7 = wx.StaticText(self, wx.ID_ANY, "Tithi")
        grid_sizer_1.Add(label_7, 0, wx.ALIGN_CENTER, 0)
        grid_sizer_1.Add(self.tithiTxt, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.tithiTimeTxt, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        label_13 = wx.StaticText(self, wx.ID_ANY, u"Nak\u1e63atra  ")
        grid_sizer_1.Add(label_13, 0, wx.ALIGN_CENTER, 0)
        grid_sizer_1.Add(self.nakTxt, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.nakTimeTxt, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        label_16 = wx.StaticText(self, wx.ID_ANY, "Yoga")
        grid_sizer_1.Add(label_16, 0, wx.ALIGN_CENTER, 0)
        grid_sizer_1.Add(self.yogaTxt, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.yogaTimeTxt, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        label_19 = wx.StaticText(self, wx.ID_ANY, u"Kara\u1e47a  ")
        grid_sizer_1.Add(label_19, 0, wx.ALIGN_CENTER, 0)
        grid_sizer_1.Add(self.karanaTxt, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.karanaTimeTxt, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        label_22 = wx.StaticText(self, wx.ID_ANY, u"V\u0101ra  ")
        grid_sizer_1.Add(label_22, 0, wx.ALIGN_CENTER, 0)
        grid_sizer_1.Add(self.varaTxt, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        label_24 = wx.StaticText(self, wx.ID_ANY, "")
        grid_sizer_1.Add(label_24, 0, 0, 0)
        grid_sizer_1.Add(self.aharTxt, 0, wx.ALIGN_CENTER, 0)
        grid_sizer_1.Add(self.sakaTxt, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.kaliTxt, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        static_line_4 = wx.StaticLine(self, wx.ID_ANY)
        grid_sizer_1.Add(static_line_4, 0, wx.EXPAND, 0)
        static_line_5 = wx.StaticLine(self, wx.ID_ANY)
        grid_sizer_1.Add(static_line_5, 0, wx.EXPAND, 0)
        static_line_6 = wx.StaticLine(self, wx.ID_ANY)
        grid_sizer_1.Add(static_line_6, 0, wx.EXPAND, 0)
        label_34 = wx.StaticText(self, wx.ID_ANY, "Sunrise")
        grid_sizer_1.Add(label_34, 0, wx.ALIGN_CENTER, 0)
        label_37 = wx.StaticText(self, wx.ID_ANY, "Sunset")
        grid_sizer_1.Add(label_37, 0, wx.ALIGN_CENTER, 0)
        label_5 = wx.StaticText(self, wx.ID_ANY, "Day duration")
        grid_sizer_1.Add(label_5, 0, wx.ALIGN_CENTER, 0)
        grid_sizer_1.Add(self.sunriseTxt, 0, wx.ALIGN_CENTER, 0)
        grid_sizer_1.Add(self.sunsetTxt, 0, wx.ALIGN_CENTER, 0)
        grid_sizer_1.Add(self.duraTxt, 0, wx.ALIGN_CENTER, 0)
        label_10 = wx.StaticText(self, wx.ID_ANY, "")
        grid_sizer_1.Add(label_10, 0, 0, 0)
        label_9 = wx.StaticText(self, wx.ID_ANY, "https://github.com/bdsatish/drik-panchanga")
        grid_sizer_1.Add(label_9, 0, wx.ALIGN_CENTER, 0)
        sizer_1.Add(grid_sizer_1, 1, 0, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

    def calculate_panchanga(self, event):  # wxGlade: Panchanga.<event_handler>
        jd = gregorian_to_jd(self.parse_date())
        self.set_place(event)
        place = self.place

        ti = tithi(jd, place)
        nak = nakshatra(jd, place)
        yog = yoga(jd, place)
        mas = masa(jd, place)
        rtu = ritu(mas[0])

        kar = karana(jd, place)
        vara = vaara(jd)
        srise = sunrise(jd, place)[1]
        sset = sunset(jd, place)[1]
        kday = ahargana(jd)
        kyear, sakayr = elapsed_year(jd, mas[0])
        samvat = samvatsara(jd, mas[0])
        day_dur = day_duration(jd, place)[1]
        gauri = self.gauri_panchanga(jd)

        # Update GUI one by one. First the easy ones
        self.karanaTxt.SetLabel("%s" % self.karanas[str(kar[0])])
        self.karanaTimeTxt.SetLabel(" -- ")
        self.varaTxt.SetLabel("%s" % self.vaaras[str(vara)])
        self.sunriseTxt.SetLabel(format_time(srise))
        self.sunsetTxt.SetLabel(format_time(sset))
        self.sakaTxt.SetLabel(u"\u015a\u0101liv\u0101hana \u015baka %d" % (sakayr))
        self.kaliTxt.SetLabel("GataKali %d" % (kyear))
        self.aharTxt.SetLabel("KaliDay %d" % (kday))
        self.rituTxt.SetLabel(u"%s \u1e5btu" % (self.ritus[str(rtu)]))
        self.samvatTxt.SetLabel("%s samvatsara" % (self.samvats[str(samvat)]))
        self.duraTxt.SetLabel(format_time(day_dur))

        # Next update the complex ones
        month_name = self.masas[str(mas[0])]
        is_leap = mas[1]
        if is_leap:  month_name = "Adhika " + month_name.lower()
        self.masaTxt.SetLabel(month_name + u" m\u0101sa")

        name, hms = format_name_hms(yog, self.yogas)
        self.yogaTxt.SetLabel(name)
        self.yogaTimeTxt.SetLabel(hms)

        name, hms = format_name_hms(ti, self.tithis)
        self.tithiTxt.SetLabel(name)
        self.tithiTimeTxt.SetLabel(hms)

        name, hms = format_name_hms(nak, self.nakshatras)
        self.nakTxt.SetLabel(name)
        self.nakTimeTxt.SetLabel(hms)

        event.Skip()


    def search_location(self, event):  # wxGlade: Panchanga.<event_handler>
        city = self.placeTxt.Value.title()  # Convert to title-case
        if self.cities.has_key(city):
            self.searchBtn.SetForegroundColour(wx.Colour(0x2C, 0x2C, 0x2C))
            # self.searchBtn.SetLabel("Found!")

            date = self.parse_date()
            city = self.cities[city]
            lat = city['latitude']
            lon = city['longitude']
            tzname = city['timezone']
            self.tzone = timezone(tzname)
            tz_offset = self.compute_timezone_offset()
            self.place = Place(lat, lon, tz_offset)

            # update coordinate textboxes
            self.latTxt.SetValue("%.5f" % lat)
            self.lonTxt.SetValue("%.5f" % lon)
            self.tzTxt.SetValue("%+.2f" % tz_offset)
        else:
            # Find nearest match
            nearest = difflib.get_close_matches(city, self.all_cities, 5)
            all_matches = ""
            for m in nearest:
                all_matches += m + '\n'
            msg = city + ' not found!\n\n' + 'Did you mean any of these?\n\n' + all_matches
            wx.MessageBox(msg, 'Error', wx.OK | wx.ICON_ERROR)

        event.Skip()

    def parse_date(self):
        date = self.dateTxt.Value
        try:
            dt = strptime(date, "%d/%m/%Y")
            date = Date(dt.tm_year, dt.tm_mon, dt.tm_mday)
        except ValueError:
            # Probably the user entered negative year, strptime can't handle it.
            day, month, year = map(int, date.split('/'))
            date = Date(year, month, day)
        return date

    def init_db(self):
        fp = open("cities.json")
        self.cities = json.load(fp)
        self.all_cities = self.cities.keys()
        fp.close()
        sktnames = load_json_file("sanskrit_names.json")
        self.tithis = sktnames["tithis"]
        self.nakshatras = sktnames["nakshatras"]
        self.vaaras = sktnames["varas"]
        self.yogas = sktnames["yogas"]
        self.karanas = sktnames["karanas"]
        self.masas = sktnames["masas"]
        self.samvats = sktnames["samvats"]
        self.ritus = sktnames["ritus"]
        self.gauri = sktnames["gauri"]

    def set_place(self, event):  # wxGlade: Panchanga.<event_handler>
        lat = float(self.latTxt.Value)
        lon = float(self.lonTxt.Value)
        tz = float(self.tzTxt.Value)
        self.place = Place(lat, lon, tz)
        event.Skip()


    def compute_timezone_offset(self):
        date = self.parse_date()
        timezone = self.tzone
        dt = datetime(date.year, date.month, date.day)
        # offset from UTC (in hours). Needed especially for DST countries
        tz_offset = timezone.utcoffset(dt, is_dst = True).total_seconds() / 3600.
        return tz_offset

    def gauri_panchanga(self, jd):
        times = gauri_chogadiya(jd, self.place)
        vara = vaara(jd)
        names = self.gauri[str(vara)]

        return zip(names, times)

# end of class Panchanga

# Global functions
# Load json file ignoring single-line comments (//)
def load_json_file(filename):
    comment = re.compile('(^)?[^\S\n]*/(?:\*(.*?)\*/[^\S\n]*|/[^\n]*)($)?',
                         re.DOTALL | re.MULTILINE)
    with open(filename) as fp:
        content = ''.join(fp.readlines())
        match = comment.search(content)  ## Look for comments
        while match:
            # single line comment
            content = content[:match.start()] + content[match.end():]
            match = comment.search(content)

        return json.loads(content)

# Converts list [12, [23, 45, 50]] to lookup[12] and 23:45:50
def format_name_hms(nhms, lookup):
    name_txt = lookup[str(nhms[0])]
    time_txt = format_time(nhms[1])
    if len(nhms) == 4:
        name_txt += "\n" + lookup[str(nhms[2])]
        time_txt += "\n" + format_time(nhms[3])

    return  name_txt, time_txt


if __name__ == "__main__":
    app = wx.App(False)
    frame_1 = Panchanga(None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()
