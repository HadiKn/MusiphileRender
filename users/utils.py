from rest_framework.response import Response

def api_response(data=None, message=None, status="success", status_code=200):
    """
    Standardized API response format
    
    Args:
        data: The data to return (optional)
        message: A message to include in the response (optional)
        status: The status of the response (success, error, etc.)
        status_code: The HTTP status code
        
    Returns:
        Response object with standardized format
    """
    response_data = {"status": status}
    
    if data is not None:
        response_data["data"] = data
        
    if message is not None:
        response_data["message"] = message
        
    return Response(response_data, status=status_code)
