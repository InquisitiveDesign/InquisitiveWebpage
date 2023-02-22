from calculator import app, db
from flask import Flask, render_template, request, jsonify, logging, make_response, json, redirect
from calculator.my_bearing import my_bearing
from calculator.bearing_selector import bearing_selector
from calculator.keydcal import key_d
from calculator.shaft_design import shaft_combined, shaft_from_rigiditymodulus
from calculator.Beam_design import beamd
import json

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def index():
	return render_template('index.html')

@app.route('/about_us', methods=['GET'])
def about_us():
	return render_template('about.html')

@app.route('/bearing_selector', methods=['GET','POST'])
def bearing_selector():
	return render_template('bearing_cal.html')

@app.route('/bearing_result', methods=['POST'])
def bearing_result():
	if request.method == 'POST':
		Data = request.get_json()
		bore_dia = Data["shaftdia"]
		RPM = Data["ang_velo"]
		VFC = Data["vfc"]
		HFC = Data["hfc"]
		AFC = Data["afc"]
		hr_eachdy = Data["hrperday"]
		yr = Data["exp_years"]

		if Data["beartype"] == "Deep Groove Ball Bearing":
			btype = "B"
		else:
			btype = "R"
		
		if Data["rfact"] == "Inner Race":
			Rotation_fact = 1
		else:
			Rotation_fact = 1.2

		output = bearing_selector(bore_dia,RPM,VFC,HFC,AFC,Rotation_fact,yr,hr_eachdy,btype)
		list1 = ['Bearing_desigination','Bore','OD','Width','Cd','Co','Ref_Speed','Lim_Speed','Required_Cd','Bearing_type']
		result = dict(zip(list1,output))
		response = json.dumps(result, indent=10)
		return response

@app.route('/shaftdesign_rigiditybased', methods=['GET','POST'])
def shaftdesign_rigiditybased():
	return render_template('shaftrigiditydesign_cal.html')

@app.route('/shaft_rigid', methods=['POST'])
def shaft_rigid():
	if request.method == 'POST':
		Data = request.get_json()
		Theta = float(Data["thetamax"])
		G = float(Data["rigidity"])
		TM = float(Data["torsionmom"])
		L = float(Data["shaftlength"])
		Rdia = float(Data["diar"])
		rig_outcome = shaft_from_rigiditymodulus(Theta,G,TM,L,Rdia)

		list1 = ['outerdia', 'innerdia']
		result = dict(zip(list1,rig_outcome))
		response = json.dumps(result, indent=2)
		return response

@app.route('/shaftdesign_strengthbased', methods=['GET','POST'])
def shaftdesign_strengthbased():
	return render_template('shaftdesign_cal.html')

@app.route('/shaft_rec', methods=['POST'])
def shaft_rec():
	if request.method == 'POST':
		Data = request.get_json()
		BM = float(Data["bendingmom"])
		TM = float(Data["torsionalmom"])
		S = float(Data["yield"])
		F = float(Data["fos"])
		dr = float(Data["diaratio"])

		#loadtype
		if Data["loadtype"] == "Gradual Load":
			LT = "G"
		elif Data["loadtype"] == "Minor Shock Load":
			LT = "M"
		else:
			LT = "H"
		
		#theory
		if Data["theory"] == "Max Shear Stress Theory":
			Th = "S"
		else:
			Th = "D"

		#designbase
		if Data["designbase"] == "Torsion Equivalent":
			db = "T"
		else:
			db = "B"

		outcome = shaft_combined(BM,TM,S,F,LT,Th,db,dr)
		list1 = ['outerdia', 'innerdia']
		result = dict(zip(list1,outcome))
		response = json.dumps(result, indent=2)
		return response
	
@app.route('/keydesign', methods=['GET','POST'])
def keydesign():
	return render_template('keydesign_cal.html')

@app.route('/key_data', methods=['POST'])
def key_data():
	if request.method == 'POST':
		Data = request.get_json()
		P = float(Data["power"])
		N = float(Data["nspeed"])
		S = float(Data["yield"])
		F = float(Data["fos"])
		D = float(Data["sdia"])

		if Data["theory"] == "Max Shear Stress Theory":
			Th = "S"
		else:
			Th = "D"
		
		if Data["keytype"] == "Square key":
			Kt = "Sq"
		else:
			Kt = "Fl"
			
		R = key_d(P,N,S,F,D,Th,Kt)
		list1 = ['L', 'B', 'H']
		result = dict(zip(list1,R))
		response = json.dumps(result, indent=3)
		return response

@app.route('/beamdesign', methods=['GET','POST'])
def beamdesign():
	return render_template('beamdesign_cal.html')

@app.route('/beam_data', methods=['POST'])
def beam_data():
	if request.method == 'POST':
		Data = request.get_json()
		bl = float(Data['form1']['beamlength'])
		ns = float(Data['form1']['supportnum'])
		nl = float(Data['form1']['loadnum'])
			
		supportloc = []
		supporttype = []
		supportdirec = []
		loadloc = []
		loadtype = []
		loaddirec = []
		loadvalue = []
		suppdata = Data['form2']
		loaddata = Data['form3']

		for S in range(len(suppdata)-1):
			supportloc.append(float(suppdata[S+1]['col2']))
			supporttype.append(suppdata[S+1]['col3'])
			supportdirec.append(suppdata[S+1]['col4'])
			
		for L in range(len(loaddata)-1):
			loadloc.append(float(loaddata[L+1]['col2']))
			loadtype.append(loaddata[L+1]['col3'])
			loaddirec.append(loaddata[L+1]['col4'])
			loadvalue.append(float(loaddata[L+1]['col5']))

		supportrxn = beamd(bl,ns,nl,supportloc,supporttype,supportdirec,loadloc,loadtype,loaddirec,loadvalue)

		list1 = ['R1', 'R2']
		result = dict(zip(list1,supportrxn))
		response = json.dumps(result, indent=2)
		return response
	
