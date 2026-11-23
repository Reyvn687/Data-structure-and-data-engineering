from collections import deque


class Node:
    def __init__(self, v):
        self.v = v
        self.next = None
        self.prev = None
        self.left = None
        self.right = None


tasks = []
h = [[], [], [], [], []]
root = None
wait = []
done = []
recent = deque()
jhead = None
bhead = None
btail = None
week = [None] * 7
days = ["Bazar ertəsi", "Çərşənbə axşamı", "Çərşənbə", "Cümə axşamı", "Cümə", "Şənbə", "Bazar"]

a = Node("Aysel")
b = Node("Kamran")
c = Node("Leyla")
a.next = b
b.next = c
c.next = a
cur = a

tree = Node("Tapşırıqlar")
tree.left = Node("İş")
tree.right = Node("Şəxsi")
tree.left.left = Node("Proqramlaşdırma")
tree.left.right = Node("Toplantı")
tree.right.left = Node("Alış-veriş")
tree.right.right = Node("İdman")


def ins(n, k):
    if n == None:
        return Node(k)
    if k < n.v:
        n.left = ins(n.left, k)
    else:
        n.right = ins(n.right, k)
    return n


def inorder(n):
    if n == None:
        return []
    return inorder(n.left) + [n.v] + inorder(n.right)


def preorder(n):
    if n == None:
        return []
    return [n.v] + preorder(n.left) + preorder(n.right)


def postorder(n):
    if n == None:
        return []
    return postorder(n.left) + postorder(n.right) + [n.v]


def note(t):
    global jhead
    n = Node(t)
    if jhead == None:
        jhead = n
    else:
        x = jhead
        while x.next != None:
            x = x.next
        x.next = n
    recent.appendleft(t)
    if len(recent) > 3:
        recent.pop()


def add(t):
    global root, cur, bhead, btail
    owner = cur.v
    cur = cur.next
    tasks.append(t)
    h[len(tasks) % 5].append([len(tasks), t])
    root = ins(root, t)
    wait.append(t)
    n = Node(t)
    if bhead == None:
        bhead = n
        btail = n
    else:
        n.prev = btail
        btail.next = n
        btail = n
    note("Əlavə olundu: " + t + " -> " + owner)
    return owner


for s in ["Hesabat yaz", "Süd al", "Kodu yoxla", "İdmana get", "Dərs oxu", "Zəng et"]:
    add(s)

while True:
    print()
    print("=== TAPŞIRIQ MENECERİ ===")
    print("1. Əlavə et")
    print("2. Bütün tapşırıqlar")
    print("3. ID ilə tap")
    print("4. Əlifba sırası ilə")
    print("5. Növbətini tamamla")
    print("6. Axırıncı tamamlananı geri aç")
    print("7. İrəli və geri bax")
    print("8. Həftəlik plan")
    print("9. Komanda növbəsi")
    print("10. Son 3 əməliyyat")
    print("11. Tam jurnal")
    print("12. Kateqoriya ağacı")
    print("0. Çıxış")
    x = input("Seçim: ")

    if x == "0":
        break
    elif x == "1":
        t = input("Tapşırıq adı: ")
        o = add(t)
        print("Məsul şəxs:", o)
    elif x == "2":
        print("ölçü:", len(tasks))
        i = 1
        for t in tasks:
            print("#" + str(i), t)
            i = i + 1
    elif x == "3":
        id = int(input("ID: "))
        r = None
        for p in h[id % 5]:
            if p[0] == id:
                r = p[1]
        print("Nəticə:", r)
        print("bucket:", id % 5)
        for i in range(5):
            print("bucket", i, [p[0] for p in h[i]])
    elif x == "4":
        for t in inorder(root):
            print("-", t)
    elif x == "5":
        if len(wait) == 0:
            print("Gözləyən yoxdur")
        else:
            t = wait.pop(0)
            done.append(t)
            note("Tamamlandı: " + t)
            print("Tamamlandı:", t)
    elif x == "6":
        if len(done) == 0:
            print("Tamamlanan yoxdur")
        else:
            t = done.pop()
            wait.append(t)
            note("Yenidən açıldı: " + t)
            print("Geri açıldı:", t)
    elif x == "7":
        l = []
        n = bhead
        while n != None:
            l.append(n.v)
            n = n.next
        print("irəli:", l)
        l = []
        n = btail
        while n != None:
            l.append(n.v)
            n = n.prev
        print("geri:", l)
    elif x == "8":
        for i in range(7):
            print(i + 1, days[i] + ":", week[i] or "-")
        d = input("Gün nömrəsi (1-7): ")
        if d.isdigit() and 1 <= int(d) <= 7:
            week[int(d) - 1] = input("Tapşırıq: ")
    elif x == "9":
        l = [a.v, a.next.v, a.next.next.v]
        print(l)
        print("Növbəti:", cur.v)
    elif x == "10":
        for t in recent:
            print("-", t)
    elif x == "11":
        n = jhead
        while n != None:
            print("-", n.v)
            n = n.next
    elif x == "12":
        print("preorder:", preorder(tree))
        print("inorder:", inorder(tree))
        print("postorder:", postorder(tree))
    else:
        print("Yanlış seçim")
