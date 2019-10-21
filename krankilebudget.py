#!/usr/bin/env python

import sys

from gsp import GSP
from util import argmax_index


class Krankilebudget:
    """Balanced bidding agent"""

    def __init__(self, id, value, budget):
        self.id = id
        self.value = value
        self.budget = budget

    def initial_bid(self, reserve):
        return self.value / 2

    def slot_info(self, t, history, reserve):
        """Compute the following for each slot, assuming that everyone else
        keeps their bids constant from the previous rounds.

        Returns list of tuples [(slot_id, min_bid, max_bid)], where
        min_bid is the bid needed to tie the other-agent bid for that slot
        in the last round.  If slot_id = 0, max_bid is 2* min_bid.
        Otherwise, it's the next highest min_bid (so bidding between min_bid
        and max_bid would result in ending up in that slot)
        """
        prev_round = history.round(t-1)
        other_bids = filter(lambda (a_id, b): a_id != self.id, prev_round.bids)

        clicks = prev_round.clicks

        def compute(s):
            (min, max) = GSP.bid_range_for_slot(s, clicks, reserve, other_bids)
            if max == None:
                max = 2 * min
            return (s, min, max)

        info = map(compute, range(len(clicks)))
#        sys.stdout.write("slot info: %s\n" % info)
        return info


def expected_utils(self, t, history, reserve):
        """
        Figure out the expected utility of bidding such that we win each
        slot, assuming that everyone else keeps their bids constant from
        the previous round.

        returns a list of utilities per slot.
        """
        utilities = []
        # To increase readability
        slotsinfo = self.slot_info(t, history, reserve)
        # pos_effect as presented in krankilehelper.py
        pos = pos_effect((history.round(history.last_round())).clicks)
        for i in range(len(slotsinfo)):
            # u_i based on the PSET definiton (The expression inside argmax).
            #  This is NOT the first utility definiton presented.
            u_i = pos[i]*(self.value-((slotsinfo[i][1] + slotsinfo[i][2]) / 2) /
                          ((slotsinfo[i][1] + slotsinfo[i][2]) / 2)
            utilities.append(u_i)

        return utilities

    def target_slot(self, t, history, reserve):
        """Figure out the best slot to target, assuming that everyone else
        keeps their bids constant from the previous rounds.

        Returns (slot_id, min_bid, max_bid), where min_bid is the bid needed to tie
        the other-agent bid for that slot in the last round.  If slot_id = 0,
        max_bid is min_bid * 2
        """
        i=argmax_index(self.expected_utils(t, history, reserve))
        info=self.slot_info(t, history, reserve)
        return info[i]

    def bid(self, t, history, reserve):
            prev_round=history.round(t-1)
            (slot, min_bid, max_bid)=self.target_slot(t, history, reserve)
            if min_bid > self.value:
                # When price is too high
                bid=self.value
            else:
                if slot > 0:
                    pos=pos_effect(
                        (history.round(history.last_round())).clicks)
                    # Place bid as described in PSET
                    bid=self.value - (pos[slot]/pos[slot-1]
                                      )*(self.value-min_bid)
                else:
                    # When slot is first slot
                    bid=self.value
            return bid

    def __repr__(self):
        return "%s(id=%d, value=%d)" % (
            self.__class__.__name__, self.id, self.value)
