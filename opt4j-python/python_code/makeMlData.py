import pandas as pd
from numpy.random import RandomState

"""
Rudimentary implementation of the conversion of the raw TSM data into data that can be processed by ML algos. Usable as
reference until done properly.
"""

column_name_objective = 'objective'
column_name_generation = 'generation'


def make_training_data(n_training_points, generation_start, generation_stop, random_state=None,
                       fileName='data/tsm_simple.csv', genotype_combination="concatenate"):
    rand = RandomState(random_state)
    names = []
    for i in range(0, 100):
        names.append(str(i))
    names.append(column_name_objective)
    names.append(column_name_generation)

    # read the data into a data frame
    df = pd.read_csv(fileName, sep='\t', names=names)

    # remove the non-unique entries
    df.drop_duplicates(inplace=True, subset=df[df.columns.difference([column_name_generation, column_name_objective])])

    # remove unrelated generations
    df = df[df[column_name_generation] <= generation_stop]
    df = df[df[column_name_generation] >= generation_start]

    # make the necessary amount of training points
    result = pd.DataFrame()
    for _ in xrange(n_training_points):
        result = pd.concat([result, make_training_series(pick_two_samples(df, generation_start,
                                                                          generation_stop, rand=rand, mode='generation_wise'), genotype_combination)],
                           axis=1, ignore_index=True)
    return result.transpose()


def pick_two_samples(original_data, start_gen, end_gen, rand=RandomState(), mode='fully_random'):
    """
    randomly picks two samples from the provided data frame

    :param original_data: dataframe containing the genotypes and the objectives
    :param rand: random_state
    :param start_gen: the first generation to consider
    :param end_gen: the last generation to consider
    :param mode: parameter to choose how learner is trained
    :return: a tuple of genotype data for the training
    """
    if mode == 'fully_random':
        row_num = original_data.shape[0]
        indices = rand.randint(0, row_num, 2)
        return original_data.iloc[indices[0], :], original_data.iloc[indices[1], :]
    if mode == 'generation_wise':
        parent_gen = rand.randint(start_gen, end_gen - 1)
        offspring_gen = parent_gen + 1
        df_parents = original_data[original_data[column_name_generation] == parent_gen]
        df_offsprings = original_data[original_data[column_name_generation] == offspring_gen]
        parent_row_n = rand.randint(0, df_parents.shape[0])
        offspring_row_n = rand.randint(0, df_offsprings.shape[0])
        parent = df_parents.iloc[parent_row_n, :]
        offspring = df_offsprings.iloc[offspring_row_n, :]
        return parent, offspring





def make_training_series(series_tuple, genotype_combination):
    """
    Takes two series representing two genotypes and returns a training input representing their comparison
    :param series_tuple: a tuple of genotype data
    :return: training input series
    """

    series_a, series_b = series_tuple[0], series_tuple[1]

    # make the class label
    class_label = 1 if series_a[column_name_objective] > series_b[column_name_objective] else 0

    # drop the generation and the objective column
    part_a = series_a.drop([column_name_objective, column_name_generation])
    part_b = series_b.drop([column_name_objective, column_name_generation])

    # generate the result series
    if genotype_combination == 'concatenate':
        combined_series = concatenate_genotypes(part_a, part_b)
    elif genotype_combination == 'difference_abs':
        combined_series = difference_abs(part_a, part_b)
    else:
        raise ValueError("Unknown type of genotype combination")

    label_series = pd.Series([class_label])
    result = pd.concat([combined_series, label_series], ignore_index=True)
    return result

def difference_abs(geno_a, geno_b):
    """
    Substracts second genotype from first. Positive differences scaled to 1, negative to -1. The result is a feature
    vector with n feature, where n is the number of the genes.

    :param geno_a:
    :param geno_b:
    :return:
    """
    result = geno_a - geno_b
    result[result > 0] = 1
    result[result < 0] = -1
    return result


def concatenate_genotypes(geno_a, geno_b):
    """
    Simply concatenates the given gynotype. If n is the gene number of a genotype, the result will be a feature vector
    with 2*n features.

    :param geno_a:
    :param geno_b:
    :return: concatenated genotype
    """
    return geno_a.append(geno_b, ignore_index=True)


