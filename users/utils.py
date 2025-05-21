from rest_framework.response import Response

def api_response(data=None, message=None, status="success", status_code=200):
    response_data = {"status": status}
    
    if data is not None:
        response_data["data"] = data
        
    if message is not None:
        response_data["message"] = message
        
    return Response(response_data, status=status_code)
