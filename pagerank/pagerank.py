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
    # Total number of pages, and the number of pages linked to in current page
    total_number, current_number = len(corpus), len(corpus[page])
    probability_distribution = dict()

    # If current page contains link to other pages
    if not current_number == 0:
        # Probability of randomly arriving at a page through damping factor
        for webpage in corpus:
            probability_distribution[webpage] = (1 - damping_factor) / total_number
        # Probability of arriving at page through links in current page
        for webpage in corpus[page]:
            probability_distribution[webpage] += (damping_factor / current_number)
    # If current page contains no link to other pages
    else:
        for webpage in corpus:
            probability_distribution[webpage] = 1 / total_number

    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Initialize pagerank dict with all the pages in corpus
    page_rank = dict()
    for page in corpus:
        page_rank[page] = 0

    # First randomly choose a page
    curr_page = random.choice(list(corpus.keys()))
    
    # Iterate n times
    for i in range(n):
        # Add to pagerank dict for given page
        page_rank[curr_page] += (1 / n)
        
        # Based on the transition model, "go" to next page
        distribution = transition_model(corpus, curr_page, damping_factor)
        curr_page = random.choices(list(distribution.keys()), distribution.values())[0]

    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Initialize pagerank dict with all pages with equal probability
    total_number, pagerank = len(corpus), dict()
    for page in corpus:
        pagerank[page] = 1 / total_number

    # Run iterative algorithm to determine pagerank
    change, random_surfer = True, (1 - damping_factor) / total_number
    while change:
        # Set change to false for each round
        change = False
        
        for page in corpus:
            link_surfer = 0

            # For all pages that contains link to page
            for page_linker in links_to_page(corpus, page):
                number_of_links = len(corpus[page_linker])
                
                # If the page has no link, interpret as having link to ALL pages
                if number_of_links == 0:
                    number_of_links = total_number
                link_surfer += (pagerank[page_linker] / number_of_links)
            
            # Calculate new rank
            new_rank = random_surfer + damping_factor * link_surfer

            # If new rank differs from current by more than 0.001, let loop run once more
            if abs(pagerank[page] - new_rank) > 0.001:
                change = True
            
            # Change pagerank
            pagerank[page] = new_rank

    return pagerank


def links_to_page(corpus, page):
    """
    Return list of pages in the corpus that contains links to given page
    """
    answer =  []
    for webpage in corpus:
        if page in corpus[webpage] or len(corpus[webpage]) == 0:
            answer.append(webpage)
    return answer


if __name__ == "__main__":
    main()
