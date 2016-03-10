class Node:
    def __init__(self, data=None, meaning=None):
        self.data = data
        self.right = None
        self.left = None
        self.eq = None
        self.meaning = meaning


class TST:
    def __init__(self):
        self.root = None
   
    def insert(self, node, word, meaning):
        if node is None:
            new_node = Node(word[0])
            if(len(word) == 1):
                new_node.meaning = meaning
            else:
                new_node.eq = self.insert(new_node.eq, word[1:], meaning)
            return new_node

        elif node.data == word[0]:
            node.eq = self.insert(node.eq, word[1:], meaning)
        elif word[0] < node.data:
            node.left = self.insert(node.left, word, meaning)
        else:
            node.right = self.insert(node.right, word, meaning)
        return node
    
    def suggested_words(self, node, string, word_list):
        if node is None:
            return []
        if node.meaning is not None:
            word_list.append(string + node.data)

        self.suggested_words(node.eq, string + node.data, word_list)
        self.suggested_words(node.left, string, word_list)
        self.suggested_words(node.right, string, word_list)

        return word_list

    def auto_suggestion(self, chars):
        node = self.root
        count = 0
        res = []
        while(count < len(chars)):
            if(node is None):
                return res
            else:
                if(node.data == chars[count]):
                    node = node.eq
                    count += 1
                elif (chars[count] < node.data):
                    node = node.left
                else:
                    node = node.right
            

        return self.suggested_words(node, chars, [])
    
    def search(self, chars):
        node = self.root
        count = 0

        while(count < len(chars)):
            if(node is None):
                return None # "Sorry, Word not present !"
            elif ((len(chars)-1 == count) and (chars[-1] == node.data)):
                meaning = node.meaning
                if(meaning is None):
                    return None # "Sorry, Word not present !"
                else:
                    return meaning
            else:
                if(node.data == chars[count]):
                    node = node.eq
                    count += 1
                elif (chars[count] < node.data):
                    node = node.left
                else:
                    node = node.right
            

        return None # "Sorry, Word not present !"
    
    def edits1(self, word):

        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes    = [a + b[1:] for a, b in splits if b]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
        replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
        inserts    = [a + c + b     for a, b in splits for c in alphabet]
       
        return set(deletes + transposes + replaces + inserts)
    
    
    def incorrect_input_meaning(self, incorrect_word):

        all_words = list(self.edits1(incorrect_word))

        meanings = []
        for each in all_words:
            mean = self.search(each)
            if mean is not None:
                meanings.append(mean)
            if(len(meanings) == 3):
                return meanings

        return meanings

    def get_meaning(self, word):
        res = tst.search(word)
        if(res is not None):
            return [res]
        else:
            return self.incorrect_input_meaning(word)


if __name__ == '__main__':
    
    tst = TST()
    fp = open("sample_parsed_data.txt", "rU")
    lines = fp.readlines()
    fp.close()

    for each in lines:
        word = each.split(',')[0]
        meaning = each.split(',')[1]
        tst.root = tst.insert(tst.root, word.strip(), meaning.strip())

    
    res = tst.auto_suggestion('ta') # Auto suggestion
    print (res)

    res = tst.get_meaning('tactics') # correct word input
    print (res)

    res = tst.get_meaning('tactucs') # incorrect word input
    print (res)
    