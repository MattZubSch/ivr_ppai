from django.db import models

# Create your models here.

#buscar como conectar las distintas clases 
#como tratarlas como si fueran una agregacion
#mejorar las restricciones de respuesta

class Estado(models.Model):
    nombre = models.CharField(max_length=30),
    def esFinalizada(self):
        return self.nombre == 'Finalizada'
    def esInicial(self):
        return self.nombre == 'Iniciada'
    def getNombre(self):
        return self.nombre

class CambioEstado(models.Model):
    fechaHoraInicio = models.DateField(),
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE),
    def getFechaHoraInicio(self):
        return self.fechaHoraInicio
    def getNombreEstado(self):
        return self.estado.nombre
    def new(self, param_fechaHoraInicio, param_estado):
        return self.objects.create(fechaHoraInicio=param_fechaHoraInicio, estado=param_estado)
#probar si el metodo new funciona. Caso contrario, implementar via create

class RespuestaPosible(models.Model):
    descripcion = models.CharField(max_length=40),
    valor = models.IntegerField(max_length=2),
    def getDescripcionRta(self):
        return self.descripcion

class RespuestaDeCliente(models.Model):
    fechaEncuesta = models.DateField(),
    respuestaPosible = models.OneToOneField(RespuestaPosible, on_delete=models.CASCADE),
    def getDescripcionRta(self):
        return self.respuestaPosible.descripcion
    
class Cliente(models.Model):
    dni = models.IntegerField(),
    nombreCompleto = models.CharField(max_length=60),
    nroCelular = models.IntegerField(),
    def getNombre(self):
        return self.nombreCompleto

class Llamada(models.Model):
    descipcionOperador = models.CharField(max_length=100),
    detalleAccionRequerida = models.CharField(max_length=100),
    duracion = models.DurationField(),
    encuestaEnviada = models.BooleanField(),
    observacionAuditor = models.CharField(max_length=100),
    cambioEstado = models.ForeignKey(CambioEstado, on_delete=models.CASCADE),
    respuestaDelCliente = models.ForeignKey(RespuestaDeCliente, on_delete=models.CASCADE, null=True),
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE),
    def __str__(self):
        return self.descipcionOperador

    
class Pregunta(models.Model):
    pregunta = models.CharField(max_length=100),
    respuestaPosible = models.ForeignKey(RespuestaPosible, on_delete=models.CASCADE, related_name='respuestaPosible'),

class Encuesta(models.Model):
    descripcion = models.CharField(max_length=100),
    fechaFinVigenca = models.DateField(),
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='pregunta'),  


