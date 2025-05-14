# BST Variation 3

from __future__ import annotations
from typing import List
import json

verbose = False

# The class for a particular node in the tree.
# DO NOT MODIFY!
class Node():
    def  __init__(self,
                  age        : int       = None,
                  rownumbers : List[int] = [],
                  leftchild  : Node      = None,
                  rightchild : Node      = None):
        self.age        = age
        self.rownumbers = rownumbers
        self.leftchild  = leftchild
        self.rightchild = rightchild

# The class for a database.
# DO NOT MODIFY!
class DB():
    def __init__(self,
                 rows : List[List] = [],
                 root : Node       = None):
        self.rows = rows
        self.root = root

    # These dump_ methods are done for you.
    # DO NOT MODIFY!
    # Dump the rows of the database.
    def dump_rows(self) -> str:
        return('\n'.join([f'{i},{l[0]},{l[1]}' for i,l in enumerate(self.rows)]))
    # Dump the index of the database.
    def dump_index(self) -> str:
        def _to_dict(node) -> dict:
            return {
                "age"        : node.age,
                "rownumbers" : node.rownumbers,
                "leftchild"  : (_to_dict(node.leftchild) if node.leftchild is not None else None),
                "rightchild" : (_to_dict(node.rightchild) if node.rightchild is not None else None)
            }
        if self.root == None:
            dict_repr = {}
        else:
            dict_repr = _to_dict(self.root)
        return json.dumps(dict_repr,indent = 2)


    # Insert a row into the database and into the index.
    def insert(self,name: str, age: int):
        row_index = len(self.rows)  
        self.rows.append([name, age])  

        if self.root is None:
            self.root = Node(age, [row_index])
            return
        current = self.root
        while True:
            if age == current.age:
                current.rownumbers.append(row_index)
                return
            elif age < current.age:
                if current.leftchild is None:
                    current.leftchild = Node(age,[row_index])
                    return
                else:
                    current = current.leftchild
            else:
                if current.rightchild is None:
                    current.rightchild = Node(age,[row_index])
                    return
                else:
                    current = current.rightchild
    

    # Delete a row from the database and from the index.
    # For the index since it's a BST use the inorder successor when a replacement is needed.
    def delete(self,name:str):
        row_to_delete = None
        index = 0
        for row in self.rows:
            if row[0] == name:
                row_to_delete = index
                break
            index +=1
        if row_to_delete is None:
            return
        age = self.rows[row_to_delete][1]
        self.rows.pop(row_to_delete)

        #remove from BST
        current = self.root
        parent = None
        while current is not None:
            if age == current.age:
                current.rownumbers.remove(row_to_delete)
                #update others
                if current.rownumbers == []:
                    if current.leftchild is None and current.rightchild is None:
                        if parent is None:
                            self.root = None
                        elif parent.leftchild == current:
                            parent.leftchild = None
                        else:
                            parent.rightchild = None

                    #node has one child
                    elif current.leftchild is None:
                        if parent is None:
                            self.root = current.rightchild
                        elif parent.leftchild == current:
                            parent.leftchild = current.rightchild
                        else:
                            parent.rightchild = current.rightchild
                    elif current.rightchild is None:
                        if parent is None:
                            self.root = current.leftchild
                        elif parent.leftchild == current:
                            parent.leftchild = current.leftchild
                        else:
                            parent.rightchild = current.leftchild
                    #node has two children
                    else:
                        in_order_successor = current.rightchild
                        while in_order_successor.leftchild is not None:
                            in_order_successor = in_order_successor.leftchild
                        current.age = in_order_successor.age
                        current.rownumbers = in_order_successor.rownumbers

                        #print("has two kids:",current.age, current.rownumbers)
                        parent_successor = current.rightchild
                        while parent_successor.leftchild is not None:
                            #print(parent_successor.leftchild.age)
                            if parent_successor.leftchild.leftchild is None:
                                break
                            parent_successor = parent_successor.leftchild
                        #print("parent",parent_successor.age)
                        if in_order_successor == current.rightchild:
                            current.rightchild = current.rightchild.rightchild
                        if parent_successor.leftchild == in_order_successor:

                            parent_successor.leftchild = in_order_successor.rightchild
                        else:
                            parent_successor.rightchild = in_order_successor.rightchild
                def update_row_numbers(node:Node):
                    if node is None:
                        return
                    else:
                        for i in range(len(node.rownumbers)):
                            if node.rownumbers[i]>row_to_delete:
                                node.rownumbers[i] -=1
                                #print("in update:" ,node.age,node.rownumbers)
                        update_row_numbers(node.leftchild)
                        update_row_numbers(node.rightchild)
                update_row_numbers(self.root)
                return
            elif age < current.age:
                parent = current
                current = current.leftchild
            else:
                parent = current
                current = current.rightchild


    # Use the index to find a list of people whose age is specified.
    # This should return a list of the form:
    # [d,n1,n2,...]
    # Where d is the depth of the appropriate node in the index (BST)
    # and n1,n2,... are the people.
    def find_people(self,age:int):
        # These next two lines are just to make it run.
        # You'll need to replace these with your code.
        d = 0
        l = []
        current = self.root 
        while current is not None:
            if age == current.age:
                l = [self.rows[i][0] for i in current.rownumbers]
                return [d] + l
            elif age < current.age:
                current = current.leftchild
            else:
                current = current.rightchild
            d+=1
        # Return the result.
        return [-1]