from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .topsis import topsis
import os
from django.conf import settings
from django.core.mail import EmailMessage
import numpy as np

def index(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)
        
        weights = list(map(float, request.POST['weights'].split(',')))
        impacts = request.POST['impacts'].split(',')
        email_id = request.POST['email']

        if len(weights) != len(impacts):
            return render(request, 'index.html', {'error': "Number of weights must be equal to number of impacts."})

        if not all(i in ['+', '-'] for i in impacts):
            return render(request, 'index.html', {'error': "Impacts must be either +ve or -ve."})

        # Process the TOPSIS method
        result = topsis(file_path, np.array(weights), np.array(impacts))
        result_file = os.path.join(settings.MEDIA_ROOT, 'result.csv')
        result.to_csv(result_file, index=False)

        # Send the result via email
        email = EmailMessage('TOPSIS Result', 'Please find the TOPSIS result attached.', to=[email_id])
        email.attach_file(result_file)
        email.send()

        fs.delete(filename)
        os.remove(result_file)

        return render(request, 'index.html', {'success': "The result file has been sent to your email."})

    return render(request, 'index.html')
