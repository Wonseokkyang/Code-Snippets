#include"FastQueue.h"
#include<iostream>

using namespace std;

int main(){
	FastQueue<int> test_queue;

	// cout<<"==================================="<<endl;
	// cout<<"FastQueue creation.."<<endl;
	// // test_queue.enqueue(4);
	// cout<<"test_queue size: "<<test_queue.size()<<endl;
	// cout<<"test_queue capacity: "<<test_queue.capacity()<<endl;
	// cout<<"head value: "<<test_queue.head()<<endl;
	// cout<<"tail value: "<<test_queue.tail()<<endl;


	//	TESTING	//
	// Adding numbers to queue
	for(int i{0}; i<test_queue.capacity(); ++i){
		test_queue.enqueue(test_queue.capacity()-i);
	}

	cout<<endl;

	test_queue.print_props();
	test_queue.print_all();
	cout<<endl;

	//	TESTING	//
	// Dequeing
	cout<<"=Dequeing"<<endl;
	test_queue.dequeue();

	test_queue.print_props();
	test_queue.print_all();
	cout<<endl;

	//	TESTING	//
	// Adding 0 to queue
	cout<<"=Adding 0 to queue"<<endl;
	test_queue.enqueue(0);

	test_queue.print_props();
	test_queue.print_all();
	cout<<endl;

	//	TESTING	//
	// Dequeing 4 times
	cout<<"=Dequeing 4 times"<<endl;
	for(int i{0}; i<4; ++i){
		test_queue.dequeue();
	}

	test_queue.print_props();
	test_queue.print_all();
	cout<<endl;

	//	TESTING	//
	// Testing for at(index) out of range
	cout<<"=Testing for element at index-th 0 of queue: "<<test_queue.at(0)<<endl;
	cout<<"=Testing for element at index-th 1 of queue: "<<test_queue.at(1)<<endl;
	cout<<"=Testing for element at index-th 2 of queue: "<<test_queue.at(2)<<endl;
	cout<<"=Testing for element at index-th 3 of queue: "<<test_queue.at(3)<<endl;

	test_queue.print_props();
	test_queue.print_all();
	cout<<endl;

	//Works and throw out_of_range
	// cout<<"=Testing for element at index-th 5 of queue: "<<test_queue.at(5)<<endl;

	//	TESTING	//
	// Testing for tail out of range
	FastQueue<int> empty_q;
	// cout<<"Testing for empty container tail()"<<endl;
	// empty_q.tail();	//Works
	// cout<<"Testing for empty container head()"<<endl;
	// empty_q.head();	//Works

	//	TESTING	//
	// Testing shrink to fit
	cout<<"=BEFORE adding an element and shrinking"<<endl;
	empty_q.print_props();
	empty_q.print_all();
	cout<<endl;

	empty_q.enqueue(99);
	empty_q.shrink_to_fit();

	cout<<"\n=AFTER adding an element and shrinking"<<endl;
	empty_q.print_props();
	empty_q.print_all();
	cout<<endl;

	cout<<"\n=Adding an element to test queue resizing"<<endl;
	empty_q.enqueue(11);
	empty_q.print_props();
	empty_q.print_all();
	cout<<endl;

	cout<<"\n=Adding another element to test queue resizing"<<endl;
	empty_q.enqueue(88);
	empty_q.print_props();
	empty_q.print_all();
	cout<<endl;

	cout<<"\n=Deqeuing 2 elements to move head forwards and adding 3 elements "<<endl;
	empty_q.dequeue();
	empty_q.dequeue();

	empty_q.print_props();
	empty_q.print_all();
	cout<<endl;

	cout<<"\n=Now adding 3 elements"<<endl;
	empty_q.enqueue(33);
	empty_q.enqueue(33);
	empty_q.enqueue(33);
	empty_q.print_props();
	empty_q.print_all();
	cout<<endl;

	cout<<"\n=Another element to test resizing again"<<endl;
	empty_q.enqueue(44);
	empty_q.print_props();
	empty_q.print_all();
	cout<<endl;

	return 0;
}
