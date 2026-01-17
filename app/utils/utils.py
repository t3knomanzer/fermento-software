import gc


def print_mem():
    print(f"Mem Free: {gc.mem_free() / 1000}Kb -- Allocated: {gc.mem_alloc() / 1000}Kb")
