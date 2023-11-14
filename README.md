# fsearch

My attempt at building my own search index for the web.

## method

1. get the top 1000 websites
2. for each website:
    1. get the sitemap
    2. for each page in the sitemap:
        1. get the page
        2. extract the text
        3. split the text into sentences
        4. for each sentence:
            1. calculate the sentence vector using [googles universal sentence encoder/4](https://tfhub.dev/google/universal-sentence-encoder/4)
        5. calculate the page vector by averaging the sentence vectors
            if the page vectors vary too much, calculate as many average vectors such that all the vectors are within a certain distance of any of the average vectors
        6. store the page vector(s) together with its url in a vector database

## search method
1. calculate the query vector
2. find the closest page vectors in the vector database
3. return the urls of the closest page vectors

