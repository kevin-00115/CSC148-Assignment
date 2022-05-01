"""Assignment 2: Society Hierarchy (all tasks)

CSC148, Winter 2022

This code is provided solely for the personal and private use of students
taking the CSC148 course at the University of Toronto. Copying for purposes
other than this use is expressly prohibited. All forms of distribution of this
code, whether as given or with any changes, are expressly prohibited.

Authors: Sadia Sharmin, Diane Horton, Dina Sabie, Sophia Huynh, and
         Jonathan Calver.

All of the files in this directory and all subdirectories are:
Copyright (c) 2022 Sadia Sharmin, Diane Horton, Dina Sabie, Sophia Huynh, and
                   Jonathan Calver

=== Module description ===
This module contains all of the classes necessary to model the entities in a
society's hierarchy.

REMINDER: You must NOT use list.sort() or sorted() in your code. Instead, use
the merge() function we provide for you below.
"""
from __future__ import annotations
from typing import List, Optional, TextIO, Any


def merge(lst1: list, lst2: list) -> list:
    """Return a sorted list with the elements in <lst1> and <lst2>.

    Preconditions:
    - <lst1>> is sorted and <lst2> is sorted.
    - All of the elements of <lst1> and <lst2> are of the same type, and they
      are comparable (i.e. their type implements __lt__).

    >>> merge([1, 2, 5], [3, 4, 6])
    [1, 2, 3, 4, 5, 6]
    >>> merge([4], [1, 3])
    [1, 3, 4]
    """

    i1 = 0
    i2 = 0
    new_list = []

    while i1 < len(lst1) and i2 < len(lst2):
        if lst1[i1] < lst2[i2]:
            new_list.append(lst1[i1])
            i1 += 1
        else:
            new_list.append(lst2[i2])
            i2 += 1

    new_list.extend(lst1[i1:])
    new_list.extend(lst2[i2:])

    return new_list


###########################################################################

###########################################################################
class Citizen:
    """A Citizen: a citizen in a Society.

    === Public Attributes ===
    cid:
        The ID number of this citizen.
    manufacturer:
        The manufacturer of this Citizen.
    model_year:
        The model year of this Citizen.
    job:
        The name of this Citizen's job within the Society.
    rating:
        The rating of this Citizen.

    === Private Attributes ===
    _superior:
        The superior of this Citizen in the society, or None if this Citizen
        does not have a superior.
    _subordinates:
        A list of this Citizen's direct subordinates (that is, Citizens that
        work directly under this Citizen).

    === Representation Invariants ===
    - cid > 0
    - 0 <= rating <= 100
    - self._subordinates is in ascending order by the subordinates' IDs
    - If _superior is a Citizen, this Citizen is part of its _subordinates list
    - Each Citizen in _subordinates has this Citizen as its _superior
    """
    cid: int
    manufacturer: str
    model_year: int
    job: str
    rating: int
    _superior: Optional[Citizen]
    _subordinates: List[Citizen]

    def __init__(self, cid: int, name: str, model_year: int,
                 job: str, rating: int) -> None:
        """Initialize this Citizen with the ID <cid>, manufacturer
        <manufacturer>, model year <model_year>, job <job>, and rating <rating>.

        A Citizen initially has no superior and no subordinates.

        >>> c1 = Citizen(1, "Starky Industries", 3042, "Labourer", 50)
        >>> c1.cid
        1
        >>> c1.rating
        50
        """
        self.cid = cid
        self.manufacturer = name
        self.model_year = model_year
        self.job = job
        self.rating = rating
        self._superior = None
        self._subordinates = []

    def __lt__(self, other: Any) -> bool:
        """Return True if <other> is a Citizen and this Citizen's cid is less
        than <other>'s cid.

        If other is not a Citizen, raise a TypeError.

        >>> c1 = Citizen(1, "Starky Industries", 3042, "Labourer", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3042, "Manager", 30)
        >>> c1 < c2
        True
        """
        if not isinstance(other, Citizen):
            raise TypeError

        return self.cid < other.cid

    def __str__(self) -> str:
        """Return a string representation of the tree rooted at this Citizen.
        """
        return self._str_indented().strip()

    def _str_indented(self, depth: int = 0) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        me = f'{str(self.cid)} (rating = {self.rating})'
        if isinstance(self, DistrictLeader):
            me += f' --> District Leader for {self._district_name}'
        s = '  ' * depth + me + '\n'
        for subordinate in self.get_direct_subordinates():
            # Note that the ‘depth’ argument to the recursive call is
            # modified.
            s += subordinate._str_indented(depth + 1)
        return s

    def get_superior(self) -> Optional[Citizen]:
        """Return the superior of this Citizen or None if no superior exists.

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c1.get_superior() is None
        True
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        >>> c1.become_subordinate_to(c2)
        >>> c1.get_superior().cid
        2
        """

        return self._superior

    def set_superior(self, new_superior: Optional[Citizen]) -> None:
        """Update the superior of this Citizen to <new_superior>

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        >>> c1.set_superior(c2)
        >>> c1.get_superior().cid
        2
        """
        self._superior = new_superior

    def get_direct_subordinates(self) -> List[Citizen]:
        """Return a new list containing the direct subordinates of this Citizen.

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        >>> c3 = Citizen(3, "S.T.A.R.R.Y Lab", 3010, "Commander", 60)
        >>> c1.become_subordinate_to(c2)
        >>> c2.become_subordinate_to(c3)
        >>> c3.get_direct_subordinates()[0].cid
        2
        """
        # print(self._subordinates)
        return self._subordinates[:]

    ###########################################################################
    ###########################################################################

    def add_subordinate(self, subordinate: Citizen) -> None:
        """Add <subordinate> to this Citizen's list of direct subordinates,
        keeping the list of subordinates in ascending order by their ID.

        Update the new subordinate's superior to be this Citizen.

        # >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        # >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        # >>> c3 = Citizen(3, "S.T.A.R.R.Y Lab", 3010, "Commander", 60)
        # >>> c2.add_subordinate(c3)
        # >>> c2.add_subordinate(c1)
        # >>> c2.get_direct_subordinates()[0].cid
        # 1
        # >>> c1.get_superior() is c2
        # True
        #
        # >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        # >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        # >>> c3 = Citizen(3, "S.T.A.R.R.Y Lab", 3010, "Commander", 60)
        # >>> c4 = Citizen(4, "S.T.A.R.R.Y Lab", 3010, "Commander", 60)
        # >>> c2.add_subordinate(c4)
        # >>> c2.add_subordinate(c3)
        # >>> c2.add_subordinate(c1)
        # >>> c2.get_direct_subordinates()[0].cid
        # 1
        # >>> c2.get_direct_subordinates()[1].cid
        # 3
        # >>> c2.get_direct_subordinates()[2].cid
        # 4
        # >>> c1.get_superior() is c2
        # True

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        >>> c3 = Citizen(3, "S.T.A.R.R.Y Lab", 3010, "Commander", 60)
        >>> c4 = Citizen(4, "S.T.A.R.R.Y Lab", 3010, "Commander", 60)
        >>> c4.add_subordinate(c1)
        >>> c4.add_subordinate(c3)
        >>> c4.add_subordinate(c2)
        >>> c4.get_direct_subordinates()[0].cid
        1
        >>> c4.get_direct_subordinates()[1].cid
        2
        >>> c4.get_direct_subordinates()[2].cid
        3

        """
        # if not self._subordinates:
        #     self._subordinates.append(subordinate)
        # else:
        #     lst1 = []
        #     lst2 = []
        #     for c in self._subordinates:
        #         if c.cid < subordinate.cid:
        #             lst1.append(c)
        #         elif c.cid > subordinate.cid:
        #             lst2.append(c)
        #
        #         if lst1 != []:
        #             lst1.append(subordinate)
        #             if lst2 != []:
        #                 for c in lst2:
        #                     lst1.append(c)
        #         else:
        #             self._subordinates.insert(0, subordinate)
        #     for c in lst1:
        #         if c not in self._subordinates:
        #             self._subordinates.append(c)
        # for c in self._subordinates:
        #     c._superior = self
        if subordinate not in self._subordinates:
            self._subordinates.append(subordinate)
            subordinate._superior = self
        self._sort_subordinate()

    def _sort_subordinate(self) -> None:
        """ sort the lst of suboridinate in an ascending order by their cid
        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        >>> c3 = Citizen(3, "S.T.A.R.R.Y Lab", 3010, "Commander", 60)
        >>> c4 = Citizen(4, "S.T.A.R.R.Y Lab", 3010, "Commander", 60)
        >>> c2.add_subordinate(c4)
        >>> c2.add_subordinate(c3)
        >>> c2.add_subordinate(c1)
        >>> c2._sort_subordinate()
        >>> c2.get_direct_subordinates()[0].cid
        1
        >>> c1.get_superior() is c2
        True
        """
        for i in range(0, len(self._subordinates)):
            for j in range(i + 1, len(self._subordinates)):
                if self._subordinates[i].cid > self._subordinates[j].cid:
                    temp = self._subordinates[i]
                    self._subordinates[i] = self._subordinates[j]
                    self._subordinates[j] = temp

    def remove_subordinate(self, cid: int) -> None:
        """Remove the subordinate with the ID <cid> from this Citizen's list
        of subordinates.

        Furthermore, remove that (former) subordinate from the hierarchy by
        setting its superior to None.

        Precondition: This Citizen has a subordinate with ID <cid>.

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        >>> c1.become_subordinate_to(c2)
        >>> c2.get_direct_subordinates()[0].cid
        1
        >>> c2.remove_subordinate(1)
        >>> c2.get_direct_subordinates()
        []
        >>> c1.get_superior() is None
        True
        """
        for sub in self._subordinates:
            if sub.cid == cid:
                self._subordinates.remove(sub)
                sub._superior = None

    def become_subordinate_to(self, superior: Optional[Citizen]) -> None:
        """Make this Citizen a direct subordinate of <superior>.

        If this Citizen already had a superior, remove this Citizen from the
        old superior's list of subordinates.

        If <superior> is None, just set this Citizen's superior to None.

        # >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        # >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        # >>> c1.become_subordinate_to(c2)
        # >>> c1.get_superior().cid
        # 2
        # >>> c2.get_direct_subordinates()[0].cid
        # 1
        # >>> c1.become_subordinate_to(None)
        # >>> c1.get_superior() is None
        # True
        # >>> c2.get_direct_subordinates()
        # []
        # >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        # >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        # >>> c3 = Citizen(3, "S.T.A.R.R.Y Lab", 3010, "Commander", 60)
        # >>> c4 = Citizen(4, "S.T.A.R.R.Y Lab", 3010, "Commander", 60)
        # >>> c5 = Citizen(5, "S.T.A.R.R.Y Lab", 3010, "Commander", 60)
        # >>> c6 = Citizen(6, "S.T.A.R.R.Y Lab", 3010, "Commander", 60)
        # >>> c5.become_subordinate_to(c1)
        # >>> c1.become_subordinate_to(c4)
        # >>> c2.become_subordinate_to(c4)
        # >>> c3.become_subordinate_to(c1)
        # >>> c6.become_subordinate_to(c2)
        # >>> c4.get_direct_subordinates()[0].cid
        # 1
        # >>> c4.get_direct_subordinates()[1].cid
        # 2
        # >>> c2.get_direct_subordinates()[0].cid
        # 6
        # >>> c1.get_direct_subordinates()[0].cid
        # 3
        # >>> c1.get_direct_subordinates()[1].cid
        # 5
        #
        # >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        # >>> c = None
        # >>> c1.become_subordinate_to(c)
        >>> c1 = Citizen(11, 'Citizen 11', 3011, 'Watcher', 25)
        >>> c2 = Citizen(2, 'Citizen 11', 3011, 'Watcher', 25)
        >>> c1.add_subordinate(c2)
        >>> c1.become_subordinate_to(c2)
        """
        if superior is None and self._superior is not None:
            self._superior._subordinates.remove(self)
            self._superior = None
        elif superior is None and self._superior is None:
            self._superior = None
        elif self._superior is None:
            self._superior = superior
            superior.add_subordinate(self)
        else:
            self._superior.remove_subordinate(self.cid)
            self._superior = superior
            superior.add_subordinate(self)

    def get_citizen(self, cid: int) -> Optional[Citizen]:
        """Check this Citizen and its subordinates to find and return the
        Citizen that has the ID <cid>.

        If neither this Citizen nor any of its subordinates (both direct and
        indirect) have the ID <cid>, return None.

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        >>> c3 = Citizen(3, "S.T.A.R.R.Y Lab", 3010, "Commander", 60)
        >>> c1.become_subordinate_to(c2)
        >>> c2.become_subordinate_to(c3)
        >>> c3.get_citizen(1) is c1
        True
        >>> c2.get_citizen(3) is None
        True
        """
        if self.cid == cid:
            return self
        elif self.cid != cid and self._subordinates == []:
            return None
        elif self._subordinates[0].cid == cid:
            return self._subordinates[0]
        else:
            for sub in self._subordinates:
                if sub._is_subordinate(cid):
                    return sub.get_citizen(cid)
            return None

    # helper function

    def _is_subordinate(self, cid: int) -> bool:
        """ return True iff cid is one of its subordinate
        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        >>> c3 = Citizen(3, "S.T.A.R.R.Y Lab", 3010, "Commander", 60)
        >>> c1.become_subordinate_to(c2)
        >>> c2.become_subordinate_to(c3)
        >>> c3._is_subordinate(1)
        True
        >>> c1._is_subordinate(3)
        False
        """
        if self.cid != cid and self._subordinates == []:
            return False
        elif self.cid == cid:
            return True
        elif self._subordinates[0].cid == cid:
            return True
        else:
            for sub in self._subordinates:
                if sub._is_subordinate(cid):
                    return True
            return False

    ###########################################################################
    ###########################################################################

    def get_all_subordinates(self) -> List[Citizen]:
        """Return a new list of all of the subordinates of this Citizen in
        order of ascending IDs.

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        >>> c3 = Citizen(3, "S.T.A.R.R.Y Lab", 3010, "Commander", 60)
        >>> c4 = Citizen(4, "S.T.A.R.R.Y Lab", 3010, "Commander", 60)
        >>> c5 = Citizen(5, "S.T.A.R.R.Y Lab", 3010, "Commander", 60)
        >>> c6 = Citizen(6, "S.T.A.R.R.Y Lab", 3010, "Commander", 60)
        >>> c5.become_subordinate_to(c1)
        >>> c1.become_subordinate_to(c4)
        >>> c2.become_subordinate_to(c4)
        >>> c3.become_subordinate_to(c1)
        >>> c6.become_subordinate_to(c2)
        >>> c4.get_direct_subordinates()[0].cid
        1
        >>> c4.get_direct_subordinates()[1].cid
        2
        >>> c2.get_direct_subordinates()[0].cid
        6
        >>> c4.get_direct_subordinates()[0].cid
        1
        >>> c4.get_direct_subordinates()[1].cid
        2
        >>> c2.get_direct_subordinates()[0].cid
        6
        >>> c1.get_direct_subordinates()[0].cid
        3
        >>> c1.get_direct_subordinates()[1].cid
        5
        >>> c4.get_all_subordinates()[0].cid
        1
        >>> c4.get_all_subordinates()[1].cid
        2
        """

        if not self.get_direct_subordinates():
            return []
        else:
            lst = []
            for subtree in self.get_direct_subordinates():
                # get a list of all indirect subordinate
                subtree_sub = subtree.get_all_subordinates()
                lst = merge(lst, subtree_sub)
            return merge(lst, self.get_direct_subordinates())

    def get_society_head(self) -> Citizen:
        """Return the head of the Society (i.e. the top-most superior Citizen,
        a.k.a. the root of the hierarchy).

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        >>> c3 = Citizen(3, "S.T.A.R.R.Y Lab", 3010, "Commander", 60)
        >>> c1.become_subordinate_to(c2)
        >>> c2.become_subordinate_to(c3)
        >>> c1.get_society_head() is c3
        True
        """
        # Note: This method must call itself recursively

        if self._superior is None:
            return self
        else:
            return self._superior.get_society_head()

    def get_closest_common_superior(self, cid: int) -> Citizen:
        """Return the closest common superior that this Citizen and the
        Citizen with ID <cid> share.

        If this Citizen is the superior of <cid>, return this Citizen.
        precondition: citizen with cid already in the tree

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        >>> c3 = Citizen(3, "S.T.A.R.R.Y Lab", 3010, "Commander", 60)
        >>> c4 = Citizen(4, "Starky Industries", 3022, "Manager", 55)
        >>> c5 = Citizen(5, "Hookins National Lab", 3023, "Engineer", 50)
        >>> c1.become_subordinate_to(c2)
        >>> c2.become_subordinate_to(c3)
        >>> c4.become_subordinate_to(c3)
        >>> c5.become_subordinate_to(c4)
        >>> c3.get_closest_common_superior(1) == c3
        True
        >>> c3.get_closest_common_superior(3) == c3
        True
        >>> c1.get_closest_common_superior(5) == c3
        True
        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        >>> c3 = Citizen(3, "S.T.A.R.R.Y Lab", 3010, "Commander", 60)
        >>> c4 = Citizen(4, "Starky Industries", 3022, "Manager", 55)
        >>> c5 = Citizen(5, "Hookins National Lab", 3023, "Engineer", 50)
        >>> c1.become_subordinate_to(c2)
        >>> c2.become_subordinate_to(c3)
        >>> c4.become_subordinate_to(c3)
        >>> c5.become_subordinate_to(c4)
        >>> c2.get_closest_common_superior(1) == c2

        """
        # Note: This method must call itself recursively
        if self.get_superior() is None:
            return self
        elif self.cid == cid:
            return self
        else:
            curr_sup = self.get_superior()
            curr_sup_subs = curr_sup.get_all_subordinates()
            if cid not in curr_sup_subs:
                return curr_sup.get_closest_common_superior(cid)
            else:
                return curr_sup

    ###########################################################################
    ###########################################################################
    def get_district_name(self) -> str:
        """Return the immediate district that the Citizen belongs to (or
        leads).

        If the Citizen is not part of any districts, return an empty string.

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = DistrictLeader(2, "Hookins National Lab", 3024, "Manager", \
        30, "District A")
        >>> c1.get_district_name()
        ''
        >>> c1.become_subordinate_to(c2)
        >>> c1.get_district_name()
        'District A'
        """
        # Note: This method must call itself recursively
        if isinstance(self, DistrictLeader):
            return self.get_district_name()
        elif not isinstance(self, DistrictLeader) and self._superior is None:
            return ''
        else:
            return self._superior.get_district_name()

    def rename_district(self, district_name: str) -> None:
        """Rename the immediate district which this Citizen is a part of to
        <district_name>.

        If the Citizen is not part of a district, do nothing.

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = DistrictLeader(2, "Hookins National Lab", 3024, "Manager", \
        30, "District A")
        >>> c3 = Citizen(3, "Starky Industries", 3024, "Labourer", 50)
        >>> c1.become_subordinate_to(c2)
        >>> c3.become_subordinate_to(c1)
        >>> c1.rename_district('District B')
        >>> c1.get_district_name()
        'District B'
        >>> c2.get_district_name()
        'District B'
        >>> c3.rename_district('District C')
        >>> c1.get_district_name()
        'District C'
        >>> c2.get_district_name()
        'District C'
        >>> c3.get_district_name()
        'District C'

        """
        # Note: This method must call itself recursively
        if isinstance(self, DistrictLeader):
            self.rename_district(district_name)
        elif self == self.get_society_head() and not isinstance(self, DistrictLeader):
            pass
        else:
            self._superior.rename_district(district_name)

    ###########################################################################
    ###########################################################################
    def get_highest_rated_subordinate(self) -> Citizen:
        """Return the direct subordinate of this Citizen with the highest
        rating.

        Precondition: This Citizen has at least one subordinate.

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = DistrictLeader(2, "Hookins National Lab", 3024, "Manager", 50,
        ... "District A")
        >>> c3 = DistrictLeader(3, "S.T.A.R.R.Y Lab", 3000, "Commander", 60,
        ... "District X")
        >>> c1.become_subordinate_to(c2)
        >>> c2.become_subordinate_to(c3)
        >>> c3.get_highest_rated_subordinate().manufacturer
        'Hookins National Lab'
        >>> c1.become_subordinate_to(c3)
        >>> c3.get_highest_rated_subordinate().manufacturer
        'Starky Industries'
        """
        # Hint: This can be used as a helper function for `delete_citizen`
        current = self.get_direct_subordinates()[0]
        for c in self.get_direct_subordinates():
            if c.rating > current.rating:
                current = c
        return current


class Society:
    """A society containing citizens in a hierarchy.

    === Private Attributes ===
    _head:
        The root of the hierarchy, which we call the "head" of the Society.
        If _head is None, this indicates that this Society is empty (there are
        no citizens in this Society).

    === Representation Invariants ===
    - No two Citizens in this Society have the same cid.
    """
    _head: Optional[Citizen]

    def __init__(self, head: Optional[Citizen] = None) -> None:
        """Initialize this Society with the head <head>.

        >>> o = Society()
        >>> o.get_head() is None
        True
        """
        self._head = head

    def __str__(self) -> str:
        """Return a string representation of this Society's tree.

        For each node, its item is printed before any of its descendants'
        items. The output is nicely indented.

        You may find this method helpful for debugging.
        """
        return str(self._head)

    ###########################################################################
    # You may use the methods below as helper methods if needed.
    ###########################################################################
    def get_head(self) -> Optional[Citizen]:
        """Return the head of this Society.
        """
        return self._head

    def set_head(self, new_head: Citizen) -> None:
        """Set the head of this Society to <new_head>.
        """
        self._head = new_head

    ###########################################################################
    ###########################################################################
    def get_citizen(self, cid: int) -> Optional[Citizen]:
        """Return the Citizen in this Society who has the ID <cid>. If no such
        Citizen exists, return None.

        # >>> o = Society()
        # >>> c1 = Citizen(1, "Starky Industries", 3024,  "Labourer", 50)
        # >>> c2 = Citizen(2, "Starky Industries", 3024,  "Labourer", 50)
        # >>> o.add_citizen(c1)
        # >>> o.get_citizen(1) is c1
        # True
        # >>> o.get_citizen(2) is None
        # True
        # >>> o.add_citizen(c2, 1)
        # >>> o.get_citizen(2) is c2
        # True
        >>> c = DistrictLeader(6, "Star", 3036, "CFO", 20, "Area 52")
        >>> c2 = DistrictLeader(5, "S.T.A.R.R.Y Lab", 3024, "Manager", 50, "Finance")
        >>> c3 = Citizen(7, "Hookins", 3071, "Labourer", 60)
        >>> c4 = Citizen(11, "Starky", 3036, "Repairer", 90)
        >>> c5 = Citizen(13, "STARRY", 3098, "Eng", 86)
        >>> s = Society()
        >>> s.add_citizen(c)
        >>> s.add_citizen(c2, 6)
        >>> s.add_citizen(c3, 5)
        >>> s.add_citizen(c4, 7)
        >>> s.add_citizen(c5, 7)
        >>> s.get_citizen(7) is c3
        True

        """
        # Hint: Recall that self._head is a Citizen object, so any of Citizen's
        # methods can be used as a helper method here.
        if self._head is None:
            return None
        elif self._head.cid == cid:
            return self._head
        else:
            for c in self._head.get_all_subordinates():
                if c.cid == cid:
                    return c
        return None

    def get_all_citizens(self) -> List[Citizen]:
        """Return a list of all citizens, in order of increasing cid.

        >>> o = Society()
        >>> c1 = Citizen(1, "Starky Industries", 3024, "Manager", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 65)
        >>> c3 = Citizen(3, "Starky Industries", 3024, "Labourer", 50)
        >>> c4 = Citizen(4, "S.T.A.R.R.Y Lab", 3024, "Manager", 30)
        >>> c5 = Citizen(5, "Hookins National Lab", 3024, "Labourer", 50)
        >>> c6 = Citizen(6, "S.T.A.R.R.Y Lab", 3024, "Lawyer", 30)
        >>> o.add_citizen(c4, None)
        >>> o.add_citizen(c2, 4)
        >>> o.get_all_citizens() == [c2, c4]
        True
        >>> o.add_citizen(c6, 2)
        >>> o.get_all_citizens() == [c2, c4, c6]
        True
        >>> o.add_citizen(c1, 4)
        >>> o.get_all_citizens() == [c1, c2, c4, c6]
        True
        >>> o.add_citizen(c3, 1)
        >>> o.get_all_citizens() == [c1, c2, c3, c4, c6]
        True
        >>> o.add_citizen(c5, 1)
        >>> o.get_all_citizens() == [c1, c2, c3, c4, c5, c6]
        True

        """
        if self._head is not None:
            lst1 = []
            lst2 = []
            for sub in self._head.get_all_subordinates():
                if sub.cid < self._head.cid:
                    lst1.append(sub)
                elif sub.cid > self._head.cid:
                    lst2.append(sub)
            if lst1:
                lst1.append(self._head)
                for c in lst2:
                    lst1.append(c)
                return lst1
            else:
                lst2.insert(0, self._head)
                return lst2
        else:
            return []

    def add_citizen(self, citizen: Citizen, superior_id: int = None) -> None:
        """Add <citizen> to this Society as a subordinate of the Citizen with
        ID <superior_id>.

        If no <superior_id> is provided, make <citizen> the new head of this
        Society, with the original head becoming the one and only subordinate
        of <citizen>.

        Preconditions:
        - citizen.get_superior() is None.
        - if <superior_id> is not None, then the Society contains a Citizen with
          ID <superior_id>.
        - Society does not already contain any Citizen with the same ID as
          <citizen>.

        # >>> o = Society()
        # >>> c1 = Citizen(1, "Starky Industries", 3024, "Manager", 50)
        # >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 65)
        # >>> c3 = Citizen(3, "Starky Industries", 3024, "Labourer", 50)
        # >>> c4 = Citizen(4, "S.T.A.R.R.Y Lab", 3024, "Manager", 30)
        # >>> c5 = Citizen(5, "Hookins National Lab", 3024, "Labourer", 50)
        # >>> c6 = Citizen(6, "S.T.A.R.R.Y Lab", 3024, "Lawyer", 30)
        # >>> o.add_citizen(c4, None)
        # >>> o.add_citizen(c2, 4)
        # >>> c2.get_superior() is c4
        # True
        # >>> o.add_citizen(c6, 2)
        # >>> c6.get_superior() is c2
        # True
        # >>> o.add_citizen(c1, 4)
        # >>> c1.get_superior() is c4
        # True

        >>> c = DistrictLeader(6, "Star", 3036, "CFO", 20, "Area 52")
        >>> c2 = DistrictLeader(5, "S.T.A.R.R.Y Lab", 3024, "Manager", 50, "Finance")
        >>> c3 = Citizen(7, "Hookins", 3071, "Labourer", 60)
        >>> c4 = Citizen(11, "Starky", 3036, "Repairer", 90)
        >>> c5 = Citizen(13, "STARRY", 3098, "Eng", 86)
        >>> s = Society()
        >>> s.add_citizen(c)
        >>> s.add_citizen(c2, 6)
        >>> s.add_citizen(c3, 5)
        >>> s.add_citizen(c4, 7)
        >>> s.add_citizen(c5, 7)
        """
        if superior_id is None:
            if self._head is None:
                self._head = citizen
            else:
                citizen.add_subordinate(self._head)
                self._head = citizen
        else:
            if self._head.cid == superior_id:
                self._head.add_subordinate(citizen)
            else:
                new_superior = self.get_citizen(superior_id)
                citizen.become_subordinate_to(new_superior)

    def get_citizens_with_job(self, job: str) -> List[Citizen]:
        """Return a list of all citizens with the job <job>, in order of
        increasing cid.

        >>> o = Society()
        >>> c1 = Citizen(1, "Starky Industries", 3024, "Manager", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 65)
        >>> c3 = Citizen(3, "Starky Industries", 3024, "Labourer", 50)
        >>> c4 = Citizen(4, "S.T.A.R.R.Y Lab", 3024, "Manager", 30)
        >>> c5 = Citizen(5, "Hookins National Lab", 3024, "Labourer", 50)
        >>> c6 = Citizen(6, "S.T.A.R.R.Y Lab", 3024, "Lawyer", 30)
        >>> o.add_citizen(c4, None)
        >>> o.add_citizen(c2, 4)
        >>> o.add_citizen(c6, 2)
        >>> o.add_citizen(c1, 4)
        >>> o.add_citizen(c3, 1)
        >>> o.add_citizen(c5, 1)
        >>> o.get_citizens_with_job('Manager') == [c1, c2, c4]
        True
        """
        lst = []
        for citizen in self.get_all_citizens():
            if citizen.job == job:
                lst.append(citizen)
        return lst

    ###########################################################################
    ###########################################################################
    def change_citizen_type(self, cid: int,
                            district_name: Optional[str] = None) -> Citizen:
        """Change the type of the Citizen with the given <cid>

        If the Citizen is currently a DistrictLeader, change them to become a
        regular Citizen (with no district name). If they are currently a regular
        Citizen, change them to become DistrictLeader for <district_name>.
        Note that this requires creating a new object of type either Citizen
        or DistrictLeader.

        The new Citizen/DistrictLeader should keep the same placement in the
        hierarchy (that is, the same superior and subordinates) that the
        original Citizen had, as well as the same ID, manufacturer, model year,
        job, and rating.

        Return the newly created Citizen/DistrictLeader.

        The original citizen that's being replaced should no longer be in the
        hierarchy (it should not be anyone's subordinate nor superior).

        Precondition:
        - If <cid> is the id of a DistrictLeader, <district_name> must be None
        >>> c = DistrictLeader(6, "Starky Industries", 3036, "Commander", 50, "A")
        >>> c2 = Citizen(2, "Hookins National", 3027, "Manager", 55)
        >>> c3 = Citizen(3, "Starky Industries", 3050, "Labourer", 50)
        >>> c4 = Citizen(5, "S.T.A.R.R.Y Lab", 3024, "Manager", 17)
        >>> c5 = Citizen(8, "Hookins National", 3024, "Cleaner", 70)
        >>> c6 = Citizen(7, "Hookins National", 3071, "Labourer", 35)
        >>> c7 = Citizen(9, "S.T.A.R.R.Y Lab", 3098, "Engineer", 86)
        >>> s = Society()
        >>> s.add_citizen(c)
        >>> s.add_citizen(c2, 6)
        >>> s.add_citizen(c3, 6)
        >>> s.add_citizen(c4, 6)
        >>> s.add_citizen(c5, 6)
        >>> s.add_citizen(c6, 5)
        >>> s.add_citizen(c7, 5)
        >>> s._head.cid
        6
        >>> s.change_citizen_type(6).cid == 6
        True
        """
        # change district leader to citizen
        member = None
        for c in self.get_all_citizens():
            if c.cid == cid:
                # change district leader to citizen
                if isinstance(c, DistrictLeader):
                    member = Citizen(cid, c.manufacturer,
                                     c.model_year, c.job, c.rating)
                    for i in c.get_direct_subordinates():
                        member.add_subordinate(i)

                    if c != self._head and c.get_superior():
                        c.get_superior().add_subordinate(member)
                        c.get_superior().remove_subordinate(c.cid)
                    else:
                        self._head = member
                # change citizen to district leader
                else:
                    member = DistrictLeader(cid, c.manufacturer,
                                            c.model_year, c.job,
                                            c.rating, district_name)
                    for i in c.get_direct_subordinates():
                        member.add_subordinate(i)
                    if c != self._head:
                        c.get_superior().add_subordinate(member)
                        c.get_superior().remove_subordinate(c.cid)
                    else:
                        self._head = member

        return member

    ###########################################################################
    ###########################################################################
    def _swap_up(self, citizen: Citizen) -> Citizen:
        """Swap <citizen> with their superior in this Society (they should
         swap their job, and their position in the tree, but otherwise keep
         all the same attribute data they currently have).

        If the superior is a DistrictLeader, the citizens being swapped should
        also switch their citizen type (i.e. the DistrictLeader becomes a
        regular Citizen and vice versa).

        Return the Citizen after it has been swapped up ONCE in the Society.

        Precondition:
        - <citizen> has a superior (i.e., it is not the head of this Society),
          and is not a DistrictLeader.
        """
        lst = []
        dummy2 = None
        member = None
        if self._head.cid == citizen.cid:
            pass
        elif isinstance(citizen.get_superior(), DistrictLeader):
            member = self.change_citizen_type(citizen.cid,
                                              citizen.get_superior().
                                              get_district_name())
            member2 = self.change_citizen_type(member.get_superior().cid)
            if self._head.cid == member.get_superior().cid:
                if member.get_direct_subordinates() == [] \
                        and len(self._head.get_direct_subordinates()) == 1:
                    member.job, self._head.job = self._head.job, member.job
                    for i in self._head.get_direct_subordinates():
                        self._head.remove_subordinate(i.cid)
                    self._head = member
                    member2.become_subordinate_to(self._head)

                else:
                    for i in member.get_direct_subordinates():
                        member.remove_subordinate(i.cid)
                        lst.append(i)
                    for i in self._head.get_direct_subordinates():
                        if i.cid != member.cid:
                            i.become_subordinate_to(member)
                    for i in lst:
                        i.become_subordinate_to(self._head)
                    member.job, self._head.job = self._head.job, member.job
                    member.add_subordinate(self._head)
                    self._head = member

            else:
                dummy = member.get_superior()
                dummy1 = member.get_superior().get_superior()
                member.get_superior().get_superior(). \
                    remove_subordinate(dummy.cid)
                dummy1.add_subordinate(member)
                for i in dummy.get_direct_subordinates():
                    if i.cid != member.cid:
                        member.add_subordinate(i)
                dummy2 = dummy1
                for i in member2.get_direct_subordinates():
                    member2.remove_subordinate(i.cid)
                member2.become_subordinate_to(member)
                member.become_subordinate_to(self._head)
                member.job, dummy.job = dummy.job, member.job

        else:
            if self._head == citizen.get_superior():
                for i in citizen.get_direct_subordinates():
                    citizen.remove_subordinate(i.cid)
                    lst.append(i)
                for i in self._head.get_direct_subordinates():
                    if i.cid != citizen.cid:
                        citizen.add_subordinate(i)
                        self._head.remove_subordinate(i.cid)
                for i in lst:
                    self._head.add_subordinate(i)
                citizen.job, self._head.job = self._head.job, citizen.job
                citizen.add_subordinate(self._head)
                self._head = citizen

            else:
                dummy = citizen.get_superior()
                dummy1 = citizen.get_superior().get_superior()
                dummy2 = dummy1
                citizen.get_superior().get_superior(). \
                    remove_subordinate(dummy.cid)
                dummy1.add_subordinate(citizen)
                for i in dummy.get_direct_subordinates():
                    if i.cid != citizen.cid:
                        citizen.add_subordinate(i)
                        dummy.remove_subordinate(i.cid)
                    dummy.remove_subordinate(i.cid)
                citizen.add_subordinate(dummy)
                citizen.job, dummy.job = dummy.job, citizen.job
            citizen.set_superior(dummy2)
            return citizen

        return member

    def promote_citizen(self, cid: int) -> None:
        """Promote the Citizen with cid <cid> until they either:
             - have a superior with a higher rating than them or,
             - become DistrictLeader for their district.
        See the Assignment 2 handout for further details.

        Precondition: There is a Citizen with the cid <cid> in this Society.
        # >>> c = DistrictLeader(6, "Star", 3036, "CFO", 20, "Area 52")
        # >>> c2 = DistrictLeader(5, "S.T.A.R.R.Y Lab", 30, "Manager", 50, "Finance")
        # >>> c3 = Citizen(7, "Hookins", 3071, "Labourer", 60)
        # >>> c4 = Citizen(11, "Starky", 3036, "Repairer", 90)
        # >>> c5 = Citizen(13, "STARRY", 3098, "Eng", 86)
        # >>> s = Society()
        # >>> s.add_citizen(c)
        # >>> s.add_citizen(c2, 6)
        # >>> s.add_citizen(c3, 5)
        # >>> s.add_citizen(c4, 7)
        # >>> s.add_citizen(c5, 7)
        # >>> s.promote_citizen(11)
        >>> c = DistrictLeader(6, "Star", 3036, "CFO", 20, "Area 52")
        >>> c2 = Citizen(5, "S.T.A.R.R.Y Lab", 30, "Manager", 50)
        >>> s = Society()
        >>> s.add_citizen(c)
        >>> s.add_citizen(c2, 6)
        >>> s.promote_citizen(5)



        """
        c = self.get_citizen(cid)
        while c.cid != self._head.cid:
            if isinstance(c, DistrictLeader) \
                    or c.get_superior().rating > c.rating:
                break
            else:
                c = self._swap_up(c)

    ###########################################################################
    ###########################################################################

    def delete_citizen(self, cid: int) -> None:
        """Remove the Citizen with ID <cid> from this Society.

        If this Citizen has subordinates, their subordinates become subordinates
        of this Citizen's superior.

        If this Citizen is the head of the Society, their most highly rated
        direct subordinate becomes the new head. If they did not have any
        subordinates, the society becomes empty (the society head becomes None).

        Precondition: There is a Citizen with the cid <cid> in this Society.
        >>> s = Society()
        >>> c1 = Citizen(1, 'Citizen 1', 3001, 'Big boss', 10)
        >>> s.add_citizen(c1)
        >>> c2 = DistrictLeader(2, 'Citizen 2', 3002, 'Bank robber', 19, 'D2')
        >>> c3 = Citizen(3, 'Citizen 3', 3003, 'Cook', 82)
        >>> c4 = Citizen(4, 'Citizen 4', 3004, 'Cook', 5)
        >>> s.add_citizen(c2, 1)
        >>> s.add_citizen(c3, 1)
        >>> s.add_citizen(c4, 1)
        >>> c5 = Citizen(5, 'Citizen 5', 3005, 'Farmer', 101)
        >>> c6 = Citizen(6, 'Citizen 6', 3006, 'Coach', 56)
        >>> s.add_citizen(c5, 2)
        >>> s.add_citizen(c6, 2)
        >>> c8 = Citizen(8, 'Citizen 8', 3008, 'Farmer', 22)
        >>> c9 = Citizen(9, 'Citizen 9', 3009, 'Farmer', 22)
        >>> c10 = Citizen(10, 'Citizen 10', 3010, 'Driver', 22)
        >>> s.add_citizen(c8, 6)
        >>> s.add_citizen(c9, 6)
        >>> s.add_citizen(c10, 6)
        >>> c7 = DistrictLeader(7, 'Citizen 7', 3007, 'Builder', 58, 'D7')
        >>> s.add_citizen(c7, 4)
        >>> s.delete_citizen(6)
        >>> c2.get_direct_subordinates()[0].cid
        >>> c2.get_direct_subordinates()[1].cid



        """
        for c in self.get_all_citizens():
            if c.cid == cid:
                # if c is not the head of the society
                if c != self._head:
                    # C does have subordinates
                    if c.get_direct_subordinates():
                        for i in c.get_direct_subordinates():
                            c.get_superior().add_subordinate(i)
                        c.get_superior().remove_subordinate(cid)
                    # C doesn't have subordinates
                    else:
                        c.get_superior().remove_subordinate(cid)
                # c is the head of the society then get
                # the highest rated subordinate to become the new head.
                else:
                    # know c is self._head
                    if self._head.get_direct_subordinates():
                        highest_rated = self._head. \
                            get_highest_rated_subordinate()
                        for i in self._head.get_direct_subordinates():
                            if i.cid != highest_rated.cid:
                                highest_rated.add_subordinate(i)
                                self._head.remove_subordinate(i.cid)
                        self._head = highest_rated
                    else:
                        self._head = None


###############################################################################
###############################################################################
class DistrictLeader(Citizen):
    """The leader of a district in a society.

    === Private Attributes ===
    _district_name:
        The name of the district that this DistrictLeader is the leader of.

    === Inherited Public Attributes ===
    cid:
        The ID number of this citizen.
    manufacturer:
        The manufacturer of this Citizen.
    model_year:
        The model year of this Citizen.
    job:
        The name of this Citizen's job within the Society.
    rating:
        The rating of this Citizen.

    === Inherited Private Attributes ===
    _superior:
        The superior of this Citizen in the society, or None if this Citizen
        does not have a superior.
    _subordinates:
        A list of this Citizen's direct subordinates (that is, Citizens that
        work directly under this Citizen).

    === Representation Invariants ===
    - All Citizen RIs are inherited.
    """
    _district_name: str

    ###########################################################################
    ###########################################################################
    def __init__(self, cid: int, manufacturer: str, model_year: int,
                 job: str, rating: int, district: str) -> None:
        """Initialize this DistrictLeader with the ID <cid>, manufacturer
        <manufacturer>, model year <model_year>, job <job>, rating <rating>, and
        district name <district>.

        >>> c2 = DistrictLeader(2, "Some Lab", 3024, "Lawyer", 30, "District A")
        >>> c2.manufacturer
        'Some Lab'
        >>> c2.get_district_name()
        'District A'
        """
        Citizen.__init__(self, cid, manufacturer, model_year, job, rating)
        self._district_name = district

    def get_district_citizens(self) -> List[Citizen]:
        """Return a list of all citizens in this DistrictLeader's district, in
        increasing order of cid.

        Include the cid of this DistrictLeader in the list.

        >>> c1 = DistrictLeader(
        ...     1, "Hookins National Lab", 3024, "Commander", 65, "District A"
        ... )
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Lawyer", 30)
        >>> c3 = Citizen(3, "S.T.A.R.R.Y Lab", 3010, "Labourer", 55)
        >>> c2.become_subordinate_to(c1)
        >>> c3.become_subordinate_to(c1)
        >>> c1.get_district_citizens() == [c1, c2, c3]
        True

        """
        lst1 = []
        lst2 = []
        for sub in self.get_all_subordinates():
            if sub.cid < self.cid:
                lst1.append(sub)
            elif sub.cid > self.cid:
                lst2.append(sub)
        if lst1 != []:
            lst1.append(self)
            for c in lst2:
                lst1.append(c)
            return lst1
        else:
            lst2.insert(0, self)
            return lst2

    ###########################################################################
    ###########################################################################
    def get_district_name(self) -> str:
        """Return the name of the district that this DistrictLeader leads.
        If the Citizen is not part of any districts, return an empty string.
        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = DistrictLeader(2, "Hookins National Lab", 3024, "Manager", \
        30, "District A")
        >>> c1.get_district_name()
        ''
        >>> c1.become_subordinate_to(c2)
        >>> c1.get_district_name()
        'District A'
        """
        if isinstance(self, DistrictLeader):
            return self._district_name
        elif isinstance(self.get_superior(), DistrictLeader):
            return self.get_superior()._district_name
        else:
            head = self.get_society_head()
            for sub in head.get_all_subordinates():
                if isinstance(sub, DistrictLeader):
                    if self in sub.get_all_subordinates():
                        return self.get_district_name()
                else:
                    return ''

    def rename_district(self, district_name: str) -> None:
        """Rename this district leader's district to the given <district_name>.
         If the Citizen is not part of a district, do nothing.

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = DistrictLeader(2, "Hookins National Lab", 3024, "Manager", \
        30, "District A")
        >>> c1.become_subordinate_to(c2)
        >>> c1.rename_district('District B')
        >>> c1.get_district_name()
        'District B'
        >>> c2.get_district_name()
        'District B'
        """
        if isinstance(self, DistrictLeader):
            self._district_name = district_name
        elif isinstance(self.get_superior(), DistrictLeader):
            self.get_superior()._district_name = district_name
        else:
            head = self.get_society_head()
            for sub in head.get_all_subordinates():
                if isinstance(sub, DistrictLeader):
                    if self in sub.get_all_subordinates():
                        self.rename_district(district_name)


###########################################################################
# ALL PROVIDED FUNCTIONS BELOW ARE COMPLETE, DO NOT CHANGE
###########################################################################
def create_society_from_file(file: TextIO) -> Society:
    """Return the Society represented by the information in file.

    >>> o = create_society_from_file(open('citizens.csv'))
    >>> o.get_head().manufacturer
    'Hookins National Lab'
    >>> len(o.get_head().get_all_subordinates())
    11
    """
    head = None
    people = {}
    for line in file:
        info: List[Any] = line.strip().split(',')
        info[0] = int(info[0])
        info[2] = int(info[2])
        info[4] = int(info[4])

        if len(info) == 7:
            inf = info[:5] + info[-1:]
            person = DistrictLeader(*inf)
        else:
            person = Citizen(*info[:5])

        superior = info[5]
        if not info[5]:
            head = person
            superior = None
        else:
            superior = int(superior)
        people[info[0]] = (person, superior)

    for key in people:
        if people[key][1] is not None:
            people[people[key][1]][0].add_subordinate(people[key][0])

    return Society(head)


###########################################################################
# Sample societies from the handout
###########################################################################
def simple_society_demo() -> Society:
    """Handout example related to a simple society.
    """
    c = Citizen(6, "Starky Industries", 3036, "Commander", 50)
    c2 = Citizen(2, "Hookins National", 3027, "Manager", 55)
    c3 = Citizen(3, "Starky Industries", 3050, "Labourer", 50)
    c4 = Citizen(5, "S.T.A.R.R.Y Lab", 3024, "Manager", 17)
    c5 = Citizen(8, "Hookins National", 3024, "Cleaner", 74)
    c6 = Citizen(7, "Hookins National", 3071, "Labourer", 5)
    c7 = Citizen(9, "S.T.A.R.R.Y Lab", 3098, "Engineer", 86)

    s = Society()
    s.add_citizen(c)
    s.add_citizen(c2, 6)
    s.add_citizen(c3, 6)
    s.add_citizen(c4, 6)
    s.add_citizen(c5, 6)
    s.add_citizen(c6, 5)
    s.add_citizen(c7, 5)

    return s


def district_society_demo() -> Society:
    """Handout example related to a simple society with districts.
    """
    c = DistrictLeader(6, "Starky Industries", 3036, "Commander", 50, "Area 52")
    c2 = DistrictLeader(2, "Hookins National", 3027, "Manager", 55,
                        "Repair Support")
    c3 = Citizen(3, "Starky Industries", 3050, "Labourer", 50)
    c4 = DistrictLeader(5, "S.T.A.R.R.Y Lab", 3024, "Manager", 17, "Finance")
    c5 = Citizen(8, "Hookins National", 3024, "Cleaner", 74)
    c6 = Citizen(7, "Hookins National", 3071, "Labourer", 5)
    c7 = Citizen(9, "S.T.A.R.R.Y Lab", 3098, "Engineer", 86)

    s = Society()
    s.add_citizen(c)
    s.add_citizen(c2, 6)
    s.add_citizen(c3, 6)
    s.add_citizen(c4, 6)
    s.add_citizen(c5, 6)
    s.add_citizen(c6, 5)
    s.add_citizen(c7, 5)

    return s


def promote_citizen_demo() -> Society:
    """Handout example related to promote_citizen.
    """
    c = DistrictLeader(6, "Star", 3036, "CFO", 20, "Area 52")
    c2 = DistrictLeader(5, "S.T.A.R.R.Y Lab", 3024, "Manager", 50, "Finance")
    c3 = Citizen(7, "Hookins", 3071, "Labourer", 60)
    c4 = Citizen(11, "Starky", 3036, "Repairer", 90)
    c5 = Citizen(13, "STARRY", 3098, "Eng", 86)
    s = Society()
    s.add_citizen(c)
    s.add_citizen(c2, 6)
    s.add_citizen(c3, 5)
    s.add_citizen(c4, 7)
    s.add_citizen(c5, 7)

    s.promote_citizen(11)
    return s


def create_from_file_demo() -> Society:
    """Handout example related to reading from the provided file citizens.csv.
    """
    return create_society_from_file(open("citizens.csv"))


if __name__ == "__main__":
    # As you complete your tasks, you can uncomment any of the function calls
    # and the print statement below to create and print out a sample society:
    soc = simple_society_demo()
    # soc = district_society_demo()
    # soc = promote_citizen_demo()
    # soc = create_from_file_demo()
    # print(soc)

    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': ['typing', '__future__',
                                   'python_ta', 'doctest'],
        'disable': ['E9998', 'R0201'],
        'max-args': 7,
        'max-module-lines': 1600
    })
