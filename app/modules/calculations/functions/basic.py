from app.tools.registry import register


@register("mass")
def mass(volume: float, density: float):
    return volume * density


@register("heat_energy")
def heat_energy(mass: float, c: float, dt: float):
    return mass * c * dt


@register("sum")
def sum_values(a: float, b: float):
    return a + b


@register("multiply")
def multiply(a: float, b: float):
    return a * b


@register("power")
def power(energy: float):
    return energy / 3600
