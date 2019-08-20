# Sentence-Differences

Given a list of possible "correct" answer strings and a user response string, find which answer the response is most similar to

Motivation: Exercises on the language learning app Duolingo often have multiple possible correct responses.  If you type a wrong answer, it shows you a correct answer, which should ideally be the correct answer most similar to the wrong answer you typed, thus giving you the most intuitive corrections.  However, it fails horribly at this; instead, it often picks a random correct sentence, leading you to believe your answer was entirely wrong when perhaps you just misspelled a word or conjugated something wrong.  My program, given a list of "correct" answers and a response supposedly submitted by the user, aims to find the correct answer most similar to the user response.
