from django.db import models
from django.utils.timezone import now
from datetime import date

# Función nombrada para devolver la fecha actual
def default_date():
    return now().date()
 
# Create your models here.
class Socios(models.Model): 
    Nombre = models.CharField(max_length=100, null=True)
    Dni = models.CharField(max_length=50, null=True)
    Telefono = models.CharField(max_length=15, null=True) 
    saldo_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # 🔹 Agregamos el campo

    def obtener_saldo(self):
        # Obtener todas las suscripciones del socio y sumar los saldos
        total_saldo = Subscripcion.objects.filter(socio=self).aggregate(total=models.Sum('saldo'))['total'] or 0.00
        return total_saldo
   

    def __str__(self):
        return f"{self.Nombre} ({self.Dni})"
    
    class Meta:
        ordering = ['-id']  # Orden descendente por ID

    
    
class Planes (models.Model):
    Nombre = models.CharField(max_length=100, null=True)
    Precio = models.CharField(max_length=100, null=True)
    Dias = models.IntegerField(default=0)

    def __str__(self):
        return self.Nombre
 

class Subscripcion (models.Model):
    socio = models.ForeignKey(Socios, on_delete=models.CASCADE)
    plan = models.ForeignKey(Planes, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_inicio = models.DateField(default=default_date) 
    fecha_fin = models.DateField(default=default_date)  
    dias = models.IntegerField( null=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Campo para el monto de dinero 
    saldo =  models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        ordering = ['-id']  # Orden descendente por ID


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Guarda la suscripción primero
        
        # 🔹 Actualiza el saldo del socio con el saldo de la última suscripción
        self.socio.saldo_actual = self.saldo
        self.socio.save()

     # 🔹 Recalcular el saldo total sumando todas las suscripciones del socio
        saldo_total = Subscripcion.objects.filter(socio=self.socio).aggregate(total=models.Sum("saldo"))["total"] or 0
        
        # 🔹 Guardar el saldo total en la tabla de socios
        self.socio.saldo_actual = saldo_total
        self.socio.save()

 
class Pago(models.Model):
    socio = models.ForeignKey(Socios, on_delete=models.CASCADE, related_name='pagos')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateField(default=now)

    def __str__(self):
        return f"Pago de {self.monto} a {self.socio.Nombre} en {self.fecha_pago}"


class Asistencia(models.Model):
    subscripcion = models.ForeignKey(Subscripcion, on_delete=models.CASCADE)
    fecha_asistencia = models.DateTimeField(default=now)  # Fecha y hora de la asistencia

    def __str__(self):
     return f"Asistencia el {self.fecha_asistencia.strftime('%Y-%m-%d %H:%M')}"


# Modelo para los profesores
class Profesor(models.Model):
    dni = models.CharField(max_length=8, unique=True) 
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)


    def __str__(self):
        return f"{self.nombre} {self.apellido}"  


# Modelo para registrar ingreso y egreso
class RegistroIngresoEgreso(models.Model):
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    fecha_hora_ingreso = models.DateTimeField(null=True, blank=True)
    fecha_hora_egreso = models.DateTimeField(null=True, blank=True)