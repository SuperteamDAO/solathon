LAMPORT_PER_SOL = 1000000000
SOL_PER_LAMPORT = 1 / LAMPORT_PER_SOL
SOL_FLOATING_PRECISION = 9


def truncate_float(number, length):
    number = number * pow(10, length)
    number = int(number)
    number = float(number)
    number /= pow(10, length)
    return number


def lamport_to_sol(lamports: int) -> float:
    return truncate_float(lamports * SOL_PER_LAMPORT, SOL_FLOATING_PRECISION)


def sol_to_lamport(sol: float) -> int:
    return int(sol * LAMPORT_PER_SOL)
