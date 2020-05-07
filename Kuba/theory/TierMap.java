import java.util.ArrayList;
class HashNode<K,V> 
{
	K key;
	V value;
	
	HashNode<K,V> next;
	public HashNode(K key, V value) 
	{
		this.key = key;
		this.value = value;
	}
}

//End HashMaps
class HashMap<K,V> 
{
	K key;
	V value;
	private ArrayList<HashNode<K,V>> buckets;
	
	private int numBuckets;
	
	private int size;

	public HashMap(int numBuckets) {
		this.buckets = new ArrayList<>(numBuckets);
		this.numBuckets = numBuckets;
		this.size = 0;
		for (int i = 0; i < this.numBuckets; i++) {
			this.buckets.add(null);
		}
	}
	public int size() { return this.size;}
	public boolean isEmpty() {return (this.size == 0)} 		
	//Need to figure out hash function
	private int getBucketIndex(K Key) {
		
	}
	public V get(K Key) {}
	public void add(K Key, V Value) {}
}
//Third Layer pass in number of black and get correct map
class ThirdLayer<Integer,HashMap<K,V>> {
	private ArrayList<HashMap<K,V>> buckets;
	private int numBuckets;
	private int size;
	public ThirdLayer(int numBuckets) {
		this.buckets = new ArrayList<>(numBuckets);
		this.numBuckets = numBuckets;
		this.size = 0;
		for (int i = 0; i < this.numBuckets; i++){
			this.buckets.add(null);
		}
	}
	public int size() {return this.size;}
	
	private HashMap<K,V> get(int key) {
		HashNode<K,V> head = this.buckets.get(key);
		while (head != null) {
			if (head.key.equals(key)) {
				return head.value;
			} else {
				head = head.next;
			}
		}
		return null;
	}
	private void add(int key, HashMap<K,V> value) {
		HashNode<K,V> head = this.buckets.get(key);
		
		while (head != null) {
			if (head.key.equals(key)) {
				head.value = value;
				return;
			} else {
				head = head.next;
			}
		}	
		this.size++;
		head = this.buckets.get(key);
		HashNode<K, V> newNode = new HashNode<K,V>(key,value);
		newNode.next = head;
		this.buckets.set(key,newNode);
	}
}
class TierMap<Position,FirstLayer<Position,SecondLayer<Position,ThirdLayer<Position,HashMap<Position,int>>>>
