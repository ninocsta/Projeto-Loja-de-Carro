from django import forms
from cars.models import Car, CarClientForm, Photo
from django.forms.models import modelformset_factory


class CarModelForm(forms.ModelForm):
    acessories = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={'style': 'height: 150px;'}),
        queryset=Car.acessories.through.objects.all()
    )
    class Meta:
        model = Car
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CarModelForm, self).__init__(*args, **kwargs)
        self.fields['model'].label = 'Modelo' 
        self.fields['brand'].label = 'Marca'
        self.fields['plate'].label = 'Placa'
        self.fields['value'].label = 'Valor' 
        self.fields['acessories'].label = 'Acessórios' 
        self.fields['km_atual'].label = 'Km Atual' 


    def clean_value(self):
        value = self.cleaned_data.get('value')
        if value < 2000:
            self.add_error('value', 'Valor mínimo do carro deve ser de R$2.000,00')
        return value

    def clean_year(self):
        year = self.cleaned_data.get('year')
        if year < 1975:
            self.add_error('year', 'Não é possível cadastrar carros com data menor que 1975!')
        return year


class ClientForm(forms.ModelForm):
    mensagem = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'style': 'width: 62.18%;'}))
    class Meta:
        model = CarClientForm
        fields = ('name', 'email', 'phone', 'mensagem')

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Nome'
        self.fields['email'].label = 'Email'
        self.fields['phone'].label = 'Telefone'
        self.fields['mensagem'].label = 'Mensagem'
        

class PhotoForm(forms.ModelForm):
    model = Photo
    fields = ('photo',)
    widget = forms.ClearableFileInput(attrs={"allow_multiple_selected": True})    