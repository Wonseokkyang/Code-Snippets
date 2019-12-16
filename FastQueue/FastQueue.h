/** 
Name: Won Seok Yang
Class: CS335 - Project 3 - Fast Queue

Prompt: 
Develop a queue system by re-utilizing the vector class.

Requirements:
FastQueue()  //default constructor
enqueue(<T> new_element)  //add to tail of queue
dequeue()  //remove element from head of queue
<T>& head()  //return reference to head
<T>& tail()  //return reference to tail
<T>& at(int index)  //returns ref to index after checking for out of bounds. Throw standard exception if out of bounds
<int> side()  //return # of elements in the queue
capacity()  //how much memory is allocated for the container
shrink_to_fit()  //shrinks container exactly to fit it's size
*/

#ifndef FASTQUEUE_H
#define FASTQUEUE_H

#include <iostream>
#include <vector>
#include <stdexcept>
#include <exception>


template<typename T> 
class FastQueue {
  private:
    vector<T> vq;
    int vq_head; //index of the head of the queue
    int vq_size;
  public:
    FastQueue();
    void enqueue(T new_element);
    void dequeue();
    T& head();
    T& tail();
    T& at(int index);
    int size();
    int capacity();
    void shrink_to_fit();
    //for testing
    void print_all();
    void print_props();
};  //end FastQueue class

#include"FastQueue.cpp"

#endif 