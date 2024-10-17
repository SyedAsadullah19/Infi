from flask import Flask, render_template, redirect, request,session, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime as dt
import os





current_file = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET_KEY"
app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///"+os.path.join(current_file,"project_db.sqlite3")
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

###### Databases #############

# Admin
class Admin(db.Model):
    __tablename__ = "Admin"
    A_id = db.Column(db.Integer, primary_key= True, autoincrement = True)
    username = db.Column(db.String, unique= True, nullable = False)
    email = db.Column(db.String, unique= True, nullable = False)
    password = db.Column(db.String, nullable = False)
    

# Sponsor
class Sponsor(db.Model):
    __tablename__ = "Sponsor"
    S_id = db.Column(db.Integer, primary_key= True, autoincrement = True)
    username = db.Column(db.String, unique= True, nullable = False)
    email = db.Column(db.String, unique= True, nullable = False)
    password = db.Column(db.String, nullable = False)
    industry = db.Column(db.String, nullable = False)
    flag = db.Column(db.Integer, nullable = False)
    
    
    

# Influencer
class Influencer(db.Model):
    __tablename__ = "Influencer"
    I_id = db.Column(db.Integer, primary_key= True, autoincrement = True)
    username = db.Column(db.String, unique= True, nullable = False)
    email = db.Column(db.String, unique= True, nullable = False)
    password = db.Column(db.String, nullable = False)
    category = db.Column(db.String, nullable = False)
    niche = db.Column(db.String, nullable = False)
    instagram = db.Column(db.Integer, nullable = False)
    youtube = db.Column(db.Integer, nullable = False)
    tiktok = db.Column(db.Integer, nullable = False)
    flag = db.Column(db.Integer, nullable = False)
    followers = db.Column(db.Integer, nullable = False)
    contracts = db.relationship('CampaignSponsor', secondary='contract')
    

#Campaign
class Campaign(db.Model):
    __tablename__ = "Campaign"
    C_id = db.Column(db.Integer, primary_key= True, autoincrement = True)
    name = db.Column(db.String, unique= True, nullable = False)
    category = db.Column(db.String, nullable = False)
    description = db.Column(db.String, nullable = False)
    start_date = db.Column(db.String, nullable = False)
    end_date = db.Column(db.String, nullable = False)
    budget = db.Column(db.Integer, nullable = False)
    visib = db.Column(db.String, nullable = False)
    goals = db.Column(db.String, nullable = False)
    flag = db.Column(db.Integer, nullable = False)
    campaigns = db.relationship('Sponsor', secondary='campaign_sponsor')
    
class CampaignSponsor(db.Model):
    __tablename__ = 'campaign_sponsor'
    L_id = db.Column(db.Integer, primary_key= True, autoincrement = True)
    C_id = db.Column(db.Integer, db.ForeignKey("Campaign.C_id"))
    S_id = db.Column(db.Integer, db.ForeignKey("Sponsor.S_id"))

    
class Contract(db.Model):
    __tablename__ = 'contract'
    Sno = db.Column(db.Integer, primary_key= True, autoincrement = True)
    L_id = db.Column(db.Integer, db.ForeignKey("campaign_sponsor.L_id"))
    I_id = db.Column(db.Integer, db.ForeignKey("Influencer.I_id"))
    message = db.Column(db.String)
    Request = db.Column(db.String)
    Response= db.Column(db.String)
##############################################################################



###### Extra Functions #############

def check_d(password, passwordr, email, name, table_Class):
    query = db.session.query(table_Class).filter(table_Class.email==email).first()
    query1 = db.session.query(table_Class).filter(table_Class.username==name).first()
    if password != passwordr:
        return False
    elif query:
        return False
    elif query1:
        return False
    else:
        return True
    
def check_n( name, table_Class):
    query1 = db.session.query(table_Class).all()
    l=[]
    for q in query1:
        l.append(q.username)
    if name in l:
        return False
    elif name not in l:
        return True

##############################################################################




###### Routes and Controllers #############



###### Home  and  Registration #############
#Home
@app.route("/")
def home():
    return render_template('Home.html')


# Admin Registration
@app.route("/aregister", methods=['GET','POST'])
def aregister():
    if request.method == 'GET':
        return render_template("Aregister.html")
    if request.method == 'POST':
        username = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        passwordr = request.form.get("passwordr")
        S_K= request.form.get("password_s")
        secret_key= "SECRET_KEY"
        if check_d(password,passwordr,email,username,Admin) == False:
            return render_template('detailser.html')
        elif check_d(password,passwordr,email,username,Admin) == True:
            if S_K != secret_key:
                return render_template('detailser.html')
            else:
                data = Admin(username=username,email=email,password=password)
                db.session.add(data)
                db.session.commit()
                return redirect("/login")


#Influencer Registration
@app.route("/iregister", methods=['GET','POST'])
def iregister():
    if request.method == 'GET':
        return render_template("Iregister.html")
    if request.method == 'POST':
        username = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        passwordr = request.form.get("passwordr")
        category = request.form.get('category')
        niche = request.form.get("niche")
        platform= request.form.getlist("platform")
        inf_t = request.form.get("inf_t")
        pltf = {'instagram':0, 'youtube':0, 'tiktok':0}
        follower_n = {'nano':5500, 'micro':30000, 'mid-tier':275000, 'macro':750000, 'mega':1500000}
        for i in pltf:
            if i in platform:
                pltf[i]=1
        if check_d(password,passwordr,email,username,Influencer) == False:
            return render_template('detailser.html')
        elif check_d(password,passwordr,email,username,Influencer) == True:
                data = Influencer(username=username,email=email,password=password,category=category,niche=niche,instagram=pltf['instagram'],youtube=pltf['youtube'],tiktok=pltf['tiktok'],flag=0,followers=follower_n[inf_t])
                db.session.add(data)
                db.session.commit()
                return redirect("/login")
        return redirect("/")


#Sponosor Registration
@app.route("/sregister", methods=['GET','POST'])
def sregister():
    if request.method == 'GET':
        return render_template("Sregister.html")
    if request.method == 'POST':
        username = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        passwordr = request.form.get("passwordr")
        industry = request.form.get("industry")
        if check_d(password,passwordr,email,username,Sponsor) == False:
            return render_template('detailser.html')
        elif check_d(password,passwordr,email,username,Sponsor) == True:
                data = Sponsor(username=username,email=email,password=password,industry=industry,flag=0)
                db.session.add(data)
                db.session.commit()
                return redirect("/login")
##############################################################################






###### Login and Logout #############  
@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("Login.html")
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_t = request.form.get('user_type')
        if user_t == "Sponsor":
            query = db.session.query(Sponsor).filter(Sponsor.email==email).filter(Sponsor.password==password).first()
            if query:
                if query.flag==1:
                    return("You are flagged, your account can not be accessed")
                return redirect(url_for('sdash', id=query.S_id))
            else:
                return render_template('loginerror.html')
        elif user_t == "Influencer":
            query = db.session.query(Influencer).filter(Influencer.email==email).filter(Influencer.password==password).first()
            if query:
               if query.flag==1:
                    return("You are flagged, your account can not be accessed")
               return redirect(url_for('idash', id=query.I_id))
            else:
                return render_template('loginerror.html')
        elif user_t == "Admin":
            query = db.session.query(Admin).filter(Admin.email==email).filter(Admin.password==password).first()
            if query:
               return redirect(url_for('adash', id=query.A_id))
            else:
                return render_template('loginerror.html')


#Logout
@app.route("/logout")
def logout():
    return redirect('/')
##############################################################################



###### Sponsor Dashboard And Controllers #############
@app.route("/sdash/<int:id>")
def sdash(id):
    id=int(id)
    query = db.session.query(Sponsor).filter(Sponsor.S_id==id).first()
    return render_template('Sdash.html',query=query,id=id)

# Update Details
@app.route("/supdateinfo/<id>", methods=['GET','POST'])
def supdateinfo(id):
    if request.method == 'GET':
        query = db.session.query(Sponsor).filter(Sponsor.S_id==id).first()
        return render_template("Supdateinfo.html", query=query)
    if request.method == 'POST':
        username = request.form.get("name")
        password = request.form.get("password")
        industry = request.form.get("industry")
        query=db.session.query(Sponsor).filter(Sponsor.S_id==id).first()
        if check_n(username,Sponsor)==True:
            query.username=username
            query.password=password
            query.industry=industry
            db.session.commit()
        elif check_n(username,Sponsor)==False:
            query.password=password
            query.industry=industry
            db.session.commit()
        return redirect(url_for('sdash',id=query.S_id))

# Delete Sponsors

@app.route("/sponsor/deleted/sponsor/<int:Sid>")
def deletesponsor(Sid):
    query=db.session.query(Sponsor).filter(Sponsor.S_id==Sid).first()
    query1=db.session.query(CampaignSponsor).filter(CampaignSponsor.S_id==Sid).all()
    l=[]
    empty=[]
    for q in query1:
        l.append(q.C_id)
    
    for q in query1:
        db.session.delete(q)
        db.session.commit()
    db.session.delete(query)
    db.session.commit()
    
    if l!=empty:
        for list in l:
            query2=db.session.query(Campaign).filter(Campaign.C_id==list).first()
            db.session.delete(query2)
            db.session.commit()
    return redirect("/")










#Create Campaign 

@app.route("/create/campaign/<int:id>", methods=['GET','POST'])
def create_campaign(id):
    if request.method == 'GET':
        query=db.session.query(Sponsor).filter(Sponsor.S_id==id).first()
        return render_template("Campaign.html", query=query)
    elif request.method=='POST':
        name=request.form.get('pname')
        category=request.form.get('category')
        description=request.form.get('description')
        start_date=request.form.get('start_date')
        end_date=request.form.get('end_date')
        budget=request.form.get('budget')
        visiblity=request.form.get('visiblity')
        goals=request.form.get('goals')
        print(name,category,description,start_date,end_date,budget,visiblity,goals)
        query=db.session.query(Campaign).filter(Campaign.name==name).first()
        if query:
            query1=db.session.query(Sponsor).filter(Sponsor.S_id==id).first()
            return render_template("Campexist.html",query=query1)
        else:
            data=Campaign(name=name,category=category,description=description,start_date=start_date,end_date=end_date,budget=budget,visib=visiblity,goals=goals,flag=0)
            db.session.add(data)
            db.session.commit()
            query3=db.session.query(Campaign).filter(Campaign.name==name).first()
            data2=CampaignSponsor(C_id=query3.C_id,S_id=id)
            db.session.add(data2)
            db.session.commit()
        return redirect(url_for("mycampaigns",id=id))
    
    
    
#Show Upcomming Campaigns
@app.route("/upcoming/campaign/<int:id>")
def upcoming(id):
    query1=db.session.query(Campaign).filter(Campaign.C_id==CampaignSponsor.C_id).filter(CampaignSponsor.S_id==id).all()
    currdate=dt.date.today()
    dates=[]
    empty=[]
    for q in query1:
        print(q)
        st_date=q.start_date
        format_string = "%Y-%m-%d"
        datetime_obj = dt.datetime.strptime(st_date, format_string).date()
        day=datetime_obj.strftime("%d")
        month=datetime_obj.strftime("%m")
        year=datetime_obj.strftime("%Y")
        date_obj=dt.date(int(year),int(month),int(day))
        if date_obj>currdate:
            dates.append(str(datetime_obj))
    if dates==empty:
        return render_template("upcamp.html",date=dates,empty=empty,query=query1,dates=dates,id=id)
    elif dates!=empty:   
        return render_template("upcamp.html",date=dates,empty=empty,query=query1,dates=dates,id=id)
    return redirect('/')



#Show Ongoing Campaigns
@app.route("/ongoing/campaign/<int:id>")
def ongoing(id):
    query1=db.session.query(Campaign).filter(Campaign.C_id==CampaignSponsor.C_id).filter(CampaignSponsor.S_id==id).all()
    currdate=dt.date.today()
    names=[]
    empty=[]
    for q in query1:
        st_date=q.start_date
        ed_date=q.end_date
        format_string = "%Y-%m-%d"
        format_string1 = "%Y-%m-%d"
        datetime_obj = dt.datetime.strptime(st_date, format_string).date()
        datetime_obj1 = dt.datetime.strptime(ed_date, format_string1).date()
        day=datetime_obj.strftime("%d")
        day1=datetime_obj1.strftime("%d")
        month=datetime_obj.strftime("%m")
        month1=datetime_obj1.strftime("%m")
        year=datetime_obj.strftime("%Y")
        year1=datetime_obj1.strftime("%Y")
        date_obj=dt.date(int(year),int(month),int(day))
        date_obj1=dt.date(int(year1),int(month1),int(day1))
        if date_obj1>=currdate>=date_obj:
            query=db.session.query(Campaign).filter(Campaign.C_id==CampaignSponsor.C_id).filter(CampaignSponsor.S_id==id).filter(Campaign.start_date==st_date).filter(Campaign.end_date==ed_date).first()
            names.append(query.name)
    if names==empty:
        return render_template("oncamp.html",names=names,empty=empty,query=query1,id=id)
    elif names!=empty:   
        return render_template("oncamp.html",names=names,empty=empty,query=query1,id=id)
    print(names)
    return redirect('/')
#Show Completed Campaigns
@app.route("/completed/campaign/<int:id>")
def completed(id):
    query1=db.session.query(Campaign).filter(Campaign.C_id==CampaignSponsor.C_id).filter(CampaignSponsor.S_id==id).all()
    currdate=dt.date.today()
    dates=[]
    empty=[]
    for q in query1:
        st_date=q.end_date
        format_string = "%Y-%m-%d"
        datetime_obj = dt.datetime.strptime(st_date, format_string).date()
        day=datetime_obj.strftime("%d")
        month=datetime_obj.strftime("%m")
        year=datetime_obj.strftime("%Y")
        date_obj=dt.date(int(year),int(month),int(day))
        if date_obj<currdate:
            dates.append(str(datetime_obj))
    if dates==empty:
        return render_template("ccamp.html",date=dates,empty=empty,query=query1,dates=dates,id=id)
    elif dates!=empty:   
        return render_template("ccamp.html",date=dates,empty=empty,query=query1,dates=dates,id=id)
    return redirect('/')



#Show Flagged Campaigns
@app.route("/flag/campaign/<int:id>")
def flaggedcampaigns(id):
    query=db.session.query(Campaign).filter(Campaign.C_id==CampaignSponsor.C_id).filter(CampaignSponsor.S_id==id).filter(Campaign.flag==1).all()
    flagged=[]
    empty=[]
    for q in query:
        flagged.append(q)
    if flagged==empty:
        return render_template("cflag.html",date=flagged,empty=empty,query=query,id=id)
    elif flagged!=empty:   
        return render_template("cflag.html",date=flagged,empty=empty,query=query,id=id)
    return redirect('/')


#My Campaigns
@app.route("/mycampaigns/<int:id>")
def mycampaigns(id):
    query=db.session.query(Campaign).filter(Campaign.C_id==CampaignSponsor.C_id).filter(CampaignSponsor.S_id==id).all()
    query1=db.session.query(Sponsor).filter(Sponsor.S_id==id).first()
    return render_template("mycampaign.html", query=query, id=id, query1=query1)


#Update Campaign 
@app.route("/update/<int:sid>/campaign/<int:cid>", methods=['GET','POST'])
def updatecampaign(sid,cid):
    if request.method=='GET':
        query=db.session.query(Campaign).filter(Campaign.C_id==CampaignSponsor.C_id).filter(CampaignSponsor.S_id==sid).filter(CampaignSponsor.C_id==cid).first()
        return render_template("Ucampaign.html",query=query,sid=sid)
    if request.method =='POST':
        category = request.form.get("category")
        description = request.form.get("description")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        budget = request.form.get("budget")
        visib = request.form.get("visib")
        goals = request.form.get("goals")
        query1=db.session.query(Campaign).filter(Campaign.C_id==cid).first()
        query1.category=category
        query1.description=description
        query1.start_date=start_date
        query1.end_date=end_date
        query1.budget=budget
        query1.visib=visib
        query1.goals=goals
        db.session.add(query1)
        db.session.commit()
    return redirect(url_for("mycampaigns",id=sid))


#Delete Campaign 
@app.route("/delete/<int:sid>/campaign/<int:cid>")
def deletecampaign(sid,cid):
    query=db.session.query(Campaign).filter(Campaign.C_id==cid).first()
    query1=db.session.query(CampaignSponsor).filter(CampaignSponsor.C_id==cid).filter(CampaignSponsor.S_id==sid).first()
    db.session.delete(query1)
    db.session.commit()
    db.session.delete(query)
    db.session.commit()
    return redirect(url_for("mycampaigns",id=sid))



#Show Influencer
@app.route("/show/influencer/<int:id>")
def showinfluencer(id):
    query = db.session.query(Influencer).filter(Influencer.flag==0).all()
    query1=db.session.query(Sponsor).filter(Sponsor.S_id==id).first()
    if query1.flag==1:
        return("You are flagged")
    return render_template("Sinflu.html",id=id,query=query,query1=query1)

# Search Influencer
@app.route("/search/influencer/<int:id>",methods=['GET','POST'])
def searchinfluencer(id):
    if request.method =='GET':
        query4=db.session.query(Sponsor).filter(Sponsor.S_id==id).first()
        return render_template("Ssearch.html",id=id,query4=query4)
    elif request.method =='POST':
        inf_name= request.form.get("inf_name")
        inf_t= request.form.get("inf_t")
        dic={5500:'Nano-Influencers (1,000 to 10,000 followers)', 
                30000:'Micro-Influencers (10,000 to 50,000 followers)',
                275000:'Mid-Tier Influencers (50,000 to 500,000 followers)', 
                750000:'Macro-Influencers (500,000 to 1 million followers)', 
                1500000:'Mega Influencer (over 1 million followers)'}
        result=db.session.query(Influencer).filter(Influencer.followers==inf_t).filter(Influencer.flag==0).filter(Influencer.username.like(f'%{inf_name}%')|Influencer.category.like(f'%{inf_name}%')|Influencer.niche.like(f'%{inf_name}%')).all()
        query4=db.session.query(Sponsor).filter(Sponsor.S_id==id).first()
        return render_template("Ssearch.html",id=id,query4=query4,result=result,inf_name=inf_name,inf_t=dic[int(inf_t)])



@app.route("/show/influencer/<int:iid>/sponsor/request/<int:sid>",methods=['GET','POST'])
def sendinfluencerrequest(iid,sid):
    if request.method=='GET':
      spons=db.session.query(Sponsor).filter(Sponsor.S_id==sid).first()
      inf=db.session.query(Influencer).filter(Influencer.I_id==iid).first()
      camp=db.session.query(Campaign).filter(Campaign.C_id==CampaignSponsor.C_id).filter(CampaignSponsor.S_id==sid).all()
      if spons.flag==1:
          return("You are flagged you can not send reuqest")
      return render_template("Ireqform.html",camp=camp,spons=spons,inf=inf)

    elif request.method=='POST':
        message=request.form.get('message')
        cid=request.form.get('cname')
        campspons=db.session.query(CampaignSponsor).filter(CampaignSponsor.C_id==cid).filter(CampaignSponsor.S_id==sid).first()
        create=Contract(L_id=campspons.L_id, I_id=iid,message=message,Request="Influencer",Response="Unknown")
        db.session.add(create)
        db.session.commit()  
        return redirect(url_for("showinfluencer",id=sid))
       

    
#Show Influencer Sent Request
@app.route("/show/influencer/request/<int:id>")
def showinfluencerrequest(id):
    query4=db.session.query(Sponsor).filter(Sponsor.S_id==id).first()
    empty=[]
    detail=[]
    details=[]
    list_contract=db.session.query(Contract).filter(Contract.L_id==CampaignSponsor.L_id).filter(CampaignSponsor.S_id==id).filter(Contract.Response=='Unknown').filter(Contract.Request=='Influencer').all()
    for l in list_contract:
        query=db.session.query(Influencer).filter(Influencer.I_id==l.I_id).first()
        detail.append(query.username)
        query1=db.session.query(CampaignSponsor).filter(CampaignSponsor.L_id==l.L_id).first()
        query2=db.session.query(Campaign).filter(Campaign.C_id==query1.C_id).first()
        query3=db.session.query(Sponsor).filter(Sponsor.S_id==query1.S_id).first()
        detail.append(query3.username)
        detail.append(query2.name)
        detail.append(l.message)
        detail.append(l.Sno)
        details.append(detail)
        detail=[]
    print(details)
    return render_template("Ssent.html",id=id,contracts=list_contract,empty=empty,details=details,query4=query4)

#Delete Request
@app.route("/route/delete/reuqest/<int:id>/<int:sno>")
def delreq(id,sno):
    query=db.session.query(Contract).filter(Contract.Sno==sno).first()
    db.session.delete(query)
    db.session.commit()
    return redirect(url_for("showinfluencerrequest",id=id))
#Update Request
@app.route("/route/update/campaign/reuqest/<int:id>/<int:sno>",methods=['GET','POST'])
def updreq(id,sno):
    if request.method=='GET':
        query=db.session.query(Contract).filter(Contract.Sno==sno).first()
        influ=db.session.query(Influencer).filter(Influencer.I_id==query.I_id).first()
        campspons=db.session.query(CampaignSponsor).filter(CampaignSponsor.L_id==query.L_id).first()
        campsponsa=db.session.query(CampaignSponsor).all()
        spons=db.session.query(Sponsor).filter(Sponsor.S_id==campspons.S_id).first()
        camp1=db.session.query(Campaign).filter(Campaign.C_id==campspons.C_id).first()
        list=[]
        lists=[]
        for ca in campsponsa:
            if ca.S_id==spons.S_id:
                query65=db.session.query(Campaign).filter(Campaign.C_id==ca.C_id).first()
                list.append(query65.C_id)
                list.append(query65.name)
                lists.append(list)
                list=[]
        messg=query.message
        print(camp1,influ,spons,lists)
        return render_template("Supreq.html",id=id,influ=influ,spons=spons,camp=lists,messg=messg,camp1=camp1)
    if request.method=='POST':
        cid=request.form.get("cid")
        message=request.form.get("message")
        query=db.session.query(Contract).filter(Contract.Sno==sno).first()
        campsp=db.session.query(CampaignSponsor).filter(CampaignSponsor.C_id==cid).first()
        query.L_id=campsp.L_id
        query.message=message
        db.session.commit()
        return redirect(url_for("showinfluencerrequest",id=id))
#Show Influencer Recieved Request 
@app.route("/show/influencer/recived/<int:id>")
def showinfluencerrecived(id):
    query4=db.session.query(Sponsor).filter(Sponsor.S_id==id).first()
    empty=[]
    detail=[]
    details=[]
    list_contract=db.session.query(Contract).filter(Contract.L_id==CampaignSponsor.L_id).filter(CampaignSponsor.S_id==id).filter(Contract.Response=='Unknown').filter(Contract.Request=='Campaign').all()
    for l in list_contract:
        query=db.session.query(Influencer).filter(Influencer.I_id==l.I_id).first()
        detail.append(query.username)
        query1=db.session.query(CampaignSponsor).filter(CampaignSponsor.L_id==l.L_id).first()
        query2=db.session.query(Campaign).filter(Campaign.C_id==query1.C_id).first()
        query3=db.session.query(Sponsor).filter(Sponsor.S_id==query1.S_id).first()
        detail.append(query3.username)
        detail.append(query2.name)
        detail.append(l.message)
        details.append(detail)
        detail.append(l.Sno)
        detail=[]
    print(details)
    return render_template("Srecive.html",id=id,contracts=list_contract,empty=empty,details=details, query4=query4)


#Accept Request
@app.route("/accept/campaign/recived/<int:id>/<int:Sno>")
def acceptcampaignrecived(id,Sno):
    query=db.session.query(Contract).filter(Contract.Sno==Sno).first()
    query.Response='Accepted'
    db.session.commit()
    return(redirect(url_for('showinfluencerrecived',id=id)))


#Rejected Request
@app.route("/reject/campaign/recived/<int:id>/<int:Sno>")
def rejectcampaignrecived(id,Sno):
    query=db.session.query(Contract).filter(Contract.Sno==Sno).first()
    query.Response='Rejected'
    db.session.commit()
    return(redirect(url_for('showinfluencerrecived',id=id)))

#Show completed details
@app.route("/show/complete/details/<int:id>/<nameo>")
def completeddetails(id,nameo):
    query1=db.session.query(Influencer).filter(Influencer.username==nameo).first()
    query = db.session.query(Influencer).filter(Influencer.I_id==query1.I_id).first()
    follow_d = {5500:'Nano-Influencers (1,000 to 10,000 followers)', 
                30000:'Micro-Influencers (10,000 to 50,000 followers)',
                275000:'Mid-Tier Influencers (50,000 to 500,000 followers)', 
                750000:'Macro-Influencers (500,000 to 1 million followers)', 
                1500000:'(over 1 million followers)'}
    ans={1:'yes',0:'no'}
    data2={'instagram':ans[query.instagram], 'youtube':ans[query.youtube], 'tiktok':ans[query.tiktok]}
    return render_template('compdet.html',query=query, data=follow_d, data2 =data2, id=id)



#Show Influencer Response
@app.route("/show/influencer/response/<int:id>")
def showinfluencerresponse(id):
    query4=db.session.query(Sponsor).filter(Sponsor.S_id==id).first()
    empty=[]
    detail=[]
    details=[]
    list_contract=db.session.query(Contract).filter(Contract.L_id==CampaignSponsor.L_id).filter(CampaignSponsor.S_id==id).filter(Contract.Response=='Accepted').all()
    for l in list_contract:
        query=db.session.query(Influencer).filter(Influencer.I_id==l.I_id).first()
        detail.append(query.username)
        query1=db.session.query(CampaignSponsor).filter(CampaignSponsor.L_id==l.L_id).first()
        query2=db.session.query(Campaign).filter(Campaign.C_id==query1.C_id).first()
        query3=db.session.query(Sponsor).filter(Sponsor.S_id==query1.S_id).first()
        detail.append(query3.username)
        detail.append(query2.name)
        detail.append(l.message)
        detail.append(l.Sno)
        if l.Request=="Campaign":
            detail.append("Campaign")
        if l.Request=="Influencer":
            detail.append("Influencer")
        details.append(detail)
        detail=[]
        
    detail1=[]
    details1=[]
    list_contract1=db.session.query(Contract).filter(Contract.L_id==CampaignSponsor.L_id).filter(CampaignSponsor.S_id==id).filter(Contract.Response=='Rejected').all()
    for l in list_contract1:
        query5=db.session.query(Influencer).filter(Influencer.I_id==l.I_id).first()
        detail1.append(query.username)
        query6=db.session.query(CampaignSponsor).filter(CampaignSponsor.L_id==l.L_id).first()
        query7=db.session.query(Campaign).filter(Campaign.C_id==query6.C_id).first()
        query8=db.session.query(Sponsor).filter(Sponsor.S_id==query6.S_id).first()
        detail1.append(query8.username)
        detail1.append(query7.name)
        detail1.append(l.message)
        detail1.append(l.Sno)
        if l.Request=="Campaign":
            detail1.append("Campaign")
        if l.Request=="Influencer":
            detail1.append("Influencer")
        detail1.append(query5.I_id)
        detail1.append(query6.L_id)
        details1.append(detail1)
        detail1=[]
    return render_template("Sresponse.html",id=id,contracts=list_contract,empty=empty,details=details, query4=query4,contracts1=list_contract1,details1=details1)

# Send Again
@app.route("/send/again/<int:id>/influencer/<int:inf>/<int:lid>/<message>")
def sendagainrequesti(id,inf,lid,message):
    query=Contract(L_id=lid,I_id=inf,message=message,Request="Influencer",Response="Unknown")
    db.session.add(query)
    db.session.commit()
    return redirect(url_for("showinfluencerrequest",id=id))
#Delete Request

#Delete Your Account(S)
##############################################################################


###### Admin Dashboard And Controllers #############


# Dashboard
@app.route("/adash/<int:id>")
def adash(id):
    id = int(id)
    query = db.session.query(Admin).filter(Admin.A_id==id).first()
    return render_template('Adash.html',query=query, id=id)


# Update Details
@app.route("/aupdateinfo/<int:id>", methods=['GET','POST'])
def aupdateinfo(id):
    id=int(id)
    if request.method == 'GET':
        query = db.session.query(Admin).filter(Admin.A_id==id).first()
        return render_template("Aupdateinfo.html", query=query)
    if request.method == 'POST':
        username = request.form.get("name")
        password = request.form.get("password")
        print(username, password)
        query=db.session.query(Admin).filter(Admin.A_id==id).first()
        if check_n(username,Admin)==True:
            query.username=username
            query.password=password
            db.session.commit()
        elif check_n(username,Admin)==False:
            query.password=password
            db.session.commit()
        return redirect(url_for('adash',id=id))
#admin delete
@app.route("/admin/delete/admin/<int:id>")
def deleteadmin(id):
    query=db.session.query(Admin).filter(Admin.A_id==id).first()
    db.session.delete(query)
    db.session.commit()
    return redirect("/")
# admin-sponsor
@app.route("/show/admin/sponsor/<int:id>")
def adminsponsor(id):
    query=db.session.query(Sponsor).all()
    query1=db.session.query(Admin).filter(Admin.A_id==id).first()
    empty=[]
    names=[]
    for s in query:
        if s.flag!=1:
            names.append(s.username)
    return render_template("Asopons.html",id=id, query=query, query1=query1,names=names,empty=empty)

#Influencer-Sponsor
@app.route("/show/admin/influencer/<int:id>")
def admininfluencer(id):
    query=db.session.query(Influencer).all()
    query1=db.session.query(Admin).filter(Admin.A_id==id).first()
    empty=[]
    names=[]
    for s in query:
        if s.flag!=1:
            names.append(s.username)
    return render_template("Ainflu.html",id=id,query=query, query1=query1,names=names,empty=empty)

#Campaign-Sponsor
@app.route("/show/admin/campaign/<int:id>")
def admincampaign(id):
    sponsq=db.session.query(Sponsor).all()
    name=[]
    names=[]
    for q in sponsq:
        query=db.session.query(Campaign).filter(Campaign.C_id==CampaignSponsor.C_id).filter(CampaignSponsor.S_id==q.S_id).all()
        for c in query:
            if c.flag==0:
                name.append(q.username)
                name.append(c.name)
                name.append(c.category)
                name.append(c.description)
                name.append(c.budget)
                name.append(c.start_date)
                name.append(c.end_date)
                name.append(c.visib)
                name.append(c.goals)
                name.append(c.C_id)
                names.append(name)
                name=[]
    query1=db.session.query(Admin).filter(Admin.A_id==id).first()
    empty=[]
    print(sponsq)
    for n in names:
        if len(n)==1:
            print(n)
    return render_template("Acamp.html",id=id, query1=query1,names=names,empty=empty)
# Flagged Campaign 

#Statistics
@app.route("/show/statistics/<int:id>")
def adminstats(id):
    query=db.session.query(Admin).filter(Admin.A_id==id).first()
    u1=db.session.query(Sponsor).all()
    u2=db.session.query(Campaign).all()
    u3=db.session.query(Influencer).all()
    money=0
    for m in u2:
        money+=m.budget
    cu1=len(u1)
    cu2=len(u2)
    cu3=len(u3)
    averageC =money/cu2
    averageS=money/cu1
    totalusers =cu1+cu3
    return render_template("Astats.html",query=query,id=id,cu1=cu1,cu2=cu2,cu3=cu3,averageC=averageC,averageS=averageS,totalusers=totalusers,money=money)



#Show Flagged Ones
@app.route("/show/admin/flagged/<int:id>")
def adminflagged(id):
    query85=db.session.query(Admin).first()
    id=query85.A_id
    sponsq=db.session.query(Sponsor).all()
    name=[]
    names=[]
    for q in sponsq:
        query=db.session.query(Campaign).filter(Campaign.C_id==CampaignSponsor.C_id).filter(CampaignSponsor.S_id==q.S_id).all()
        if not query:
            return("no result found")
        for c in query:
            if c.flag==1:
                name.append(q.username)
                name.append(c.name)
                name.append(c.category)
                name.append(c.description)
                name.append(c.budget)
                name.append(c.start_date)
                name.append(c.end_date)
                name.append(c.visib)
                name.append(c.goals)
                name.append(c.C_id)
                name.append(q.S_id)
                names.append(name)
                name=[]
    query1=db.session.query(Admin).first()
    empty=[]
    print(sponsq)
    for n in names:
        if len(n)==1:
            print(n)
    # Influencer
    query2=db.session.query(Influencer).all()
    empty=[]
    names1=[]
    for inf in query2:
        if inf.flag==1:
            names1.append(inf.username)
    # Sponsor
    query3=db.session.query(Sponsor).all()
    empty=[]
    names2=[]
    for s in query3:
        if s.flag==1:
            names2.append(s.username)
    return render_template("Aflag.html",id=id, query1=query1,names=names,names1=names1,empty=empty,names2=names2,query2=query2, query3=query3)

#Flag-Campaign
@app.route("/admin/flagged/campaign/<int:id>/<int:aid>")
def flaggedcampaign(id,aid):
    query=db.session.query(Campaign).filter(Campaign.C_id==id).first()
    query.flag=1
    db.session.commit()
    return redirect(url_for("adminflagged",id=aid))
#Flag-Influencer
@app.route("/admin/flagged/influencer/<int:id>/<int:iid>")
def flaggedinfluencers(id,iid):
    query=db.session.query(Influencer).filter(Influencer.I_id==iid).first()
    query.flag=1
    db.session.commit()
    return redirect(url_for("adminflagged",id=id))
#Flag-Sponsor
@app.route("/admin/flagged/sponsor/<int:id>/<int:sid>")
def flaggedsponsors(id,sid):
    query=db.session.query(Sponsor).filter(Sponsor.S_id==sid).first()
    query.flag=1
    db.session.commit()
    return redirect(url_for("adminflagged",id=id))
#Delete Campaign
@app.route("/admin/<int:id>/delete/<int:sid>/campaign/<int:cid>")
def deletedcampaign(sid,cid,id):
    query=db.session.query(Campaign).filter(Campaign.C_id==cid).first()
    query1=db.session.query(CampaignSponsor).filter(CampaignSponsor.C_id==cid).filter(CampaignSponsor.S_id==sid).first()
    db.session.delete(query1)
    db.session.commit()
    db.session.delete(query)
    db.session.commit()
    return redirect(url_for("adminflagged",id=id))


#Delete Influencer
@app.route("/admin/deleted/influencer/<int:id>/<int:Iid>")
def deletedinfluencers(id,Iid):
    query=db.session.query(Influencer).filter(Influencer.I_id==Iid).first()
    db.session.delete(query)
    db.session.commit()
    return redirect(url_for("adminflagged",id=id))
#Delete Influencer
@app.route("/admin/deleted/sponsor/<int:aid>/<int:Sid>")
def deletedsponsor(aid,Sid):
    query=db.session.query(Sponsor).filter(Sponsor.S_id==Sid).first()
    query1=db.session.query(CampaignSponsor).filter(CampaignSponsor.S_id==Sid).all()
    l=[]
    empty=[]
    for q in query1:
        l.append(q.C_id)
    
    for q in query1:
        db.session.delete(q)
        db.session.commit()
    db.session.delete(query)
    db.session.commit()
    
    if l!=empty:
        for list in l:
            query2=db.session.query(Campaign).filter(Campaign.C_id==list).first()
            db.session.delete(query2)
            db.session.commit()
    return redirect(url_for("adminflagged",id=aid))
#Unflag Campaigns
@app.route("/admin/unflagged/campaign/<int:id>")
def unflaggedcampaign(id):
    query=db.session.query(Campaign).filter(Campaign.C_id==id).first()
    query.flag=0
    db.session.commit()
    return redirect(url_for("adminflagged",id=id))
#Flag-Influencer
@app.route("/admin/unflagged/influencer/<int:id>")
def unflaggedinfluencers(id):
    query=db.session.query(Influencer).filter(Influencer.I_id==id).first()
    query.flag=0
    db.session.commit()
    return redirect(url_for("adminflagged",id=id))
#Flag-Sponsor
@app.route("/admin/unflagged/sponsor/<int:id>")
def unflaggedsponsors(id):
    query=db.session.query(Sponsor).filter(Sponsor.S_id==id).first()
    query.flag=0
    db.session.commit()
    return redirect(url_for("adminflagged",id=id))
##############################################################################


###### Influencer Dashboard And Controllers #############
@app.route("/idash/<id>")
def idash(id):
    id=int(id)
    query = db.session.query(Influencer).filter(Influencer.I_id==id).first()
    follow_d = {5500:'Nano-Influencers (1,000 to 10,000 followers)', 
                30000:'Micro-Influencers (10,000 to 50,000 followers)',
                275000:'Mid-Tier Influencers (50,000 to 500,000 followers)', 
                750000:'Macro-Influencers (500,000 to 1 million followers)', 
                1500000:'(over 1 million followers)'}
    ans={1:'yes',0:'no'}
    data2={'instagram':ans[query.instagram], 'youtube':ans[query.youtube], 'tiktok':ans[query.tiktok]}
    return render_template('Idash.html',query=query, data=follow_d, data2 =data2, id=id)

# Update Details

@app.route("/iupdateinfo/<id>", methods=['GET','POST'])
def iupdateinfo(id):
    if request.method == 'GET':
        query = db.session.query(Influencer).filter(Influencer.I_id==id).first()
        ans={1:'yes',0:'no'}
        data2={'instagram':ans[query.instagram], 'youtube':ans[query.youtube], 'tiktok':ans[query.tiktok]}
        return render_template("Iupdateinfo.html", query=query,data2=data2, id=id)
    if request.method == 'POST':
        username = request.form.get("name")
        password = request.form.get("password")
        category=request.form.get("category")
        platform=request.form.getlist("platform")
        niche=request.form.get('niche')
        inf_t= request.form.get("inf_t")
        print(username, password, category,platform,niche,inf_t)
        query=db.session.query(Influencer).filter(Influencer.I_id==id).first()
        pltf = {'instagram':0, 'youtube':0, 'tiktok':0}
        follower_n = {'nano':5500, 'micro':30000, 'mid-tier':275000, 'macro':750000, 'mega':1500000}
        for i in pltf:
            if i in platform:
                pltf[i]=1
        if check_n(username,Sponsor)==True:
            query.username=username
            query.password=password
            query.category=category
            query.niche=niche
            query.instagram=pltf['instagram']
            query.youtube=pltf['youtube']
            query.tiktok=pltf['tiktok']
            query.followers=follower_n[inf_t]
            db.session.commit()
        elif check_n(username,Sponsor)==False:
            query.password=password
            query.category=category
            query.niche=niche
            query.instagram=pltf['instagram']
            query.youtube=pltf['youtube']
            query.tiktok=pltf['tiktok']
            query.followers=follower_n[inf_t]
            db.session.commit()
        return redirect(url_for('idash',id=id))
        
#Delete Influencer

@app.route("/influencer/delete/influencer/<int:Iid>")
def deleteinfluencer(Iid):
    query=db.session.query(Influencer).filter(Influencer.I_id==Iid).first()
    db.session.delete(query)
    db.session.commit()
    return redirect("/")
#Show Campaign
@app.route("/show/campaign/<int:id>")
def showcampaign(id):
    inf=db.session.query(Influencer).filter(Influencer.I_id==id).first()
    sponsq=db.session.query(Sponsor).filter(Sponsor.flag==0).all()
    name=[]
    names=[]
    for q in sponsq:
        query=db.session.query(Campaign).filter(Campaign.C_id==CampaignSponsor.C_id).filter(CampaignSponsor.S_id==q.S_id).all()
        for c in query:
            if c.flag==0 and c.visib=='public':
                name.append(q.username)
                name.append(c.name)
                name.append(c.category)
                name.append(c.description)
                name.append(c.budget)
                name.append(c.start_date)
                name.append(c.end_date)
                name.append(c.visib)
                name.append(c.goals)
                name.append(c.C_id)
                name.append(q.S_id)
                names.append(name)
                name=[]
    empty=[]
    if inf.flag==1:
        return("You are flagged")
    return render_template("Icamp.html",id=id,query=query,inf=inf ,names=names,empty=empty)

#Send Request
@app.route("/show/campaign/<int:iid>/request/<int:sid>/<int:cid>",methods=['GET','POST'])
def sendcampaignrequest(iid,sid,cid):
    if request.method=='GET':
      camp=db.session.query(Campaign).filter(Campaign.C_id==cid).first()
      spons=db.session.query(Sponsor).filter(Sponsor.S_id==sid).first()
      inf=db.session.query(Influencer).filter(Influencer.I_id==iid).first()
      if inf.flag==1:
          return("You are flagged you can not send reuqest")
      
      return render_template("Creqform.html",camp=camp,spons=spons,inf=inf)
    elif request.method=='POST':
        message=request.form.get('message')
        campspons=db.session.query(CampaignSponsor).filter(CampaignSponsor.C_id==cid).filter(CampaignSponsor.S_id==sid).first()
        create=Contract(L_id=campspons.L_id, I_id=iid,message=message,Request="Campaign",Response="Unknown")
        db.session.add(create)
        db.session.commit()
        return redirect(url_for("showcampaign",id=iid))


#Update Request
@app.route("/update/campaign/<int:iid>/request/<int:sid>/<int:cid>",methods=['GET','POST'])
def updatesponsorrequest(iid,sid,cid):
    return render_template("Supreq.html")
#Delete Request


#Show Sponsor Sent Request
@app.route("/show/campaign/request/<int:id>")
def showcampaignrequest(id):
    empty=[]
    detail=[]
    details=[]
    query4=db.session.query(Influencer).filter(Influencer.I_id==id).first()
    list_contract=db.session.query(Contract).filter(Contract.L_id==CampaignSponsor.L_id).filter(Contract.I_id==id).filter(Contract.Response=='Unknown').filter(Contract.Request=='Campaign').all()
    for l in list_contract:
        query=db.session.query(Influencer).filter(Influencer.I_id==l.I_id).first()
        detail.append(query.username)
        query1=db.session.query(CampaignSponsor).filter(CampaignSponsor.L_id==l.L_id).first()
        query2=db.session.query(Campaign).filter(Campaign.C_id==query1.C_id).first()
        query3=db.session.query(Sponsor).filter(Sponsor.S_id==query1.S_id).first()
        detail.append(query3.username)
        detail.append(query2.name)
        detail.append(l.message)
        detail.append(l.Sno)
        details.append(detail)
        detail=[]
    print(details)
    return render_template("Isent.html",id=id,contracts=list_contract,empty=empty,details=details,query4=query4)


#Show Sponsor Recieved Request 
@app.route("/show/sponsor/recived/<int:id>")
def showsponsnorrecived(id):
    empty=[]
    detail=[]
    details=[]
    query4=db.session.query(Influencer).filter(Influencer.I_id==id).first()
    list_contract=db.session.query(Contract).filter(Contract.L_id==CampaignSponsor.L_id).filter(Contract.I_id==id).filter(Contract.Response=='Unknown').filter(Contract.Request=='Influencer').all()
    for l in list_contract:
        query=db.session.query(Influencer).filter(Influencer.I_id==l.I_id).first()
        detail.append(query.username)
        query1=db.session.query(CampaignSponsor).filter(CampaignSponsor.L_id==l.L_id).first()
        query2=db.session.query(Campaign).filter(Campaign.C_id==query1.C_id).first()
        query3=db.session.query(Sponsor).filter(Sponsor.S_id==query1.S_id).first()
        detail.append(query3.username)
        detail.append(query2.name)
        detail.append(l.message)
        detail.append(l.Sno)
        details.append(detail)
        detail=[]
    return render_template("Irecive.html",id=id,contracts=list_contract,empty=empty,details=details,query4=query4)

#Show Specific
@app.route("/specific/camp/<int:id>/<int:Sno>")
def showspecific(id,Sno):
    query=db.session.query(Contract).filter(Contract.Sno==Sno).first()
    query.Response='Accepted'
    db.session.commit()
    return(redirect(url_for('showsponsnorrecived',id=id)))
#Accept Request
@app.route("/accept/sponsor/recived/<int:id>/<int:Sno>")
def acceptponsnorrecived(id,Sno):
    query=db.session.query(Contract).filter(Contract.Sno==Sno).first()
    query.Response='Accepted'
    db.session.commit()
    return(redirect(url_for('showsponsnorrecived',id=id)))


#Rejected Request
@app.route("/reject/sponsor/recived/<int:id>/<int:Sno>")
def rejectponsnorrecived(id,Sno):
    query=db.session.query(Contract).filter(Contract.Sno==Sno).first()
    query.Response='Rejected'
    db.session.commit()
    return(redirect(url_for('showsponsnorrecived',id=id)))

#Show Influencer Response
@app.route("/show/sponsor/response/<int:id>")
def showsponsorresponse(id):
    query4=db.session.query(Influencer).filter(Influencer.I_id==id).first()
    empty=[]
    detail=[]
    details=[]
    list_contract=db.session.query(Contract).filter(Contract.L_id==CampaignSponsor.L_id).filter(Contract.I_id==id).filter(Contract.Response=='Accepted').all()
    for l in list_contract:
        query=db.session.query(Influencer).filter(Influencer.I_id==l.I_id).first()
        detail.append(query.username)
        query1=db.session.query(CampaignSponsor).filter(CampaignSponsor.L_id==l.L_id).first()
        query2=db.session.query(Campaign).filter(Campaign.C_id==query1.C_id).first()
        query3=db.session.query(Sponsor).filter(Sponsor.S_id==query1.S_id).first()
        detail.append(query3.username)
        detail.append(query2.name)
        detail.append(l.message)
        detail.append(l.Sno)
        if l.Request=="Campaign":
            detail.append("Campaign")
        if l.Request=="Influencer":
            detail.append("Influencer")
        details.append(detail)
        detail=[]
    print(details)
    detail1=[]
    details1=[]
    list_contract1=db.session.query(Contract).filter(Contract.L_id==CampaignSponsor.L_id).filter(Contract.I_id==id).filter(Contract.Response=='Rejected').all()
    for l in list_contract1:
        query5=db.session.query(Influencer).filter(Influencer.I_id==l.I_id).first()
        detail1.append(query.username)
        query6=db.session.query(CampaignSponsor).filter(CampaignSponsor.L_id==l.L_id).first()
        query7=db.session.query(Campaign).filter(Campaign.C_id==query6.C_id).first()
        query8=db.session.query(Sponsor).filter(Sponsor.S_id==query6.S_id).first()
        detail1.append(query8.username)
        detail1.append(query7.name)
        detail1.append(l.message)
        detail1.append(l.Sno)
        if l.Request=="Campaign":
            detail1.append("Campaign")
        if l.Request=="Influencer":
            detail1.append("Influencer")
        detail1.append(query5.I_id)
        detail1.append(query6.L_id)
        details1.append(detail1)
        detail1=[]
        print(details1)
    return render_template("Iresponse.html",id=id,contracts=list_contract,empty=empty,details=details, query4=query4,contracts1=list_contract1,details1=details1)


#Send Again
@app.route("/send/again/<int:id>/campaign/<int:inf>/<int:lid>/<message>")
def sendagainrequest(id,inf,lid,message):
    query=Contract(L_id=lid,I_id=inf,message=message,Request="Campaign",Response="Unknown")
    db.session.add(query)
    db.session.commit()
    return redirect(url_for("showcampaignrequest",id=id))
# Campaign
@app.route("/search/campaign/<int:id>",methods=['GET','POST'])
def searchcampaign(id):
    if request.method =='GET':
        query4=db.session.query(Influencer).filter(Influencer.I_id==id).first()
        return render_template("Isearch.html",id=id,query4=query4)
    elif request.method =='POST':
        inf_name= request.form.get("inf_name")
        sponsq=db.session.query(Sponsor).filter(Sponsor.flag==0).all()
        name=[]
        names=[]
        for q in sponsq:
          query=db.session.query(Campaign).filter(Campaign.C_id==CampaignSponsor.C_id).filter(CampaignSponsor.S_id==q.S_id).filter(Campaign.name.like(f'%{inf_name}%')|Campaign.category.like(f'%{inf_name}%')|Campaign.budget.like(f'%{inf_name}%')|Campaign.description.like(f'%{inf_name}%')|Campaign.goals.like(f'%{inf_name}%')).all()
          for c in query:
              if c.flag==0 and c.visib=='public':
                  name.append(q.username)
                  name.append(c.name)
                  name.append(c.category)
                  name.append(c.description)
                  name.append(c.budget)
                  name.append(c.start_date)
                  name.append(c.end_date)
                  name.append(c.visib)
                  name.append(c.goals)
                  name.append(c.C_id)
                  name.append(q.S_id)
                  names.append(name)
                  name=[]
        empty=[]
        query4=db.session.query(Influencer).filter(Influencer.I_id==id).first()
        if query4.flag==1:
           return("You are flagged")
        return render_template("Isearch.html",id=id,query4=query4,names=names,inf_name=inf_name)
    
    
#Update Details
@app.route("/route/update/influencer/reuqest/<int:id>/<int:sno>",methods=['GET','POST'])
def updreqinf(id,sno):
    if request.method=='GET':
        query=db.session.query(Contract).filter(Contract.Sno==sno).first()
        influ=db.session.query(Influencer).filter(Influencer.I_id==query.I_id).first()
        campspons=db.session.query(CampaignSponsor).filter(CampaignSponsor.L_id==query.L_id).first()
        spons=db.session.query(Sponsor).filter(Sponsor.S_id==campspons.S_id).first()
        camp=db.session.query(Campaign).filter(Campaign.C_id==campspons.C_id).first()
        messg=query.message
        print(influ,spons,camp)
        return render_template("Iupreq.html",id=id,influ=influ,spons=spons,camp=camp,messg=messg)
    if request.method=='POST':
       message= request.form.get("message")
       query1=db.session.query(Contract).filter(Contract.Sno==sno).first()
       query1.message=message
       db.session.add(query1)
       db.session.commit()
       return redirect(url_for("showcampaignrequest",id=id))
   
   
    
#Delete A request Influencer
@app.route("/route/delete/influencer/reuqest/<int:id>/<int:sno>")
def delreqinf(id,sno):
    query=db.session.query(Contract).filter(Contract.Sno==sno).first()
    db.session.delete(query)
    db.session.commit()
    return redirect(url_for("showcampaignrequest",id=id))
##############################################################################

##############################################################################
###### Running App #############
if __name__ =="__main__":
    app.run(debug=True)
##############################################################################
