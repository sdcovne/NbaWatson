
from flask import Flask, render_template, redirect, url_for, request
import sqlite3
import os
import datetime
import basicStatistics


#os.system("python newsDatabase.py")

names = []

def toString(value):
	if abs(value) > 999999:
	      vs = str(value)
	      value_str = "$" + vs[:len(vs)-6] + "," + vs[len(vs)-6:len(vs)-3] + "," + vs[len(vs)-3:]
	      return value_str
	else:
		 vs = str(value)
		 value_str = "$" + vs[:len(vs)-3] + "," + vs[len(vs)-3:]
		 return value_str

def urlize(string):
	s = string.lower()
	s  = s.replace(" ", "_")
	return s

def normalize(string):
	array = list(string)
	array[0] = array[0].upper()
	space_index = array.index("_")
	array[space_index+1] = array[space_index+1].upper()
	del array[space_index]
	array.insert(space_index, " ")
	s = "".join(array)
	#s = s.replace("-", " ")
	return s

news_row = []
ws_over_year= []
ows_over_year= []
dws_over_year= []
ws_48_over_year = []
game_played = []


app = Flask(__name__)


@app.route('/search', methods = ['POST', 'GET'])
def search():
        
	if request.method  == 'POST':
		player_name = request.form['nm']
	else:
                
		player_name = request.args.get('nm')
		print(request.args)
		print(player_name)

        #print urlize(player_name


	return redirect('/player/{}'.format(urlize(player_name)))
        

@app.route('/', methods = ['POST', 'GET'])
def index():

        return render_template('home.html')
        
@app.route('/player/<player_name>')
def getUrl(player_name):

		global ws_over_year, ows_over_year, dws_over_year, ws_48_over_year

		NBA_money_revenue = 7400000000
		NBA_money_revenue_to_players = NBA_money_revenue/2
		rs_games = 1230
		NBA_single_win_value = NBA_money_revenue_to_players/rs_games
		
		ws_last_rs = 0

		ws_over_year = []
		ows_over_year = []
		dws_over_year = []
		ws_48_over_year = []
		game_played = []


		labels = ['2013-14', '2014-15', '2015-16', '2016-17', '2017-18']

		

		today = datetime.datetime.now()
		this_year = today.year
		this_month = today.month
		this_day = today.day

	

		conn = sqlite3.connect('NBA_data.db')
		conn.row_factory = sqlite3.Row 
		c = conn.cursor()
		getData = c.execute('SELECT * FROM playersAllInfo WHERE name like ?', (normalize(player_name),))
		row = getData.fetchone()
		conn.commit()

		i = 8

		while i >= 4:
			conn = sqlite3.connect('NBA_data.db')
			conn.row_factory = sqlite3.Row 
			c = conn.cursor()
			getData_ws = c.execute('SELECT * FROM ws_1{} WHERE name like ?'.format(i), (normalize(player_name),))
			row_ws = getData_ws.fetchone()
			if row_ws == None:
				i -= 1
				continue
			else:
				ws_over_year.append(row_ws[1])
				ows_over_year.append(row_ws[2])
				dws_over_year.append(row_ws[3])
				ws_48_over_year.append(row_ws[4])
				game_played.append(row_ws[5])
			conn.commit()
			i -= 1
		

		ws_over_year.reverse()
		ows_over_year.reverse()
		dws_over_year.reverse()
		ws_48_over_year.reverse()

		if len(ws_48_over_year) < 5:
			missing_seasons = 5 - len(ws_48_over_year)
			i = 0
			while i < missing_seasons:
				ws_48_over_year.insert(0, 0)
				i +=1
	

		if len(ws_over_year) < 5:
			missing_seasons = 5 - len(ws_over_year)
			i = 0
			while i < missing_seasons:
				ws_over_year.insert(0, 0)
				i +=1

		if len(ows_over_year) < 5:
			missing_seasons = 5 - len(ows_over_year)
			i = 0
			while i < missing_seasons:
				ows_over_year.insert(0, 0)
				i +=1

		if len(dws_over_year) < 5:
			missing_seasons = 5 - len(dws_over_year)
			i = 0
			while i < missing_seasons:
				dws_over_year.insert(0, 0)
				i +=1



		


		ws_max = sorted(ws_over_year)[-1]
		ws_min = sorted(ws_over_year)[0]


		ws_last_rs = ws_over_year[-1]
		ws_48_last_rs = ws_48_over_year[-1]

		x_values = [0,1,2,3,4]

		lr_ws = basicStatistics.linear_regression(x_values, ws_over_year)

		lr_ws_48 = basicStatistics.linear_regression(x_values, ws_48_over_year)

		try:

			r_squared_ws = basicStatistics.r_squared(x_values, ws_over_year)

			r_squared_ws_48 = basicStatistics.r_squared(x_values, ws_48_over_year)


		except:
			r_squared_ws = 0

			r_squared_ws_48 = 0

		r_ws= basicStatistics.r(x_values, ws_over_year)

		r_ws_48= basicStatistics.r(x_values, ws_48_over_year)

		s_ws = basicStatistics.s(x_values, ws_over_year)

		s_ws_48 = basicStatistics.s(x_values, ws_48_over_year)

		mse_ws = basicStatistics.sigma(x_values, ws_over_year)
                
		mse_ws_48= basicStatistics.sigma(x_values, ws_48_over_year)

		prevision_ws = basicStatistics.slope(x_values, ws_over_year) * (x_values[-1] +1) + basicStatistics.intercept(x_values, ws_over_year)

		prevision_ws_48 = basicStatistics.slope(x_values, ws_48_over_year) * (x_values[-1] +1) + basicStatistics.intercept(x_values, ws_48_over_year)

		pv = int(ws_last_rs * NBA_single_win_value)

		ppv = int(ws_last_rs * NBA_single_win_value * (82/game_played[0]))

		conn = sqlite3.connect('NBA_data.db')

		conn.row_factory = sqlite3.Row 

		c = conn.cursor()

		getData = c.execute('SELECT * FROM salaries WHERE name like ?', (normalize(player_name),))

		row_salary = getData.fetchone()

		conn.commit()  

		salary_last_rs = int(row_salary[2])

		gap_pv = pv - salary_last_rs

		gap_ppv = ppv - salary_last_rs

		gap_pv_pct = abs(round(float(gap_pv)/pv * 100, 2))

		gap_ppv_pct = abs(round(float(gap_ppv)/ppv * 100,2))

		return render_template('player.html', player_name = player_name, nor = normalize, row = row ,  ws_over_year = ws_over_year,  int = int, str = str, this_year = this_year, this_month = this_month, this_day = this_day, round = round, len = len, type = type, labels = labels, ws_max = ws_max, ows_over_year = ows_over_year, dws_over_year = dws_over_year, ws_min = ws_min, ws_48_over_year = ws_48_over_year, lr_ws = lr_ws, r_squared_ws = r_squared_ws, r_ws = r_ws, lr_ws_48 = lr_ws_48,  r_squared_ws_48 = r_squared_ws_48, r_ws_48 = r_ws_48, s_ws = s_ws, s_ws_48 = s_ws_48, mse_ws = mse_ws, mse_ws_48 = mse_ws_48, prevision_ws = prevision_ws, prevision_ws_48 = prevision_ws_48, pv = pv, ppv = ppv, player_value = toString(pv), p_player_value = toString(ppv), salary = toString(salary_last_rs), gap_pv = toString(gap_pv), gap_ppv = toString(gap_ppv), gap_pv_pct = gap_pv_pct, gap_ppv_pct = gap_ppv_pct, gapPV = gap_pv, gapPPV = gap_ppv)

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/pv')
def pv():
		conn = sqlite3.connect('NBA_data.db')
		conn.row_factory = sqlite3.Row 
		c = conn.cursor()
		getData = c.execute('SELECT * FROM pv')
		return render_template('pv.html', rows = getData.fetchall(), urlz = urlize)


@app.route('/ws',  methods=['GET'])
def ws():
		global names

		conn = sqlite3.connect('NBA_data.db')
		conn.row_factory = sqlite3.Row 
		c = conn.cursor()
		getData = c.execute('SELECT * FROM ws_18')
		season = "2017-18"

		#data_to_url = getData.fetchall()


		return render_template('ws.html', rows = getData.fetchall(), season = "2017-18", urlz = urlize)


"""
@app.route('/ws_2018', methods=['GET'])
def ws_2018():
		conn = sqlite3.connect('NBA_data.db')
		conn.row_factory = sqlite3.Row 
		c = conn.cursor()
		getData = c.execute('SELECT * FROM ws_2018')
		return render_template('ws.html', rows = getData.fetchall(), season = "2017-18")
"""

@app.route('/ws_2017', methods=['GET'])
def ws_2017():
		conn = sqlite3.connect('NBA_data.db')
		conn.row_factory = sqlite3.Row 
		c = conn.cursor()
		getData = c.execute('SELECT * FROM ws_17')
		return render_template('ws.html', rows = getData.fetchall(), season = "2016-17", urlz = urlize)



@app.route('/ws_2016', methods=['GET'])
def ws_2016():
		conn = sqlite3.connect('NBA_data.db')
		conn.row_factory = sqlite3.Row 
		c = conn.cursor()
		getData = c.execute('SELECT * FROM ws_16')
		return render_template('ws.html', rows = getData.fetchall(), season = "2015-16", urlz = urlize)



@app.route('/ws_2015', methods=['GET'])
def ws_2015():
		conn = sqlite3.connect('NBA_data.db')
		conn.row_factory = sqlite3.Row 
		c = conn.cursor()
		getData = c.execute('SELECT * FROM ws_15')
		return render_template('ws.html', rows = getData.fetchall(), season = "2014-15", urlz = urlize)

@app.route('/ws_2014', methods=['GET'])
def ws_2014():
		conn = sqlite3.connect('NBA_data.db')
		conn.row_factory = sqlite3.Row 
		c = conn.cursor()
		getData = c.execute('SELECT * FROM ws_14')
		return render_template('ws.html', rows = getData.fetchall(), season = "2013-14", urlz = urlize)


@app.route('/conctat')
def conctat():
        return render_template('conctat.html')

@app.route('/predictions')
def how_to_pv():
	return render_template("predictions.html")

@app.route('/salaries')
def salaries():
		conn = sqlite3.connect('NBA_data.db')
		conn.row_factory = sqlite3.Row 
		c = conn.cursor()
		getData = c.execute('SELECT * FROM salaries')
		return render_template('salaries.html', rows = getData.fetchall(), urlz = urlize, int = int, round = round)

@app.route('/news')
def news():

        #os.system("python newsDatabase.py")

        global news_row

        i = 1

        conn = sqlite3.connect('NBA_data.db')

        conn.row_factory = sqlite3.Row 

        c = conn.cursor()

        getData = c.execute('SELECT * FROM news')

        rows = getData.fetchall()

        news = []

        i = 0

        while i < len(rows):

        	news_row.append(rows[i])

        	news_row.append(rows[i+1])

        	news.append(news_row)

        	news_row = []

        	i += 2


        return render_template("news.html", rows = getData.fetchall(), news=news)


if __name__ == '__main__':
	app.run(debug = True)
