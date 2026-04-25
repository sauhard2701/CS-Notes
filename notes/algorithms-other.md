# Algorithms - Miscellaneous
## Tower of Hanoi

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/69d6c38d-1dec-4f72-ae60-60dbc10e9d15.png" width="300"/> </div><br>

There are three pegs: from, buffer, and to. All disks on from need to be moved to to, while ensuring that smaller disks are always on top of larger disks.

This is a classic recursion problem, solved in three steps:

① Move n-1 disks from from -\> buffer

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/f9240aa1-8d48-4959-b28a-7ca45c3e4d91.png" width="300"/> </div><br>

② Move 1 disk from from -\> to

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/f579cab0-3d49-4d00-8e14-e9e1669d0f9f.png" width="300"/> </div><br>

③ Move n-1 disks from buffer -\> to

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/d02f74dd-8e33-4f3c-bf29-53203a06695a.png" width="300"/> </div><br>

If there is only one disk, only one move is needed.

From the discussion above, a<sub>n</sub> = 2 * a<sub>n-1</sub> + 1. Clearly, a<sub>n</sub> = 2<sup>n</sup> - 1, so n disks require 2<sup>n</sup> - 1 moves.

```java
public class Hanoi {
    public static void move(int n, String from, String buffer, String to) {
        if (n == 1) {
            System.out.println("from " + from + " to " + to);
            return;
        }
        move(n - 1, from, to, buffer);
        move(1, from, buffer, to);
        move(n - 1, buffer, from, to);
    }

    public static void main(String[] args) {
        Hanoi.move(3, "H1", "H2", "H3");
    }
}
```

```html
from H1 to H3
from H1 to H2
from H3 to H2
from H1 to H3
from H2 to H1
from H2 to H3
from H1 to H3
```

## Huffman Coding

Encode data according to the frequency with which it appears, thereby compressing the original data.

For example, in a text file, the occurrence counts of various characters are as follows:

- a : 10
- b : 20
- c : 40
- d : 80

Each character can be converted into a binary code, for example a to 00, b to 01, c to 10, and d to 11. This is the simplest encoding method and does not consider each character's weight, meaning its occurrence frequency. Huffman coding uses a greedy strategy so that the most frequent characters have the shortest codes, ensuring the shortest overall encoded length.

First generate a Huffman tree. During each generation step, choose the two nodes with the lowest frequencies and create a new node as their parent, whose frequency is the sum of the two nodes. The reason for choosing the lowest frequencies is that nodes selected earlier are placed lower in the tree and therefore require longer codes; using lower-frequency nodes there reduces the total encoded length.

When generating codes, start from the root. Add binary bit 0 when traversing left, and binary bit 1 when traversing right, until reaching a leaf node. The code for the character represented by that leaf node is the path code.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/8edc5164-810b-4cc5-bda8-2a2c98556377.jpg" width="300"/> </div><br>

```java
public class Huffman {

    private class Node implements Comparable<Node> {
        char ch;
        int freq;
        boolean isLeaf;
        Node left, right;

        public Node(char ch, int freq) {
            this.ch = ch;
            this.freq = freq;
            isLeaf = true;
        }

        public Node(Node left, Node right, int freq) {
            this.left = left;
            this.right = right;
            this.freq = freq;
            isLeaf = false;
        }

        @Override
        public int compareTo(Node o) {
            return this.freq - o.freq;
        }
    }

    public Map<Character, String> encode(Map<Character, Integer> frequencyForChar) {
        PriorityQueue<Node> priorityQueue = new PriorityQueue<>();
        for (Character c : frequencyForChar.keySet()) {
            priorityQueue.add(new Node(c, frequencyForChar.get(c)));
        }
        while (priorityQueue.size() != 1) {
            Node node1 = priorityQueue.poll();
            Node node2 = priorityQueue.poll();
            priorityQueue.add(new Node(node1, node2, node1.freq + node2.freq));
        }
        return encode(priorityQueue.poll());
    }

    private Map<Character, String> encode(Node root) {
        Map<Character, String> encodingForChar = new HashMap<>();
        encode(root, "", encodingForChar);
        return encodingForChar;
    }

    private void encode(Node node, String encoding, Map<Character, String> encodingForChar) {
        if (node.isLeaf) {
            encodingForChar.put(node.ch, encoding);
            return;
        }
        encode(node.left, encoding + '0', encodingForChar);
        encode(node.right, encoding + '1', encodingForChar);
    }
}
```
