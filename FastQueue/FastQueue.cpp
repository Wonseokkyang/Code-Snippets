/**
  Won Seok Yang
  CS335 - Home Project 3 - FastQueue
*/

/* Professor suggested starting capacity to be 8 */
#include <iostream>
#include <vector>
#include <stdexcept>
#include <exception>

template <typename T> 
FastQueue<T>::FastQueue(){
	vq_head = 0;
    vq_size = 0;
    vq.resize(8);
}; //end FastQueue()

/* Adds an element to the tail of queue. If the queue is full, double the capacity. */
template <typename T> 
void FastQueue<T>::enqueue(T new_element){	
	if (vq.capacity()==vq_size) { 	//vector is at full capacity
		std::vector<T> temp_v;
		temp_v.resize(vq.capacity()*2);

		for (int i{0}; i<vq_size; ++i){
			std::swap(temp_v[i], vq[(vq_head+i)%vq.capacity()]);
		}
		std::swap(vq, temp_v);
		vq_head = 0;	//head is at the beginning again
	}
    vq[(vq_head+vq_size) % vq.capacity()] = new_element;
    ++vq_size;
};  //end enqueue()


/* Removes an element from the head of the queue. 
   Does nothing if the queue is already empty. */
template <typename T> 
void FastQueue<T>::dequeue(){
	if(vq_size>0){	//
		//dont actually need to erase because the previous head will be overwritten
		vq_head = (vq_head+1) % (vq.capacity()-1);
		--vq_size;
	}
};	//end dequeue()


/* Returns reference to the first element of the queue. 
   Throws out_of_range if the container is empty. */
template <typename T> 
T& FastQueue<T>::head(){
	if (vq_size==0){
		throw std::out_of_range("FastQueue<T>::head() : container is empty");
	}
	else{
		return vq[vq_head];
	}
};	//end head()


/* Returns reference to the last element of the queue. 
   Throws out_of_range if the container is empty.  */
template <typename T> 
T& FastQueue<T>::tail(){
	if (vq_size==0){
		throw std::out_of_range("FastQueue<T>::tail() : container is empty");
	}
	else{
		return vq[((vq_head+vq_size)%vq.capacity())-1];
	}
};	//end tail()


/* Returns reference to the index-th element of the queue. 
   Throws out_of_range if the container size is less than index.*/
template <typename T> 
T& FastQueue<T>::at(int index){
	if (index>vq_size){
		throw std::out_of_range("FastQueue<T>::at() : index is out of range");
	}
	else{
		return vq[(index+vq_head)%vq.capacity()];
	}
};	//end at()


/* Get size */
template <typename T> 
int FastQueue<T>::size(){
	return vq_size;
};


/* Get capacity */
template <typename T> 
int FastQueue<T>::capacity(){
	return vq.capacity();
};	//end capacity()


/* Resizes the container to the number of elements in the container */
template <typename T> 
void FastQueue<T>::shrink_to_fit(){
	std::vector<T> temp_v;
	temp_v.resize(vq_size);
	for (int i{0}; i<vq_size; ++i){
		std::swap(temp_v[i], vq[(vq_head+i)%vq.capacity()]);
	}
	std::swap(vq, temp_v);
	vq_head = 0;	//head is at the beginning of the resized vector
};	//end shrink_to_fit()


/**=========================*/
/*	For testing				*/
/**=========================*/

template <typename T> 
void FastQueue<T>::print_all(){
	std::cout<<"Index: \t\t|";
	for (int i{0}; i<vq.capacity(); ++i){
		std::cout<<i<<" | ";
	}

	std::cout<<"\n------------------------------------------------";
	
	std::cout<<"\nVector as is: \t|";
	for (int i{0}; i<vq.capacity(); ++i){
		std::cout<<vq[i]<<" | ";
	}

	std::cout<<"\nPOV from queue: |";
	for (int i{0}; i<vq_size; ++i){
		std::cout<<vq[(i+vq_head)%vq.capacity()]<<" | ";
	}
	std::cout<<"\n";
};

template <typename T> 
void FastQueue<T>::print_props(){
	std::cout<<"Head index: "<<vq_head<<"\n";
	std::cout<<"Size: "<<vq_size<<"\n";
};