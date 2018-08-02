class AvlTree:
    class Node:
        def __init__(self, val, lchild=None, rchild=None):
            self.val = val
            self.size = 1
            self.height = 1
            self.parent = None
            self.lchild = lchild
            self.rchild = rchild
            
        def setLChild(self,child):
            print("*node %s setLchild(%s)"%(str(self.val),"None" if child is None else str(child.val)))
            if not self.lchild is None:
                self.size -= self.lchild.size
                #self.lchild.parent = None
            if not child is None:
                self.size += child.size
                #print("Setting lchild %s parent to %s"%(str(child),str(self.val)))
                child.parent = self
                #print("\tNode %s parent is now %s"%(str(child),str(child.parent)))
            self.lchild = child
            
        def setRChild(self,child):
            print("*node %s setRchild(%s)"%(str(self.val),"None" if child is None else str(child.val)))
            if not self.rchild is None:
                self.size -= self.rchild.size
                #self.rchild.parent = None
            if not child is None:
                self.size += child.size
                #print("Setting rchild %s parent to %s"%(str(child),str(self.val)))
                child.parent = self
                #print("\tNode %s parent is now %s"%(str(child),str(child.parent)))
            self.rchild = child

        def _updateParent(self):
            if not self.parent is None:
                self.parent.update()
            else:
                print("*reached root update on "+str(self))
                
        def update(self):
            lheight,lsize = (0,0) if self.lchild is None else (
                self.lchild.height,self.lchild.size)
            rheight,rsize = (0,0) if self.rchild is None else (
                self.rchild.height,self.rchild.size)
            print("*node %s update height:max(%i,%i)+1, size:%i+%i+1"%(str(self),lheight,rheight,lsize,rsize))
            self.height = max(lheight,rheight) + 1
            self.size = lsize+rsize+1
            self._updateParent()
        
        def getOrder(self):
            lheight = 0 if self.lchild is None else self.lchild.height
            rheight = 0 if self.rchild is None else self.rchild.height
            return rheight - lheight

        def __repr__(self):
            lchild = "_" if self.lchild is None else str(self.lchild.val)
            rchild = "_" if self.rchild is None else str(self.rchild.val)
            return "{%s<%s>%s}"%(lchild,str(self.val),rchild)
        
    def __init__(self):
        self.root = None
    
    def __len__(self):
        if self.root is None:
            return 0
        return self.root.size
    
    def add(self,val):
        if self.root is None:
            self.root = AvlTree.Node(val)
        else:
            self._add(val,self.root)

    def _findValParent(self,val,node,parent,isLeft):
        if node is None:
            return None
        elif val > node.val:
            return self.findVal(val,node.rchild,False)
        elif val < node.val:
            return self.findVal(val,node.node.lchild,True)
        else:
            return (parent,isLeft)

    def _findParentSetter(self,node):
        if node.parent is None:
            return self._setRoot
        elif node is node.parent.lchild:
            return node.parent.setLChild
        else:
            return node.parent.setRChild
        
    def remove(self,val):
        #any duplicate would be stored in the left subtree
        valParent,isLeftChild = self._findValParent(val,self.root,self)
        if removeNode is None:
            raise ValueError("Cannot remove value '%s' from tree!"%str(val))
        if removeNode is self:
            self.root = None
        else:
            '''
            if isLeftChild:
                #swap out with  
                valParent.setLChild(
            else:
            '''
            pass
            
            
    def _setRoot(self,node):
        print("Set root to "+str(node))
        self.root = node
        node.parent = None
        
    def _add(self,val,node):
        print("Add node %s to subtree %s"%(val,node))
        #traverse until there is a place to add
        if val <= node.val:
            if node.lchild is None:
                node.setLChild(AvlTree.Node(val))
                node.update()
                self._balance(node)
            else:
                self._add(val,node.lchild)
        else:
            if node.rchild is None:
                node.setRChild(AvlTree.Node(val))
                node.update()
                self._balance(node)
            else:
                self._add(val,node.rchild)
        #balance the parent and its subsequent parents
        
    def _rotL(self,nodeX,nodeZ):
        print("Rotating Left on %s \\ %s"%(str(nodeX),str(nodeZ)))
        parentSetter = self._findParentSetter(nodeX)
        #given parentSetter is X's parent node's setter function
        #set x rchild to z's lchild
        nodeX.setRChild(nodeZ.lchild)
        #set z lchild to x
        nodeZ.setLChild(nodeX)
        #x's parent, replace x w/z
        parentSetter(nodeZ)
        nodeX.update()
        
    def _rotR(self,nodeX,nodeZ):
        print("Rotating Right on %s / %s"%(str(nodeZ),str(nodeX)))
        parentSetter = self._findParentSetter(nodeX)
        #given parentSetter is X's parent node's setter function
        #set x lchild to z's rchild
        nodeX.setLChild(nodeZ.rchild)
        #set z rchild to x
        nodeZ.setRChild(nodeX)
        #x's parent, replace x w/z
        parentSetter(nodeZ)
        nodeX.update()
        
    def _balance(self,node):
        print("Balancing %s height:%i order:%i"%(str(node), node.height, node.getOrder() ))
            
        if node.getOrder() < -1:
            #LL
            if node.lchild.getOrder() < 0:
                print("\tLL CASE")
                #rotate right on node and its lchild
                self._rotR(node,node.lchild)
            #LR
            elif node.lchild.getOrder() > 0:
                print("\tLR CASE")
                #rotate left on node's lchild's rchild & node's lchild
                self._rotL(node.lchild,node.lchild.rchild)
                #rotate right on node's lchild and node
                self._rotR(node,       node.lchild)
            else:
                #violation of AVL tree
                raise AssertionError("node %s was leftheavy but lchild %s was order 0"%(str(node),str(node.lchild)))
        elif node.getOrder() > 1:
            #RR
            if node.rchild.getOrder() > 0:
                print("\tRR CASE")
                #rotate left on node and its rchild
                self._rotL(node,node.rchild)
            #RL
            elif node.rchild.getOrder() < 0:
                print("\tRL CASE")
                #rotate right on node's rchild's lchild & node's rchild
                self._rotR(node.rchild, node.rchild.lchild)
                #rotate left on node's rchild and node
                self._rotL(node,        node.rchild)
            else:
                #violation of AVL tree
                raise AssertionError("node %s was rightheavy but rchild %s was order 0"%(str(node),str(node.rchild)))
        if not node.parent is None:
            self._balance(node.parent)
    def assertIntegrity(self,node=None):
        if node is None:
            if self.root is None:
                return
            node = self.root
        if not node.lchild is None:
            assert node.lchild.parent is node, "node %s to lchild %s broken"%(str(node),str(node.lchild))
            self.assertIntegrity(node.lchild)
        if not node.rchild is None:
            assert node.rchild.parent is node, "node %s to rchild %s broken"%(str(node),str(node.rchild))
            self.assertIntegrity(node.rchild)
            
    def _inOrderRepr(self,node):
        lchild = "" if node.lchild is None else self._inOrderRepr(node.lchild) + "<"
        rchild = "" if node.rchild is None else ">" + self._inOrderRepr(node.rchild)
        return "{%s%s%s}"%(lchild, str(node.val), rchild)
    
    def __repr__(self):
        return "{}" if self.root is None else self._inOrderRepr(self.root)

#test the tree
print("-"*10)
print("Creating AvlTree")
tree = AvlTree()
assert str(tree) == "{}","FAILED: Tree failed creation"
print(str(tree))

print("-"*10)
print("Add 5")
tree.add(5)
assert str(tree) == "{5}","FAILED: Add 5 tree:"+str(tree)
tree.assertIntegrity()
print(str(tree))

print("-"*10)
print("Add 2")
tree.add(2)
assert str(tree) == "{{2}<5}","FAILED: Add 2 tree:"+str(tree)
tree.assertIntegrity()
print(str(tree))

print("-"*10)
print("Add 8")
tree.add(8)
assert str(tree) == "{{2}<5>{8}}","FAILED: Add 8 tree:"+str(tree)
tree.assertIntegrity()
print(str(tree))

print("-"*10)
print("Add 10")
tree.add(10)
assert str(tree) == "{{2}<5>{8>{10}}}","FAILED: Add 10 tree:"+str(tree)
tree.assertIntegrity()
print(str(tree))

print("-"*10)
print("Add 12")
#triggers RR condition on 8
tree.add(12)
assert str(tree) == "{{2}<5>{{8}<10>{12}}}","FAILED: Add 12 tree:"+str(tree)
tree.assertIntegrity()
print(str(tree))

print("-"*10)
print("Add 6")
#triggers RL condition on the root
tree.add(6)
assert str(tree) == "{{{2}<5>{6}}<8>{10>{12}}}","FAILED: Add 6 tree:"+str(tree)
tree.assertIntegrity()
print(str(tree))

print("-"*10)
print("Add 1")
tree.add(1)
assert str(tree) == "{{{{1}<2}<5>{6}}<8>{10>{12}}}","FAILED: Add 1 tree:"+str(tree)
tree.assertIntegrity()
print(str(tree))

print("-"*10)
print("Add 3")
tree.add(3)
assert str(tree) == "{{{{1}<2>{3}}<5>{6}}<8>{10>{12}}}","FAILED: Add 3 tree:"+str(tree)
tree.assertIntegrity()
print(str(tree))

print("-"*10)
print("Add 4")
#triggers LR condition on 5
tree.add(4)
assert str(tree) == "{{{{1}<2}<3>{{4}<5>{6}}}<8>{10>{12}}}","FAILED: Add 4 tree:"+str(tree)
tree.assertIntegrity()
print(str(tree))


print("-"*10)
print("Add 0")
#triggers LL condition on 2
tree.add(0)
assert str(tree) == "{{{{0}<1>{2}}<3>{{4}<5>{6}}}<8>{10>{12}}}","FAILED: Add 0 tree:"+str(tree)
tree.assertIntegrity()
print(str(tree))
