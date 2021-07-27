#simulated annealing (SA) approach to tag algorithm

import random as rand
from math import exp
import copy
import Utils
from itertools import chain
from functools import partial, reduce
from typing import Iterator
from os.path import commonprefix

def squeeze_names(sol):
    for i in range(len(sol)):
        sol[i][1] = list(map(lambda l: l[1], sol[i][1]))

    return sol

def ngram(seq: str, n: int) -> Iterator[str]:
    return (seq[i: i+n] for i in range(0, len(seq)-n+1))

def allngram(seq: str, minn=1, maxn=None) -> Iterator[str]:
    lengths = range(minn, maxn+1) if maxn else range(minn, len(seq))
    ngrams = map(partial(ngram, seq), lengths)
    return set(chain.from_iterable(ngrams))

def commonaffix(group):
    maxn = min(map(len, group))
    seqs_ngrams = map(partial(allngram, maxn=maxn), group)
    intersection = reduce(set.intersection, seqs_ngrams)
    try:
        check_presub = sorted(intersection, key=len, reverse=True)
        presuf = False
        ret = ""
        for sub in check_presub:
            count = 0
            for i in group:
                if i.startswith(sub) or i.endswith(sub):
                    count+=1
            if count==len(group):
                presuf=True
                ret = sub
                break
        if presuf:
            return True, ret

        # sub = max(intersection, key=len)
        # if len(sub)<=1:
        #     sub = ""
        return False, ""
    except:
        sub = ""

    return False, sub

class SimulatedAnnealing:
    def __init__(self, players, per_team, temp = 1.0, alpha = 0.9, iterations = 275):
        self.T = temp
        self.ALPHA = alpha
        self.ITERS = iterations

        self.num_per_team = per_team
        self.players = players

    
    def init_state(self):
        rand.shuffle(self.players)
        chunks = list(Utils.chunks(self.players, self.num_per_team))
        for i in range(len(chunks)):
            chunks[i] = ["" , chunks[i]]
        return chunks
    
    # TODO: finish the energy evaluation methods (most important)

    def findTag(self,group):
        #check prefix
        pre = commonprefix(group)
        
        #check suffix
        suf = commonprefix(list(map(lambda l: l[::-1], group)))
        
        #check mixed suffix
        mixed = ''
        is_pre_suf, to_det = commonaffix(group)
        if is_pre_suf:
            mixed = to_det
        
        # return [pre.strip()] + ([suf.strip(),sub.strip()] if pre.strip()=="" else [])
        return pre.strip(), suf.strip(), mixed.strip()

    def tags_eval(self, state):
        seen_tags = []
        energy = 0

        for group in state:
            possible = self.findTag(list(map(lambda l: l[0], group[1])))
            longest_tag = max(possible, key=len)
            group[0] = longest_tag
            if longest_tag =="":
                energy+=5000
            else:
                if longest_tag in seen_tags:
                    energy+=500  
                seen_tags.append(longest_tag) 

                energy+=self.affix_score(possible, longest_tag)

            for player in group[1]:
                if not player[0].startswith(longest_tag):
                    energy+=50

        return energy


    def affix_score(self, possible, longest_tag):
        energy = 0
        if possible.index(longest_tag)!=0:
            if possible.index(longest_tag) == 1:
                energy+=250   
            elif possible.index(longest_tag) == 2:
                energy += 175

        return energy
    
    def E(self, state):
        '''
        return energy (cost) of solution
        '''
        energy = self.tags_eval(state)

        return energy

    def P(self, old_E, new_E):
        '''
        return acceptance probability
        '''
        if new_E < old_E:
            return 1.0

        return exp(-(new_E - old_E) / self.T)

    def n_swap(self, state):
        '''
        randomly swap two strings' groupings
        '''
        neighbor_state = copy.deepcopy(state)
        swap_from = rand.randint(0, len(neighbor_state)-1)
        swap_to = rand.randint(0, len(neighbor_state)-1)
        ch1 = rand.choice(neighbor_state[swap_from][1])
        ch2 = rand.choice(neighbor_state[swap_to][1])
        
        neighbor_state[swap_from][1].remove(ch1)
        neighbor_state[swap_from][1].append(ch2)
        neighbor_state[swap_to][1].remove(ch2)
        neighbor_state[swap_to][1].append(ch1)

        return neighbor_state

    def anneal(self):
        '''
        return a solution
        '''
        curr_solution = self.init_state()
        curr_energy = self.E(curr_solution)

        for _n in range(self.ITERS):
            new_solution = self.n_swap(curr_solution)
            new_energy = self.E(new_solution)
            
            acceptance_prob = self.P(curr_energy, new_energy)
            if acceptance_prob > rand.random():
                curr_solution, curr_energy = new_solution, new_energy
            
            self.T*=self.ALPHA
            print(f"ITERATION {_n+1}-> Energy: {curr_energy}")
        
        return squeeze_names(curr_solution), curr_energy

if __name__ == "__main__":
    
    players = ['AYA hello', '!!m&m?!', 'mong', 'MV math', 'pringle@MV', '@*', 'AYAYA', 'i need ZZZ', 'Z - stop', 'USA h', 'USA K', 'ABBA']

    players = list(map(lambda l: (Utils.sanitize_uni(l.strip()).lower(), l), players))
    tag_algo = SimulatedAnnealing(players, per_team = 2)
    sol, energy = tag_algo.anneal()
    print(sol)
    print(energy)
