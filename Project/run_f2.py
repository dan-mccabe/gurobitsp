from formulations import solve_f2, load_instances

# Load instances
instances = load_instances()

# Solve as-is initially
for inst in instances:
    print('NEW SOLVE')
    solve_f2(inst)
    print('\n\n\n')


