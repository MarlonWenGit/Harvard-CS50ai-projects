import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    probability_distribution = dict()
    base_probability = round((1 - damping_factor) / len(corpus), 9)

    links_on_page = corpus[page] #set containing all links on that page
    
    if len(links_on_page) == 0:
        for link in corpus:
            probability_distribution[link] == base_probability
        return probability_distribution
    
    probability_distribution[page] = base_probability
    for link in links_on_page:
        add_probability = round(damping_factor / len(links_on_page), 9)
        total_probability = base_probability + add_probability
        probability_distribution[link] = total_probability
    
    
    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    samples = list()
    page_rank = dict()
    
    while len(samples) < n:
        i = random.randint(0, 1000000)
        if i < damping_factor*1000000 and len(samples) != 0:
            probability_distribution = transition_model(corpus, samples[-1], damping_factor)
            total = 0
            cumulative_probability = dict()
            for page in probability_distribution:
                probability = probability_distribution[page]
                cumulative_probability[page] = total + probability
                total += probability #create dictionary of cumulative probabilities
            
            values = list()
            keys = list()
            for p in cumulative_probability:
                keys.append(p)
                values.append(cumulative_probability[p])
            randomNum = random.randint(0, 1000000)
            for i in range(len(cumulative_probability)):
                if i == 0:
                    if 0 <= randomNum < values[i] * 1000000:
                        samples.append(keys[i])
                elif values[i-1] * 1000000 <= randomNum < values[i] * 1000000:
                    samples.append(keys[i])
                    
        else:
            random_index = random.randint(0, len(corpus) - 1)
            pages = list()
            for page in corpus:
                pages.append(page)
            samples.append(pages[random_index])
    
    for page in corpus:
        page_rank[page] = samples.count(page) / len(samples)

    return page_rank
            

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = dict()
    p_of_choosing_randomly = (1 - damping_factor) / len(corpus)
    
    num_iterations = 10000
    n = 0
    
    for page in corpus:
        page_rank[page] = 1 / len(corpus) #Sets all page rank values equal to each other in the beginning

    while n < num_iterations:
        for page in corpus:
            p_link = 0
            for page2 in corpus:
                if page in corpus[page2]:
                    p_link += page_rank[page2] / len(corpus[page2])
            
            page_rank[page] = p_of_choosing_randomly + damping_factor * p_link
        n += 1
    return page_rank


if __name__ == "__main__":
    main()
