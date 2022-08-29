from calculator import app, db
from flask import Flask, render_template, request
from calculator.bearforms import UserForm
from calculator.my_bearing import my_bearing
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
	d1 = float(request.form["shaftdia"])
	d2 = float(request.form["dynamicloadcap"])
	output = my_bearing(d2,d1)
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
	LT = request.form["loadtype"]
	Th = request.form["theory"]
	db = request.form["designbase"]
	dr = request.form["diaratio"]
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
	Th = request.form["theory"]
	R = key_d(P,N,S,F,D,Th)
	return render_template('keydesign_cal.html',R = R)


@app.route('/beam cal', methods=['GET','POST'])
def beamd_cal():
	form = bearforms.UserForm()
	form1 = bearforms.DataForm()
	NS = 0
	NL = 0
	if form.validate_on_submit():
		if form.supportnum.data:
			NS = int(form.supportnum.data)
		else:
			NS = 0
		if form.loadnum.data:
			NL = int(form.loadnum.data)
		else:
			NL = 0
		d = Infoform(beamlength=form.beamlength.data,supportnum=form.supportnum.data,loadnum=form.loadnum.data)
		db.session.add(d)
		db.session.commit()
		info = Infoform.query.all()
		return render_template('beamdesign_cal.html', form = form, BL = form.beamlength.data, NS = NS, NL = NL,form1 = form1, info = info)
	return render_template('beamdesign_cal.html', form = form, form1 = form1, NS = NS, NL = NL)

@app.route('/beam cal', methods=['GET','POST'])
def beamd_supp():
	form1 = bearforms.DataForm()
	form = bearforms.UserForm()
	NS = int(form.supportnum.data)
	lst = []
	if form1.validate_on_submit():
		lst[0] = [form1.supportloc.data, form1.supporttype.data, form1.supportdirec.data]

	e = Dtform(supportloc=form1.supportloc.data,supporttype=form1.supporttype.data,supportdirec=form1.supportdirec.data,loadloc=form1.loadloc.data,loadtype=form1.loadtype.data,loaddirec=form1.loaddirec.data,loadvalue=form1.loadvalue.data)
	db.session.add(e)
	db.session.commit()
	dt = Dtform.query.all()
	return render_template('beamdesign_cal.html', form = form, form1 = form1, dt = dt, BL = form.beamlength.data, NS = NS, NL = NL, info = info)
