import azure.functions as func
import logging
import math

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="CalculateArea", methods=['GET', 'POST'])
def CalculateArea(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Get parameters from query string or request body
    shape = req.params.get('shape')
    if not shape:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            shape = req_body.get('shape')

    if not shape:
        return func.HttpResponse(
            "Please provide a shape type (circle, rectangle, triangle, square) in the query string or request body.",
            status_code=400
        )

    shape = shape.lower()

    try:
        if shape == 'circle':
            radius = req.params.get('radius') or req_body.get('radius')
            if not radius:
                return func.HttpResponse("Radius is required for circle calculation.", status_code=400)
            radius = float(radius)
            if radius < 0:
                return func.HttpResponse("Radius cannot be negative.", status_code=400)
            area = math.pi * radius ** 2
            result = {"shape": "circle", "radius": radius, "area": round(area, 2)}

        elif shape == 'rectangle':
            length = req.params.get('length') or req_body.get('length')
            width = req.params.get('width') or req_body.get('width')
            if not length or not width:
                return func.HttpResponse("Length and width are required for rectangle calculation.", status_code=400)
            length = float(length)
            width = float(width)
            if length < 0 or width < 0:
                return func.HttpResponse("Dimensions cannot be negative.", status_code=400)
            area = length * width
            result = {"shape": "rectangle", "length": length, "width": width, "area": round(area, 2)}

        elif shape == 'triangle':
            base = req.params.get('base') or req_body.get('base')
            height = req.params.get('height') or req_body.get('height')
            if not base or not height:
                return func.HttpResponse("Base and height are required for triangle calculation.", status_code=400)
            base = float(base)
            height = float(height)
            if base < 0 or height < 0:
                return func.HttpResponse("Dimensions cannot be negative.", status_code=400)
            area = 0.5 * base * height
            result = {"shape": "triangle", "base": base, "height": height, "area": round(area, 2)}

        elif shape == 'square':
            side = req.params.get('side') or req_body.get('side')
            if not side:
                return func.HttpResponse("Side length is required for square calculation.", status_code=400)
            side = float(side)
            if side < 0:
                return func.HttpResponse("Side length cannot be negative.", status_code=400)
            area = side ** 2
            result = {"shape": "square", "side": side, "area": round(area, 2)}

        else:
            return func.HttpResponse(
                f"Unsupported shape: {shape}. Supported shapes: circle, rectangle, triangle, square.",
                status_code=400
            )

        return func.HttpResponse(
            body=str(result),
            status_code=200,
            headers={"Content-Type": "application/json"}
        )

    except (ValueError, TypeError) as e:
        return func.HttpResponse(
            f"Invalid input: {str(e)}. Please provide valid numeric values.",
            status_code=400
        )
    except Exception as e:
        logging.error(f"Error calculating area: {str(e)}")
        return func.HttpResponse(
            "An error occurred while processing your request.",
            status_code=500
        )