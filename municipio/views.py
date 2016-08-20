from django.shortcuts import render
from django.http import JsonResponse
from municipio.models import Cidade

def create_basic_data(cidade):
    return {'nome': c.nome, 'estado': c.estado.sigla}

def cidades_list(request):
    data = [create_basic_data (cidade) for c in Cidade.objects.all()]
    return JsonResponse(data, safe=False)

def cidade_summary(request, pk):
    cidade = get_object_or_404(Cidade, id=pk)
    data = create_basic_data(cidade)
    orgaos = OrgaoPublico.objects.filter(cidade=cidade)
    mes, ano = request.GET.get('mes', None), request.GET.get('ano', None)
    if not mes or not ano:
        raise Http404

    data_orgaos = []
    for org in orgaos:
        folha = EstatisticaFolhaDePagamento.objects.get(orgao=org, ano=ano, mes=mes)
        data_orgaos.append({'orgao': org.nome,
                            'quantidades': folha.get_funcionarios_count()})
    data['orgaos'] = data_orgaos
    return JsonResponse(data)
