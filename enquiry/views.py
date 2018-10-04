from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail

from .forms import EnquiryForm

# Create your views here.
def enquiry(request):
    if request.method == 'POST':
        form = EnquiryForm(request.POST)

        if form.is_valid():
            name = request.POST['name']
            email = request.POST['email']
            phone = request.POST['contact']
            msg = request.POST['msg']
            form.save()

            message = 'A Query from {}, Email {}, Contact {} has come.'.format(name, email, phone)

            from_email = 'codenjump@gmail.com'
            send_mail('Query from Nescoder Website', message, from_email, ['kuntal.karmakar@nescode.com'], fail_silently=False)
            messages.success(request, 'Your response has been saved')
            return redirect('contact')

        else:
            form = EnquiryForm()
            return render(request, 'home/contact.html', {'enquiry_form':form})

    else:
        form = EnquiryForm()
        return render(request, 'home/contact.html', {'enquiry_form':form})
