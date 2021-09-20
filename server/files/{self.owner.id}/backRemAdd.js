class SLLNode {
    constructor(value) {
        this.value = value;
        this.next = null;
    }
}

class SLL {
    constructor() {
        this.head = null;
    }
    addFront(value) {
        var newNode = new SLLNode(value);
        newNode.next = this.head;
        this.head = newNode;
        return this;
    }
    addBack(value) {
        var newNode = new SLLNode(value);
        var runner = this.head;
        if (this.head == null) {
            this.head = newNode;
            return this;
        }
        while (runner.next != null) {
            runner = runner.next;
        }
        runner.next = newNode;
        return this;
    }
    removeFront() {
        var oldHead = this.head;
        var newHead = oldHead.next;
        console.log(oldHead.value + " is no longer the head node");
        console.log("The head node's value is now " + newHead.value);
        this.head = newHead;
        oldHead = newHead;
        return this;
    }
    removeBack() {
        var pointer = this.head;
        var runner = pointer.next;
        while (pointer.next != null) {
            pointer = pointer.next;
            runner = pointer.next;
            if (runner.next == null) {
                pointer.next = null;
                return this;
            }
        }
    }
    viewFront() {
        var headNode = this.head;
        console.log("The head node's value is " + headNode.value);
        return headNode.value;
    }
    viewBack() {
        var runner = this.head;
        while (runner != null) {
            if (runner.next == null) {
                return runner.value;
            }
            runner = runner.next;
        }
    }
    display() {
        var currentNode = this.head;
        var i = 1;
        while (currentNode != null) {
            if (currentNode == this.head) {
                console.log("Node head (#" + i + ") value is " + currentNode.value);
            } else {
                if (currentNode.next != null) {
                    console.log("Next node (#" + i + ") value is " + currentNode.value);
                } else {
                    console.log("Last node (#" + i + ") value is " + currentNode.value);
                }
            }
            currentNode = currentNode.next;
            i++;
        }
    }
    containsVal(value) {
        var runner = this.head;
        while (runner != null) {
            if (runner.value == value) {
                return true;
            }
            runner = runner.next;
        }
        return false;
    }
    nodeLength() {
        var length = 1;
        var currentNode = this.head;
        while (currentNode.next != null) {
            currentNode = currentNode.next;
            length += 1;
        }
        return "Length of SLL is " + length + " nodes.";
    }
    min() {
        var runner = this.head;
        var min = runner.value;
        while (runner != null) {
            if (runner.value < min) {
                min = runner.value;
            }
            runner = runner.next;
        }
        return "The minimum value is " + min;
    }
    avg() {
        var count = 1;
        var runner = this.head;
        var sum = runner.value;
        while (runner != null) {
            count++;
            sum += runner.value;
            runner = runner.next;
        }
        var avg = sum / count;
        return "The average value is (" + sum + "/" + count + ") = "+ avg;
    }
    max() {
        var runner = this.head;
        var max = runner.value;
        while (runner != null) {
            if (runner.value > max) {
                max = runner.value;
            }
            runner = runner.next;
        }
        return "The maximum value is " + max;
    }
}

var firstSLL = new SLL();
firstSLL.addFront(47);
// console.log(firstSLL);
// console.log("--------------------------------------------------");
firstSLL.addFront(88);
// console.log(firstSLL);
// console.log("--------------------------------------------------");
firstSLL.addFront(23);
// console.log(firstSLL);
// console.log("--------------------------------------------------");
firstSLL.addFront(77);
// console.log(firstSLL);
firstSLL.display();
console.log("-------------------------------------------------------------------");
console.log(firstSLL.nodeLength());
console.log("-------------------------------------------------------------------");
console.log(firstSLL.removeBack().viewBack());
console.log("-------------------------------------------------------------------");
console.log(firstSLL.nodeLength());
console.log("-------------------------------------------------------------------");
firstSLL.display();
console.log("-------------------------------------------------------------------");
console.log(firstSLL.addBack(33).viewBack());
console.log("-------------------------------------------------------------------");
firstSLL.display();
