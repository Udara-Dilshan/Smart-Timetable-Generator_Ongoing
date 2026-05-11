from app.ga.population import generate_population

from app.ga.selection import select_best

from app.ga.crossover import crossover

from app.ga.mutation import mutate

from app.ga.fitness import calculate_fitness

from app.ga.repair import repair_timetable


def evolve_timetable(

    db,

    generations=30
):

    population = generate_population(

        db,

        size=10
    )

    best_solution = None

    best_fitness = 0

    for generation in range(generations):

        scored_population = []

        for timetable in population:

            repaired = repair_timetable(

                timetable
            )

            fitness = calculate_fitness(

                repaired
            )

            scored_population.append({

                "fitness": fitness,

                "timetable": repaired
            })

        scored_population.sort(

            key=lambda x: x["fitness"],

            reverse=True
        )

        if (

            scored_population[0]["fitness"]

            >

            best_fitness
        ):

            best_fitness = (

                scored_population[0]["fitness"]
            )

            best_solution = (

                scored_population[0]["timetable"]
            )

        selected = select_best(

            scored_population
        )

        new_population = []

        while len(new_population) < 10:

            parent1 = selected[0]["timetable"]

            parent2 = selected[1]["timetable"]

            child = crossover(

                parent1,

                parent2
            )

            child = mutate(child)

            child = repair_timetable(child)

            new_population.append(child)

        population = new_population

    return {

        "best_fitness": best_fitness,

        "best_timetable": best_solution
    }