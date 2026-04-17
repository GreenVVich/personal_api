from app.modules.calculations.schemas import SCalculator, SInput, SValue, SValueAction

calculator = SCalculator(
    id="equilateral_triangle",
    inputs=[
        SInput(id="side", required=True),
    ],
    values=[
        SValue(
            id="perimeter",
            actions=[
                SValueAction(
                    id="perimeter_raw",
                    function="multiply",
                    args=["side", 3],
                ),
            ],
            tags=["Show"],
            text_template="Периметр = {perimeter}",
        ),
        SValue(
            id="height",
            actions=[
                SValueAction(
                    id="sqrt_three",
                    function="sqrt",
                    args=[3],
                ),
                SValueAction(
                    id="height_numerator",
                    function="multiply",
                    args=["side", "sqrt_three"],
                ),
                SValueAction(
                    id="height_rounded",
                    function="divide",
                    args={"dividend": "height_numerator", "divisor": 2},
                ),
                SValueAction(
                    id="height_final",
                    function="round",
                    args={"value": "height_rounded", "digits": 4},
                ),
            ],
            tags=["Show"],
            text_template="Высота = {height}",
        ),
        SValue(
            id="area",
            actions=[
                SValueAction(
                    id="side_square",
                    function="power",
                    args={"base": "side", "exponent": 2},
                ),
                SValueAction(
                    id="area_numerator",
                    function="multiply",
                    args=["side_square", "sqrt_three"],
                ),
                SValueAction(
                    id="area_raw",
                    function="divide",
                    args={"dividend": "area_numerator", "divisor": 4},
                ),
                SValueAction(
                    id="area_final",
                    function="round",
                    args={"value": "area_raw", "digits": 4},
                ),
            ],
            tags=["Show"],
            text_template="Площадь = {area}",
        ),
        SValue(
            id="median",
            actions=[
                SValueAction(
                    id="median_final",
                    function="assign",
                    args={"value": "height"},
                ),
            ],
            tags=["Show"],
            text_template="Медиана = {median}",
        ),
        SValue(
            id="bisector",
            actions=[
                SValueAction(
                    id="bisector_final",
                    function="assign",
                    args={"value": "height"},
                ),
            ],
            tags=["Show"],
            text_template="Биссектриса = {bisector}",
        ),
        SValue(
            id="inradius",
            actions=[
                SValueAction(
                    id="inradius_raw",
                    function="divide",
                    args={"dividend": "height", "divisor": 3},
                ),
                SValueAction(
                    id="inradius_final",
                    function="round",
                    args={"value": "inradius_raw", "digits": 4},
                ),
            ],
            tags=["Show"],
            text_template="Радиус вписанной окружности = {inradius}",
        ),
        SValue(
            id="circumradius",
            actions=[
                SValueAction(
                    id="circumradius_numerator",
                    function="multiply",
                    args=["height", 2],
                ),
                SValueAction(
                    id="circumradius_raw",
                    function="divide",
                    args={"dividend": "circumradius_numerator", "divisor": 3},
                ),
                SValueAction(
                    id="circumradius_final",
                    function="round",
                    args={"value": "circumradius_raw", "digits": 4},
                ),
            ],
            tags=["Show"],
            text_template="Радиус описанной окружности = {circumradius}",
        ),
        SValue(
            id="angle_a",
            actions=[
                SValueAction(
                    id="angle_a_final",
                    function="assign",
                    args={"value": 60},
                ),
            ],
            tags=["Show"],
            text_template="Угол A = {angle_a}",
        ),
        SValue(
            id="angle_b",
            actions=[
                SValueAction(
                    id="angle_b_final",
                    function="assign",
                    args={"value": 60},
                ),
            ],
            tags=["Show"],
            text_template="Угол B = {angle_b}",
        ),
        SValue(
            id="angle_c",
            actions=[
                SValueAction(
                    id="angle_c_final",
                    function="assign",
                    args={"value": 60},
                ),
            ],
            tags=["Show"],
            text_template="Угол C = {angle_c}",
        ),
    ],
)
