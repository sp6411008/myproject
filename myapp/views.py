from django.shortcuts import render
from .forms import SignUpForm,LoginForm
from .models import User,Products,Cart
from django.shortcuts import redirect
from django.core.mail import send_mail
import random
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Create your views here.
def index(request):
	return render(request,'myapp/index.html')
def fashion(request):
	fashions=Products.objects.filter(product_category="Fashion")
	for i in fashions:
		if i.product_sale:
			i.after_dicount_price=(i.product_price*i.product_sale_percentage)/100
			print(i.after_dicount_price)
			i.after_dicount_price=i.product_price-i.after_dicount_price
			i.save()
	return render(request,'myapp/fashion.html',{'fashions':fashions})
def electronics(request):
	electronics=Products.objects.filter(product_category="Electronics")
	for i in electronics:
		if i.product_sale:
			i.after_dicount_price=(i.product_price*i.product_sale_percentage)/100
			print(i.after_dicount_price)
			i.after_dicount_price=i.product_price-i.after_dicount_price
			i.save()
	return render(request,'myapp/electronics.html',{'electronics':electronics})
def home_appliance(request):
	appliances=Products.objects.filter(product_category="Home Appliance")
	for i in appliances:
		if i.product_sale:
			i.after_dicount_price=(i.product_price*i.product_sale_percentage)/100
			print(i.after_dicount_price)
			i.after_dicount_price=i.product_price-i.after_dicount_price
			i.save()
	return render(request,'myapp/home_appliance.html',{'appliances':appliances})
def sale(request):
	products=Products.objects.filter(product_sale=True)
	return render(request,'myapp/sale.html',{'products':products})
def signup(request):
	if request.method=="POST":
		fname=request.POST["first_name"]
		lname=request.POST["last_name"]
		email=request.POST["email"]
		address=request.POST["address"]
		mobile=request.POST["mobile"]
		passw=request.POST["password"]
		cpassw=request.POST["confirm_password"]
		user=User.objects.filter(email=email)
		if user:
			error="This email id is already registered with us"
			form=SignUpForm()
			return render(request,'myapp/signup.html',{'form':form,'error':error})
		else:
			User.objects.create(first_name=fname,last_name=lname,email=email,address=address,mobile=mobile,password=passw,confirm_password=cpassw)
			rec=[email,]
			subject="OTP For Successfull Registration"
			otp=random.randint(1000,9999)
			message="Your OTP For Registration Is "+str(otp)
			email_from = settings.EMAIL_HOST_USER
			send_mail(subject, message, email_from, rec)
			return render(request,'myapp/otp.html',{'otp':otp,'email':email})
	else:
		form=SignUpForm()
	return render(request,'myapp/signup.html',{'form':form})
def login(request):
	if request.method=="POST":
		email=request.POST["email"]
		passw=request.POST["password"]
		try:
			user=User.objects.get(email=email,password=passw)
			if user.status=="active":
				request.session['fname']=user.first_name
				request.session['lname']=user.last_name
				request.session['userpk']=user.pk
				
				return render(request,'myapp/index.html')
			else:
				error="Your Status Is Still Not Active. Do This By OTP."
				return render(request,'myapp/resend.html',{'error':error})

		except:
			error="Invalid Email Or Password"
			form=LoginForm()
			return render(request,'myapp/login.html',{'form':form,'error':error})
	else:
		form=LoginForm()
	return render(request,'myapp/login.html',{'form':form})
def logout(request):
	try:
		del request.session['fname']
		del request.session['lname']
		return redirect('index')
	except:
		pass
def detail(request,pk):
	product=Products.objects.get(pk=pk)
	return render(request,'myapp/detail.html',{'product':product})
def add_cart(request,pk1,pk2):
	user=User.objects.get(pk=pk1)
	product=Products.objects.get(pk=pk2)
	Cart.objects.create(user=user,product=product)
	return redirect('show_cart')
def show_cart(request):
	user=User.objects.get(pk=request.session['userpk'])
	carts=Cart.objects.filter(user=user)
	return render(request,'myapp/show_cart.html',{'carts':carts})
def remove_cart(request,pk):
	cart=Cart.objects.get(pk=pk)
	cart.delete()
	return redirect('show_cart')
def validate_otp(request):
	g_otp=request.POST["g_otp"]
	otp=g_otp
	e_otp=request.POST["e_otp"]
	email=request.POST["email"]

	if g_otp==e_otp:
		user=User.objects.get(email=email)
		user.status="active"
		user.save()
		return redirect('login')
	else:
		error="Invalid OTP"
		return render(request,'myapp/otp.html',{'otp':otp,'email':email,'error':error})
def resend(request):
	email=request.POST["email"]
	rec=[email,]
	subject="OTP For Successfull Registration"
	otp=random.randint(1000,9999)
	message="Your OTP For Registration Is "+str(otp)
	email_from = settings.EMAIL_HOST_USER
	send_mail(subject, message, email_from, rec)
	return render(request,'myapp/otp.html',{'otp':otp,'email':email})
def enter_email(request):
	if request.method=="POST":
		email=request.POST["email"]
		try:
			user=User.objects.get(email=email)
			if user:
				rec=[email,]
				subject="OTP For Reset Password"
				otp=random.randint(1000,9999)
				message="Your OTP For Reset Password Is "+str(otp)
				email_from = settings.EMAIL_HOST_USER
				send_mail(subject, message, email_from, rec)
				return render(request,'myapp/reset_password_otp.html',{'otp':otp,'email':email})
		except:
			error="This Email Id Is Not Registered With Us."
			return render(request,'myapp/enter_email.html',{'error':error})	
	else:
		return render(request,'myapp/enter_email.html')
def validate_password_OTP(request):
	g_otp=request.POST["g_otp"]
	otp=g_otp
	e_otp=request.POST["e_otp"]
	email=request.POST["email"]

	if g_otp==e_otp:
		user=User.objects.get(email=email)
		return render(request,'myapp/enter_new_password.html',{'email':email})
	else:
		error="Invalid OTP"
		return render(request,'myapp/reset_password_otp.html',{'otp':otp,'email':email,'error':error})
def change_password(request):
	email=request.POST['email']
	password=request.POST['password']
	cpassword=request.POST['cpassword']

	if password==cpassword:
		user=User.objects.get(email=email)
		user.password=password
		user.confirm_password=cpassword
		user.save()
		form=LoginForm()
	return redirect("login")
def profile(request):
	if request.session["fname"]:
		user=User.objects.get(pk=request.session['userpk'])
		return render(request,'myapp/profile.html',{'user':user})
	return redirect("index")
def profile_update(request):
	if request.method=="POST":
		address=request.POST["address"]
		mobile=request.POST["mobile"]
		user_image=request.FILES["user_image"]
		fs = FileSystemStorage()
		filename = fs.save(user_image.name, user_image)
		uploaded_file_url = fs.url(filename)
		user=User.objects.get(pk=request.session["userpk"])
		user.address=address
		user.mobile=mobile
		user.user_image=user_image
		user.save()
		return redirect("profile")
	return redirect("profile")
def change_user_password(request):
	if request.method=="POST":
		old_password=request.POST["old_password"]
		new_password=request.POST["new_password"]
		confirm_new_password=request.POST["confirm_new_password"]
		user=User.objects.get(pk=request.session["userpk"])
		if user.password==old_password:
			if new_password==confirm_new_password:
				user.password=new_password
				user.confirm_password=new_password
				user.save()
				return redirect("index")
			else:
				error="New Password And Confirm New Password Does Not Match"
				return render(request,'myapp/change_user_password.html',{'error':error})
		else:
			error="Old Password Is Incorrect"
			return render(request,'myapp/change_user_password.html',{'error':error})	
	else:
		return render(request,"myapp/change_user_password.html")
