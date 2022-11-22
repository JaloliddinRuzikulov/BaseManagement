from multiprocessing import context
from re import search
from urllib import request
from django.shortcuts import render, get_object_or_404
from .models import ratsiyaModel,tadbirModel,Enrollment
from django.shortcuts import redirect
from django.views.generic import CreateView,DetailView,ListView,TemplateView
from django.views.decorators.http import require_http_methods
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

def ratsiyaPrint(request,datalist):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
    from reportlab.lib.pagesizes import letter, landscape

    buffer = io.BytesIO()
    doc = SimpleDocTemplate("simple_table.pdf", pagesize=landscape(letter))
# container for the 'Flowable' objects
    elements = []
 # T/r n0 Seriya nomer Ism Familiya Soxa xizmat Tel nomer Qaytarildi
    data= [['T/r ', 'N_', 'Seriya nomer', 'Ism Familiya', 'Soxa xizmat','Tel nomer','Imzo','Qaytarildi']]
    tr=0
    for obyekt in datalist:
        datas=[]
        tr+=1
        datas.append(tr)
        datas.append(obyekt[0].rcode)
        datas.append(obyekt[0].qr_code)
        data.append(datas)

    t=Table(data,100, 50)
    t.setStyle(TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
    ('VALIGN',(0,0),(0,-1),'TOP'),
    ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ]))
    t._argW[0],t._argW[1],t._argW[2],t._argW[3],t._argW[4]=30,30,100,150,150
    elements.append(t)
# write the document to disk
    doc.build(elements)    
    return FileResponse(open('simple_table.pdf','rb'), as_attachment=False, filename='hello.pdf')

def boshqaPrint(request,datalist):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
    from reportlab.lib.pagesizes import letter, landscape

    buffer = io.BytesIO()
    doc = SimpleDocTemplate("simple_table.pdf", pagesize=letter)
# container for the 'Flowable' objects
    elements = []
 # T/r n0 Seriya nomer Ism Familiya Soxa xizmat Tel nomer Qaytarildi
    data= [['T/r ','Katalog', 'Model', 'QR Code']]
    tr=0
    for obyekt in datalist:
        datas=[]
        tr+=1
        datas.append(tr)
        datas.append(obyekt[0].katalog)
        datas.append(obyekt[0].model)        
        datas.append(obyekt[0].qr_code)
        data.append(datas)

    t=Table(data,100, 50)
    t.setStyle(TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
    ('VALIGN',(0,0),(0,-1),'TOP'),
    ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ]))
    t._argW[0]= 50
    elements.append(t)
# write the document to disk
    doc.build(elements)    
    return FileResponse(open('simple_table.pdf','rb'), as_attachment=False, filename='hello.pdf')

def printerView(request,tadbirid):
    if (tadbirModel.objects.get(id=tadbirid).nametadbir) in ['Prezident tashrif','Yangi yil','Festivallar','Futbol','DTM Test','Bazaga qaytarish']:
          datalist = []
          enrolments = Enrollment.objects.filter(tadbirModel_id=tadbirid)
          for datas in enrolments:
              datalist.append(ratsiyaModel.objects.filter(id=datas.ratsiyaModel_id))
          return ratsiyaPrint(request,datalist)
    else:
          datalist = []
          enrolments = Enrollment.objects.filter(tadbirModel_id=tadbirid)
          for datas in enrolments:
              datalist.append(ratsiyaModel.objects.filter(id=datas.ratsiyaModel_id))
          return boshqaPrint(request,datalist)    


def some_view(request):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
    from reportlab.lib.pagesizes import letter, landscape

    buffer = io.BytesIO()
    doc = SimpleDocTemplate("simple_table.pdf", pagesize=landscape(letter))
# container for the 'Flowable' objects
    elements = []
 # T/r n0 Seriya nomer Ism Familiya Soxa xizmat Tel nomer Qaytarildi
    data= [['T/r ', 'N_', 'Seriya nomer', 'Ism Familiya', 'Soxa xizmat','Tel nomer','Imzo','Qaytarildi'],
    ['30', '31', '32', '', '34', '23', '24']]
    t=Table(data,100, 50)
    t.setStyle(TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
    ('VALIGN',(0,0),(0,-1),'TOP'),
    ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ]))
    t._argW[0],t._argW[1],t._argW[2],t._argW[3],t._argW[4]=30,30,100,150,150
    elements.append(t)
# write the document to disk
    doc.build(elements)    
    return FileResponse(open('simple_table.pdf','rb'), as_attachment=False, filename='hello.pdf')
    
def eventClose(request,tadbirid):
    tadbirModel.objects.filter(id=tadbirid).update(closeEvent=True)
    return redirect('/events/'+str(tadbirid))   

def addRatsiya(request):
    context={}
    context['group'] =  str(request.user.groups.all()[0])
    if request.POST and request.POST['katalog']=='Ratsiya':
        countit = int(request.POST['counts'])+1
        for i in range(1,countit):
            if not ratsiyaModel.objects.filter(qr_code=str(request.POST['field'+str(i)])):
                ratsiyaModel.objects.get_or_create(katalog=str(request.POST['katalog']),model=str(request.POST['model']),qr_code=str(request.POST['field'+str(i)]),rcode=str(request.POST['quantity'+str(i)]))
        return redirect('/detial/'+str((ratsiyaModel.objects.last()).id))

    if request.POST:
        countit = int(request.POST['counts'])+1
        for i in range(1,countit):
            if not ratsiyaModel.objects.filter(qr_code=str(request.POST['field'+str(i)])):
                ratsiyaModel.objects.get_or_create(katalog=str(request.POST['katalog']),model=str(request.POST['model']),qr_code=str(request.POST['field'+str(i)]))
        return redirect('/detial/'+str((ratsiyaModel.objects.last()).id))
    return render(request,'add.html',context)

class RatDetailView(DetailView):
    model = ratsiyaModel
    template_name = 'detail.html'    
##################################
class TadbirViews(ListView):
    model = tadbirModel
    template_name = 'events.html'    
  
class EventsListView(ListView):
    model = ratsiyaModel
    template_name = 'lists.html'    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        listoff = tadbirModel.objects.all()
        context['tadbirlid'] = list(listoff.values( 'id','nametadbir'))   
        return context    
###############################

class RatListView(ListView):
    model = ratsiyaModel
    template_name = 'lists.html'    
    context_object_name = 'profiles'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        listoff = tadbirModel.objects.all()
        context['tadbirlid'] = list(listoff.values( 'id','nametadbir'))   
        return context    

class omborListView(ListView):
    model = ratsiyaModel
    template_name = 'ombor.html'    
    context_object_name = 'profiles'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        listoff = tadbirModel.objects.all()
        context['tadbirlid'] = list(listoff.values( 'id','nametadbir'))   
        return context    


def userManager(request):
    if request.user.is_authenticated:
        return redirect('main')
    else:
        return redirect('login')      
   
def appsView(request):
    context={}
    context['group'] =  str(request.user.groups.all()[0])
    if 'browser' in request.POST:
        searchbox = request.POST['browser']
        tadbirModel.objects.create(nametadbir = searchbox ,authuser= request.user)
        return redirect('/events/'+str((tadbirModel.objects.last()).id))
    elif 'sabab' in request.POST:
        searchbox = request.POST['sabab']
        tadbirModel.objects.create(nametadbir = searchbox ,authuser= request.user)
        return redirect('/events/'+str((tadbirModel.objects.last()).id))
    return render(request,'index.html',context)




def TadbirView(request,tadbirid):
    context = {}
    datalist = []
    enrolments = Enrollment.objects.filter(tadbirModel_id=tadbirid)
    for datas in enrolments:
        datalist.append(ratsiyaModel.objects.filter(id=datas.ratsiyaModel_id))
    context['tadbirid'] = datalist[:]
    tadbir = tadbirModel.objects.get(id=tadbirid)
    context['tadbir'] = tadbir
    if tadbir.nametadbir == 'Bazaga qaytarish':
            if 'sabab' in request.POST and tadbir.closeEvent ==False:
                searchbox = (request.POST['sabab']).strip()
                rMid = ratsiyaModel.objects.filter(qr_code=searchbox)
                if rMid and rMid.values('lasteventid')[0]['lasteventid']!=0:
                    lastevents = ratsiyaModel.objects.get(qr_code=str(searchbox))
                    lastevents.lasteventid = 0
                    lastevents.save()
                    rMid=rMid.values('id')[0]['id']
                    s1=Enrollment(tadbirModel_id = tadbirid , ratsiyaModel_id = rMid )
                    s1.save()
                    return redirect('/events/'+str(tadbirid)+'/')
        
    if 'sabab' in request.POST and tadbir.closeEvent ==False and tadbir.nametadbir != 'Bazaga qaytarish':
        searchbox = (request.POST['sabab']).strip()
        rMid = ratsiyaModel.objects.filter(qr_code=searchbox)
        if rMid and rMid.values('lasteventid')[0]['lasteventid']!=tadbirid:
            lastevents = ratsiyaModel.objects.get(qr_code=str(searchbox))
            lastevents.lasteventid = tadbirid
            lastevents.save()
            rMid=rMid.values('id')[0]['id']
            s1=Enrollment(tadbirModel_id = tadbirid , ratsiyaModel_id = rMid )
            s1.save()
            return redirect('/events/'+str(tadbirid)+'/')
    return render(request,'details.html',context)
def Adds(request):
    return render(request,'adds.html')    

   