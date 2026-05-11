def select_best(population):

    sorted_population = sorted(

        population,

        key=lambda x: x["fitness"],

        reverse=True
    )

    return sorted_population[:2]