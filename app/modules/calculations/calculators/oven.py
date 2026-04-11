from app.modules.calculations.schemas import SCalculator, SConstant, SInput, SValue


calculator = SCalculator(
    id="oven",
    inputs=[
        SInput(id="volume", required=True),
        SInput(id="object_volume", required=True),
    ],
    constants={
        "air_density": SConstant(value=1200),
        "object_density": SConstant(value=1500),
        "heat_capacity": SConstant(value=1000),
        "delta_temp": SConstant(value=60),
        "efficiency_loss": SConstant(value=0.2),
    },
    values=[
        SValue(
            id="air_mass",
            function="mass",
            args={"volume": "volume", "density": "air_density"},
            tags=["Partial", "Show"],
            text_template="Масса воздуха = {air_mass} кг",
        ),
        SValue(
            id="object_mass",
            function="mass",
            args={"volume": "object_volume", "density": "object_density"},
            tags=["Partial"],
        ),
        SValue(
            id="air_energy",
            function="heat_energy",
            args={"mass": "air_mass", "c": "heat_capacity", "dt": "delta_temp"},
            tags=["Partial"],
        ),
        SValue(
            id="object_energy",
            function="heat_energy",
            args={"mass": "object_mass", "c": "heat_capacity", "dt": "delta_temp"},
            tags=["Partial"],
        ),
        SValue(
            id="needed_energy",
            function="sum",
            args={
                "air_energy": "air_energy",
                "object_energy": "object_energy",
            },
            tags=["Required", "Show"],
            text_template="Энергия = {needed_energy} Дж",
        ),
        SValue(
            id="total_energy_with_loss",
            function="multiply",
            args={
                "needed_energy": "needed_energy",
                "efficiency_loss": "efficiency_loss",
            },
            tags=["Required", "Show"],
            text_template="С учётом потерь = {total_energy_with_loss} Дж",
        ),
    ],
)
