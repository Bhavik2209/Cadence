# myapp/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import process_data

@api_view(['POST'])
def process_data_view(request):
    input_data = request.data.get('input_data')
    if input_data is None:
        return Response({"error": "No input_data provided"}, status=400)
    
    processed_data = process_data(input_data)
    return Response({"processed_data": processed_data})
