from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.sessions.models import Session
from .gui import *
from django.views import View
from django.http import JsonResponse
# Create your views here.
def home(request):
	return render(request,'home.html',{})

def base(request):
	return render(request,'base.html',{})

def Registeration(request):
	if request.method == "POST":
		F_name = request.POST['fname']
		L_name = request.POST['lname']
		U_mobile = request.POST['phone']
		U_email = request.POST['Eid']
		U_username = request.POST['uname']
		U_password = request.POST['pwd']
		if  UserDetails.objects.filter(Email = U_email ,Username = U_username).exists():
			myObjects = UserDetails.objects.all().filter(Email = U_email ,Username = U_username )
			name = myObjects[0].Username
			messages.error(request,'Already Registered Please Login')
			return render(request,'Login.html',{})
		else:
			users = UserDetails(Firstname = F_name, Lastname= L_name, Number =  U_mobile, Email =  U_email, Username = U_username, Password= U_password)
			users.save()
			messages.info(request,'Registered Sucessfully')
			return render(request,'Login.html',{})
	else:
		return render(request,'Registeration.html',{})

def Login(request):
	if request.method == "POST":
		C_name = request.POST['uname']
		C_password = request.POST['pwds']
		if UserDetails.objects.filter(Username=C_name, Password=C_password).exists():
			user = UserDetails.objects.all().filter(Username=C_name, Password=C_password)
			print(user)
			request.session['UserId'] = user[0].id
			print(request.session['UserId'])
			messages.info(request, 'logged in')
			request.session['UserId'] = user[0].id
			print(request.session['UserId'])
			request.session['type_id'] = 'User'
			request.session['UserType'] = C_name
			request.session['login'] = "Yes"
			return redirect("/")
		else:
			messages.info(request, 'Please Register')
			return redirect("/Registeration")
	else:
		return render(request,'Login.html',{})

def Logout(request):
	Session.objects.all().delete()
	return redirect("/")

def EditDetails(request):
	if request.method == "POST":
		UserID = request.session['UserId']
		F_name = request.POST['fname']
		L_name = request.POST['lname']
		U_mobile = request.POST['phone']
		U_email = request.POST['Eid']
		U_username = request.POST['uname']
		U_password = request.POST['pwd']
		UserDetails.objects.filter(id=UserID).update(Firstname = F_name, Lastname= L_name, Number =  U_mobile, Email =  U_email, Username = U_username, Password= U_password)
		return redirect('/EditDetails')
	else:
		UserID = request.session['UserId']
		user = UserDetails.objects.all().filter(id = UserID)
		return render(request,'EditDetails.html',{'user':user})

class Message(View):

	def post(self, request):
		msg = request.POST.get('text')
		response = chatbot_response(msg)
		print(response)
		valid=validators.url(response)
		if valid==True:
			data1 = 'True'
			data = {
			'respond': response,'respond1':data1
			}
			return JsonResponse(data)
		else:
			data1 = 'False'
			data = {
			'respond': response,'respond1':data1
			}
			return JsonResponse(data)
		

		#return HttpResponse('data')


	def clean_up_sentence(sentence):
		sentence_words = nltk.word_tokenize(sentence)
		sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
		return sentence_words

	def bow(sentence, words, show_details=True):
		sentence_words = clean_up_sentence(sentence)
		bag = [0] * len(words)
		for s in sentence_words:
			for i, w in enumerate(words):
				if w == s:
					bag[i] = 1
					if show_details:
						print("found in bag: %s" % w)
		return (np.array(bag))


	def predict_class(sentence, model):
		p = bow(sentence, words, show_details=False)
		print(p)
		res = model.predict(np.array([p]))[0]
		print(res)
		ERROR_THRESHOLD = 0.25
		results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
		results.sort(key=lambda x: x[1], reverse=True)
		return_list = []
		for r in results:
			return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
		return return_list

	def getResponse(ints, intents_json):
		tag = ints[0]['intent']
		list_of_intents = intents_json['intents']
		for i in list_of_intents:
			if (i['tag'] == tag):
				result = random.choice(i['responses'])
				print(result)
				break
		return result

	def chatbot_response(msg):
		ints = predict_class(msg, model)
		res = getResponse(ints, intents)
		print(res)
		
		return res

		
	   
	 
def ChatWindow(request):
	return render(request,'ChatWindow.html',{})


def ChatWindows(request):
	return render(request,'ChatWindows.html',{})
