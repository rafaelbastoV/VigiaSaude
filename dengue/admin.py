from django.contrib import admin
from .models import DadosDengueEstado, ControleAtualizacao


@admin.register(DadosDengueEstado)
class DadosDengueEstadoAdmin(admin.ModelAdmin):

    list_display = (
        "uf",
        "ano",
        "semana",
        "total_casos",
        "casos_hospitalizados",
    )

    list_filter = (
        "ano",
        "semana",
        "uf",
    )

    search_fields = ("uf",)

    ordering = ("-ano", "-semana")

    readonly_fields = ("total_casos",)

    fieldsets = (
        ("Informações Gerais", {
            "fields": ("uf", "ano", "semana")
        }),
        ("Casos por Sexo", {
            "fields": ("casos_masculino", "casos_feminino")
        }),
        ("Hospitalizações", {
            "fields": ("casos_hospitalizados",)
        }),
        ("Faixa Etária", {
            "fields": (
                "faixa_0_18",
                "faixa_19_35",
                "faixa_36_50",
                "faixa_51_65",
                "faixa_65_mais",
            )
        }),
        ("Totais Calculados", {
            "fields": ("total_casos",)
        }),
    )

@admin.register(ControleAtualizacao)
class ControleAtualizacaoAdmin(admin.ModelAdmin):
    list_display = ('nome_arquivo', 'ultima_atualizacao')
    search_fields = ('nome_arquivo',)
    ordering = ('-ultima_atualizacao',)
    list_filter = ('ultima_atualizacao',)