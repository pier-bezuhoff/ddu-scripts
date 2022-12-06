#!/usr/bin/env python
from itertools import chain, groupby
from functools import reduce
from copy import copy
from math import hypot
from random import uniform
from dataclasses import dataclass
from collections.abc import Sequence, Iterable
from statistics import mean
import os
import numpy as np
from numpy.linalg import det
from llist import dllist # setup: pip install llist
# mine
from run_ddu import invert
from polar_transformation import circle2pole, pole2circle, pole2matrix

Rule = tuple[int]

@dataclass
class Circle:
    x: float
    y: float
    r: float
    color: int = 0 # f"#{color:06X}" -> css color format
    visible: bool = False
    rule: str = ""
    fill: bool = False

    # simple test of inv. matrix correctness: compare
    # pt.pole2circle(*pt.pole2xyz(c.to_matrix(1000) @ c1.to_pole(1000)), R=1000)
    # with c.invert(c1)
    def invert(self, circle: 'Circle') -> 'Circle':
        "*self* $ *circle*"
        dx, dy = circle.x - self.x, circle.y - self.y
        d = hypot(dx, dy)
        r = circle.r
        if d == r: # supposed to transform into a straight line
            d += 1e-6
        ratio = self.r * self.r / (d*d - r*r)
        new_x = self.x + ratio * dx
        new_y = self.y + ratio * dy
        new_r = abs(r * ratio)
        new_circle = copy(circle)
        new_circle.x = new_x
        new_circle.y = new_y
        new_circle.r = new_r
        return new_circle

    def show_coords(self):
        return f"Circle(x={self.x:.2f}, y={self.y:.2f}, r={self.r:.2f})"

    def show_pole(self, R=1):
        x,y,z = circle2pole(self.x, self.y, self.r, R)
        return f"({x:.4f}, {y:.4f}, {z:.4f})"

    def show_matrix(self, R=1) -> str:
        m = self.to_matrix(R=R)
        s = ""
        for i in range(4):
            s += '\n' + "  ".join(f"{m[i,j]:.4f}" for j in range(4))
        return s

    def print_pole(self, R=1):
        print(self.show_pole(R=R))

    def print_matrix(self, R=1):
        print(self.show_matrix(R=R))

    def __repr__(self):
        return self.show_coords()

    def to_pole(self, R=1):
        x,y,z = circle2pole(self.x, self.y, self.r, R)
        return np.array([[x,y,z,1.0]]).T

    def to_matrix(self, R=1):
        x,y,z = circle2pole(self.x, self.y, self.r, R)
        return pole2matrix(x,y,z, R=R)

    @staticmethod
    def random():
        return Circle(uniform(-1000, 1000), uniform(-1000, 1000), uniform(1e-6, 1000))


class Ddu:

    def __init__(self, circles: Sequence[Circle]):
        self.circles = list(circles)

    def __repr__(self):
        return self.show_ranks()

    def print_all_rules(self):
        snd = lambda ir: ir[1]
        rule_groups = groupby(sorted(enumerate(self.str_rules), key=snd), key=snd)
        for rule, nrs in rule_groups:
            if rule == '':
                rule = '-'
            ns = ','.join(f"#{n}" for (n, _r) in nrs)
            print(f"{ns}: {rule}")

    def print_unique_rules(self):
        print_short_rules(self.unique_rules)

    def show_ranks(self) -> str:
        rules = self.rules
        output = ""
        ranks, cringe = self.calculate_ranks()
        key = lambda n: rules[n]
        for i, r in enumerate(ranks):
            if r:
                output += f"\n| rank {i} | "
                for (rule, ns) in groupby(sorted(r, key=key), key=key):
                    rule = ''.join(str(x) for x in rule)
                    if rule == '':
                        rule = '-'
                    l = list(ns)
                    if len(l) > 10:
                        ns = f"#{l[0]}...#{l[-1]}"
                    else:
                        ns = ','.join(f"#{n}" for n in l)
                    output += f"{ns}: {rule}   "
        if cringe:
            output += "\n|> cringe <| "
            for (rule, ns) in groupby(sorted(cringe, key=key), key=key):
                rule = ''.join(str(x) for x in rule)
                ns = ','.join(f"#{n}" for n in ns)
                output += f"\n    {ns}: {rule}"
        return output

    def calculate_ranks(self) -> tuple[list[int], set[int]]:
        "-> ([rank:[#]], {unranked circle #s})"
        rules = self.rules
        left = set(range(len(rules)))
        ranks = []
        rank0 = []
        for i, rule in enumerate(rules):
            if not rule:
                rank0.append(i)
        ranks.append(rank0)
        left -= set(rank0)
        i = 1
        while left and i < 100:
            rank_i = []
            upper_ranks = set(chain.from_iterable(ranks))
            for k in left:
                if set(rules[k]).issubset(upper_ranks):
                    rank_i.append(k)
            ranks.append(rank_i)
            left -= set(rank_i)
            i += 1
        return (ranks, left)

    def step(self):
        cs = []
        for c in self.circles:
            for j in c.rule:
                cj = self.circles[int(j)]
                c = cj.invert(c)
            cs.append(c)
        self.circles = cs

    def iterate(self, n_steps: int) -> tuple[Rule]:
        rules = self.rules
        unique_rules = self.unique_rules
        d = dict((r,ix) for (ix,r) in enumerate(unique_rules))
        rule_ixs = [d[r] for r in rules] # [#:rule_ix]
        for _ in range(n_steps):
            new_rules = []
            for ix in range(len(unique_rules)):
                rule = unique_rules[ix]
                new_rule = tuple(chain.from_iterable(
                    apply_rule(unique_rules[rule_ix], tuple(part))
                    for (rule_ix, part)
                    in groupby(rule, key=lambda c: rule_ixs[c])
                ))
                new_rules.append(cancel_rule(new_rule))
            unique_rules = new_rules
        return unique_rules

    def split_parts(self):
        # note: reverses all the rules for matrix repr
        all_rules = self.rules
        rules = self.unique_rules
        parts = set()
        rule_splits = []
        for rule in rules:
            split = tuple(
                (r, tuple(p)) for (r, p)
                in groupby(
                    reversed(rule),
                    key=lambda c: all_rules[c][::-1]
                )
            )
            rule_splits.append([part for (_, part) in split])
            for (r, part) in split:
                parts.add((r, part))
        parts = tuple(sorted(parts))
        parts_only = tuple(p for (r, p) in parts)
        rules4parts = tuple(r for (r, _) in parts)
        rule_blueprints = tuple(tuple(parts_only.index(part) for part in split) for split in rule_splits)

        # step
        #new_parts = parts_repr + rules4parts + rules_repr
        #new_rules_repr = rule_blueprints + new_parts
        return (parts_only, rules4parts, rule_blueprints)
        #return (
        #        [rule2str(p) for p in parts_only],
        #        [rule2str(r) for r in rules4parts],
        #        rule_blueprints
        #        )

    def _run(self, n_steps):
        cs0 = tuple((c.x, c.y, c.r, tuple(int(x) for x in c.rule)) for c in self.circles)
        cs = cs0
        for _ in range(n_steps):
            new_cs = []
            for (x,y,r,rule) in cs:
                for ix in rule:
                    x0, y0, r0, _ = cs[ix]
                    x,y,r = invert(x0, y0, r0, x, y, r)
                new_cs.append(x, y, r, rule)
            cs = new_cs

        parts, rules4parts, rule_blueprints = self.split_parts()
        pivot_ixs = set(chain.from_iterable(self.unique_rules))
        poles = dict() # [c#: 1x4]
        pivots = dict() # [c#: 4x4]
        for ix in pivot_ixs:
            cx, cy, r, _ = cs0[ix]
            x, y, z = circle2pole(cx, cy, r)
            poles[ix] = (x, y, z, 1)
            pivots[ix] = pole2matrix(x, y, z)
        # [p#: 4x4]
        parts = [reduce(np.matmul, (pivots[ix] for ix in part), np.eye(4, 4)) for part in parts]
        # [r#: 4x4]
        rules = [reduce(np.matmul, (parts[ix] for ix in rb), np.eye(4, 4)) for rb in rule_blueprints]
        cumulative_rules = [np.eye(4, 4) for _ in range(len(rules))]

        for _ in range(n_steps):
            cumulative_rules = [r@cr for (r, cr) in zip(rules, cumulative_rules)]
            parts = [rules[r_ix] * p * rules[r_ix].inv() for (r_ix, p) in zip(rules4parts, parts)]
            rules = [reduce(np.matmul, (parts[ix] for ix in rb)) for rb in rule_blueprints]
        ps = [cr.dot(p) for (cr, p) in zip(cumulative_rules, poles)]
        cs2 = [pole2circle(x, y, z, w) for (x,y,z,w) in ps] # ERROR: non-scalar xyzw

        av_squared_error = mean((x1-x2)**2 + (y1-y2)**2 + (r1-r2)**2 for ((x1,y1,r1,_), (x2,y2,r2,_)) in zip(cs, cs2))
        return av_squared_error


    @property
    def str_rules(self) -> list[str]:
        return [c.rule for c in self.circles]

    @property
    def str_unique_rules(self) -> tuple[str]:
        return tuple(rule2str(x) for x in sorted(set(self.rules)))

    @property
    def rules(self) -> tuple[Rule]:
        return tuple(tuple(int(x) for x in c.rule) for c in self.circles)

    @property
    def unique_rules(self) -> tuple[Rule]:
        return tuple(sorted(set(self.rules)))

    @staticmethod
    def read_from(path: str) -> "Ddu":
        "from *.ddu"
        circles = []
        circle = {}

        def read_float(s):
            return float(s.replace(',', '.'))
        def read_bool(s):
            if s == '1':
                return True
            elif s == '0':
                return False
            else:
                return bool(s)
        def read_color(s): # in hex: BBGGRR -> RRGGBB
            bgr = int(s)
            b = (bgr >> 16) & 0xff
            g = (bgr >> 8) & 0xff
            r = bgr & 0xff
            rgb = r << 16 | g << 8 | b
            return rgb

        def add_circle():
            if {'x', 'y', 'r'}.issubset(circle.keys()):
                if 'rule' not in circle:
                    circle['visible'] = False
                    circle['rule'] = ""
                if 'visible' in circle:
                    circles.append(Circle(**circle))

        with open(path, 'r') as f:
            param_line = -1
            for i, line in enumerate(f.readlines()):
                line = line.strip()
                if i == 2: # bg color in the 3rd line
                    bg_color = read_color(line)
                elif line.startswith("circle"):
                    add_circle()
                    param_line = 0
                    circle = {}
                elif param_line >= 0:
                    if param_line == 0:
                        circle['r'] = read_float(line)
                    elif param_line == 1:
                        circle['x'] = read_float(line)
                    elif param_line == 2:
                        circle['y'] = read_float(line)
                    elif param_line == 3: # color (stored as hex BBGGRR in base 10)
                        circle['color'] = read_color(line)
                    elif param_line == 4:
                        circle['fill'] = read_bool(line)
                    elif param_line == 5: # ['n']<rule>
                        if line.startswith('n'):
                            circle['visible'] = False
                            circle['rule'] = line[1:]
                        elif line:
                            circle['visible'] = True
                            circle['rule'] = line
                    param_line += 1
            add_circle()
        return Ddu(circles)


def cancel_rule(rule: Rule) -> Rule:
    "remove all consecutive equal elements"
    r = dllist(rule)
    focus = r.first
    while focus is not None and focus.next is not None:
        nxt = focus.next
        if focus.value == nxt.value:
            prev = focus.prev or nxt.next
            r.remove(nxt)
            r.remove(focus)
            focus = prev
        else:
            focus = nxt
    return tuple(r)

def find_repeating_subsequences(seq: Sequence[int]) -> list[tuple[int, tuple[int]]]:
    "[30101016784545] -> [(1 [3]) (3 [01]) (1 [678]) (2 [45])]"
    # NOTE: only len=2 subsequences
    seq = tuple(seq)
    i = 0
    n = len(seq)
    parts = []
    chunk = []
    while i+3 < n:
        if seq[i] == seq[i+2] and seq[i+1] == seq[i+3]:
            if chunk:
                parts.append((1, tuple(chunk)))
                chunk = []
            j = i+2
            while j+3 < n and seq[j] == seq[j+2] and seq[j+1] == seq[j+3]:
                j += 2
            power = (j-i)//2 + 1
            part = (power, seq[i:i+2])
            parts.append(part)
            i = j+2
        else:
            chunk.append(seq[i])
            i += 1
    rest = seq[i:i+3]
    if chunk:
        chunk += rest
        parts.append((1, tuple(chunk)))
    elif rest:
        parts.append((1, rest))
    return parts

def print_short_rule(rule: Rule):
    if rule == '':
        print('-', end='')
    for p, seq in find_repeating_subsequences(rule):
        s = ''.join(str(x) for x in seq)
        if p == 1:
            print(s, end='')
        else:
            print(f" {p}x/{s}/ ", end='')

def print_short_rules(rules: Iterable[Rule]):
    for rule in rules:
        print_short_rule(rule)
        print()

def str2rule(s: str) -> Rule:
    return [int(x) for x in s]

def rule2str(rule: Rule) -> str:
    return ''.join(str(x) for x in rule)

def apply_rule(rule: Rule, target_rule: Rule) -> Rule:
    return rule + target_rule + rule[::-1]


dir_path = "/home/pierbezuhoff/Programming/Android/Dodeca/app/src/main/assets/ddu/"
triada_path = dir_path + "Triada.ddu"
triada = Ddu.read_from(triada_path)
winter = Ddu.read_from(dir_path + "Winter.ddu")

def ddu_named(name: str) -> Ddu:
    return Ddu.read_from(dir_path + name + ".ddu")

if __name__ == '__main__':
    for filename in os.listdir(dir_path):
        ddu = Ddu.read_from(dir_path + filename)
        print(f"\n\n[( {filename} )] {ddu}")
