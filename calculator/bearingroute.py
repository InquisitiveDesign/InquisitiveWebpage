from calculator import app, db
from flask import Flask, render_template, request, jsonify, logging, make_response, json
from calculator.bearforms import UserForm
from calculator.my_bearing import my_bearing
from calculator.bearing_selector import bearing_selector
from calculator.keydcal import key_d
from calculator.shaft_design import shaft_combined, shaft_from_rigiditymodulus
from calculator.Beam_design import beamd
from calculator import bearforms
from calculator.models import Infoform, Dtform
import json

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def index():
	return render_template('index.html')

@app.route('/bearing cal', methods=['GET'])
def bear_cal():
	return render_template('bearing_cal.html')

@app.route('/bearing cal', methods=['GET','POST'])
def result():
	bore_dia = float(request.form["shaftdia"])
	RPM = float(request.form["ang_velo"])
	VFC = float(request.form["vfc"])
	HFC = float(request.form["hfc"])
	AFC = float(request.form["afc"])
	
	if request.form["rfact"] == "Inner Race":
		Rotation_fact = 1
	else:
		Rotation_fact = 1.2

	hr_eachdy = float(request.form["hrperday"])
	yr = float(request.form["exp_years"])
	output = bearing_selector(bore_dia,RPM,VFC,HFC,AFC,Rotation_fact,yr,hr_eachdy)
	return render_template('bearing_cal.html',output = output)

@app.route('/shaftrigid cal', methods=['GET'])
def shaftrigid_cal():
	return render_template('shaftrigiditydesign_cal.html')

@app.route('/shaftrigid cal', methods=['GET','POST'])
def shaft_rigid():
	Theta = request.form["thetamax"]
	G = request.form["rigidity"]
	TM = request.form["torsionmom"]
	L = request.form["shaftlength"]
	Rdia = request.form["diar"]
	rig_outcome = shaft_from_rigiditymodulus(Theta,G,TM,L,Rdia)
	return render_template('shaftrigiditydesign_cal.html',rig_outcome = rig_outcome)

@app.route('/shaftd cal', methods=['GET'])
def shaftd_cal():
	return render_template('shaftdesign_cal.html')

@app.route('/shaftd cal', methods=['GET','POST'])
def shaft_rec():
	BM = request.form["bendingmom"]
	TM = request.form["torsionalmom"]
	S = request.form["yield"]
	F = request.form["fos"]
	dr = request.form["diaratio"]

	#loadtype
	if request.form["loadtype"] == "Gradual Load":
		LT = "G"
	elif request.form["loadtype"] == "Minor Shock Load":
		LT = "M"
	else:
		LT = "H"
	
	#theory
	if request.form["theory"] == "Max Shear Stress Theory":
		Th = "S"
	else:
		Th = "D"

	#designbase
	if request.form["designbase"] == "Torsion Equivalent":
		db = "T"
	else:
		db = "B"

	outcome = shaft_combined(BM,TM,S,F,LT,Th,db,dr)
	return render_template('shaftdesign_cal.html',outcome = outcome)

@app.route('/keyd cal', methods=['GET'])
def keyd_cal():
	return render_template('keydesign_cal.html')


@app.route('/keyd cal', methods=['GET','POST'])
def key_rec():
	P = float(request.form["power"])
	N = float(request.form["nspeed"])
	S = float(request.form["yield"])
	F = float(request.form["fos"])
	D = float(request.form["sdia"])

	if request.form["theory"] == "Max Shear Stress Theory":
		Th = "S"
	else:
		Th = "D"

	R = key_d(P,N,S,F,D,Th)
	return render_template('keydesign_cal.html',R = R)

@app.route('/beamd_cal', methods=['GET'])
def beamd_cal():
	return render_template('beamdesign_cal.html')

@app.route('/beam_data', methods=['GET','POST'])
def beam_data():
	if request.method == 'POST':
		Data = request.get_json()
		#print("Data: ", Data)

		bl = float(Data['form1']['beamlength'])
		#print("Beam length: ",BL)
		ns = float(Data['form1']['supportnum'])
		#print("Support number: ",Snum)
		nl = float(Data['form1']['loadnum'])
		#print("Load number: ",Lnum)
			
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

		#print("supportrxn: ",supportrxn)
		list1 = ['R1', 'R2']
		result = dict(zip(list1,supportrxn))
		print(result)
		#d = json.dumps(result, indent=2)
		response = json.dumps(result, indent=2)
		print("response data type: ",type(response))
		print(response)
		return response
