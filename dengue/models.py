from django.db import models

class ControleAtualizacao(models.Model):
    nome_arquivo = models.CharField(max_length=100)
    ultima_atualizacao = models.DateTimeField(null=True, blank=True)

class DadosDengueEstado(models.Model):
    
    ano = models.PositiveIntegerField()
    semana = models.PositiveIntegerField()
    uf = models.CharField(max_length=2)

    casos_masculino = models.PositiveIntegerField(default=0)
    casos_feminino = models.PositiveIntegerField(default=0)

    casos_hospitalizados = models.PositiveIntegerField(default=0)

    faixa_0_18 = models.PositiveIntegerField(default=0)
    faixa_19_35 = models.PositiveIntegerField(default=0)
    faixa_36_50 = models.PositiveIntegerField(default=0)
    faixa_51_65 = models.PositiveIntegerField(default=0)
    faixa_65_mais = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('ano', 'semana', 'uf')
        verbose_name = "Dados de Dengue por Estado"
        verbose_name_plural = "Dados de Dengue por Estado"

    def __str__(self):
        return f"{self.uf} - Semana {self.semana}/{self.ano}"

    @property
    def total_casos(self):
        return self.casos_masculino + self.casos_feminino