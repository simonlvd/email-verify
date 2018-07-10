from django.shortcuts import render, redirect
from emailautoverify.models import eMail
from emailautoverify.VerifyEmail import Verify_Emai
import xlrd
# Create your views here.


def index(request):
    pwd = request.get_full_path()
    if len(pwd) > 4:
        req = request.GET.get('q')
        email_list = eMail.objects.filter(email__contains=req)
    else:
        email_list = eMail.objects.all()
    email_num = email_list.__len__()
    return render(
        request, 'index.html', {
            'email_list': email_list, 'email_num': email_num})


def commit(request):
    req_action = request.POST.get('action')
    req_idlist = request.POST.getlist('_selected_action')
    print(req_action, req_idlist)
    if req_action == "delete_selected":
        for id in req_idlist:
            eMail.objects.filter(id=id).delete()
    elif req_action == "AutoVerify":
        for id in req_idlist:
            email_obj = eMail.objects.get(id=id)
            Verify_Emai(email_obj.email, email_obj.password)
    return redirect('/?q=')


def add_email(request):
    return render(request, 'add_email.html')


def add_commit(request):
    emailaddr = request.POST.get('emailaddr')
    emailpsd = request.POST.get('emailpsd')
    if (emailaddr != '') & (emailpsd != ''):
        eMail.objects.create(email=emailaddr, password=emailpsd)
        return redirect('/?q=')
    return redirect('/add')


# def change_email(request):
#     return render(request,'change_email.html')


def excel_commit(request):
    # ecxel_data = request.FILES
    # print(req,ecxel_data)
    req = request.FILES.get('file_upload')
    print(req)
    if req is not None:
        wb = xlrd.open_workbook(
            filename=None, file_contents=req.read())
        table = wb.sheets()[0]
        row = table.nrows
        for i in range(0, row):
            col = table.row_values(i)
            eMail.objects.create(email=col[0], password=col[1])

        return redirect('/?q=')
    return redirect('/add')
