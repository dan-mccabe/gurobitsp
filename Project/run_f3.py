from formulations import solve_f3, load_instances


def run_f3():
    print('\n\n*** FORMULATION F3 ***\n\n')

    # Load instances
    instances = load_instances()

    names = ['bays29', 'dantzig42', 'pr76', 'rat99']
    for i, inst in enumerate(instances):
        # Solve as-is initially
        print('*** Solving Model {} ***'.format(names[i]))
        solve_f3(inst)
        print()

        # Turn off Presolve
        print('Presolve Turned Off\n')
        solve_f3(inst, **{'Presolve': 0})
        print()

        # Turn off cuts
        print('Cuts Turned Off\n')
        solve_f3(inst, **{'Cuts': 0})
        print()

        # Turn off both presolve and cuts
        print('Presolve and Cuts Turned Off\n')
        solve_f3(inst, **{'Presolve': 0, 'Cuts': 0})
        print()


if __name__ == '__main__':
    from run_f2 import run_f2
    run_f2()
    run_f3()


