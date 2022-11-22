from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .appm.pdfgen import pdf_printer
from .models import RatsiyaModel, TadbirModel, Enrollment


def printer_view(request, tadbirid):
    if TadbirModel.objects.get(id=tadbirid).nametadbir in ['Prezident tashrif', 'Yangi yil', 'Festivallar', 'Futbol',
                                                           'DTM Test', 'Bazaga qaytarish']:
        datalist = []
        enrolments = Enrollment.objects.filter(TadbirModel_id=tadbirid)
        for datas in enrolments:
            datalist.append(RatsiyaModel.objects.filter(id=datas.RatsiyaModel_id))
        return pdf_printer(request, datalist, idevents=tadbirid, ratsiya=True)
    else:
        datalist = []
        enrolments = Enrollment.objects.filter(TadbirModel_id=tadbirid)
        for datas in enrolments:
            datalist.append(RatsiyaModel.objects.filter(id=datas.RatsiyRatsiyaModel_idaModel_id))
        return pdf_printer(request, datalist, idevents=tadbirid, ratsiya=False)


def event_close(request, tadbirid):
    TadbirModel.objects.filter(id=tadbirid).update(closeEvent=True)
    return redirect('/events/' + str(tadbirid))


def add_ratsiya(request):
    context = dict()
    context['group'] = str(request.user.groups.all()[0])
    if request.POST and request.POST['katalog'] == 'Ratsiya':
        countit = int(request.POST['counts']) + 1
        for i in range(1, countit):
            if not RatsiyaModel.objects.filter(qr_code=str(request.POST['field' + str(i)])):
                RatsiyaModel.objects.get_or_create(katalog=str(request.POST['katalog']),
                                                   model=str(request.POST['model']),
                                                   qr_code=str(request.POST['field' + str(i)]),
                                                   rcode=str(request.POST['quantity' + str(i)]))
        return redirect('/detial/' + str((RatsiyaModel.objects.last()).id))

    if request.POST:
        countit = int(request.POST['counts']) + 1
        for i in range(1, countit):
            if not RatsiyaModel.objects.filter(qr_code=str(request.POST['field' + str(i)])):
                RatsiyaModel.objects.get_or_create(katalog=str(request.POST['katalog']),
                                                   model=str(request.POST['model']),
                                                   qr_code=str(request.POST['field' + str(i)]))
        return redirect('/detial/' + str((RatsiyaModel.objects.last()).id))
    return render(request, 'add.html', context)


class RatDetailView(DetailView):
    model = RatsiyaModel
    template_name = 'detail.html'


class TadbirViews(ListView):
    model = TadbirModel
    template_name = 'events.html'


class EventsListView(ListView):
    model = RatsiyaModel
    template_name = 'lists.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        listoff = TadbirModel.objects.all()
        context['tadbirlid'] = list(listoff.values('id', 'nametadbir'))
        return context


class RatListView(ListView):
    model = RatsiyaModel
    template_name = 'lists.html'
    context_object_name = 'profiles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        listoff = TadbirModel.objects.all()
        context['tadbirlid'] = list(listoff.values('id', 'nametadbir'))
        return context


class OmborListView(ListView):
    model = RatsiyaModel
    template_name = 'ombor.html'
    context_object_name = 'profiles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        listoff = TadbirModel.objects.all()
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
        TadbirModel.objects.create(nametadbir=searchbox, authuser=request.user)
        return redirect('/events/' + str((TadbirModel.objects.last()).id))
    elif 'sabab' in request.POST:
        searchbox = request.POST['sabab']
        TadbirModel.objects.create(nametadbir=searchbox, authuser=request.user)
        return redirect('/events/' + str((TadbirModel.objects.last()).id))
    return render(request, 'index.html', context)


def tadbir_view(request, tadbirid):
    context = dict()
    datalist = list()
    enrolments = Enrollment.objects.filter(TadbirModel_id=tadbirid)
    for datas in enrolments:
        datalist.append(RatsiyaModel.objects.get(id=datas.RatsiyaModel_id))
    context['tadbirid'] = datalist
    tadbir = TadbirModel.objects.get(id=tadbirid)
    context['tadbir'] = tadbir
    if tadbir.nametadbir == 'Bazaga qaytarish':
        if 'sabab' in request.POST and not tadbir.closeEvent:
            searchbox = (request.POST['sabab']).strip()
            rmid = RatsiyaModel.objects.filter(qr_code=searchbox)
            if rmid and rmid.values('lasteventid')[0]['lasteventid'] != 0:
                lastevents = RatsiyaModel.objects.get(qr_code=str(searchbox))
                lastevents.lasteventid = 0
                lastevents.save()
                rmid = rmid.values('id')[0]['id']
                s1 = Enrollment(TadbirModel_id=tadbirid, RatsiyaModel_id=rmid)
                s1.save()
                return redirect('/events/' + str(tadbirid) + '/')

    if 'sabab' in request.POST and not tadbir.closeEvent and tadbir.nametadbir != 'Bazaga qaytarish':
        searchbox = (request.POST['sabab']).strip()
        rmid = RatsiyaModel.objects.filter(qr_code=searchbox)
        if rmid and rmid.values('lasteventid')[0]['lasteventid'] != tadbirid:
            lastevents = RatsiyaModel.objects.get(qr_code=str(searchbox))
            lastevents.lasteventid = tadbirid
            lastevents.save()
            rmid = rmid.values('id')[0]['id']
            s1 = Enrollment(TadbirModel_id=tadbirid, RatsiyaModel_id=rmid)
            s1.save()
            return redirect('/events/' + str(tadbirid) + '/')
    return render(request, 'details.html', context)
