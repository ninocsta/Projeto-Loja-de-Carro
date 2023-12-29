from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import os
from django.urls import reverse

class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Acessories(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Car(models.Model):
    id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='car_brand')
    ano = models.IntegerField(blank=True, null=True)
    plate = models.CharField(max_length=8, blank=True, null=True, unique=True)
    value = models.FloatField(blank=True, null=True)
    capa = models.ImageField(upload_to='cars/', blank=False, null=False, default='null')
    acessories = models.ManyToManyField(Acessories)
    created_date = models.DateTimeField(auto_now_add=True)
    km_atual = models.IntegerField(blank=True, null=True)
    cor = models.CharField(max_length=20,blank=True, null=True)

    AUTOMATICO = 'Automático'
    MANUAL = 'Manual'

    CAMBIO_CHOICES = [
        (AUTOMATICO, 'Automático'),
        (MANUAL, 'Manual'),
    ]

    cambio = models.CharField(
        max_length=20,
        choices=CAMBIO_CHOICES,
        default=MANUAL,  # Pode definir o valor padrão se desejar
    )

    DIRECAO_CHOICES = [
        ('Hidráulica', 'Hidráulica'),
        ('Elétrica', 'Elétrica'),
        ('Mecânica', 'Mecânica'),
        # Adicione mais opções conforme necessário
    ]

    direcao = models.CharField(
        max_length=20,
        choices=DIRECAO_CHOICES,
        default='Hidráulica',
    )

    class Meta:
        db_table = 'car'

    def __str__(self):
        return f'{self.model} - {self.id} - {self.plate}'
    

    def get_absolute_url(self):
        return reverse('id_car', args=[str(self.id)])

# Função para excluir fisicamente o arquivo da foto quando o objeto Car é excluído
@receiver(pre_delete, sender=Car)
def photo_delete(sender, instance, **kwargs):
    # Exclui o arquivo da foto do sistema de arquivos
    if instance.capa:
        if os.path.isfile(instance.capa.path):
            os.remove(instance.capa.path)


# Conectar a função de exclusão de fotos ao sinal pre_delete
pre_delete.connect(photo_delete, sender=Car)



class Photo(models.Model):
    photo = models.ImageField(upload_to='cars/', blank=False, null=False)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='carimg')

    def save(self, *args, **kwargs):
        # If photo field is empty and the instance exists in the database, delete the instance
        if not self.photo and self.pk:
            self.delete()
            return
        super().save(*args, **kwargs)

# Função para excluir fisicamente o arquivo da foto quando o objeto Photo é excluído
@receiver(pre_delete, sender=Photo)
def photo_delete(sender, instance, **kwargs):
    # Exclui o arquivo da foto do sistema de arquivos
    if instance.photo:
        if os.path.isfile(instance.photo.path):
            os.remove(instance.photo.path)

    
# Conectar a função de exclusão de fotos ao sinal pre_delete
pre_delete.connect(photo_delete, sender=Photo)


class CarClientForm(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, related_name='car_clients')
    mensagem = models.TextField(max_length=2000, null=True, blank=True)
    def __str__(self):
        return self.name
