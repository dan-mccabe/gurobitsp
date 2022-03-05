from formulations import solve_f0, load_instances

# Load instances
instances = load_instances()

for inst in instances:
    print('NEW SOLVE')
    solve_f0(inst)
    print('\n\n\n')


