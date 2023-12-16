from django import forms
from cars.models import Car, CarClientForm, Photo


class CarModelForm(forms.ModelForm):

    class Meta:
        model = Car
        fields = '__all__'
    
    def clean_value(self):
        value = self.cleaned_data.get('value')
        if value < 2000:
            self.add_error('value', 'Valor mínimo do carro deve ser de R$2.000,00')
        return value

    def clean_factory_year(self):
        factory_year = self.cleaned_data.get('factory_year')
        if factory_year < 1975:
            self.add_error('factory_year', 'Não é possível cadastrar carros com data menor que 1975!')
        return factory_year


class ClientForm(forms.ModelForm):

    class Meta:
        model = CarClientForm
        fields = ('name', 'email', 'phone',)


class PhotoForm(forms.ModelForm):
    model = Photo
    fields = ('photo',)
    widget = forms.ClearableFileInput(attrs={"allow_multiple_selected": True})
