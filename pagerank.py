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

    if len(corpus[page]) == 0:
        # No outgoing links → uniform distribution over all pages
        return dict.fromkeys(corpus.keys(), 1 / len(corpus))

    # Base probability for every page (teleport term)
    prob = dict.fromkeys(corpus.keys(), (1 - damping_factor) / len(corpus))

    # Add the "follow a link" probability to each linked page
    for p in corpus[page]:
        prob[p] += damping_factor / len(corpus[page])

    return prob
    
    #raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
 
    
          """
    pages = list(corpus.keys())
    pagerank = {page: 0 for page in pages}

    page = random.choice(pages)
    pagerank[page] += 1


    for _ in range(n - 1):
        probs = transition_model(corpus, page, damping_factor)
        page = random.choices(pages, weights=probs.values(), k=1)[0]
        pagerank[page] += 1


    return {page: pagerank[page] / n for page in pagerank}
    
    #raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """


    N = len(corpus)
    pagerank = {page: 1 / N for page in corpus}

    
    for page in corpus:
        if len(corpus[page]) == 0:
            corpus[page] = set(corpus.keys())

    while True:
        new_pagerank = {}
        max_diff = 0

        for page in corpus:
            # Teleport term
            new_pagerank[page] = (1 - damping_factor) / N

            # Link contribution: sum over all pages that link TO this page
            for other in corpus:
                if page in corpus[other]:
                    new_pagerank[page] += (
                        damping_factor * pagerank[other] / len(corpus[other])
                    )

            max_diff = max(max_diff, abs(new_pagerank[page] - pagerank[page]))

        pagerank = new_pagerank

        if max_diff < 0.001:
            break

    return pagerank    
    #raise NotImplementedError


if __name__ == "__main__":
    main()
