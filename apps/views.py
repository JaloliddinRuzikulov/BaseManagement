from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .appm.pdfgen import pdf_printer
from .models import ratsiyaModel, tadbirModel, Enrollment


def printer_view(request, tadbirid):
    if tadbirModel.objects.get(id=tadbirid).nametadbir in ['Prezident tashrif', 'Yangi yil', 'Festivallar', 'Futbol',
                                                           'DTM Test', 'Bazaga qaytarish']:
        datalist = []
        enrolments = Enrollment.objects.filter(tadbirModel_id=tadbirid)
        for datas in enrolments:
            datalist.append(ratsiyaModel.objects.filter(id=datas.ratsiyaModel_id))
        return pdf_printer(request, datalist, idevents=tadbirid, ratsiya=True)
    else:
        datalist = []
        enrolments = Enrollment.objects.filter(tadbirModel_id=tadbirid)
        for datas in enrolments:
            datalist.append(ratsiyaModel.objects.filter(id=datas.ratsiyaModel_id))
        return pdf_printer(request, datalist, idevents=tadbirid, ratsiya=False)


def event_close(request, tadbirid):
    tadbirModel.objects.filter(id=tadbirid).update(closeEvent=True)
    return redirect('/events/' + str(tadbirid))


def add_ratsiya(request):
    context = dict()
    context['group'] = str(request.user.groups.all()[0])
    if request.POST and request.POST['katalog'] == 'Ratsiya':
        countit = int(request.POST['counts']) + 1
        for i in range(1, countit):
            if not ratsiyaModel.objects.filter(qr_code=str(request.POST['field' + str(i)])):
                ratsiyaModel.objects.get_or_create(katalog=str(request.POST['katalog']),
                                                   model=str(request.POST['model']),
                                                   qr_code=str(request.POST['field' + str(i)]),
                                                   rcode=str(request.POST['quantity' + str(i)]))
        return redirect('/detial/' + str((ratsiyaModel.objects.last()).id))

    if request.POST:
        countit = int(request.POST['counts']) + 1
        for i in range(1, countit):
            if not ratsiyaModel.objects.filter(qr_code=str(request.POST['field' + str(i)])):
                ratsiyaModel.objects.get_or_create(katalog=str(request.POST['katalog']),
                                                   model=str(request.POST['model']),
                                                   qr_code=str(request.POST['field' + str(i)]))
        return redirect('/detial/' + str((ratsiyaModel.objects.last()).id))
    return render(request, 'add.html', context)


class RatDetailView(DetailView):
    model = ratsiyaModel
    template_name = 'detail.html'


class TadbirViews(ListView):
    model = tadbirModel
    template_name = 'events.html'


class EventsListView(ListView):
    model = ratsiyaModel
    template_name = 'lists.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        listoff = tadbirModel.objects.all()
        context['tadbirlid'] = list(listoff.values('id', 'nametadbir'))
        return context


class RatListView(ListView):
    model = ratsiyaModel
    template_name = 'lists.html'
    context_object_name = 'profiles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        listoff = tadbirModel.objects.all()
        context['tadbirlid'] = list(listoff.values('id', 'nametadbir'))
        return context


class OmborListView(ListView):
    model = ratsiyaModel
    template_name = 'ombor.html'
    context_object_name = 'profiles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        listoff = tadbirModel.objects.all()
        context['tadbirlid'] = list(listoff.values('id', 'nametadbir'))
        return context


def user_manager(request):
    if request.user.is_authenticated:
        return redirect('main')
    else:
        return redirect('login')


def apps_view(request):
    context = dict()
    context['group'] = str(request.user.groups.all()[0])
    if 'browser' in request.POST:
        searchbox = request.POST['browser']
        tadbirModel.objects.create(nametadbir=searchbox, authuser=request.user)
        return redirect('/events/' + str((tadbirModel.objects.last()).id))
    elif 'sabab' in request.POST:
        searchbox = request.POST['sabab']
        tadbirModel.objects.create(nametadbir=searchbox, authuser=request.user)
        return redirect('/events/' + str((tadbirModel.objects.last()).id))
    return render(request, 'index.html', context)


def tadbir_view(request, tadbirid):
    context = {}
    datalist = []
    enrolments = Enrollment.objects.filter(tadbirModel_id=tadbirid)
    for datas in enrolments:
        datalist.append(ratsiyaModel.objects.filter(id=datas.ratsiyaModel_id))
    context['tadbirid'] = datalist[:]
    tadbir = tadbirModel.objects.get(id=tadbirid)
    context['tadbir'] = tadbir
    if tadbir.nametadbir == 'Bazaga qaytarish':
        if 'sabab' in request.POST and not tadbir.closeEvent:
            searchbox = (request.POST['sabab']).strip()
            rmid = ratsiyaModel.objects.filter(qr_code=searchbox)
            if rmid and rmid.values('lasteventid')[0]['lasteventid'] != 0:
                lastevents = ratsiyaModel.objects.get(qr_code=str(searchbox))
                lastevents.lasteventid = 0
                lastevents.save()
                rmid = rmid.values('id')[0]['id']
                s1 = Enrollment(tadbirModel_id=tadbirid, ratsiyaModel_id=rmid)
                s1.save()
                return redirect('/events/' + str(tadbirid) + '/')

    if 'sabab' in request.POST and not tadbir.closeEvent and tadbir.nametadbir != 'Bazaga qaytarish':
        searchbox = (request.POST['sabab']).strip()
        rmid = ratsiyaModel.objects.filter(qr_code=searchbox)
        if rmid and rmid.values('lasteventid')[0]['lasteventid'] != tadbirid:
            lastevents = ratsiyaModel.objects.get(qr_code=str(searchbox))
            lastevents.lasteventid = tadbirid
            lastevents.save()
            rmid = rmid.values('id')[0]['id']
            s1 = Enrollment(tadbirModel_id=tadbirid, ratsiyaModel_id=rmid)
            s1.save()
            return redirect('/events/' + str(tadbirid) + '/')
    return render(request, 'details.html', context)
