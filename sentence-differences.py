'''
Given a list of possible "correct" answer strings and a user response string, find which answer the response is most similar to

Motivation: Exercises on the language learning app Duolingo often have multiple possible correct responses.  If you type a wrong answer, it shows you a correct answer, which should ideally be the correct answer most similar to the wrong answer you typed, thus giving you the most intuitive corrections.  However, it fails horribly at this; instead, it often picks a random correct sentence, leading you to believe your answer was entirely wrong when perhaps you just misspelled a word or conjugated something wrong.  My program, given a list of "correct" answers and a response supposedly submitted by the user, aims to find the correct answer most similar to the user response.

Currently assumes letters are the only meaningful characters in sentence (anything else is removed before processing, so numbers, for instance, are ignored)
'''

'''
Currently should behave well if:
    words are typed in the correct order, with some misspelled ("sie habt meinen hand halten")
    extra words appear in response ("sie haben meine hand qq gehalten")
    words are omitted in response ("sie haben hand gehalten")
    spaces are omitted, so that two or more words may be combined into one ("sie haben meinehand gehalten")
Sometimes behaves well if:
    words are typed in a wrong order, but all are spelled exactly right ("haben sie meine hand gehalten")
    words are typed in a wrong order, with some misspelled ("habt sie meine hand gehalten")
Doesn't behave well if:
    there are multiple ways to fix the sentence, and the more intuitive fix is farther from response than a different one
        e.g., "Du trinkst, weil du hast Durst" will change to "denn" instead of fixing word order, which is probably bad fix (yields confusion of "why can't i use 'weil'?")
'''


'''
IDEA: do damerau-levenshtein, but also allow removing/transposing entire words (but not inserting or replacing words)
        actually, this might be impractical to implement; and also, it will only handle word order problems if two adjacent words are transposed
'''

import numpy
import itertools

def DLDist(response,correct,rLen,cLen,table):
    '''
    find the Damerau-Levenshtein distance between the two strings
    alternatively, find similar distance between two lists (based on how their elements match)
    input: two strings, their lengths, and a None-filled (len1+1)x(len2+1) table
    (based on Wikipedia's description of the algorithm at https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance#Definition, modified to include tabulation for speed purposes)
    '''
    compare = []
    if not rLen and not cLen:
        compare.append(0)
    if rLen>0:
        # corresponds to deletions
        if table[rLen-1][cLen] != None:
            compare.append(table[rLen-1][cLen]+1)
        else:
            table[rLen-1][cLen] = DLDist(response,correct,rLen-1,cLen,table)
            compare.append(table[rLen-1][cLen]+1)
    if cLen>0:
        # corresponds to insertions
        if table[rLen][cLen-1] != None:
            compare.append(table[rLen][cLen-1]+1)
        else:
            table[rLen][cLen-1] = DLDist(response,correct,rLen,cLen-1,table)
            compare.append(table[rLen][cLen-1]+1)
    if rLen>0 and cLen>0:
        # corresponds to substitutions
        if table[rLen-1][cLen-1] != None:
            compare.append(table[rLen-1][cLen-1]+(0 if response[rLen-1]==correct[cLen-1] else 1))
        else:
            table[rLen-1][cLen-1] = DLDist(response,correct,rLen-1,cLen-1,table)
            compare.append(table[rLen-1][cLen-1]+(0 if response[rLen-1]==correct[cLen-1] else 1))
    if rLen>1 and cLen>1 and response[rLen-1]==correct[cLen-2] and response[rLen-2]==correct[cLen-1]:
        # corresponds to transpositions
        if table[rLen-2][cLen-2] != None:
            compare.append(table[rLen-2][cLen-2]+1)
        else:
            table[rLen-2][cLen-2] = DLDist(response,correct,rLen-2,cLen-2,table)
            compare.append(table[rLen-2][cLen-2]+1)
    return min(compare)

def wordDiff(response,correct):
    '''return the difference between two words (currently equals Damerau-Levenshtein distance)'''
    return DLDist(response,correct,len(response),len(correct),[[None for _ in range(len(correct)+1)] for _ in range(len(response)+1)])

def strDiff(response,correct):
    '''find distance between two strings (currently is D-L difference between strings)'''
    # remove anything that isn't letter or space
    response = ''.join([c if c.isalpha() or c==' ' else '' for c in response]).lower()
    correct = ''.join([c if c.isalpha() or c==' ' else '' for c in correct]).lower()
    
    '''
    this code was originally intended to do D-L algorithm on all permutations of the words in the user response; however, this runs much too slow
    
    instead of generating all permutations, could allow D-L algorithm to swap and remove entire words
    doing algorithm for all possible permutations is way too slow
    
    # rPerms = [list(l) for l in list(itertools.permutations(response.split()))]
    # strDiff = min([wordDiff(' '.join(rPerm),correct) for rPerm in rPerms])
    '''
    
    strDiff = wordDiff(response,correct)

    return strDiff

if __name__ == '__main__':
    # correctAnswers = [
        # 'Du hast meine Hand gehalten.',
        # 'Ihr habt meine Hand gehalten.',
        # 'Sie haben meine Hand gehalten.',
        # 'Meine Hand hast du gehalten.',
        # 'Meine Hand habt ihr gehalten.',
        # 'Meine Hand haben Sie gehalten.',
        # 'Du hieltst meine Hand.',
        # 'Ihr hieltet meine Hand.',
        # 'Sie hielten meine Hand.',
        # 'Du hieltest meine Hand.',
        # 'Meine Hand hieltst du.',
        # 'Meine Hand hieltet ihr.',
        # 'Meine Hand hielten Sie.',
        # 'Meine Hand hieltest du.'
    # ]
    correctAnswers = [
        'Du trinkst, weil du Durst hast.',
        'Ihr trinkt, weil ihr Durst habt.',
        'Sie trinken, weil Sie Durst haben.',
        'Du trinkst, denn du hast Durst.',
        'Ihr trinkt, denn ihr habt Durst.',
        'Sie trinken, denn Sie haben Durst.',
        'Weil du Durst hast, trinkst du.',
        'Weil ihr Durst habt, trinkt ihr.',
        'Weil Sie Durst haben, trinken Sie.'
    ]
    response = input('Your response: ')
    diffs = [strDiff(response,corr) for corr in correctAnswers]
    print('      Correct:',correctAnswers[numpy.argmin(diffs)],'/ diff='+str(min(diffs)),'/',('ACCEPT' if min(diffs) <= 2 else 'REJECT'))