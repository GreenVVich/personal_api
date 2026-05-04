from app.box.core import Box, BoxAction

box = Box(
    name="oven",
    cells={
        "inputs": [
            {"id": "volume", "required": True},
            {"id": "object_volume", "required": True},
        ],
        "constants": [
            {"id": "air_density", "value": 1200},
            {"id": "object_density", "value": 1500},
            {"id": "heat_capacity", "value": 1000},
            {"id": "delta_temp", "value": 60},
            {"id": "efficiency_loss", "value": 0.2},
        ],
        "values": [
            {
                "id": "air_mass",
                "actions": [{"id": "air_mass_raw", "function": "multiply", "args": ["volume", "air_density"]}],
                "tags": ["Partial", "Show"],
                "text_template": "Масса воздуха = {air_mass} кг",
            },
            {
                "id": "object_mass",
                "actions": [
                    {"id": "object_mass_raw", "function": "multiply", "args": ["object_volume", "object_density"]}
                ],
                "tags": ["Partial"],
            },
            {
                "id": "air_energy",
                "actions": [
                    {
                        "id": "air_energy_raw",
                        "function": "multiply",
                        "args": ["air_mass", "heat_capacity", "delta_temp"],
                    }
                ],
                "tags": ["Partial"],
            },
            {
                "id": "object_energy",
                "actions": [
                    {
                        "id": "object_energy_raw",
                        "function": "multiply",
                        "args": ["object_mass", "heat_capacity", "delta_temp"],
                    }
                ],
                "tags": ["Partial"],
            },
            {
                "id": "needed_energy",
                "actions": [{"id": "needed_energy_raw", "function": "sum", "args": ["air_energy", "object_energy"]}],
                "tags": ["Required", "Show"],
                "text_template": "Энергия = {needed_energy} Дж",
            },
            {
                "id": "total_energy_with_loss",
                "actions": [
                    {"id": "loss_multiplier", "function": "sum", "args": [1, "efficiency_loss"]},
                    {
                        "id": "total_energy_with_loss_raw",
                        "function": "multiply",
                        "args": ["needed_energy", "loss_multiplier"],
                    },
                ],
                "tags": ["Required", "Show"],
                "text_template": "С учётом потерь = {total_energy_with_loss} Дж",
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
