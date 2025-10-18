from django import forms
from .models import Socios, Planes, Subscripcion,Profesor
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

class ClaveForm(forms.Form):
    clave = forms.CharField(widget=forms.PasswordInput, label="Ingrese la clave", max_length=100)

class SociosForm(forms.ModelForm):
    class Meta:
        model = Socios
        fields = ('Nombre','Telefono','Dni','saldo_actual')
        widgets = {
            'Nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'Dni': forms.NumberInput(attrs={'class': 'form-control'}),
            'Telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'saldo_actual': forms.NumberInput(attrs={'class':  'form-control', 'readonly': True}),
        }

    def clean_Dni(self):
        dni = self.cleaned_data.get('Dni')
        if not dni:
            return dni

        qs = Socios.objects.filter(Dni=dni)
        
        # Si se está editando un socio, excluir el mismo de la validación
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("El DNI ingresado ya está registrado.")

        return dni

class PlanesForm(forms.ModelForm):
    class Meta:
        model = Planes
        fields = ('Nombre','Precio', 'Dias')
        widges = {
            'Nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'Precio ': forms.NumberInput(attrs={'class': 'form-control'}),
            'Dias ': forms.NumberInput(attrs={'class': 'form-control'}),
            
           
        }

#------------------------------------------------------------------------------------------------------



class SubscripcionForm(forms.ModelForm):
    class Meta:
        model = Subscripcion
        fields = ['plan', 'socio', 'monto', 'saldo', 'dias', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'plan': forms.Select(attrs={'id': 'id_plan', 'class': 'form-select'}),
            'socio': forms.Select(attrs={'id': 'id_socio', 'class': 'form-select'}),
            'monto': forms.TextInput(attrs={'id': 'id_monto', 'class': 'form-control'}),  # Asegúrate de que este campo sea editable
            
            'saldo': forms.TextInput(attrs={'id': 'id_saldo', 'class': 'form-control', 'placeholder': 'Ingrese el monto pagado'}),  # Cambié el ID aquí
            
            'dias': forms.TextInput(attrs={'id': 'id_dias', 'class': 'form-control', 'readonly': True}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'id_fecha_inicio'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'id_fecha_fin'}),
        }
        labels = {
            'plan': 'Seleccione un Plan',
            'socio': 'Seleccione un Socio',
            'monto': 'Monto',
            'saldo': 'Saldo',
            'fecha_inicio': 'Fecha inicio',
            'fecha_fin': 'Fecha fin',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['socio'].widget.attrs.update({'readonly': True})  # Haz que el campo sea solo lectura
        self.fields['socio'].queryset = Socios.objects.all()  # Carga todos los socios para la validación


class EditarPerfilForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    
    class Meta:
        model = User
        fields = ['username', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    

class ProfesorForm(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = ('nombre','apellido','dni')
        widges = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'dni ': forms.NumberInput(attrs={'class': 'form-control'}),
           
        }

# Formulario para el ingreso y egreso
class RegistroForm(forms.Form):
    dni = forms.CharField(max_length=8, min_length=8, label="DNI")


    def clean_dni(self):
        dni = self.cleaned_data['dni']
        if not Profesor.objects.filter(dni=dni).exists():
            raise forms.ValidationError("DNI no registrado.")
        return dni