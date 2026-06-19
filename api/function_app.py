import azure.functions as func
import logging
import math
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="CalculateArea", methods=['GET', 'POST', 'OPTIONS'])
def CalculateArea(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Handle CORS preflight request
    if req.method == 'OPTIONS':
        return func.HttpResponse(
            status_code=204,
            headers={
                'Access-Control-Allow-Origin': '*',  # Or specify your domain
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, x-functions-key',
                'Access-Control-Max-Age': '86400'
            }
        )

    # Get parameters from query string or request body
    shape = req.params.get('shape')
    req_body = None
    
    if not shape:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            shape = req_body.get('shape')

    if not shape:
        response = func.HttpResponse(
            "Please provide a shape type (circle, rectangle, triangle, square) in the query string or request body.",
            status_code=400
        )
    else:
        shape = shape.lower()

        try:
            if shape == 'circle':
                radius = req.params.get('radius') or (req_body.get('radius') if req_body else None)
                if not radius:
                    response = func.HttpResponse("Radius is required for circle calculation.", status_code=400)
                else:
                    radius = float(radius)
                    if radius < 0:
                        response = func.HttpResponse("Radius cannot be negative.", status_code=400)
                    else:
                        area = math.pi * radius ** 2
                        result = {"shape": "circle", "radius": radius, "area": round(area, 2)}
                        response = func.HttpResponse(
                            body=json.dumps(result),
                            status_code=200,
                            headers={"Content-Type": "application/json"}
                        )

            elif shape == 'rectangle':
                length = req.params.get('length') or (req_body.get('length') if req_body else None)
                width = req.params.get('width') or (req_body.get('width') if req_body else None)
                if not length or not width:
                    response = func.HttpResponse("Length and width are required for rectangle calculation.", status_code=400)
                else:
                    length = float(length)
                    width = float(width)
                    if length < 0 or width < 0:
                        response = func.HttpResponse("Dimensions cannot be negative.", status_code=400)
                    else:
                        area = length * width
                        result = {"shape": "rectangle", "length": length, "width": width, "area": round(area, 2)}
                        response = func.HttpResponse(
                            body=json.dumps(result),
                            status_code=200,
                            headers={"Content-Type": "application/json"}
                        )

            elif shape == 'triangle':
                base = req.params.get('base') or (req_body.get('base') if req_body else None)
                height = req.params.get('height') or (req_body.get('height') if req_body else None)
                if not base or not height:
                    response = func.HttpResponse("Base and height are required for triangle calculation.", status_code=400)
                else:
                    base = float(base)
                    height = float(height)
                    if base < 0 or height < 0:
                        response = func.HttpResponse("Dimensions cannot be negative.", status_code=400)
                    else:
                        area = 0.5 * base * height
                        result = {"shape": "triangle", "base": base, "height": height, "area": round(area, 2)}
                        response = func.HttpResponse(
                            body=json.dumps(result),
                            status_code=200,
                            headers={"Content-Type": "application/json"}
                        )

            elif shape == 'square':
                side = req.params.get('side') or (req_body.get('side') if req_body else None)
                if not side:
                    response = func.HttpResponse("Side length is required for square calculation.", status_code=400)
                else:
                    side = float(side)
                    if side < 0:
                        response = func.HttpResponse("Side length cannot be negative.", status_code=400)
                    else:
                        area = side ** 2
                        result = {"shape": "square", "side": side, "area": round(area, 2)}
                        response = func.HttpResponse(
                            body=json.dumps(result),
                            status_code=200,
                            headers={"Content-Type": "application/json"}
                        )

            else:
                response = func.HttpResponse(
                    f"Unsupported shape: {shape}. Supported shapes: circle, rectangle, triangle, square.",
                    status_code=400
                )

        except (ValueError, TypeError) as e:
            response = func.HttpResponse(
                f"Invalid input: {str(e)}. Please provide valid numeric values.",
                status_code=400
            )
        except Exception as e:
            logging.error(f"Error calculating area: {str(e)}")
            response = func.HttpResponse(
                "An error occurred while processing your request.",
                status_code=500
            )

    # Add CORS headers to all responses
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, x-functions-key'
    
    return response