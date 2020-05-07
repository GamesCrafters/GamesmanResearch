class Position {
	private int boardsize;
	private int reds;
	private int white;
	private int black;
	private int p0taken;
	private int p1taken;
	public int arr[];
	//Intial Construction
	public Position(int boardsize, int r, int w, int b, int arr[]) {
		this.boardsize = boardsize;
		this.reds = r;
		this.white = w;
		this.black = b;
		this.arr = arr;
		this.p0taken = 0; this.p1taken = 0;
	}
	//Creates a new position from do move and 
	//flips the colors.
	private Position(Position p,Move m) {
	}
	private void flip() {
		int temp;
		temp = this.white; this.white = this.black; this.black = temp;
		temp = this.p0taken; this.p0taken = this.p1taken; this.p1taken = temp;
	}

}  
class Move {
	private int[] oldPosition;
	private int[] newPosition;
}
class MoveNode {
	private Move m;
	//private MoveNode prev;
	private MoveNode next;
	private ModeNode() {
		this.m = null;
	//	this.prev = null;
		this.next = null;
	}
	private MoveNode(Move m) {
		this.m = m;
	//	this.prev = null;
		this.next = null;
	}
	private Move getMove() {return this.m;}
	//private void setPrev(MoveNode prev) {this.prev = prev;}
	private void setNext(MoveNode next) {this.next = next;}
	//private MoveNode getPrev() {return this.prev;}
	private MoveNode getNext() {return this.next;}
}
class MoveQueue {
	//Actually a queue
	private int MovesLeft;
	private MoveNode current;
	
	public MoveQueue() {
		this.MovesLeft = 0;
		this.current = new MoveNode();
	}
	private void AddMove(Move m) {
		this.MovesLeft++;
		MoveNode newNode = new MoveNode(m);
		newNode.setNext(this.current);
		this.current = newNode;
	}
	private boolean isEmpty() {return (this.MovesLeft == 0)}
	private Move getNext() {
		if (this.isEmpty()) {
			return null;
		}
		Move m = this.current.getMove();
		this.MovesLeft--;
		this.current = this.current.getNext();
		return m;
	}
}	
class Kuba {
	private Position DoMove(Position p, Move m) {}
	private MoveQueue GenerateMove(Position p) {}
	private int PrimitiveValue(Position p) {}
}
