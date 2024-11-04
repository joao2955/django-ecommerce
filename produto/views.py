from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponse as HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import ListView
from django.views.generic import DetailView, View, ListView
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.db.models import Q

from . import models
from perfil import models as PerfilModels

# Create your views here.


class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/index.html'
    context_object_name = 'produtos'
    paginate_by = 3
    ordering = ['-pk']

class DetalheProduto(DetailView):
    model = models.Produto
    template_name = 'produto/detail.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'

class AdicionarAoCarrinho(View):
    

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

        http_referer = self.request.META.get('HTTP_REFERER', 'produto:lista')
        variacao_id = self.request.GET.get('vid')
        
        if not variacao_id:
            messages.error(
                self.request,
                'Produto não existe'
            )

            return redirect(http_referer)

        variacao = get_object_or_404(models.Variacao, pk=variacao_id)
        produto = variacao.produto

        produto_id = produto.pk
        produto_nome = produto.nome
        variacao_nome = variacao.nome
        variacao_estoque = variacao.estoque
        preco_unitario = variacao.preco
        preco_unitario_promocional = variacao.preco_promocional
        quantidade = 1
        slug = produto.slug
        imagem = produto.imagem.url if produto.imagem else 'None'

        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()

        carrinho:dict = self.request.session['carrinho']

        if variacao_estoque < 1:
            messages.error(
                self.request,
                'Estoque insuficiente'
            )
            return redirect(http_referer)

        if variacao_id in carrinho:
            # Variação existe no carrinho
            quantidade_carrinho = carrinho[variacao_id]['quantidade']
            quantidade_carrinho += 1

            if variacao_estoque < quantidade_carrinho:
                messages.warning(
                    self.request,
                    f'Estoque insuficiente para {quantidade_carrinho}x no '
                    f'produto "{produto_nome}". Adicionamos {variacao_estoque}x '
                    'no seu carrinho.'
                )
                quantidade_carrinho = variacao_estoque
            
            carrinho[variacao_id]['quantidade'] = quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo'] = preco_unitario * quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo_promocional'] = preco_unitario_promocional * quantidade_carrinho

        else:
            #  Variação não existe no carrinho
            carrinho[variacao_id] = {
                'produto_id' : produto_id,
                'produto_nome' : produto_nome,
                'variacao_nome' : variacao_nome,
                'variacao_id' : variacao_id,
                'preco_unitario' : preco_unitario,
                'preco_unitario_promocional' : preco_unitario_promocional,
                'preco_quantitativo': preco_unitario,
                'preco_quantitativo_promocional': preco_unitario_promocional,
                'quantidade' : quantidade,
                'slug' : slug,
                'imagem' : imagem,
            }
        
        self.request.session.save()

        messages.success(
            self.request,
            f'Produto {produto_nome} {variacao_nome} adicionado ao seu '
            f'carrinho {carrinho[variacao_id]["quantidade"]}x'
        )

        return redirect(http_referer)

class RemoverDoCarrinho(View):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        http_referer = request.META.get('HTTP_REFERER', 'produto:lista')
        variacao_id = request.GET.get('vid')

        if not variacao_id:
            return redirect(http_referer)
        
        if not request.session.get('carrinho'):
            return redirect(http_referer)
        
        if variacao_id not in request.session.get('carrinho'):
            return redirect(http_referer)
        
        carrinho = request.session['carrinho'][variacao_id]

        messages.success(
            request,
            f'Produto {carrinho["produto_nome"]} {carrinho["variacao_nome"]} '
            'foi removido do seu carrinho.'
        )

        del request.session['carrinho'][variacao_id]
        request.session.save()

        return redirect(http_referer)

class Carrinho(View):
    def get(self, *args, **kwargs):
        contexto = {
            'carrinho': self.request.session.get('carrinho', {})
        }
        return render(self.request, 'produto/cart.html', contexto)
    
class Busca(ListaProdutos):
    def get_queryset(self) -> QuerySet[Any]:

        termo = self.request.GET.get('termo')
        qs = super().get_queryset()
        
        if not termo:
            return qs

        qs = qs.filter(
            Q(nome__icontains=termo) |
            Q(descricao_curta__icontains=termo) |
            Q(descricao_longa__icontains=termo)
        )

        return qs

class ResumoDaCompra(DetailView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

        if not request.user.is_authenticated:
            return redirect('perfil:criar')
        
        if not request.session.get('carrinho'):
            messages.error(
                request,
                'Seu carrinho está vazio'
            )

            return redirect('produto:lista')
        
        perfil = PerfilModels.Perfil.objects.filter(usuario=request.user).first()

        if not perfil:
            messages.error(
                request,
                'Usuário sem perfil'
            )

            return redirect('perfil:criar')

        contexto = {
            'usuario': request.user,
            'perfil': perfil,
            'carrinho': request.session['carrinho']
        }

        return render(request, 'produto/resumodacompra.html', contexto)