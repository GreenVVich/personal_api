from app.tools.registry import register


def _sum_all(**values: float) -> float:
    return sum(values.values())


def _multiply_all(**values: float) -> float:
    result: float = 1.0
    for value in values.values():
        result *= value
    return result


@register("mass")
def mass(volume: float, density: float) -> float:
    return multiply(volume=volume, density=density)


@register("heat_energy")
def heat_energy(mass: float, c: float, dt: float) -> float:
    return multiply(mass=mass, c=c, dt=dt)


@register("sum")
def sum_values(**values: float) -> float:
    return _sum_all(**values)


@register("multiply")
def multiply(**values: float) -> float:
    return _multiply_all(**values)


@register("power")
def power(energy: float) -> float:
    return energy / 3600
