from django.shortcuts import render
import json
from test_dev_app.forms import UploadJSONForm
from test_dev_app.Logic.main import main
from test_dev_app.Logic.main import error_class

def upload_json(request):
    context = {}
    if request.method == 'POST':
        form = UploadJSONForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                json_file = request.FILES['json_file']
                chanceProba=main(json_file)
                context['data'] = "The survival probability is "+str(chanceProba)
        except Exception as exception:
            context['data']=error_class.errorsList[0]
    else:
        form = UploadJSONForm()

    context['form'] = form
    return render(request, 'upload.html', context)