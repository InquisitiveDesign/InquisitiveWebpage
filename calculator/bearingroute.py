from calculator import app, db
from flask import Flask, render_template, request
from calculator.bearforms import UserForm
from calculator.my_bearing import my_bearing
from calculator.bearing_selector import bearing_selector
from calculator.keydcal import key_d
from calculator.shaft_design import shaft_combined, shaft_from_rigiditymodulus
from calculator.Beam_design import beamd
from calculator import bearforms
from calculator.models import Infoform, Dtform

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


@app.route('/beam cal', methods=['GET','POST'])
def beamd_cal():
	return render_template('beamdesign_cal.html')
	

@app.route('/beam cal', methods=['POST'])
def beamsolu_cal():
	if request.method == "POST":
		supportloc = request.form["supportloc"]
		supporttype = request.form["supporttype"]
		supportdirec = request.form["supportdirec"]
		loadloc = request.form["loadloc"]
		loadtype = request.form["loadtype"]
		loaddirec = request.form["loaddirec"]
		loadvalue = request.form["loadvalue"]
		design = Dtform(supportloc = supportloc, supporttype = supporttype, supportdirec = supportdirec, loadloc = loadloc, loadtype = loadtype, loaddirec = loaddirec, loadvalue = loadvalue)
		db.session.add(design)
		db.session.commit()

	suppvalues = Dtform.query.all()
	return render_template('beamdesign_cal.html', suppvalues = suppvalues)
	#form = bearforms.UserForm()
	#form1 = bearforms.DataForm()


	#	BL = float(request.form["beamlength"])
	#	NS = int(request.form["supportnum"])
	#	NL = int(request.form["loadnum"])
		#print(NS)
		#d = Infoform(beamlength=BL,supportnum=NS,loadnum=NL)
		#db.session.add(d)
		#db.session.commit()
		#info = Infoform.query.all()
	#	SECONF = true;
	#	return render_template('beamdesign_cal.html', SECONF = SECONF,BL = BL, NS = NS, NL = NL)
	#SECONF = false;


	#if form.beamdata.data:
	#	if form.validate_on_submit():
	#		if form.beamlength.data:
	#			BL = float(form.beamlength.data)
	#		else:
	#			BL = 0
	#		if form.supportnum.data:
	#			NS = int(form.supportnum.data)
	#		else:
	#			NS = 0
	#		if form.loadnum.data:
	#			NL = int(form.loadnum.data)
	#		else:
	#			NL = 0
	#		d = Infoform(beamlength=form.beamlength.data,supportnum=int(form.supportnum.data),loadnum=int(form.loadnum.data))
	#		db.session.add(d)
	#		db.session.commit()
	#		info = Infoform.query.all()

	#		return render_template('beamdesign_cal.html', form = form, BL = form.beamlength.data, NS = NS, NL = NL,form1 = form1, info = info)

	#if form1.LoadSuppdata.data:
	#	if form1.validate_on_submit():
	#		SL1 = [0]
	#		SL2 = [0]
	#		SL3 = [0]
	#		LL1 = [0]
	#		LL2 = [0]
	#		LL3 = [0]
	#		LL4 = [0]
	#		info = Infoform.query.all()
	#		for i in info:
	#			a = float(i.beamlength)
	#			b = int(i.supportnum)
	#			c = int(i.loadnum)
#
	#		for x in range(0,b):
	#			if form1.supportloc.data:
	#				SL1.append(int(form1.supportloc.data))
	#			else:
	#				SL1
	#			if form1.supporttype.data:
	#				SL2.append(form1.supporttype.data)
	#			else:
	#				SL2
	#			if form1.supportdirec.data:
	#				SL3.append(form1.supportdirec.data)
	#			else:
	#				SL3
#
	#		for y in range(0,c):
	#			if form1.loadloc.data:
	#				LL1.append(int(form1.loadloc.data))
	#			else:
	#				LL1
	#			if form1.loadtype.data:
	#				LL2.append(form1.loadtype.data)
	#			else:
	#				LL2
	#			if form1.loaddirec.data:
	#				LL3.append(form1.loaddirec.data)
	#			else:
	#				LL3
	#			if form1.loadvalue.data:
	#				LL4.append(int(form1.loadvalue.data))
	#			else:
	#				LL4
	#		e = Dtform(supportloc=SL1[b],supporttype=SL2[b],supportdirec=SL3[b],loadloc=LL1[c],loadtype=LL2[c],loaddirec=LL3[c],loadvalue=LL4[c])
	#		db.session.add(e)
	#		db.session.commit()
	#		dt = Dtform.query.all()
	#		return render_template('beamdesign_cal.html', form = form,BL = a,NS = b,NL = c,form1 = form1,SL1 = SL1, SL2 = SL2, SL3 = SL3, LL1 = LL1, LL2 = LL2, LL3 = LL3, LL4 = LL4,info = info)
	#return render_template('beamdesign_cal.html', form = form, form1 = form1, NS = NS, NL = NL)

#@app.route('/beam cal', methods=['GET','POST'])
#def beamd_supp():
#	form1 = bearforms.DataForm()
#	form = bearforms.UserForm()
#	NS = int(info.beamlength)
#	lst = []
#	if form1.validate_on_submit():
#		lst[0] = [form1.supportloc.data, form1.supporttype.data, form1.supportdirec.data]
#
#	e = Dtform(supportloc=form1.supportloc.data,supporttype=form1.supporttype.data,supportdirec=form1.supportdirec.data,loadloc=form1.loadloc.data,loadtype=form1.loadtype.data,loaddirec=form1.loaddirec.data,loadvalue=form1.loadvalue.data)
#	db.session.add(e)
#	db.session.commit()
#	dt = Dtform.query.all()
#	return render_template('beamdesign_cal.html', form = form, form1 = form1, dt = dt, BL = form.beamlength.data, NS = NS, NL = NL, info = info)
