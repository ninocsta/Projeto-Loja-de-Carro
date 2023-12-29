from django.shortcuts import render, redirect
from cars.models import Car
from cars.forms import CarModelForm, ClientForm, Photo
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
import math
from django.forms import inlineformset_factory

# Create your views here.
class CarsListView(ListView):
    model = Car
    template_name = 'cars.html'
    context_object_name = 'cars'
    ordering = ['id']
    def get_queryset(self):
        cars = super(CarsListView, self).get_queryset()
        search = self.request.GET.get('search')
        if search:
            cars = cars.filter(model__icontains=search).order_by('model')
        return cars
    


def view_id_car(request, id):
    car = Car.objects.get(id=id)
    images = Photo.objects.filter(car_id=car)
    client_form = ClientForm()
    success_message = ''
    half = math.ceil(len(car.acessories.all()) / 2)
    acessories1 = car.acessories.all()[:half]
    acessories2 = car.acessories.all()[half:]
    if request.method == 'POST':
        client_form = ClientForm(request.POST)
        if client_form.is_valid():
            answers = client_form.save(commit=False)
            answers.car_id = car
            answers.save()
            
            success_message = 'Dados salvos com sucesso! Em breve entraremos em contato!'
            client_form.send_email(car)            
            client_form = ClientForm()
        else:
            messages.error(request, 'Erro ao enviar email')
    else:
        client_form = ClientForm()
    return render(
        request,
        'id.html',
        {'car': car, 'client_form': client_form, 'success_message': success_message, 'images': images, 'acessories1': acessories1, 'acessories2': acessories2},
        )



class CarDetailView(DetailView):
    model = Car    
    template_name = 'id.html'
    context_object_name = 'car'    
    form_class = ClientForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client_form'] = ClientForm()
        context['images'] = Photo.objects.filter(car_id=self.object)
        context['acessories1'] = self.object.acessories.all()[:math.ceil(len(self.object.acessories.all()) / 2)]
        context['acessories2'] = self.object.acessories.all()[math.ceil(len(self.object.acessories.all()) / 2):]
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST)
        if form.is_valid():
            answers = form.save(commit=False)
            answers.car_id = self.object
            answers.save()
            messages.success(request, 'Dados salvos com sucesso! Em breve entraremos em contato!')
            return redirect(self.object.get_absolute_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


@method_decorator(login_required(login_url='login'), name='dispatch')
class NewCarView(CreateView):
    model = Car
    template_name = 'new_car.html'
    form_class = CarModelForm
    success_url = '/cars/'

    def form_valid(self, form):
        response = super().form_valid(form)
        images = self.request.FILES.getlist('photo')
        for image in images:
            Photo.objects.create(photo=image, car=self.object)
        return response


@method_decorator(login_required(login_url='login'), name='dispatch')
class CarUpdateView(UpdateView):
    model = Car
    form_class = CarModelForm
    template_name = 'car_update.html'
    success_url = '/cars/'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['photos'] = PhotoFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['photos'] = PhotoFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        photos = context['photos']
        self.object = form.save()
        if photos.is_valid():
            photos.instance = self.object
            photos.save()
        return super().form_valid(form)

PhotoFormSet = inlineformset_factory(Car, Photo, fields=('photo',), extra=3, can_delete=True)


@method_decorator(login_required(login_url='login'), name='dispatch')
class CarDeleteView(DeleteView):
    model = Car
    template_name = 'delete.html'
    success_url = '/cars/'