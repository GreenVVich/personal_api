from app.modules.calculations.schemas import SCalculator, SConstant, SInput, SValue, SValueAction

calculator = SCalculator(
    id="oven",
    inputs=[
        SInput(id="volume", required=True),
        SInput(id="object_volume", required=True),
    ],
    constants=[
        SConstant(id="air_density", value=1200),
        SConstant(id="object_density", value=1500),
        SConstant(id="heat_capacity", value=1000),
        SConstant(id="delta_temp", value=60),
        SConstant(id="efficiency_loss", value=0.2),
    ],
    values=[
        SValue(
            id="air_mass",
            actions=[
                SValueAction(
                    id="air_mass_raw",
                    function="multiply",
                    args=["volume", "air_density"],
                ),
            ],
            tags=["Partial", "Show"],
            text_template="Масса воздуха = {air_mass} кг",
        ),
        SValue(
            id="object_mass",
            actions=[
                SValueAction(
                    id="object_mass_raw",
                    function="multiply",
                    args=["object_volume", "object_density"],
                ),
            ],
            tags=["Partial"],
        ),
        SValue(
            id="air_energy",
            actions=[
                SValueAction(
                    id="air_energy_raw",
                    function="multiply",
                    args=["air_mass", "heat_capacity", "delta_temp"],
                ),
            ],
            tags=["Partial"],
        ),
        SValue(
            id="object_energy",
            actions=[
                SValueAction(
                    id="object_energy_raw",
                    function="multiply",
                    args=["object_mass", "heat_capacity", "delta_temp"],
                ),
            ],
            tags=["Partial"],
        ),
        SValue(
            id="needed_energy",
            actions=[
                SValueAction(
                    id="needed_energy_raw",
                    function="sum",
                    args=["air_energy", "object_energy"],
                ),
            ],
            tags=["Required", "Show"],
            text_template="Энергия = {needed_energy} Дж",
        ),
        SValue(
            id="total_energy_with_loss",
            actions=[
                SValueAction(
                    id="loss_multiplier",
                    function="sum",
                    args=[1, "efficiency_loss"],
                ),
                SValueAction(
                    id="total_energy_with_loss_raw",
                    function="multiply",
                    args=["needed_energy", "loss_multiplier"],
                ),
            ],
            tags=["Required", "Show"],
            text_template="С учётом потерь = {total_energy_with_loss} Дж",
        ),
    ],
)
