#!/usr/bin/env python

import random

from gsp import GSP
from krankilehelper import pos_effect


class VCG:
    """
    Implements the Vickrey-Clarke-Groves mechanism for ad auctions.
    """
    @staticmethod
    def compute(slot_clicks, reserve, bids):
        """
        Given info about the setting (clicks for each slot, and reserve price),
        and bids (list of (id, bid) tuples), compute the following:
          allocation:  list of the occupant in each slot
              len(allocation) = min(len(bids), len(slot_clicks))
          per_click_payments: list of payments for each slot
              len(per_click_payments) = len(allocation)

        If any bids are below the reserve price, they are ignored.

        Returns a pair of lists (allocation, per_click_payments):
         - allocation is a list of the ids of the bidders in each slot
            (in order)
         - per_click_payments is the corresponding payments.
        """

        # The allocation is the same as GSP, so we filled that in for you...

        def valid((a, bid)): return bid >= reserve
        valid_bids = filter(valid, bids)

        def rev_cmp_bids((a1, b1), (a2, b2)): return cmp(b2, b1)
        # shuffle first to make sure we don't have any bias for lower or
        # higher ids
        random.shuffle(valid_bids)
        valid_bids.sort(rev_cmp_bids)

        num_slots = len(slot_clicks)
        allocated_bids = valid_bids[:num_slots]
        if len(allocated_bids) == 0:
            return ([], [])

        (allocation, just_bids) = zip(*allocated_bids)

        def total_payment(k):
            """
            Total payment for a bidder in slot k.
            """
            c = slot_clicks
            n = len(allocation)

            # Using the recursive form of VCG payment rule
            # If the bid is the lowest bid, compute payment as the max of the
            # reserve and the highest non-valid bid, multiplied by the
            # position effect i.e. slot_clicks
            if k == n - 1:
                highest_invalid = sorted(bids, rev_cmp_bids)[n][0]
                return slot_clicks[k] * max(reserve, highest_invalid)

            # If the bid is not the lowest, compute payment according to eq. 10.21
            return (slot_clicks[k]-slot_clicks[k+1]) * just_bids[k+1] + total_payment(k+1)

        def norm(totals):
            """Normalize total payments by the clicks in each slot"""
            return map(lambda (x, y): x/y, zip(totals, slot_clicks))

        per_click_payments = norm(
            [total_payment(k) for k in range(len(allocation))])

        return (list(allocation), per_click_payments)

    @staticmethod
    def bid_range_for_slot(slot, slot_clicks, reserve, bids):
        """
        Compute the range of bids that would result in the bidder ending up
        in slot, given that the other bidders submit bidders.
        Returns a tuple (min_bid, max_bid).
        If slot == 0, returns None for max_bid, since it's not well defined.
        """
        # Conveniently enough, bid ranges are the same for GSP and VCG:
        return GSP.bid_range_for_slot(slot, slot_clicks, reserve, bids)
