from socket import fromshare
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from contact.models import Contact
from contact.tasks import contact_us_mail
from hotelenquiry.tasks import enquiry_hotel_mail
from review.models import Review
from hotelenquiry.models import HotelEnquiry   


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class':'form-control border border-none text-dark', 'type':'password', 'align':'center', 'placeholder':'Password'}),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={'class':'form-control border border-none text-dark', 'type':'password', 'align':'center', 'placeholder':'Password'}),
    )
    
    class Meta:
        model = User
        fields = ("first_name",'last_name','username',"email","password1","password2")
        widgets = {
            'first_name':forms.TextInput(attrs={"class":'form-control  border border-none text-dark',"type":"text","placeholder":"First Name","id":"first_name_id"}),
            'last_name':forms.TextInput(attrs={"class":'form-control border border-none text-dark',"type":"text","placeholder":"Last Name","id":"last_name_id"}),
            'username':forms.TextInput(attrs={"class":'form-control border border-none text-dark',"type":"text","placeholder":" Userame","id":"username_id"}),
            'email':forms.EmailInput(attrs={"class":'form-control border border-none text-dark',"placeholder":"E-mail","id":"email_id"}),
        }

    def clean_username(self):
        username=self.cleaned_data['username']
        if len(username) < 4:
            print("firstname validation error")
            raise forms.ValidationError("enter name morethan 4")
        return username

class ContactForm(forms.ModelForm):
    
    class Meta:
        model = Contact
        fields = ("name","email","subject","message","phone")
        widgets = {
            'name':forms.TextInput(attrs={"class":'form-control',"placeholder":"Name"}),
            'email':forms.EmailInput(attrs={"class":'form-control',"placeholder":"Email"}),
            'subject':forms.TextInput(attrs={"class":'form-control',"placeholder":"Subject"}),
            'message':forms.Textarea(attrs={"class":'form-control',"placeholder":"Message","style":"height:120px"}),
            'phone':forms.TextInput(attrs={"class":'form-control',"placeholder":"Phone"}),
            
        }

    def send_email(self):
        message_body="\t"+self.cleaned_data['name']+" is trying to contact us for some information and left a message:\n\t"+self.cleaned_data['message']+"\n\nEmail : "+self.cleaned_data['email']+"\nPhone Number : "+self.cleaned_data['phone']

        contact_us_mail.delay(self.cleaned_data['subject'],self.cleaned_data['email'],message_body)

class ReviewForm(forms.ModelForm):
    
    class Meta:
        model=Review
        fields=('rating','review','hotel','user')
        widgets={
            'hotel':forms.TextInput(attrs={"class":'form-control',"placeholder":"hotel","value":"","type":"hidden"}),
            'user':forms.TextInput(attrs={"class":'form-control',"placeholder":"user","value":"","type":"hidden"}),
            'review':forms.Textarea(attrs={"class":'form-control',"placeholder":"Leave Review","style":"height:120px"}),
            

        }

class HotelEnquiryForm(forms.ModelForm):
    
    class Meta:
        model = HotelEnquiry
        fields = ("name","email","subject","message","phone")
        widgets = {
            'name':forms.TextInput(attrs={"class":'form-control w-100',"placeholder":"Name"}),
            'email':forms.EmailInput(attrs={"class":'form-control w-100',"placeholder":"Email"}),
            'subject':forms.TextInput(attrs={"class":'form-control w-100',"placeholder":"Subject"}),
            'message':forms.Textarea(attrs={"class":'form-control w-100',"placeholder":"Message","style":"height:120px"}),
            'phone':forms.TextInput(attrs={"class":'form-control w-100',"placeholder":"Phone"}),
            
        }

    def clean_phone(self):

        phone=self.cleaned_data['phone']
        if len(phone) != 10:
            print("this is phone validation")
            raise forms.ValidationError("Enter 10 digit Phone number only")
        return phone

    def send_enquiry_mail(self,hotel_id):
        message_body="\t"+self.cleaned_data['name']+" wants to do some enquiry and left a message:\n\t"+self.cleaned_data['message']+"\n\nEmail : "+self.cleaned_data['email']+"\nPhone Number : "+self.cleaned_data['phone']

        enquiry_hotel_mail.delay(self.cleaned_data['subject'],self.cleaned_data['email'],message_body,hotel_id)
