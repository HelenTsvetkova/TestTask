class SimilarityAnalyzer:
    '''
    A class used to calculate similarity between pre-known corpus of texts and input string.

    Methods
    -------
    generate_bow(self, text: str, source: str, vocab_size: int = 10, word_size: int = 4, skip_spaces: bool = True, non_unique_words: bool = True) -> dict
        Generate bag of words (bow) for given text. 
    
    generate_bow_ngram(self, text: str, source: str, vocab_size: int = 10, ngram_range: tuple = (1,1), non_unique_words: bool = True) -> dict
        Generate bag of words for given text using n-gram model. 
    
    get_similarity(self, base_bows: list, input_bow: dict, case_sensitive: bool = False) -> dict
        Calculate similarity between bag of words for input string and each of bow from base of pre-known bows.

    __read_text_file(self, file_name: str) -> str
        Read text from .txt file and return it.

    '''

    def generate_bow(self, text: str, source: str, bow_size: int = 10, word_size: int = 4, skip_spaces: bool = True, non_unique_words: bool = True) -> dict:
        '''Generate bag of words (bow) for given text.

        Parameters
        ----------
        text : str
            Input text to generate bow OR input text file name to read text and generate bow.
        source : str
            Argument has only two options: 'file' and 'string'.
        bow_size : int, optional
            Maximum size of bag of words.
        word_size : int, optional
            Size of one word in bow.
        skip_spaces : bool, optional
            Generate bow by skipping whitespace characters (spaces) or not.
        non_unique_words : bool, optional
            Generate bow only from non-unidue words or not.

        Returns
        -------
        dict
            A dictionary where each key corresponds to a word, and the value corresponds to the number of occurrences of that word in the text.
        
        '''

        bow = {}

        if source == 'file':
            text = self.__read_text_file(file_name=text)
        elif source != 'string':
            print('Wrong \'source\' value: ', source, '. Available choises: \'string\', \'file\'')
            return bow

        if len(text) == 0:
            print('Warning! Text is empty.')
            return bow

        if bow_size <= 0:
            print('Wrong vocab_size: ', bow_size)
            return bow
        
        if word_size <= 0:
            print('Wrong word_size: ', word_size)
            return bow

        for i in range(len(text) - word_size + 1):
            new_word = text[i:i+word_size]
            if skip_spaces:
                if new_word.find(' ') != -1:
                    continue

            word_occurence_num = text.count(new_word)
            if non_unique_words:
                if word_occurence_num < 2:
                    continue
            bow.setdefault(new_word, word_occurence_num)

        
        bow = {k: v for k, v in sorted(bow.items(), key=lambda word: word[1], reverse=True)}
        
        if(len(bow) > bow_size):
            keys_to_del = list(bow.keys())[10:]
            for key in keys_to_del:
                bow.pop(key)

        return bow

    def generate_bow_ngram(self, text: str, source: str, bow_size: int = 10, ngram_range: tuple = (1,1), non_unique_words: bool = True) -> dict:
        '''Generate bag of words (bow) for given text using n-gram model.

        Parameters
        ----------
        text : str
            Input text to generate bow OR input text file name to read text and generate bow.
        source : str
            Argument has only two options: 'file' and 'string'.
        bow_size : int, optional
            Maximum size of bag of words.
        ngram_range: tuple, optional
            The lower and upper boundary of the range of n-values for different word n-grams to be extracted from text. Minimum lower boundary is 1.
        non_unique_words : bool, optional
            Generate bow only from non-unidue words or not.

        Returns
        -------
        dict
            A dictionary where each key corresponds to a word, and the value corresponds to the number of occurrences of that word in the text.
        
        '''

        bow = {}

        if source == 'file':
            text = self.__read_text_file(file_name=text)
        elif source != 'string':
            print('Wrong \'source\' value: ', source, '. Available choises: \'string\', \'file\'')
            return bow

        if len(text) == 0:
            print('Warning! Text is empty.')
            return bow

        if bow_size <= 0:
            print('Wrong vocab_size: ', bow_size)
            return bow

        if ngram_range[0] == 0:
            print('Wrong ngram_range: ', ngram_range)
            return bow

        if ngram_range[1] < ngram_range[0]:
            print('Wrong ngram_range: ', ngram_range)
            return bow

        new_words = text.split(' ')
        for n_gram in range(ngram_range[0], ngram_range[1] + 1):  
            for i in range(len(new_words) - n_gram + 1):
                new_word = ' '.join([new_words[i + n] for n in range(0, n_gram)])
                if new_word == '':
                    continue
                word_occurence_num = text.count(new_word)
                if non_unique_words:
                    if word_occurence_num < 2:
                        continue
                bow.setdefault(new_word, word_occurence_num)
        
        bow = {k: v for k, v in sorted(bow.items(), key=lambda word: word[1], reverse=True)}
        
        if(len(bow) > bow_size):
            keys_to_del = list(bow.keys())[bow_size:]
            for key in keys_to_del:
                bow.pop(key)
        
        return bow

    def get_similarity(self, base_bows: list, input_bow: dict, case_sensitive: bool = True) -> dict:
        '''Calculate similarity between bag of words for input string and each of bow from base of pre-known bows.

        Parameters
        ----------
        base_bows : list
            Base of pre-known bag of words.                        
        input_bow : dict
            Bag of words of input string.
        case_sensitive : bool, optional
            Determine the degree of similarity taking into account the case of characters or not.
            
        Returns
        -------
        dict
            A dictionary where each key corresponds to index of bow from base, and the value corresponds to the degree of similarity with the input bow.
        
        '''

        similarity = {}
        
        if len(input_bow) == 0:
            print('Warning! Input text is empty.')
            return similarity

        input_set = set(list(input_bow.keys()))
        if case_sensitive == False:
            input_set = set(word.casefold() for word in input_set)

        base_sets = [set(list(bow.keys())) for bow in base_bows]
        for i, base_set in enumerate(base_sets):
            if case_sensitive == False:
                base_set = set([word.casefold() for word in base_set])

            similarity_degree = len(base_set.intersection(input_set))
            if similarity_degree:
                similarity[i] = similarity_degree
        
        similarity = {k: v for k, v in sorted(similarity.items(), key=lambda similarity_degree: similarity_degree[1], reverse=True)}
        
        return similarity

    def __read_text_file(self, file_name: str) -> str:
        '''Read text from .txt file and return it.

        Parameters
        ----------
        file_name : str
            Name of the input file.                        
            
        Returns
        -------
        str
            Text from text file.
        
        '''    
        text = ''
        try:
            file_name = open(file_name, "r")
            text = file_name.read()
            text = text.replace("\n", " ")
            file_name.close()
        except IOError:
            print("Could not read file:", file_name)
        
        return text
    
