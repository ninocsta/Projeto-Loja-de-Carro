from django import forms
from cars.models import Car, CarClientForm, Photo
from django.core.mail import EmailMessage


class CarModelForm(forms.ModelForm):

    class Meta:
        model = Car
        fields = '__all__'
    
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


    def send_email(self, car):
        name = self.cleaned_data.get('name')
        email = self.cleaned_data.get('email')
        phone = self.cleaned_data.get('phone')
        mensagem = self.cleaned_data.get('mensagem')
        
        corpo = f" Nome: {name}\n Telefone: {phone}\n Mensagem: {mensagem},\n {car}"

        mail = EmailMessage(
            subject='Contato do Django Carros',
            from_email='nino-csta@hotmail.com',
            to=[email],
            body=corpo,
            headers={'Reply-To': 'nino-csta@hotmail.com'}
                            )
        mail.send()
        

class PhotoForm(forms.ModelForm):
    model = Photo
    fields = ('photo',)
    widget = forms.ClearableFileInput(attrs={"allow_multiple_selected": True})
