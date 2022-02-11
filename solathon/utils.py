def lamport_to_sol(lamports: int) -> int:
    return int(lamports / 1000000000)

def sol_to_lamport(lamports: int) -> int:
    return int(lamports * 1000000000)

