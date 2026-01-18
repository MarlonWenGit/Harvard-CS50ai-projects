import csv
import itertools
import sys
import copy

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def b_given_a(p_a, p_b, a_given_b):
    return (a_given_b * p_b) / p_a


def child(Mgene, Fgene):
    '''
    Calculates the probability distribution of a child's genes 
    based on the probability distributions of the parents
    '''
    pBoth = 1
    distribution = {0:0, 1:0, 2:0}
    mutation_chance = PROBS['mutation']
    if Mgene == 0:
        Mpass_down = mutation_chance
    elif Mgene == 1:
        Mpass_down = 0.5
    elif Mgene == 2:
        Mpass_down = 1 - mutation_chance
            
    if Fgene == 0:
        Fpass_down = mutation_chance
    elif Fgene == 1:
        Fpass_down = 0.5
    elif Fgene == 2:
        Fpass_down = 1 - mutation_chance

    distribution[0] = distribution[0] + (1 - Mpass_down) * (1 - Fpass_down) * pBoth
    distribution[1] = distribution[1] + ((Mpass_down) * (1 - Fpass_down) + (1 - Mpass_down) * (Fpass_down)) * pBoth
    distribution[2] = distribution[2] + (Mpass_down) * (Fpass_down) * pBoth
    return distribution


def x_gene(person, people, x, have_trait, one_gene, two_genes):
    mother = people[person]['mother']
    father = people[person]['father']
    trait = people[person]['trait']
    if mother == None and father == None:
        #if trait == None:
            #return PROBS["gene"][int(x)]
        if person in have_trait:
            return PROBS["trait"][int(x)][True] * PROBS["gene"][int(x)]
        elif person not in have_trait:
            return PROBS["trait"][int(x)][False] * PROBS["gene"][int(x)]
        else:
            raise ValueError
    else:
        if mother in one_gene:
            mother_genes = 1
        elif mother in two_genes:
            mother_genes = 2
        else:
            mother_genes = 0
        
        if father in one_gene:
            father_genes = 1
        elif father in two_genes:
            father_genes = 2
        else:
            father_genes = 0
        '''
        if mother_trait == True:
            mother_genes[0] = PROBS["trait"][0][True] * PROBS["gene"][0]
            mother_genes[1] = PROBS["trait"][1][True] * PROBS["gene"][1]
            mother_genes[2] = PROBS["trait"][2][True] * PROBS["gene"][2]
        else:
            mother_genes[0] = PROBS["trait"][0][False] * PROBS["gene"][0]
            mother_genes[1] = PROBS["trait"][1][False] * PROBS["gene"][1]
            mother_genes[2] = PROBS["trait"][2][False] * PROBS["gene"][2]
        
        if father_trait == True:
            father_genes[0] = PROBS["trait"][0][True] * PROBS["gene"][0]
            father_genes[1] = PROBS["trait"][1][True] * PROBS["gene"][1]
            father_genes[2] = PROBS["trait"][2][True] * PROBS["gene"][2]
        else:
            father_genes[0] = PROBS["trait"][0][False] * PROBS["gene"][0]
            father_genes[1] = PROBS["trait"][1][False] * PROBS["gene"][1]
            father_genes[2] = PROBS["trait"][2][False] * PROBS["gene"][2]
        
        '''
        gene_distribution = child(mother_genes, father_genes)
        if person in have_trait:
            return gene_distribution[int(x)] * PROBS["trait"][int(x)][True]
        elif person not in have_trait:
            return gene_distribution[int(x)] * PROBS["trait"][int(x)][False]
        else:
            return gene_distribution[int(x)]
    
def has_trait(person, people):
    gene_distribution = dict()
    for x in range(3):
        gene_distribution[x] = x_gene(person, people, x)
    return gene_distribution[0] * PROBS['trait'][0][True] + gene_distribution[1] * PROBS['trait'][1][True] + gene_distribution[2] * PROBS['trait'][2][True]
    

def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    joint = 1

    for person in people:
        if person in one_gene:
            joint = joint * x_gene(person, people, 1, have_trait, one_gene, two_genes)
            
        elif person in two_genes:
            joint = joint * x_gene(person, people, 2, have_trait, one_gene, two_genes)
            
        else:
            joint = joint * x_gene(person, people, 0, have_trait, one_gene, two_genes)
            
        
        #if person in have_trait:
            #if people[person]['trait'] == None:
                #joint = joint * has_trait(person, people)
        #else:
            #if people[person]['trait'] == None:
                #joint = joint * (1 - has_trait(person, people))

    return joint


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        if person in one_gene:
            probabilities[person]["gene"][1] = p
        elif person in two_genes:
            probabilities[person]["gene"][2] = p
        else:
            probabilities[person]["gene"][0] = p
        
        if person in have_trait:
            probabilities[person]["trait"][True] = p
        else:
            probabilities[person]["trait"][False] = p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        T = probabilities[person]["trait"][True]
        F = probabilities[person]["trait"][False]
        a = 1 / (T + F)
        probabilities[person]["trait"][True] = a * probabilities[person]["trait"][True]
        probabilities[person]["trait"][False] = a * probabilities[person]["trait"][False]
        gene_0 = probabilities[person]["gene"][0]
        gene_1 = probabilities[person]["gene"][1]
        gene_2 = probabilities[person]["gene"][2]
        a = 1 / (gene_0 + gene_1 + gene_2)
        probabilities[person]["gene"][0] = a * probabilities[person]["gene"][0]
        probabilities[person]["gene"][1] = a * probabilities[person]["gene"][1]
        probabilities[person]["gene"][2] = a * probabilities[person]["gene"][2]


if __name__ == "__main__":
    people = {
  'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None},
  'James': {'name': 'James', 'mother': None, 'father': None, 'trait': None},
  'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': None}
    }

    print(joint_probability(people, {}, {}, {}))
    main()
