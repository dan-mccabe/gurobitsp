from formulations import solve_f2, load_instances


def run_f2():
    print('\n\n*** FORMULATION F2 ***\n\n')
    # Load instances
    instances = load_instances()

    names = ['bays29', 'dantzig42', 'pr76', 'rat99']
    for i, inst in enumerate(instances):
        # Solve as-is initially
        print('*** Solving Model {} ***'.format(names[i]))
        solve_f2(inst)
        print()

        # Turn off Presolve
        print('Presolve Turned Off\n')
        solve_f2(inst, **{'Presolve': 0})
        print()

        # Turn off cuts
        print('Cuts Turned Off\n')
        solve_f2(inst, **{'Cuts': 0})
        print()

        # Turn off both presolve and cuts
        print('Presolve and Cuts Turned Off\n')
        solve_f2(inst, **{'Presolve': 0, 'Cuts': 0})
        print()


