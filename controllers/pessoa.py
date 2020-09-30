# -*- coding: utf-8 -*-
@auth.requires_login()
def index():
    qcheque=len(db(db.cheque.debito>0).select())
    consul=(request.args(0))
    if consul:
        rows = db(db.pessoa.nome.contains(request.args(0))).select(orderby=db.pessoa.nome)
    else:
        rows = db((db.pessoa.ativo=="True")&(db.pessoa.debito!=0)).select(orderby=db.pessoa.nome)
    return dict(rows=rows, qcheque=qcheque)


@auth.requires_login()
def inativos():
    consul=(request.args(0))
    if consul:
        rows = db((db.pessoa.nome.contains(request.args(0)))and(db.pessoa.ativo=="False")).select(orderby=db.pessoa.nome)
    else:
        rows = db(db.pessoa.ativo=="False").select(orderby=db.pessoa.nome)
    return dict(rows=rows)

@auth.requires_login()
def cadastro_pessoa():
    response.view = 'generic.html'
    form = SQLFORM(db.pessoa).process()
    if form.accepted:
        #caso aceito redireciona para tela de acesso inicial
        response.flash = 'Formulario aceito'
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    #2 consultas no banco
    return  dict(form=form)

@auth.requires_login()
def alterar_pessoa():
    response.view = 'generic.html' # use a generic view
    pessoa = db.pessoa(request.args(0, cast=int))
    db.pessoa.id.readable = False
    db.pessoa.id.writable = False
    form = SQLFORM(db.pessoa, request.args(0, cast=int), deletable=False)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)
