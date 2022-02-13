def lamport_to_sol(lamports: int) -> float:
    return float(lamports / 1000000000)


def sol_to_lamport(sol: float) -> float:
    return float(sol * 1000000000)
