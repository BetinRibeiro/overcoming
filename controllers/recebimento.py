# -*- coding: utf-8 -*-
@auth.requires_login()
@auth.requires_membership('admin')
def index():
    mes=request.now
    ano=request.now
    mes=request.args(0, cast=int)
    ano=request.args(1, cast=int)
    primeira_data=datetime.date(ano, mes, 1)
    ultima_data=datetime.date(ano, mes, 1)

    if (mes==12):
        ultima_data=datetime.date(ano+1, 1, 1)
    else:
        ultima_data=datetime.date(ano, mes+1, 1)
    rows = db((db.recebimento.data_recebimento>=primeira_data)&(db.recebimento.data_recebimento<ultima_data)).select(orderby=db.recebimento.data_recebimento)
    return locals()

@auth.requires_login()
def ver_recebimento():
    recebimento = db.recebimento(request.args(0, cast=int))
    return locals()

@auth.requires_login()
def alterar_conferencia():
    recebimento = db.recebimento(request.args(0, cast=int))
    if recebimento.conferido==True:
        recebimento.conferido=False
    else:
        recebimento.conferido=True
    recebimento.update_record()
    redirect(URL('index', args=[recebimento.data_recebimento.month,recebimento.data_recebimento.year]))
    return locals()

@auth.requires_login()
def alterar_recebimento():
    response.view = 'generic.html' # use a generic view
    recebimento = db.recebimento(request.args(0, cast=int))
    cheque = db.cheque(recebimento.cheque)
    db.recebimento.id.readable = False
    db.recebimento.id.writable = False
    form = SQLFORM(db.recebimento, request.args(0, cast=int), deletable=True)
    if form.process().accepted:
        session.flash = 'Atualizado'
        redirect(URL('ver_cheque', args=recebimento.id))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)

@auth.requires_login()
def ver_cheque():
    recebimento = db.recebimento(request.args(0, cast=int))
    cheque = db.cheque(recebimento.cheque)
    rows = db((db.recebimento.cheque==cheque.id)).select(orderby=db.recebimento.data_recebimento)
    return locals()
