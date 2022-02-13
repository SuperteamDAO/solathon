LAMPORT_PER_SOL = 1000000000
SOL_PER_LAMPORT = 1 / LAMPORT_PER_SOL


def lamport_to_sol(lamports: int) -> float:
    return float(lamports / SOL_PER_LAMPORT)


def sol_to_lamport(sol: float) -> int:
    return int(sol * LAMPORT_PER_SOL)
