from django.shortcuts import render, redirect
from cars.models import Car
from cars.forms import CarModelForm, ClientForm, Photo
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
def cars_view(request):
    cars = Car.objects.all().order_by('id')

    search = request.GET.get('search')
    if search:
        cars = Car.objects.filter(model__icontains=search).order_by('model')

    return render(
        request,
        'cars.html',
        {'cars': cars}
        )


def view_id_car(request, id):
    car = Car.objects.get(id=id)
    images = Photo.objects.filter(car_id=car)
    client_form = ClientForm()
    success_message = ''
    if request.method == 'POST':
        client_form = ClientForm(request.POST)
        if client_form.is_valid():
            answers = client_form.save(commit=False)
            answers.car_id = car
            answers.save()
            client_form = ClientForm()
            success_message = 'Dados salvos com sucesso! Em breve entraremos em contato!'
    return render(
        request,
        'id.html',
        {'car': car, 'client_form': client_form, 'success_message': success_message, 'images': images},
        )


@login_required(login_url='/login/')
def new_car_view(request):
    if request.method == 'POST':
        new_car_form = CarModelForm(request.POST, request.FILES)

        if new_car_form.is_valid():
            new_car_instance = new_car_form.save()  # Salve a instância do carro criada
            images = request.FILES.getlist('photo')

            for image in images:
                Photo.objects.create(
                    photo=image,
                    car=new_car_instance)  # Atribua a instância do carro, não a classe

            return redirect('cars_list')
    else:
        new_car_form = CarModelForm()

    return render(request, 'new_car.html', {'new_car_form': new_car_form})


def login_user(request):
    return render(request, 'login.html')


def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('new_car/')
        else:
            messages.error(request, "Usuário ou senha inválidos.")
            return render(request, 'login.html')
