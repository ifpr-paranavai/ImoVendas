from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User

FINALIDADE_CHOICES = (
    (1, "Vender"),
    (2, "Alugar"),
)

STATUS_CHOICES = (
    (1, "Publicado"),
    (2, "Destacado"),
    (3, "A retificar"),
)



# Create your models here.
class Estado(models.Model):
    nome = models.CharField(max_length=30, unique=True)
    sigla = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return self.nome

class Cidade(models.Model):
    nome = models.CharField(max_length=30)
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.nome}-{self.estado.sigla}"


class Tipo(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Perfil(models.Model):
    nome = models.CharField(help_text="Informe seu nome completo", max_length=100)
    email = models.EmailField(verbose_name="E-mail", help_text="Informe seu E-mail", max_length=50, unique=True)
    celular = models.CharField(help_text="Informe seu número de celular", max_length=12)
    cpf = models.CharField(verbose_name="CPF", help_text="Informe seu CPF", max_length=11, null=True, blank=True, unique=True)
    cidade = models.ForeignKey(Cidade, on_delete=models.PROTECT, help_text="Informe a sua cidade")

    usuario = models.OneToOneField(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.nome

class Imovel(models.Model):
    titulo = models.CharField(help_text="Digite o título do seu imóvel", max_length=50)
    descricao = models.TextField(help_text="Descreva seu imóvel", verbose_name="Descrição", max_length=300)
    preco = models.DecimalField(verbose_name="Preço do imóvel", help_text="Informe o preço de compra ou aluguel", decimal_places=2, max_digits=15)

    cep = models.CharField(verbose_name="CEP", help_text="Informe o CEP do imóvel", max_length=10)
    rua = models.CharField(help_text="Informe a rua do imóvel", max_length=80)
    bairro = models.CharField(help_text="Informe o bairro do imóvel", max_length=30)
    numero = models.CharField(verbose_name="Número", help_text="Informe o número ou lote", max_length=30, blank=True, null=True)
    cidade = models.ForeignKey(Cidade, on_delete=models.PROTECT, help_text="Cidade do imóvel")

    quantidade_quartos = models.IntegerField(verbose_name="Quantidade de quartos")
    quantidade_banheiros = models.IntegerField(verbose_name="Quantidade de banheiros")
    area = models.DecimalField(verbose_name="Área", help_text="Digite a área total do imóvel", max_digits=10, decimal_places=2)
    tipo = models.ForeignKey(Tipo, on_delete=models.PROTECT, help_text="Informe o tipo do imóvel")
    finalidade = MultiSelectField(choices=FINALIDADE_CHOICES, help_text="Informe a finalidade do imóvel")
    
    cadastrado_em = models.DateTimeField(auto_now_add=True)
    expira_em = models.DateTimeField()

    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    publicado = models.BooleanField(default=True)
    negociado = models.BooleanField(default=False)

    comprovante = models.FileField(null=True, blank=True)
    destacado = models.BooleanField(default=False)
    valor_pago_destaque = models.DecimalField(decimal_places=2, max_digits=7)

    def __str__(self):
        return f"{self.titulo} | {self.cidade} | {self.preco}"


class Foto(models.Model):
    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE)
    foto = models.ImageField()


class Historico(models.Model):
    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE)
    movimentado_em = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=2)
    motivo = models.TextField()