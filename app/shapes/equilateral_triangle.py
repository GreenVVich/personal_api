from app.box.core import Box, BoxAction

box = Box(
    name="equilateral_triangle",
    cells={
        "inputs": [
            {"id": "side", "required": True},
        ],
        "constants": [],
        "values": [
            {
                "id": "perimeter",
                "actions": [
                    {"id": "perimeter_raw", "function": "multiply", "args": ["side", 3]},
                ],
                "tags": ["Show"],
                "text_template": "Периметр = {perimeter}",
            },
            {
                "id": "height",
                "actions": [
                    {"id": "sqrt_three", "function": "sqrt", "args": [3]},
                    {"id": "height_numerator", "function": "multiply", "args": ["side", "sqrt_three"]},
                    {
                        "id": "height_rounded",
                        "function": "divide",
                        "args": {"dividend": "height_numerator", "divisor": 2},
                    },
                    {"id": "height_final", "function": "round", "args": {"value": "height_rounded", "digits": 4}},
                ],
                "tags": ["Show"],
                "text_template": "Высота = {height}",
            },
            {
                "id": "area",
                "actions": [
                    {"id": "side_square", "function": "power", "args": {"base": "side", "exponent": 2}},
                    {"id": "area_numerator", "function": "multiply", "args": ["side_square", "sqrt_three"]},
                    {"id": "area_raw", "function": "divide", "args": {"dividend": "area_numerator", "divisor": 4}},
                    {"id": "area_final", "function": "round", "args": {"value": "area_raw", "digits": 4}},
                ],
                "tags": ["Show"],
                "text_template": "Площадь = {area}",
            },
            {
                "id": "median",
                "actions": [
                    {"id": "median_final", "function": "assign", "args": {"value": "height"}},
                ],
                "tags": ["Show"],
                "text_template": "Медиана = {median}",
            },
            {
                "id": "bisector",
                "actions": [
                    {"id": "bisector_final", "function": "assign", "args": {"value": "height"}},
                ],
                "tags": ["Show"],
                "text_template": "Биссектриса = {bisector}",
            },
            {
                "id": "inradius",
                "actions": [
                    {"id": "inradius_raw", "function": "divide", "args": {"dividend": "height", "divisor": 3}},
                    {"id": "inradius_final", "function": "round", "args": {"value": "inradius_raw", "digits": 4}},
                ],
                "tags": ["Show"],
                "text_template": "Радиус вписанной окружности = {inradius}",
            },
            {
                "id": "circumradius",
                "actions": [
                    {"id": "circumradius_numerator", "function": "multiply", "args": ["height", 2]},
                    {
                        "id": "circumradius_raw",
                        "function": "divide",
                        "args": {"dividend": "circumradius_numerator", "divisor": 3},
                    },
                    {
                        "id": "circumradius_final",
                        "function": "round",
                        "args": {"value": "circumradius_raw", "digits": 4},
                    },
                ],
                "tags": ["Show"],
                "text_template": "Радиус описанной окружности = {circumradius}",
            },
            {
                "id": "angle_a",
                "actions": [{"id": "angle_a_final", "function": "assign", "args": {"value": 60}}],
                "tags": ["Show"],
                "text_template": "Угол A = {angle_a}",
            },
            {
                "id": "angle_b",
                "actions": [{"id": "angle_b_final", "function": "assign", "args": {"value": 60}}],
                "tags": ["Show"],
                "text_template": "Угол B = {angle_b}",
            },
            {
                "id": "angle_c",
                "actions": [{"id": "angle_c_final", "function": "assign", "args": {"value": 60}}],
                "tags": ["Show"],
                "text_template": "Угол C = {angle_c}",
            },
        ],
    },
    actions={
        "calculate": BoxAction(
            handler="calculator.calculate",
            args={"inputs": {"$input": "inputs"}},
            description="Run calculator using the provided inputs",
        ),
    },
)
